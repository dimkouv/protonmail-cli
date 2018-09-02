import os, datetime, time, hashlib, sys
import settings
from bs4 import BeautifulSoup as bs4
from pyvirtualdisplay.display import Display
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


def log(msg, reason="DEBUG"):
    """If settings.logfile is set write :msg in logfile else
    write in standard output"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = "[%s] %s: %s" % (reason, timestamp, msg)

    if settings.logfile and os.path.exists(settings.logfile):
        cmds = [
            "cp %s pr-cli-log.bak" % (settings.logfile),
            "cat pr-cli-log.bak | tail -%d > %s" % (settings.logfile_rows_keep, settings.logfile),
            "rm pr-cli-log.bak"
        ]
        for cmd in cmds:
            os.system(cmd)

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

    After :settings.max_retries number of times exits"""
    
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
            break

        except NoSuchElementException:
            retries += 1
            time.sleep(settings.load_wait)


def login():
    """Login to protonmail panel
    using credentials from :settings.py"""

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


def read_mails():
    """Read and return a list of mails from the main
    protonmail page (after login)"""
    
    try_until_elem_appears("conversation-meta", "class")

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
        os.system("notify-send 'You received a new message on your ProtonMail inbox'")
    else:
        log("You don't have new messages")

    with open(hash_filename, "w") as f:
        f.write(new_hash)


def print_usage():
    print("""
    NAME
        protonmail-cli - Protonmail CLI tool
    
    SYNOPSIS
        protonmail-cli [OPTION]
    
    DESCRIPTION
        protonmail-cli list-inbox
            Prints the latest mail titles
        
        protonmail-cli check-inbox
            Checks for new message and displays a system notification
            check period is defined in settings.py
        
        protonmail-cli help
            Prints this dialog
    """)


def print_mail(mail):
    """Prints a mail entry as described in :read_mails"""
    out = "[" + mail.get("time") + "] " + mail.get("name")
    if mail.get("mail") != mail.get("name"):
        out += " " + mail.get("mail")
    out += "\n" + mail.get("title") + "\n"
    print(out)


def run():
    if len(sys.argv) > 1:
        op = sys.argv[1]
        
        if op == "list-inbox":
            login()
            for mail in read_mails():
                print_mail(mail)

        elif op == "check-inbox":
            login()
            while True:
                mails = read_mails()
                check_for_new_mail(mails)
                if settings.check_mail_period == 0:
                    break
                else:
                    time.sleep(settings.check_mail_period)

        elif op == "help":
            print_usage()

        else:
            print("Operation not valid")
            print_usage()

        return

    print_usage()


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
