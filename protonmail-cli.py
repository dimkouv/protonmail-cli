#!/usr/bin/env python
import argparse
import configparser
import getpass
import os
import sys
import time

from protonmail import core, interactive, settings, utilities


def subcommand_list(args):
    for mail in client.get_mails(args.type):
        print(mail)


def subcommand_check(args):
    while True:
        if client.has_new_mail():
            print("New mail arrived")
            os.system(
                "notify-send 'You received a new mail on your ProtonMail inbox'")
        else:
            print("You don't have new mails")

        if settings.check_mail_period == 0:
            break
        else:
            print("Checking again in %ds" % settings.check_mail_period)
            time.sleep(settings.check_mail_period)


def subcommand_send(args):
    try:
        client.send_mail(args.to, args.subject, args.body,
                         args.html, args.attachment)
        print("Mail sent")
    except Exception as e:
        utilities.log("Unable to send email. Reason: " + str(e))


def overwrite_settings(args):
    if args.credential:
        config = configparser.ConfigParser(interpolation=None)
        config.read(args.credential.name)

        if "credential" in config:
            if "username" in config["credential"] and "password" in config["credential"]:
                settings.username = config["credential"]["username"]
                settings.password = config["credential"]["password"]

    if not settings.username:
        settings.username = input("ProtonMail email or username: ")

    if not settings.password:
        settings.password = getpass.getpass("ProtonMail password: ")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Command line utility for https://protonmail.com",
        epilog="Author: {name} <{email}> {url}".format(
            name="dimkouv",
            email="dimkouv@protonmail.com",
            url="dimkouv@protonmail.com"))

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="%(prog)s {version}".format(version="0.0.6"))

    parser.add_argument(
        "--credential",
        help="File path of the credential file. If present and not empty, will override any user/password found inside settings.py.",
        metavar="FILE_PATH",
        type=argparse.FileType("r"))

    subparsers = parser.add_subparsers(
        title="actions",
        description="The high level actions available to ProtonMail CLI. For more details, the help flag is available for all actions.",
        metavar="action")

    # Required to be set after the creation because of bug: https://stackoverflow.com/a/18283730
    subparsers.required = True

    # List mails arguments
    list_inbox_parser = subparsers.add_parser(
        "list",
        aliases=["l"],
        help="Print the latest mails titles.")
    list_inbox_parser.set_defaults(func=subcommand_list)

    list_inbox_parser.add_argument(
        "-t",
        "--type",
        help="Which directory you want to list: inbox drafts sent starred archive spam trash allmail",
        required=True
    )

    # Check inbox arguments
    check_inbox_parser = subparsers.add_parser(
        "check",
        aliases=["c"],
        help="Check the inbox for new mail and displays a system notification.")
    check_inbox_parser.set_defaults(func=subcommand_check)

    # Send email arguments
    send_mail_parser = subparsers.add_parser(
        "send",
        aliases=["s"],
        help="Send an email to the specified addresses.")
    send_mail_parser.set_defaults(func=subcommand_send)

    send_mail_parser.add_argument(
        "-t",
        "--to",
        help="Recipient's address. Unlimited number of -t can be added.",
        action="append",
        required=True)
    send_mail_parser.add_argument(
        "-s",
        "--subject",
        help="Subject",
        required=True)
    send_mail_parser.add_argument(
        "-b",
        "--body",
        help="Body text",
        required=True)
    send_mail_parser.add_argument(
        "-a",
        "--attachment",
        help="Attachment file location",
        action="append",
        required=False
    )
    send_mail_parser.add_argument(
        "--html",
        help="Pass this parameter to render body as html",
        required=False,
        action='store_true'
    )

    args = parser.parse_args()
    overwrite_settings(args)
    return args


if __name__ == "__main__":
    if len(sys.argv) > 1:
        args = parse_args()

        client = core.ProtonmailClient()
        client.login(
            settings.username,
            settings.password,
        )
        args.func(args)
    else:
        # run an interactive session
        session = interactive.InteractiveSession()
        session.start()
