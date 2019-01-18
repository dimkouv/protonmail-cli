"""
A mail model, used for storing and printing loaded emails
"""
class Mail:
    def __init__(self, subject, time_received, mail_alias, mail):
        self.subject = subject
        self.time_received = time_received
        self.mail_alias = mail_alias
        self.mail = mail

    def __str__(self):
        """
        Mail string representation
        """
        res = "Date: %s\n" % self.time_received
        res += "From: [%s] %s\n" % (self.mail_alias, self.mail)
        res += "Subject: %s\n" % self.subject
        return res
