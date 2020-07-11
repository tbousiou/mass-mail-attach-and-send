# MASS MAIL WITH ATTACHEMENT
# Author: Theodoros Bousiou

# Description:
# Sends multiple emails with a coressponding pdf file attachement
# It reads a list of recepient emails from a csv file
# and attaches an existing pdf file for each recipeint from the documents directory.
# The script it's not total generic, but you can easily change it to your needs

# Use case:
# You want to send with email a bunch of files you produced with mail merge, for example certificates to students
# who completed a course. MS Word does not support out of the box this function, LibreOffice does but it's quite buggy

# Instructions:
# Put in the same directory a csv file with the recepient email and other info, i.e. name
# In the same directory, create a documents folder and copy/move the pdf files to be attached in each email
# Edit the SMTP and EMAIL settings. You can use mailtrap.io service for testing
# For testing change the number of MAX_RECORDS to a small number, when ready set this number to equal or greater than the actual total

import csv
import smtplib
import configparser

# import the corresponding modules
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import path
from time import sleep

# Set the configuration type, TEST or PRODUCTION
# Always test before sending mass emails, use a service like mailtrap.io to test
CONFIG_TYPE = 'TEST'
#CONFIG_TYPE = 'PRODUCTION'


# Load Configuration fron ini file and set values
config = configparser.ConfigParser()
config.read('config-example.ini')

SMTP_SERVER = config.get(CONFIG_TYPE, 'SMTP_SERVER')
PORT = config.get(CONFIG_TYPE, 'PORT')
TLS = config.get(CONFIG_TYPE, 'TLS')
USERNAME = config.get(CONFIG_TYPE, 'USERNAME')
PASSWORD = config.get(CONFIG_TYPE, 'PASSWORD')
DELAY_TIME = float(config.get(CONFIG_TYPE, 'DELAY_TIME'))

SENDER = config.get(CONFIG_TYPE, 'SENDER')
REPLY_TO_ADDRESS = config.get(CONFIG_TYPE, 'REPLY_TO_ADDRESS')
SUBJECT = config.get(CONFIG_TYPE, 'SUBJECT')

CONTACTS_CSV = config.get(CONFIG_TYPE, 'CONTACTS_CSV')
DOCS_FOLDER = config.get(CONFIG_TYPE, 'DOCS_FOLDER')
FILE_PREFIX = config.get(CONFIG_TYPE, 'FILE_PREFIX')
SENT_FILE_PREFIX = config.get(CONFIG_TYPE, 'SENT_FILE_PREFIX')
ZERO_PADDING = int(config.get(CONFIG_TYPE, 'ZERO_PADDING'))
FILE_TYPE = config.get(CONFIG_TYPE, 'FILE_TYPE')

MAX_RECORDS = int(config.get(CONFIG_TYPE, 'MAX_RECORDS'))

# Info about the emails that wont be sent due to errors will be stored in this list
# Useful to track wich emails need to be send again
errors = []

print("Running in", CONFIG_TYPE, "mode")
print("Trying to connect")
with smtplib.SMTP(SMTP_SERVER, PORT) as server:

    if TLS == 'ON':
        print("TLS is ON")
        server.ehlo()
        # For some reason my mail server does not have ssl certificate
        # I downloaded the certificate to the script folder and load it to the script
        # If you have problems connecting you might want to do the same trick
        # I dont know what i am doing here but it works for me!
        if path.exists('cert.pem'):
            print('Found certificate file cert.pem')
            server.starttls(certfile='cert.pem')
        else:
            server.starttls()
        server.login(USERNAME, PASSWORD)
        server.ehlo()

    else:
        server.ehlo()
        server.login(USERNAME, PASSWORD)
        server.ehlo()

    print("Login Succcess")

    with open(CONTACTS_CSV) as file:
        # Count number of data rows, skip first line
        row_count = sum(1 for row in file) - 1
        # Return file pointer to start
        file.seek(0)

        # Read csv file
        reader = csv.reader(file)
        next(reader)  # it skips the header row

        # Keeps track of current record
        record = 1

        print("Read csv file sucess")
        print("Start sending emails")

        # For every record, try to send email with attachement
        # In the example CSV i use the <fullname> and <email> fields
        for fullname, email in reader:
            try:
                # Create and attach the message body to the email
                # You need to customise this message according to your needs
                # You can also insert fields from your csv file.
                # In this example i use the fullname field
                message_body = (
                    f"Hello {fullname}\n"
                    f"Congratulations for your completion of the course. In the attachment you will find your certificate."
                )

                message_body = message_body.format(fullname=fullname)
                message = MIMEMultipart()
                message['Subject'] = SUBJECT
                message['From'] = SENDER
                message['To'] = email
                message.attach(MIMEText(message_body, "plain"))
                message.add_header('reply-to', REPLY_TO_ADDRESS)

                # Create and attach the file to the email
                # You might also need to chane this code
                # In my example the files have naming like certificate_01.pdf, certificate_02.pdf ...
                filename = FILE_PREFIX + \
                    str(record).zfill(ZERO_PADDING) + '.' + FILE_TYPE
                filepath = DOCS_FOLDER + filename
                sent_filename = SENT_FILE_PREFIX + \
                    str(record).zfill(ZERO_PADDING) + '.' + FILE_TYPE

                with open(filepath, "rb") as f:
                    attach = MIMEApplication(f.read(), _subtype=FILE_TYPE)
                attach.add_header('Content-Disposition',
                                  'attachment', filename=sent_filename)

                message.attach(attach)
                server.sendmail(SENDER, email, message.as_string())
                print(
                    f'{record} of {row_count}. Sent to {fullname}, {email}, with attached file {sent_filename}')
                # Need to delay every mail a bit to bypass mailtrap.io email per second rule.
                if DELAY_TIME > 0:
                    sleep(DELAY_TIME)

            except Exception as e:
                print(f"Error occured for {record}")
                print(e)
                errors.append([record, fullname, email])
            record += 1

            # Stop execution if
            if record > MAX_RECORDS:
                break

    print("Finished sending.")
    if errors:
        print("Errors found:", errors)
    else:
        print("No errors")
