#!/usr/bin/python3
import argparse
import time

from protonmail import core, settings, utilities


def subcommand_list(args):
    print("Action: list emails")

    for mail in client.read_mails():
        utilities.print_mail(mail)


def subcommand_check(args):
    print("Action: check emails")

    while True:
        client.check_for_new_mail()
        if settings.check_mail_period == 0:
            break
        else:
            print("Checking again in %ds" % settings.check_mail_period)
            time.sleep(settings.check_mail_period)


def subcommand_send(args):
    print("Action: send email")

    try:
        client.send_mail(args.to, args.subject, args.body)
        print("Mail sent")
    except Exception as e:
        utilities.log(str(e), "ERROR")


def parse_args():
    """ """
    parser = argparse.ArgumentParser(
        description="ProtonMail CLI tool",
        epilog="Homepage: https://github.com/dimkouv/protonmail-cli")

    subparsers = parser.add_subparsers(
        title="actions",
        description="The high level actions available to ProtonMail CLI. For more detail, the help flag is available for all actions.",
        metavar="action")

    # Required to be set after the creation because of bug: https://stackoverflow.com/a/18283730
    subparsers.required = True

    # List inbox arguments
    list_inbox_parser = subparsers.add_parser(
        "list",
        aliases=["l"],
        help="Print the latest mails title from the inbox.")
    list_inbox_parser.set_defaults(func=subcommand_list)

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
        help="Recipient's address",
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

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    client = core.ProtonmailClient()
    client.login(
        settings.username,
        settings.password,
    )
    args.func(args)
