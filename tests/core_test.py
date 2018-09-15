import unittest
from getpass import getpass

from protonmail import core, settings, utilities, variables

client = None


class CoreTest(unittest.TestCase):
    client = core.ProtonmailClient()
    settings.core_logging = True

    print("Give ProtonMail credentials to initiate tests,\n",
          "use an account that has at least one mail in inbox and spam.\n")

    username = input("ProtonMail username: ")
    password = getpass("ProtonMail password: ")
    test_address = input("Give a mail address to send test mail: ")

    def test_0_init_client(self):
        self.assertNotEqual(self.client.web_driver, None)

    def test_1_login(self):
        try:
            self.client.login("wrong username", "wrong password")
            self.fail("login() should fail but it appears that we're logged in")
        except Exception as e:
            pass

        try:
            self.client.login(self.username, self.password)
        except Exception as e:
            self.fail("login() unable to login with correct credentials:" + str(e))

    def test_2_get_mails(self):
        for page in variables.page_urls:
            try:
                mails = self.client.get_mails(page)
                if mails is None:
                    self.fail("[%s] unable to load conversation wrapper" % page)

                if page in ["inbox", "spam"] and len(mails) == 0:
                    # there should be at least one mail in inbox and spam
                    self.fail("[%s] no mails found" % page)

                print("[%-10s] total mails: %d" % (page, len(mails)))

            except Exception as e:
                self.fail("[%s] unable to read any mail error: %s" % (page, str(e)))

    def test_3_has_new_mail(self):
        # generate a hash of the current inbox
        self.client.has_new_mail()

        # test if has_new_mail returns False on no changes
        # ! we suppose that inbox wasn't changed during the tests
        self.assertEqual(self.client.has_new_mail(), False)

        # alter the hash to make it think that inbox was changed
        utilities.write_hash("hello_friend_this_is_random")
        self.assertEqual(self.client.has_new_mail(), True)

    def test_4_send_mail(self):
        self.client.send_mail(
            [self.test_address],
            "[protonmail-cli] success",
            "[Success] This message was automatically send from protonmail-cli tests."
        )

    def test_5_stop(self):
        self.client.destroy()

        self.assertEqual(self.client.web_driver, None)
        self.assertEqual(self.client.virtual_display, None)


if __name__ == '__main__':
    unittest.main()
