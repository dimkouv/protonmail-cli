# Protonmail CLI
Command line utility to read my protonmail inbox 

## Setup
Download firefox `geckodriver` from mozilla
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

## Usage
```
# get an overview of the inbox
python3 protonmail-cli list-inbox

# check for mail and display notification on mail arrival
python3 protonmail-cli check-inbox
```


## Todo
- Also monitor spam folder
- Wrap as a `systemd` service
- Fix @BUG

