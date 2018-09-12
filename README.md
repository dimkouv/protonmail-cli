# Protonmail CLI
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

Test the installation by running `protonmail-cli help` on a new terminal.

Settings including user credentials can be specified on `/opt/protonmail-cli/settings.py`

## Usage

```bash
> protonmail-cli list-inbox
    Prints the latest mail titles

> protonmail-cli check-inbox
    Checks for new message and displays a system notification
    check frequency is defined in settings.py

> protonmail-cli send-mail -to "address1;address2" \
                           -subject "subject" \
                           -body "message"
    Sends an email to the specified addresses.

> ./protonmail-cli help
    Prints this dialog
```
