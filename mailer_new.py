import smtplib, ssl
import csv
import time


from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

from pathlib import Path

# SMTP Server Settings
port = 587  # For SSL
host = "mail.sch.gr"
username = "yourusername"
password = "yourpassword"

# Email Settings
sender_email = "user@example.mail.com"
sender_name = "ΔΠΕ Σχολικές Δραστηριότητες"
bcc_email = "user@gmail.com"

subject = "Αποστολή Βεβαίωσης"
body = """
    Αγαπητέ/ή {name},
    
    Σας στέλνουμε τη βεβαίωση παρακολούθησης του σεμιναρίου "Το δώρο της βροχής" 
    
    Σχολικές Δραστηριότητες - ΔΠΕ Κυκλάδων
    """

files_folder = Path("files2/")

def create_email(name, receiver_email,filetoopen):
    # Create a multipart message and set headers
    message = MIMEMultipart()
    #message["From"] = sender_email
    message["From"] = formataddr((sender_name, sender_email))
    message["To"] = receiver_email
    message["Subject"] = subject
    #message["Bcc"] = bcc_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body.format(name=name), "plain"))

    #filename = "document.pdf"  # In same directory as script

    # Open PDF file in binary mode
    with open(filetoopen, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filetoopen.name}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()
    return text


# Create a secure SSL context
context = ssl.create_default_context()

# Try to log in to server and send email
try:
    server = smtplib.SMTP(host,port)
    server.ehlo() # Can be omitted
    server.starttls(context=context) # Secure the connection
    server.ehlo() # Can be omitted
    server.login(username, password)
    
    # Send emails

    with open("data_xrys_2.csv", encoding="utf8") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for name, receiver_email, filename, no in reader:
            print(f"Sending email to {name}")
            # Send email here
            filetoopen = files_folder / filename
            print(filetoopen)
            text = create_email(name,receiver_email,filetoopen)
            server.sendmail(sender_email, [receiver_email, bcc_email], text)
            time.sleep(2)

except Exception as e:
    # Print any error messages to stdout
    print(e)
finally:
    server.quit()



