import atexit
import hashlib
import os
import time

from bs4 import BeautifulSoup
from pyvirtualdisplay.display import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from . import settings
from . import utilities
from . import variables


class ProtonmailClient:
    web_driver = None

    def __init__(self):
        utilities.log("Initiating ProtonMail client")

        try:
            virtual_display = None
            if not settings.show_browser:
                virtual_display = Display(visible=0, size=(1366, 768))
                virtual_display.start()

            self.web_driver = webdriver.Firefox()

            atexit.register(self.stop, virtual_display=virtual_display)
        except Exception as e:
            utilities.log(str(e), "ERROR")

    def login(self, username, password):
        """Login to ProtonMail panel
        
        Raises Exception on failure

        :param username:    your ProtonMail username - email
        :param password:    your ProtonMail password

        """

        def do_login():
            """
            :returns: True on successful login else False
            """
            utilities.log("Open login page")
            self.web_driver.get(variables.url)
            utilities.wait_for_elem(self.web_driver, variables.element_login['username_id'], "id")

            utilities.log("Login page loaded")
            username_input = self.web_driver.find_element_by_id(variables.element_login['username_id'])
            password_input = self.web_driver.find_element_by_id(variables.element_login['password_id'])

            username_input.send_keys(username)
            password_input.send_keys(password)

            password_input.send_keys(Keys.RETURN)
            utilities.log("Login credentials sent [" + username + "]")

            time.sleep(1)

            two_factor = False
            if "ng-hide" not in self.web_driver.find_element_by_id(
                    variables.element_twofactor['detection_id']).get_attribute('class'):
                two_factor = True

            if two_factor:
                utilities.log("Two-factor authentication enabled")
                two_factor_input = self.web_driver.find_element_by_id(variables.element_twofactor['code_id'])
                two_factor_input.send_keys(input("Enter two-factor authentication code: "))
                two_factor_input.send_keys(Keys.RETURN)

            return utilities.wait_for_elem(
                self.web_driver, variables.element_login['after_login_detection_class'], "class")

        if do_login():
            utilities.log("Logged in successfully")
        else:
            utilities.log("Unable to login", "ERROR")
            raise Exception("Unable to login")

    def read_mails(self):
        """Read and return a list of mails from the main
        ProtonMail page (after login).

        """
        soup = BeautifulSoup(self.web_driver.page_source, "html.parser")
        mails_soup = soup.select(variables.element_list_inbox['individual_email_soupclass'])

        mails = []
        subject_class = variables.element_list_inbox['individual_email_subject_soupclass']
        time_class = variables.element_list_inbox['individual_email_time_soupclass']
        sender_name_class = variables.element_list_inbox['individual_email_sender_name_soupclass']

        for mail in mails_soup:
            try:
                mails.append({
                    "title": mail.select(subject_class)[0].get("title"),
                    "time": mail.select(time_class)[0].string,
                    "name": mail.select(sender_name_class)[0].string,
                    "mail": mail.select(sender_name_class)[0].get("title")
                })
            except Exception as e:
                utilities.log(str(e), "ERROR")
                continue

        if settings.mails_read_num >= 0:
            mails = mails[:settings.mails_read_num]

        if settings.date_order == "asc":
            return list(reversed(mails))
        return mails

    def has_new_mail(self):
        """Generates a unique hash from the mail inbox
        If the hash is different from the previous call of this function
        then a new mail was received.

        :returns: True if a new mail was arrived else False
        
        @TODO in case we delete an email then the hash will be
        changed and we'll get a new mail notification.

        """
        mails = self.read_mails()
        hash_filename = ".protonmail-cli-mails-hash"
        old_hash = ""
        if os.path.exists(hash_filename):
            old_hash = open(hash_filename, "r").readline()

        new_hash = hashlib.sha256(str(mails).encode()).hexdigest()
        with open(hash_filename, "w") as f:
            f.write(new_hash)

        if old_hash and new_hash != old_hash:
            return True
        return False

    def send_mail(self, to, subject, message):
        """Sends email.

        :param to:      [str]     (list of mail addresses - recipients)
        :param message: str       (subject of the mail)
        :param subject: str       (message of the mail)

        """
        # click new mail button
        el = self.web_driver.find_element_by_class_name(variables.element_send_mail['open_composer_class'])
        el.click()

        # wait for mail dialog to appear
        utilities.wait_for_elem(self.web_driver, variables.element_send_mail['composer_detection_class'], "class")

        # type receivers list
        el = self.web_driver.find_element_by_css_selector(variables.element_send_mail['to_field_css'])
        for address in to:
            el.send_keys(address + ";")
            time.sleep(0.2)

        # type subject
        el = self.web_driver.find_element_by_css_selector(variables.element_send_mail['subject_field_css'])
        el.send_keys(subject)

        # type message
        self.web_driver.switch_to.frame(
            self.web_driver.find_element_by_class_name(variables.element_send_mail['switch_to_message_field_class']))
        el = self.web_driver.find_element_by_css_selector(variables.element_send_mail['message_field_css'])
        el.send_keys(message)
        self.web_driver.switch_to.default_content()

        # click send
        el = self.web_driver.find_element_by_css_selector(variables.element_send_mail['send_button_css'])
        el.click()

        time.sleep(settings.load_wait)

    def stop(self, virtual_display):
        """
        atexit handler; automatically executed upon normal interpreter termination.

        :param virtual_display: 

        """
        if self.web_driver is not None:
            self.web_driver.close()
            self.web_driver.quit()

        if virtual_display is not None:
            virtual_display.stop()
