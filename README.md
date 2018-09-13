# ProtonMail CLI
Command line utility for https://protonmail.com

## Installation
System dependencies
```bash
apt install -y xvfb python3-pip firefox                 # on debian
dnf install xorg-x11-server-Xvfb python3-pip firefox    # on fedora
```

Geckodriver
```bash
# Find your release: https://github.com/mozilla/geckodriver/releases

# for linux x64
wget https://github.com/mozilla/geckodriver/releases/download/v0.21.0/geckodriver-v0.21.0-linux64.tar.gz

tar -xvf geckodriver-*.tar.gz -C /bin/
rm geckodriver-*.tar.gz
```

Protonmail CLI
```bash
git clone https://github.com/dimkouv/protonmail-cli /opt/protonmail-cli
ln -s /opt/protonmail-cli/protonmail-cli.py /bin/protonmail-cli

pip3 install -r /opt/protonmail-cli/requirements.pip
```

Test the installation by running `protonmail-cli --help` on a new terminal.

Settings including user credentials can be specified on  
`/opt/protonmail-cli/protonmail/settings.py`

## Usage

Use from command line

```bash
usage: protonmail-cli.py [-h] action ...

ProtonMail CLI tool

optional arguments:
  -h, --help  show this help message and exit

actions:
  The high level actions available to ProtonMail CLI. For more detail, the
  help flag is available for all actions.

  action
    list (l)  Print the latest mails title from the inbox.
    check (c)
              Check the inbox for new message and displays a system
              notification.
    send (s)  Send an email to the specified addresses.
            optional arguments:
              -t TO, --to TO        Recipient's address
              -s SUBJECT, --subject SUBJECT
                                    Subject
              -b BODY, --body BODY  Body text
```

Use as a package

```
git clone https://github.com/dimkouv/protonmail-cli
pip3 install ./protonmail-cli
```

```python3
import protonmail

client = protonmail.core.ProtonmailClient()
client.login("mymail@protonmail.com", "mypassword")

# send mails
client.send_mail(
    ["one@protonmail.com", "two@pm.me"],
    "hello friend",
    "I am writing you to let you know about..."
)

# read mails
mails = client.read_mails()

# check for new mail
client.check_for_new_mail()
```
