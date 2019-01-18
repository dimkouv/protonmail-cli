import getpass
import sys

from . import core, settings, utilities

"""
This class is responsible for opening an interactive session.

While on this session users can perform any of the available functions
through a menu with choices.

Interactive session doesn't used any cached credentials, you have to login
each time it starts.

Usage
>>> session = interactive.InteractiveSession()
>>> session.start()
"""
class InteractiveSession:
    def __init__(self):
        """ initialize class fields and protonmail client """

        # disable logging, all logging will happen into this methods
        settings.log_level = ""

        self.is_logged_in = False
        self.username = ""
        self.client = core.ProtonmailClient()
    
    def login(self):
        """ login menu function """

        self.username = input("ProtonMail email or username: ")
        password = getpass.getpass("ProtonMail password: ")
        print("Loading...")
        try:
            self.client.login(self.username, password)
            self.is_logged_in = True
            print("Welcome " + self.username)
            self.display()
        except Exception as ignored_err:
            print("Unable to login, check your credentials or your connection.")
    
    def exit(self):
        """ exit menu function, closes client """
        print("Exiting...")
        self.client.destroy()
        sys.exit()

    def logout(self):
        """ logout menu function, reinits client """
        print("Loading...")
        self.client.destroy()
        self.is_logged_in = False
        print("You've been logged out.")
        self.display()

    def send(self):
        """ send mail menu function """
        def read_recipients():
            recipients = []
            while True:
                recipients = input("Give recipient address(es separed with ;).\n").split(";")
                recipients = [r.strip() for r in recipients]
                print("\tReceivers:", recipients)
                if utilities.validate():
                    break
            return recipients

        def read_subject():
            subject = ""
            while True:
                subject = input("Subject: ")
                print("\tSubject:", subject)
                if utilities.validate():
                    break
            return subject
        
        def read_message():
            message = ""
            while True:
                message = input("Mail content:\n")
                print("\tMail content:\n", "\t", message)
                if utilities.validate():
                    break
            return message

        recipients = read_recipients()
        subject = read_subject()
        message = read_message()

        print("-" * 30, "\nTO:", recipients, "\nSUBJECT:", subject, "\n", message, "-" * 30)
        if utilities.validate():
            self.client.send_mail(recipients, subject, message)
        else:
            print("Email cancelled")

    def show(self, page):
        """ prints all mails on the given page
        :param page: <str> Any of the available pages (inbox, spam, ...)
        """
        for mail in self.client.get_mails(page):
            print(mail)

    def get_options_for_any(self):
        """ returns menu options used by both authenticated and anonymous users """
        return {
            "m": {
                "text": "Shows this menu",
                "function": self.display
            },
            "x": {
                "text": "Exit",
                "function": self.exit
            }
        }

    def get_options_for_non_anonymous(self):
        """ menu options only for authenticated users """
        options = self.get_options_for_any()
        options["e"] = {
            "text": "Logout",
            "function": self.logout
        }
        options["send"] = {
            "text": "Send an email",
            "function": lambda: self.send()
        }

        show_options = ["inbox", "drafts", "sent", "starred", "archive", "spam", "trash", "allmail"]
        for opt in show_options:
            options[opt] = {
                "text": "Show " + opt.title() + " emails.",
                "function": lambda: self.show(opt)
            }
        return options

    def get_options_for_anonymous(self):
        """ menu options only for anonymous users """
        options = self.get_options_for_any()
        options["l"] = {
            "text": "Login",
            "function": self.login
        }
        return options

    def get_options(self):
        """ wrapper that returns menu options based on user authentication status """
        return self.get_options_for_non_anonymous() if self.is_logged_in else self.get_options_for_anonymous()

    def start(self):
        """ main program loop, reads user's menu choice on each loop """
        self.display()
        while True:
            options = self.get_options()
            choice = input("> ").lower()

            if choice in options:
                options[choice]["function"]()  # call the anonymous function that is attached on menu choice
            else:
                self.display()

    def display(self):
        """ displays the menu based on user's status """
        print("\n[{username}] {message}".format(
            username=self.username if self.is_logged_in else "Anonymous",
            message="Choose an option from the menu"
        ))

        options = self.get_options()
        for choice in options:
            print("{option_id: <12}: {option_text}".format(
                option_id=choice.lower(),
                option_text=options[choice]["text"]
            ))
