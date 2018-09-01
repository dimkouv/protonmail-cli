import os, datetime, time
import settings
import pyvirtualdisplay as display
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


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
    def login():
        retries = 0
        driver.get("https://protonmail.com/login")

        while True:
            try:
                if retries > settings.max_retries:
                    break
                elem = driver.find_element_by_name("q")    
            except NoSuchElementException:
                retries += 1
                time.sleep(settings.load_wait)

        

    display = None
    if not settings.show_browser:
        display = display.Display(visible=0, size=(800, 600))
        display.start()
    driver = webdriver.Firefox()
    if display:
        display.stop()
    
    login()
    driver.close()

if __name__ == "__main__":
    run()
