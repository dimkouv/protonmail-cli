#!/usr/bin/python3

import os
import datetime
import time
import hashlib
import sys
import argparse
import atexit

from bs4 import BeautifulSoup as bs4
from pyvirtualdisplay.display import Display
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

import settings


def tail(filename, n):
    """Keep last :n lines of file specified by :filename."""
    log_file_content = open(filename, "r").readlines()
    open(filename, "w").writelines(log_file_content[:n])


def log(msg, reason="DEBUG"):
    """If settings.logfile is set write :msg in logfile else
    write in standard output.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = "[%s] %s: %s" % (reason, timestamp, msg)

    if settings.logfile and os.path.exists(settings.logfile):
        tail(settings.logfile, settings.logfile_rows_keep)

    if settings.logfile:
        open_type = 'w'
        if os.path.exists(settings.logfile):
            open_type = 'a'
        print(log_entry, file=open(settings.logfile, open_type))
    else:
        print(log_entry)


def try_until_elem_appears(elem_val, elem_type="id"):
    """web driver helper utility used to wait until the page is fully
    loaded.

    Tries to find the element specified by :elem_val
    where :elem_val can be of :elem_type 'id', 'class' or 'css'.

    Returns True if element was found in time else False

    After :settings.max_retries number of times stops trying.
    """
    retries = 0
    time.sleep(0.5)
    while True:
        try:
            if retries > settings.max_retries:
                break

            if elem_type == "id":
                web_driver.find_element_by_id(elem_val)
            elif elem_type == "class":
                web_driver.find_element_by_class_name(elem_val)
            elif elem_type == "css":
                web_driver.find_element_by_css_selector(elem_val)
            else:
                raise ValueError("Unknown elem_type")
            return True

        except NoSuchElementException:
            log("  waiting for " + elem_type + ":" + elem_val + "...")
            retries += 1
            time.sleep(settings.load_wait)

    return False


def login():
    """Login to ProtonMail panel
    using credentials from :settings.py

    Returns True or False wether login was successful.
    """

    def do_login():
        """:returns: True on successful login else False"""
        log("Open login page")
        web_driver.get(settings.url)
        try_until_elem_appears(settings.element_login['username_id'], "id")

        log("Login page loaded")
        username_input = web_driver.find_element_by_id(settings.element_login['username_id'])
        password_input = web_driver.find_element_by_id(settings.element_login['password_id'])

        username_input.send_keys(settings.username)
        password_input.send_keys(settings.password)

        password_input.send_keys(Keys.RETURN)
        log("Login credentials sent [" + settings.username + "]")

        time.sleep(1)

        two_factor = False
        if "ng-hide" not in web_driver.find_element_by_id(
                settings.element_twofactor['detection_id']).get_attribute('class'):
            two_factor = True

        if two_factor:
            log("Two-factor authentication enabled")
            two_factor_input = web_driver.find_element_by_id(settings.element_twofactor['code_id'])
            two_factor_input.send_keys(input("Enter two-factor authentication code: "))
            two_factor_input.send_keys(Keys.RETURN)

        return try_until_elem_appears(settings.element_login['after_login_detection_class'], "class")

    if do_login():
        log("Logged in successfully")
    else:
        log("Unable to login", "ERROR")
        sys.exit(0)


def read_mails():
    """Read and return a list of mails from the main
    ProtonMail page (after login).
    """
    soup = bs4(web_driver.page_source, "html.parser")
    mails_soup = soup.select(settings.element_list_inbox['individual_email_soupclass'])

    mails = []
    subjectClass = settings.element_list_inbox['individual_email_subject_soupclass']
    timeClass = settings.element_list_inbox['individual_email_time_soupclass']
    senderNameClass = settings.element_list_inbox['individual_email_sender_name_soupclass']

    for mail in mails_soup:
        try:
            mails.append({
                "title": mail.select(subjectClass)[0].get("title"),
                "time": mail.select(timeClass)[0].string,
                "name": mail.select(senderNameClass)[0].string,
                "mail": mail.select(senderNameClass)[0].get("title")
            })
        except Exception as e:
            log(str(e), "ERROR")
            continue

    mails = mails[:settings.mails_read_num]

    if settings.date_order == "asc":
        return list(reversed(mails))
    return mails


def print_mail(mail):
    """Prints a mail entry as described in :read_mails."""
    out = "[" + mail.get("time") + "] " + mail.get("name")
    if mail.get("mail") != mail.get("name"):
        out += " " + mail.get("mail")
    out += "\n" + mail.get("title") + "\n"
    print(out)


def check_for_new_mail(mails):
    """Receives a list of mails and generates a unique hash.
    If the hash is different from the previous call of this function
    then a new mail was received.

    @TODO @BUG in case we delete an email then the hash will be changed
    and we'll get a new mail notification.
    """
    hash_filename = ".protonmail-cli-mails-hash"
    old_hash = ""
    if os.path.exists(hash_filename):
        old_hash = open(hash_filename, "r").readline()

    new_hash = hashlib.sha256(str(mails).encode()).hexdigest()

    if old_hash and new_hash != old_hash:
        log("New mail arrived")
        log("Showing latest 5 mails...")
        for mail in mails[:5]:
            print_mail(mail)
        os.system(
            "notify-send 'You received a new mail on your ProtonMail inbox'")
    else:
        log("You don't have new mails")

    with open(hash_filename, "w") as f:
        f.write(new_hash)


def send_mail(to, subject, message):
    """Sends an email.
    login() needs to be executed first.

    :to:      [str]     (list of mail addresses - recipients)
    :subject: str       (subject of the mail)
    :message: str       (message of the mail)
    """
    # click new mail button
    el = web_driver.find_element_by_class_name(settings.element_send_mail['open_composer_class'])
    el.click()

    # wait for mail dialog to appear
    try_until_elem_appears(settings.element_send_mail['composer_detection_class'], "class")

    # type receivers list
    el = web_driver.find_element_by_css_selector(settings.element_send_mail['to_field_css'])
    for address in to:
        el.send_keys(address + ";")
        time.sleep(0.2)

    # type subject
    el = web_driver.find_element_by_css_selector(settings.element_send_mail['subject_field_css'])
    el.send_keys(subject)

    # type message
    web_driver.switch_to.frame(web_driver.find_element_by_class_name(settings.element_send_mail['switch_to_message_field_class']))
    el = web_driver.find_element_by_css_selector(settings.element_send_mail['message_field_css'])
    el.send_keys(message)
    web_driver.switch_to.default_content()

    # click send
    el = web_driver.find_element_by_css_selector(settings.element_send_mail['send_button_css'])
    el.click()

    time.sleep(settings.load_wait)


def subcommand_list(args):
    log("Action: list emails")
    login()

    for mail in read_mails():
        print_mail(mail)


def subcommand_check(args):
    log("Action: check emails")
    login()

    while True:
        mails = read_mails()
        check_for_new_mail(mails)
        if settings.check_mail_period == 0:
            break
        else:
            time.sleep(settings.check_mail_period)


def subcommand_send(args):
    log("Action: send email")
    login()
    
    try:
        log("Opening mail dialog")
        send_mail(args.to, args.subject, args.body)
        log("email sent.")
    except Exception as e:
        log(str(e), "ERROR")


def parse_args():
    """Return the populated namespace from ArgumentParser.parse_args."""
    parser = argparse.ArgumentParser(
        description="ProtonMail CLI tool",
        epilog="Homepage: https://github.com/dimkouv/protonmail-cli")

    subparsers = parser.add_subparsers(
        title="actions",
        description="The high level actions available to ProtonMail CLI. For more detail, the help flag is available for all actions.",
        metavar="action")

    # Required to be set after the creation because of bug: https://stackoverflow.com/a/18283730
    subparsers.required = True

    # List inbox arguments
    list_inbox_parser = subparsers.add_parser(
        "list",
        aliases=["l"],
        help="Print the latest mails title from the inbox.")
    list_inbox_parser.set_defaults(func=subcommand_list)

    # Check inbox arguments
    check_inbox_parser = subparsers.add_parser(
        "check",
        aliases=["c"],
        help="Check the inbox for new mail and displays a system notification.")
    check_inbox_parser.set_defaults(func=subcommand_check)

    # Send email arguments
    send_mail_parser = subparsers.add_parser(
        "send",
        aliases=["s"],
        help="Send an email to the specified addresses.")
    send_mail_parser.set_defaults(func=subcommand_send)

    send_mail_parser.add_argument(
        "-t",
        "--to",
        help="Recipient's address",
        action="append",
        required=True)
    send_mail_parser.add_argument(
        "-s",
        "--subject",
        help="Subject",
        required=True)
    send_mail_parser.add_argument(
        "-b",
        "--body",
        help="Body text",
        required=True)

    return parser.parse_args()


def cleanup(web_driver, virtual_display):
    """atexit handler; automatically executed upon normal interpreter termination."""
    if web_driver is not None:
        web_driver.close()
        web_driver.quit()

    if virtual_display is not None:
        virtual_display.stop()


if __name__ == "__main__":
    args = parse_args()

    virtual_display = None
    if not settings.show_browser:
        virtual_display = Display(visible=0, size=(1366, 768))
        virtual_display.start()

    web_driver = webdriver.Firefox()

    atexit.register(cleanup, web_driver=web_driver, virtual_display=virtual_display)

    try:
        # Execute the selected subcommand/action.
        args.func(args)
    except Exception as e:
        log(str(e), "ERROR")
