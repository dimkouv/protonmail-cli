# protonmail username or email
username = "mymail@protonmail.com"

# protonmail password
password = "mysafepass"

# file to store log (leave empty string to display in cmd)
logfile = ""
#logfile = "protonmail-cli.log"

# number of rows to keep in the log file
logfile_rows_keep = 10000

# time to wait for a page to load in seconds
# increase in case of timeout errors
load_wait = 5

# number of retries before exit
# increase in case of timeout errors
max_retries = 5

# do not hide the browser under xvfb,
# useful for debugging
show_browser = False

# check mail frequency in seconds
# (used only in case of `check-inbox` operation)
# set to 0 to check just once
check_mail_period = 60

# set date order
# "asc | des"
date_order = "asc"

# max number of displayed mails
mails_read_num = 10
