# Protonmail CLI
Command line utility to read my protonmail inbox 

## Setup
```
apt install xvfb

pip install requirements.pip
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
