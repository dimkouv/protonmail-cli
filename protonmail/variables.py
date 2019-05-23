# ProtonMail web interface variables
# Current WebClient version: v3.14.10

# Base URL for the ProtonMail web interface
base_url = "https://mail.protonmail.com"

# Main URL for the login interface.
url = base_url + "/login"

# Pages that contain mails and their urls
page_urls = dict(
    inbox="https://mail.protonmail.com/inbox",
    drafts="https://mail.protonmail.com/drafts",
    sent="https://mail.protonmail.com/sent",
    starred="https://mail.protonmail.com/starred",
    archive="https://mail.protonmail.com/archive",
    spam="https://mail.protonmail.com/spam",
    trash="https://mail.protonmail.com/trash",
    allmail="https://mail.protonmail.com/allmail",
    account="https://mail.protonmail.com/account"
)

# login variables
element_login = dict(
    # ID of the username element of the login page.
    username_id="username",

    # ID of the password element of the login page.
    password_id="password",

    # Class of an element to check to validate that the user login page completed.
    after_login_detection_class="sidebar"
)

# account variables
element_account = dict(
    # user's name input box ID on account settings page
    display_name="displayName",

    # save button class on account settings page
    save_btn="identitySection-form .pm_button.primary",

    # back button class to return back to main page
    back_btn="sidebar-btn-back"
)

element_twofactor = dict(
    # ID of the two factor authentication element of the login page.
    detection_id="pm_loginTwoFactor",

    # ID of the two factor authentication code element of the login page.
    code_id="twoFactorCode"
)

# list-inbox variables
element_list_inbox = dict(
    # ID of the wrapper for conversations list
    email_list_wrapper_id="conversation-list-columns",

    # Class of the element representing an email in the conversation frame.
    individual_email_soupclass=".conversation-meta",

    # Class of the subject for an email.
    individual_email_subject_soupclass=".subject",

    # Class of the time sent for an email.
    individual_email_time_soupclass=".time",

    # Class of the sender's name for an email.
    individual_email_sender_name_soupclass=".senders-name"
)

# send-mail variables
element_send_mail = dict(
    # Class of the element to find to open the email composer.
    open_composer_class="sidebar-btn-compose",

    # Class of the element to wait on while the mail dialog opens.
    composer_detection_class="composer",

    # CSS selector of the element representing the "To" field of composing an email.
    to_field_css=".composer-field-ToList input",

    # CSS selector of the element representing the "Subject" field of composing an email.
    subject_field_css=".subjectRow input",

    # Switch to the IFrame containing the text field to type the body of the email.
    switch_to_message_field_class="squireIframe",
    # CSS selector of the actual element of the body of the email.
    message_field_css="html.angular-squire-iframe body",

    # CSS selector of the send email button.
    send_button_css=".btnSendMessage-btn-action",

    # CSS selector for 'as attachment' button that appears when you try
    # to add an image as attachment
    as_attachment_btn="button.pm_button.primary.composerAskEmbdded-btn-attachment"
)

element_folders_labels = dict(
    # CSS selector for a list-item in the sidebar
    # indicating either a folder or label
    list_element_selector=".menuLabel-item",

    # CSS selector specific to folders in the list of folders and labels
    folder_element_selector=".fa-folder.menuLabel-icon",

    # CSS selector specific to labels in the list of folders and labels
    label_element_selector=".fa-tag.menuLabel-icon",

    # CSS selector for the title in a folder or label list-item
    list_element_title_selector=".menuLabel-title"
)

# Other variables used by protonmail-cli
mail_hash_filename = "mails_hash.txt"
