# Protonmail CLI
Command line utility to read my protonmail inbox 

## Setup
```
apt install xvfb

pip install -r requirements.pip
```

## Usage
```
# get an overview of the inbox
protonmail-cli list-inbox

# check for mail and display notification on mail arrival
protonmail-cli check-inbox
```


## Todo
- Also monitor spam folder
- Wrap as a `systemd` service
- Fix @BUG
