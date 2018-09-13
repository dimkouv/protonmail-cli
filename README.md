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

# install globally for usage from terminal
ln -s /opt/protonmail-cli/protonmail-cli.py /bin/protonmail-cli
pip3 install -r /opt/protonmail-cli/requirements.pip

# install as a python3 package
pip3 install /opt/protonmail-cli
```

## Usage

### Use as a command line

`protonmail-cli` works with sub-command, like the cli command `git`. To see all possible usage, each sub-command have their own `--help` section.

```bash
# show full usage
protonmail-cli --help

# list inbox - print latest mails
protonmail-cli list

# check inbox for new mails
protonmail-cli check

# send mail
protonmail-cli send \
    -t "one@protonmail.com" \
    -t "two@pm.me" \
    -s "my subject" \
    -b "my mail message"
```

*Global settings, including user credentials, can be specified on* `/opt/protonmail-cli/protonmail/settings.py`

User credentials can also be set in their own file, overriding those found inside `settings.py`. The global argument `--credential` allow you to set the file path of this config file. This would allow better security by allowing each user of a multi-users machine to keep their credentials inside their home folder. For even better security, `chmod 600` this file, so only the user launching the application can read it. What follow is an example credential file:

```ini
# The [credential] section is required, otherwise, credential values won't be parsed.
[credential]
username = mymail@protonmail.com
password = mysafepass
```

### Use as a package

```python
import protonmail

client = protonmail.core.ProtonmailClient()
client.login("mymail@protonmail.com", "mypassword")

# send mails
client.send_mail(
    ["one@protonmail.com", "two@pm.me"],
    "subject",
    "my mail message"
)

# read mails
mails = client.read_mails()

# check for new mail
has_new_mail = client.has_new_mail()
```
