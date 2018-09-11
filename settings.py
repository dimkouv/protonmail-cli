# ProtonMail user name.
username = "mymail@protonmail.com"

# ProtonMail user password.
password = "mysafepass"

# File to store logs. Leave empty string to display in stdout.
logfile = ""
#logfile = "protonmail-cli.log"

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

#####################################################################
# ProtonMail web interface variables

# Current WebClient version: v3.14.10

# Main URL for the login interface.
url = "https://mail.protonmail.com/login"

# login variables
element_login = dict(
    # ID of the username element of the login page.
    username_id = "username",
    
    # ID of the password element of the login page.
    password_id = "password",

    # Class of an element to check to validate that the user login page completed.
    after_login_detection_class = "conversation-meta"
)

element_twofactor = dict(
    # ID of the two factor authentication element of the login page.
    detection_id = "pm_loginTwoFactor",

    # ID of the two factor authentication code element of the login page.
    code_id = "twoFactorCode"
)

# list-inbox variables
element_list_inbox = dict(
    # Class of the element representing an email in the conversation frame.
    individual_email_soupclass = ".conversation-meta",

    # Class of the subject for an email.
    individual_email_subject_soupclass = ".subject",

    # Class of the time sent for an email.
    individual_email_time_soupclass = ".time",

    # Class of the sender's name for an email.
    individual_email_sender_name_soupclass = ".senders-name"
)

# send-mail variables
element_send_mail = dict(
    # Class of the element to find to open the email composer.
    open_composer_class = "sidebar-btn-compose",

    # Class of the element to wait on while the mail dialog opens.
    composer_detection_class = "composer",

    # CSS selector of the element representing the "To" field of composing an email.
    to_field_css = ".composer-field-ToList input",

    # CSS selector of the element representing the "Subject" field of composing an email.
    subject_field_css = ".subjectRow input",

    # Switch to the IFrame containing the text field to type the body of the email.
    switch_to_message_field_class = "squireIframe",
    # CSS selector of the actual element of the body of the email.
    message_field_css = "html.angular-squire-iframe body",

    # CSS selector of the send email button.
    send_button_css = ".btnSendMessage-btn-action"
)
