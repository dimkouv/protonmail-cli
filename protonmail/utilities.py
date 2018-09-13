from __future__ import print_function

import datetime
import os
import time

from selenium.common.exceptions import NoSuchElementException

from . import settings


def tail(filename, n):
    """Keep last n lines of file specified by :filename.

    :param filename: param n:
    :param n: 

    """
    log_file_content = open(filename, "r").readlines()
    open(filename, "w").writelines(log_file_content[:n])


def log(msg, reason="DEBUG"):
    """If settings.logfile is set write :msg in logfile else
    write in standard output.

    :param msg: param reason:  (Default value = "DEBUG")
    :param reason:  (Default value = "DEBUG")

    """
    if not settings.core_logging:
        # logging is disabled
        return

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


def wait_for_elem(web_driver, elem_val, elem_type="id"):
    """web driver helper utility used to wait until the page is fully
    loaded.
    
    Tries to find the element specified by :elem_val
    where :elem_val can be of :elem_type 'id', 'class' or 'css'.
    
    Returns True if element was found in time else False
    
    After :settings.max_retries number of times stops trying.

    :param elem_val: param web_driver:
    :param elem_type: Default value = "id")
    :param web_driver: 

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


def print_mail(mail):
    """Prints a mail entry as described in :read_mails.

    :param mail: 

    """
    out = "[" + mail.get("time") + "] " + mail.get("name")
    if mail.get("mail") != mail.get("name"):
        out += " " + mail.get("mail")
    out += "\n" + mail.get("title") + "\n"
    print(out)
