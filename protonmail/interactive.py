import getpass
import sys

from . import core, settings


class InteractiveSession:
    def __init__(self):
        # disable logging
        # all logging will happen into this methods
        settings.log_level = ""

        self.is_logged_in = False
        self.username = ""
        self.client = core.ProtonmailClient()
    
    def login(self):
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
        print("Exiting...")
        self.client.destroy()
        sys.exit()

    def logout(self):
        print("Loading...")
        self.client.destroy()
        self.is_logged_in = False
        print("You've been logged out.")
        self.display()

    def show(self, page):
        for mail in self.client.get_mails(page):
            print(mail)
    
    def send(self):
        """ Send mail """
        def read_recipients():
            recipients = []
            while True:
                recipients = input("Give recipient address(es separed with ;).\n").split(";")
                recipients = [r.strip() for r in recipients]
                print("\tReceivers:", recipients)
                validate = input("Are you sure? [Y/n]").lower()
                if validate != "n":
                    break
            return recipients

        def read_subject():
            subject = ""
            while True:
                subject = input("Subject: ")
                print("\tSubject:", subject)
                validate = input("Are you sure? [Y/n]").lower()
                if validate != "n":
                    break
            return subject
        
        def read_message():
            message = ""
            while True:
                message = input("Mail content:\n")
                print("\tMail content:\n", "\t", message)
                validate = input("Are you sure? [Y/n]").lower()
                if validate != "n":
                    break
            return message

        recipients = read_recipients()
        subject = read_subject()
        message = read_message()

        print("-" * 30)
        print("TO:", recipients)
        print("SUBJECT:", subject)
        print(message)
        print("-" * 30)

        validate = input("[SEND] Are you sure? [Y/n]").lower()
        if validate != "n":
            print("Email wasn't sent...")
        else:
            self.client.send_mail(recipients, subject, message)

    def get_options_for_any(self):
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
        options = self.get_options_for_any()
        options["e"] = {
            "text": "Logout",
            "function": self.logout
        }
        options["send"] = {
            "text": "Send an email",
            "function": lambda: self.send()
        }
        options["inbox"] = {
            "text": "Show inbox mails",
            "function": lambda: self.show("inbox")
        }
        options["drafts"] = {
            "text": "Show drafts",
            "function": lambda: self.show("drafts")
        }
        options["sent"] = {
            "text": "Show sent mails",
            "function": lambda: self.show("sent")
        }
        options["starred"] = {
            "text": "Show starred mails",
            "function": lambda: self.show("starred")
        }
        options["archive"] = {
            "text": "Show archived mails",
            "function": lambda: self.show("archive")
        }
        options["spam"] = {
            "text": "Show spam mails",
            "function": lambda: self.show("spam")
        }
        options["trash"] = {
            "text": "Show trash mails",
            "function": lambda: self.show("trash")
        }
        options["allmail"] = {
            "text": "Show all mails",
            "function": lambda: self.show("allmail")
        }

        return options

    def get_options_for_anonymous(self):
        options = self.get_options_for_any()
        options["l"] = {
            "text": "Login",
            "function": self.login
        }
        return options

    def get_options(self):
        return self.get_options_for_non_anonymous() if self.is_logged_in else self.get_options_for_anonymous()

    def start(self):
        self.display()
        while True:
            options = self.get_options()
            choice = input("> ").lower()

            if choice in options:
                options[choice]["function"]()
            else:
                self.display()

    def display(self):
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
