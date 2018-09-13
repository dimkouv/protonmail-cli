# ProtonMail user name.
username = "mymail@protonmail.com"

# ProtonMail user password.
password = "mysafepass"

# File to store logs. Leave empty string to display in stdout.
logfile = ""
# logfile = "protonmail-cli.log"

# Number of rows to keep in the log file.
logfile_rows_keep = 10000

# Time to wait for a page to load in seconds.
# Increase in case of timeout errors.
load_wait = 5

# Number of retries before exit.
# Increase in case of timeout errors.
max_retries = 5

# Do not hide the browser under xvfb, useful for debugging.
show_browser = False

# Check mail frequency in seconds
# (used only in case of `check-inbox` operation).
# Set to 0 to check just once.
check_mail_period = 60

# Set date order
# "asc | des"
date_order = "asc"

# Max number of displayed mails.
mails_read_num = 10
