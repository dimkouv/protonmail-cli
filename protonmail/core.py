import atexit
import getpass
import hashlib
import sys
import time

from bs4 import BeautifulSoup
from pyvirtualdisplay.display import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from . import mail, settings, utilities, variables


class ProtonmailClient:
    """
    This class contains the core functions
    that are used by both protonmail-cli and interactive session.

    example usage for reading inbox mails
    >>> client = core.ProtonmailClient()
    >>> client.login(settings.username, settings.password)
    >>> inbox = client.get_mails("inbox")
    """

    web_driver = None
    virtual_display = None

    def __init__(self):
        utilities.log("Initiating ProtonMail client")

        try:
            if not settings.show_browser:
                self.virtual_display = Display(visible=0, size=(1366, 768))
                self.virtual_display.start()

            self.web_driver = webdriver.Firefox()

            atexit.register(self.destroy)
        except Exception as e:
            utilities.log(
                "Unable to initiate Protonmail Client. Reason: " + str(e))

    def login(self, username, password):
        """Login to ProtonMail panel

        Raises Exception on failure

        :param username:    your ProtonMail username - email
        :param password:    your ProtonMail password

        """
        try:
            utilities.log("Logging in...")
            self.web_driver.get(variables.url)
            utilities.wait_for_elem(
                self.web_driver, variables.element_login['username_id'], "id")

            utilities.log("Login page loaded...", "DEBUG")
            username_input = self.web_driver.find_element_by_id(
                variables.element_login['username_id'])
            password_input = self.web_driver.find_element_by_id(
                variables.element_login['password_id'])

            username_input.send_keys(username)
            password_input.send_keys(password)

            password_input.send_keys(Keys.RETURN)
            utilities.log("Login credentials sent [" + username + "]", "DEBUG")

            time.sleep(1)

            two_factor = False

            try:
                self.web_driver.find_element_by_id(variables.element_twofactor['detection_id']).get_attribute('class')
                two_factor = True
            except:
                pass

            if two_factor:
                utilities.log("Two-factor authentication enabled", "DEBUG")
                two_factor_input = self.web_driver.find_element_by_id(
                    variables.element_twofactor['code_id'])
                two_factor_input.send_keys(
                    input("Enter two-factor authentication code: "))
                two_factor_input.send_keys(Keys.RETURN)

            if utilities.wait_for_elem(self.web_driver, variables.element_login['after_login_detection_class'],
                                       "class"):
                utilities.log("Logged in successfully")
            else:
                raise Exception()
        except Exception as ignored_err:
            utilities.log("Login failed!")
            raise Exception("Unable to login")

    def parse_mails(self):
        """
        Reads and returns a list of Mails inside the current web driver's page
        :return: a list of Mail objects
        """
        if not utilities.wait_for_elem(self.web_driver, variables.element_list_inbox['email_list_wrapper_id'], "id"):
            # for some reason the wrapper wasn't loaded
            return None

        utilities.wait_for_elem(
            self.web_driver, variables.element_list_inbox["individual_email_soupclass"][1:], "class",
            max_retries=3)

        soup = BeautifulSoup(self.web_driver.page_source, "html.parser")
        mails_soup = soup.select(
            variables.element_list_inbox['individual_email_soupclass'])

        mails = []
        subject_class = variables.element_list_inbox['individual_email_subject_soupclass']
        time_class = variables.element_list_inbox['individual_email_time_soupclass']
        sender_name_class = variables.element_list_inbox['individual_email_sender_name_soupclass']

        for m in mails_soup:
            # @TODO mails without subject or title, etc.. are ignored
            try:
                new_mail = mail.Mail(
                    subject=m.select(subject_class)[0].get("title"),
                    time_received=m.select(time_class)[0].string,
                    mail_alias=m.select(sender_name_class)[0].get("title"),
                    mail=m.select(sender_name_class)[0].string,
                )
                mails.append(new_mail)
            except Exception as e:
                utilities.log("Skip mail... " + str(e))
                continue

        if settings.mails_read_num > 0:
            mails = mails[:settings.mails_read_num]

        if settings.date_order == "asc":
            return list(reversed(mails))
        return mails

    def get_mails(self, page):
        """
        Get a list of mails that are into the given page

        :param page: One of the pages listed in variables.py > page_urls
        :return: a list of Mail objects
        """
        url = variables.page_urls.get(page)
        if not url:
            raise ValueError("Page doesn't exist")

        if self.web_driver.current_url != url:
            utilities.log("Opening %s" % url)
            self.web_driver.get(url)
        return self.parse_mails()

    def get_mails_in_folder(self, folder):
        """
        Get a list of mails that are in the given folder

        :param page: A user defined folder, populated at runtime by get_folders()
        :return: a list of Mail objects
        """
        # this is valid because ProtonMail folders are case-insensitive
        folder = folder.lower()

        print("Folder is {}".format(folder))
        print("folder list is {}".format(self.get_folders()))

        url = self.get_folders().get(folder)
        if not url:
            raise ValueError("Folder doesn't exist")

        if self.web_driver.current_url != url:
            utilities.log("Opening %s" % url)
            self.web_driver.get(url)
        return self.parse_mails()

    def get_mails_in_label(self, label):
        """
        Get a list of mails that are in the given label

        :param label: A user defined label, populated at runtime by get_labels()
        :return: a list of Mail objects
        """
        # this is valid because ProtonMail labels are case-insensitive
        label = label.lower()

        url = self.get_labels().get(label)
        if not url:
            raise ValueError("Label doesn't exist")

        if self.web_driver.current_url != url:
            utilities.log("Opening %s" % url)
            self.web_driver.get(url)
        return self.parse_mails()

    def get_folders_and_labels(self):
        """
        Get a list of the user's mail folders and labels

        :return: a dict of mail folder and label urls, similar to page_urls
        """
        all_items = dict()

        soup = BeautifulSoup(self.web_driver.page_source, "html.parser")
        folders_and_labels = soup.select(
            variables.element_folders_labels['list_element_title_selector']
        )

        for folder_or_label in folders_and_labels:
            # this is valid because ProtonMail folders and labels are case-insensitive
            name = folder_or_label.text.lower()
            path = folder_or_label.parent['href']

            all_items[name] = variables.base_url + path

        return all_items

    def get_folders(self):
        """
        Get a list of mail folders (not labels!)

        :return: a dict of mail folder urls, similar to page_urls
        """
        all_folders = dict()

        soup = BeautifulSoup(self.web_driver.page_source, "html.parser")
        folders = soup.select(
            variables.element_folders_labels['folder_element_selector']
        )

        for folder in folders:
            # this is valid because ProtonMail folders are case-insensitive
            name = folder.find_next_sibling("span", class_="menuLabel-title").text.lower()
            path = folder.parent['href']

            all_folders[name] = variables.base_url + path

        return all_folders

    def get_labels(self):
        """
        Get a list of mail labels (not folders!)

        :return: a dict of mail label urls, similar to page_urls
        """
        all_labels = dict()

        soup = BeautifulSoup(self.web_driver.page_source, "html.parser")
        labels = soup.select(
            variables.element_folders_labels['label_element_selector']
        )

        for label in labels:
            # this is valid because ProtonMail labels are case-insensitive
            name = label.find_next_sibling("span", class_="menuLabel-title").text.lower()
            path = label.parent['href']

            all_labels[name] = variables.base_url + path

        return all_labels

    def has_new_mail(self):
        """Generates a unique hash from the mail inbox
        If the hash is different from the previous call of this function
        then a new mail was received.

        :returns: True if a new mail was arrived else False

        @TODO in case we delete an email then the hash will be
        changed and we'll get a new mail notification.

        """
        mails = self.get_mails("inbox")

        old_hash = utilities.get_hash()

        mails_str = ""
        for m in mails:
            mails_str += str(m)
            mails_str += str(m)

        new_hash = hashlib.sha256(mails_str.encode()).hexdigest()
        utilities.write_hash(new_hash)

        if old_hash and new_hash != old_hash:
            return True
        return False

    def change_name(self, new_name):
        """ Change name of your account.
        The name is the name that appears on recipients inbox.
        <Your Name> youraddress@protonmail.com

        :param new_name: str     (the updated user's name)

        """
        url = variables.page_urls.get('account')
        if not url:
            raise ValueError("Page doesn't exist")

        if self.web_driver.current_url != url:
            utilities.log("Opening %s" % url)
            self.web_driver.get(url)

        # type the new user name
        utilities.wait_for_elem(
            self.web_driver,
            variables.element_account['display_name']
        )
        el = self.web_driver.find_element_by_id(
            variables.element_account['display_name'])
        el.clear()  # clear old name
        el.send_keys(new_name)  # write new name

        # click save button
        utilities.wait_for_elem(
            self.web_driver, variables.element_account['save_btn'], "class"
        )
        el = self.web_driver.find_element_by_class_name(
            variables.element_account['save_btn'])
        el.click()
        time.sleep(settings.load_wait)

        # click back button
        el = self.web_driver.find_element_by_class_name(
            variables.element_account['back_btn'])
        el.click()

    def send_mail(self, to, subject, message, as_html=False, attachments=[]):
        """Sends email.

        :param to:          [str]     (list of mail addresses - recipients)
        :param message:     str       (subject of the mail)
        :param subject:     str       (message of the mail)
        :param as_html:     bool      (whether or not to render :message as html)
        :param attachments: [str]     (list of files to upload as attachments)

        """
        def upload_attachments(attachments):
            # wait for files to be uploaded
            initial_send_text = self.web_driver.find_element_by_css_selector(
                variables.element_send_mail['send_button_css']
            ).text

            el = self.web_driver.find_element_by_css_selector(
                'input[type=file][multiple=multiple]'
            )
            el.send_keys("\n".join(attachments))

            time.sleep(settings.load_wait)

            try:
                # this dialog appears on images for inline placing
                self.web_driver.find_element_by_css_selector(
                    variables.element_send_mail['as_attachment_btn']
                ).click()
            except:
                pass

            # wait for files to be uploaded
            while True:
                time.sleep(settings.load_wait)
                curr_send_text = self.web_driver.find_element_by_css_selector(
                    variables.element_send_mail['send_button_css']
                ).text
                if curr_send_text == initial_send_text:
                    break

        # click new mail button
        el = self.web_driver.find_element_by_class_name(
            variables.element_send_mail['open_composer_class'])
        el.click()

        # wait for mail dialog to appear
        utilities.wait_for_elem(
            self.web_driver, variables.element_send_mail['composer_detection_class'], "class")

        # type receivers list
        el = self.web_driver.find_element_by_css_selector(
            variables.element_send_mail['to_field_css'])
        for address in to:
            el.send_keys(address + ";")
            time.sleep(0.2)

        # type subject
        el = self.web_driver.find_element_by_css_selector(
            variables.element_send_mail['subject_field_css'])
        el.send_keys(subject)

        self.web_driver.switch_to.frame(
            self.web_driver.find_element_by_class_name(
                variables.element_send_mail['switch_to_message_field_class'])
        )
        el = self.web_driver.find_element_by_css_selector(
            variables.element_send_mail['message_field_css'])

        if not as_html:
            # type message if we don't want to render as html
            el.send_keys(message)
        else:
            # render as html by executing a js oneliner to alter the DOM
            self.web_driver.execute_script("""
                document.querySelector('.angular-squire-iframe body>div').innerHTML="%s"
            """ % (message.replace('"', '\\"')))

        self.web_driver.switch_to.default_content()

        if attachments:
            upload_attachments(attachments)

        # click send
        el = self.web_driver.find_element_by_css_selector(
            variables.element_send_mail['send_button_css'])
        el.click()

        time.sleep(settings.load_wait)

    def destroy(self):
        """
        atexit handler; automatically executed upon normal interpreter termination.

        Should be called after any work done with client
        """
        if self.web_driver is not None:
            self.web_driver.close()
            self.web_driver.quit()
            self.web_driver = None

        if self.virtual_display is not None:
            self.virtual_display.stop()
            self.virtual_display = None
