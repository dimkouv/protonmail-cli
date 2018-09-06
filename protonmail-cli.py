#!/usr/bin/python3
import os
import datetime
import time
import hashlib
import sys

import settings
from bs4 import BeautifulSoup as bs4
from pyvirtualdisplay.display import Display
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


def tail(filename, n):
    """Keep last :n lines of file specified by :filename"""
    tmpf = "pr-cli.tmp"
    (os.system(cmd) for cmd in [
        "tail -%d %s > %s" % (n, filename, tmpf),
        "cp %s %s; rm %s" % (tmpf, filename, tmpf)
    ])


def log(msg, reason="DEBUG"):
    """If settings.logfile is set write :msg in logfile else
    write in standard output"""
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

    After :settings.max_retries number of times stops trying"""

    retries = 0
    time.sleep(0.5)
    while True:
        try:
            if retries > settings.max_retries:
                break

            if elem_type == "id":
                driver.find_element_by_id(elem_val)
            elif elem_type == "class":
                driver.find_element_by_class_name(elem_val)
            elif elem_type == "css":
                driver.find_element_by_css_selector(elem_val)
            else:
                raise ValueError("Unknown elem_type")
            return True

        except NoSuchElementException:
            log("waiting...")
            retries += 1
            time.sleep(settings.load_wait)

    return False


def login():
    """Login to protonmail panel
    using credentials from :settings.py
    
    Returns True or False wether login was succesful
    """
    def do_login():
        log("Open login page")
        driver.get("https://protonmail.com/login")
        try_until_elem_appears("username")
        log("Login page loaded")
        username_input = driver.find_element_by_id("username")
        password_input = driver.find_element_by_id("password")
        username_input.send_keys(settings.username)
        password_input.send_keys(settings.password)
        password_input.send_keys(Keys.RETURN)
        log("Login credentials sent")
        
        time.sleep(1)

        twofactor = False
        if "ng-hide" not in driver.find_element_by_id("pm_loginTwoFactor").get_attribute('class'):
            twofactor = True

        if twofactor:
            log("Two-factor authentication enabled")
            twofactor_input = driver.find_element_by_id("twoFactorCode")
            twofactor_input.send_keys(input("Enter two-factor authentication code: "))
            twofactor_input.send_keys(Keys.RETURN)

        return try_until_elem_appears("conversation-meta", "class")
    
    if do_login():
        log("Logged in succesfully")
    else:
        log("Unable to login", "ERROR")
        sys.exit(0)


def read_mails():
    """Read and return a list of mails from the main
    protonmail page (after login)"""
    soup = bs4(driver.page_source, "html.parser")
    mails_soup = soup.select(".conversation-meta")

    mails = []

    for mail in mails_soup:
        try:
            mails.append({
                "title": mail.select(".subject")[0].get("title"),
                "time": mail.select(".time")[0].string,
                "name": mail.select(".senders-name")[0].string,
                "mail": mail.select(".senders-name")[0].get("title")
            })
        except Exception as e:
            log(str(e), "ERROR")
            continue

    mails = mails[:settings.mails_read_num]

    if settings.date_order == "asc":
        return reversed(mails)
    return mails


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
        log("New message arrived")
        os.system(
            "notify-send 'You received a new message on your ProtonMail inbox'")
    else:
        log("You don't have new messages")

    with open(hash_filename, "w") as f:
        f.write(new_hash)


def print_usage_and_exit():
    print("""
    NAME
        protonmail-cli - Protonmail CLI tool

    USAGE
        > protonmail-cli list-inbox
            Prints the latest mail titles

        > protonmail-cli check-inbox
            Checks for new message and displays a system notification
            check period is defined in settings.py

        > protonmail-cli send-mail -to "address1;address2"
                                   -subject "subject"
                                   -body "message"
            Sends an email to the specified addresses.

        > protonmail-cli help
            Prints this dialog
    """)
    sys.exit(0)


def print_mail(mail):
    """Prints a mail entry as described in :read_mails"""
    out = "[" + mail.get("time") + "] " + mail.get("name")
    if mail.get("mail") != mail.get("name"):
        out += " " + mail.get("mail")
    out += "\n" + mail.get("title") + "\n"
    print(out)


def send_mail(to, subject, message):
    """Sends an email. Requires login() to be executed first.
    Params
    ------
    :to [list of mails]
    :subject [str]
    :message [str]"""

    # click new mail button
    el = driver.find_element_by_class_name("sidebar-btn-compose")
    el.click()

    # wait for mail dialog to appear
    try_until_elem_appears("composer", "class")

    # type receivers list
    el = driver.find_element_by_css_selector(".composer-field-ToList input")
    for address in to:
        el.send_keys(address + ";")
        time.sleep(0.2)

    # type subject
    el = driver.find_element_by_css_selector(".subjectRow input")
    el.send_keys(subject)

    # type message
    driver.switch_to.frame(driver.find_element_by_class_name('squireIframe'))
    el = driver.find_element_by_css_selector("html.angular-squire-iframe body")
    el.send_keys(message)
    driver.switch_to.default_content()

    # click send
    el = driver.find_element_by_css_selector(".btnSendMessage-btn-action")
    el.click()

    time.sleep(settings.load_wait)


def parse_args():
    """Parses and returns dict of cmd line params
    returns dict {
        "operation": str
        "to": []        @operation=send-mail
        "subject": str  @operation=send-mail
        "body": str     @operation=send-mail
    }
    """
    def get_key_arg(key):
        for i, arg in enumerate(sys.argv):
            if arg == key:
                return sys.argv[i+1]
        raise ValueError("Invalid arguments")

    try:
        args = {"operation": sys.argv[1]}
        
        if args["operation"] == "send-mail":
            args["to"] = [x.strip() for x in get_key_arg("-to").split(";")]
            args["subject"] = get_key_arg("-subject")
            args["body"] = get_key_arg("-body")

        return args
    except:
        print_usage_and_exit()


def run():
    args = parse_args()

    if args["operation"] == "list-inbox":
        login()
        for mail in read_mails():
            print_mail(mail)

    elif args["operation"] == "check-inbox":
        login()
        while True:
            mails = read_mails()
            check_for_new_mail(mails)
            if settings.check_mail_period == 0:
                break
            else:
                time.sleep(settings.check_mail_period)

    elif args["operation"] == "send-mail":
        login()
        try:
            log("Opening mail dialog")
            send_mail(args["to"], args["subject"], args["body"])
            log("email sent.")
        except Exception as e:
            log(str(e), "ERROR")

    else:
        print_usage_and_exit()


if __name__ == "__main__":
    display = None
    if not settings.show_browser:
        display = Display(visible=0, size=(1366, 768))
        display.start()

    driver = webdriver.Firefox()

    try:
        run()
    except Exception as e:
        log(str(e), "ERROR")

    driver.close()
    if display is not None:
        display.stop()
