import os

# ProtonMail user name or email.
username = ""

# ProtonMail user password.
password = ""

# Set date order
# "asc | des"
date_order = "asc"

# Max number of displayed mails.
# set to -1 for no limit
mails_read_num = -1

# Check mail period in seconds
check_mail_period = 60

# File to store logs from core. Leave empty string to display in stdout.
logfile = ""
# logfile = "protonmail-cli.log"

# Enables logging from core functions
# Choices are: ['', 'INFO', 'DEBUG']
# EMPTY: Display nothing at all
# INFO: Displays minimal messages that indicate progress and/or action results
# DEBUG: Displays many information about what's going under the hood
log_level = "INFO" 

# Number of rows to keep in the log file.
logfile_rows_keep = 10000

# Time to wait for a page to load in seconds.
# Increase in case of timeout errors.
load_wait = 1

# Number of retries before exit.
# Increase in case of timeout errors.
max_retries = 20

# Do not hide the browser under xvfb, useful for debugging.
show_browser = False

# Directory to use for logging
# user should have write access to this directory
work_directory = os.getenv("HOME") + "/.protonmail-cli/"
