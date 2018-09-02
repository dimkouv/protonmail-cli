import os, datetime, time
import settings
import pyvirtualdisplay as display
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


def log(msg, reason="DEBUG"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%s %H:%M:%S")
    log_entry = "[%s] %s: %s" % (reason, timestamp, msg)

    if settings.logfile:
        open_type = 'w'
        if os.path.exists(settings.logfile):
            open_type = 'a'
        print(log_entry, file=open(settings.logfile, open_type))
    else:
        print(log_entry)


def run():
    def try_until_elem_appears(elem_val, elem_type="id"):
        retries = 0
        time.sleep(1)
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

    def read_emails():
        try_until_elem_appears("conversation", "class")

        print(driver.page_source, file=open("test.html", "w"))


    login()
    read_emails()


if __name__ == "__main__":
    display = None
    if not settings.show_browser:
        display = display.Display(visible=0, size=(1366, 768))
        display.start()
    
    driver = webdriver.Firefox()

    try:
        run()
    except Exception as e:
        print(e)

    if display:
        display.stop()
    driver.close()

