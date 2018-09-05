# Protonmail CLI
Command line utility for https://protonmail.com

## Usage
Open `settings.py` to specify your credentials.


```bash
> ./protonmail-cli.py list-inbox
    Prints the latest mail titles

> ./protonmail-cli.py check-inbox
    Checks for new message and displays a system notification
    check frequency is defined in settings.py

> ./protonmail-cli.py send-mail -to "address1;address2" \
                           -subject "subject" \
                           -body "message"
    Sends an email to the specified addresses.

> ./protonmail-cli.py help
    Prints this dialog
```

## Dependencies - Setup
Download and install firefox `geckodriver` from mozilla

```
https://github.com/mozilla/geckodriver/releases
```

After downloading extract and place `geckodriver` executable
under `/usr/bin/`

Install virtual display
```
apt install xvfb # debian
dnf install xorg-x11-server-Xvfb # fedora
```

Install python3 requirements
```
pip3 install -r requirements.pip --user
```

## Todo
- Also monitor spam folder
- Wrap as a `systemd` service
- Fix @BUG
