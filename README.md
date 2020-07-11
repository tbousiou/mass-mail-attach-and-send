# Mass mail attach and send
Send multiple emails with attachements. Use after mail merge to send the created documents by email
## What this script does
Based on a number of files and a list of contacts csv file, it sends an email to each contact with the corresponding file attachement.
## But you can do that with libreoffice or word!
I know and i have used it before. The problem with libreoffice is that it does not work always and it's extremely buggy. You can do the same with MS Word
but as far as i know you need paid plugins. If you know basic python you will find this script more fun to use and you can easily customise to it
for more complex scenarios.
# Run the  test demo
The repo includes an example csv file and file attachments to test the script. There is also an example configuration file
1. Clone the repository to your machine, you will need Python 3 installed to run the script
2. First create an account to mailtrap.io. This service gives you a virtual mailbox and smtp credentials.
3. Edit the config-example.ini file in the [TEST] section. You will need to enter **username** and **password** from mailtrap
4. Run the script in TEST mode (this is the default).
5. If there are no errors in your mailtrap.io mailbox you will be able to view the resulting emails. You can also see view the attached file.
# Use it in the real world
A typical use case scenario is: You want to send with email a bunch of certificates you produced with mail merge for your students
who completed a course.
1. First you need a csv file with at least an email column. Of course your csv file can contain other fields like name, surname to use them
in the text message. Put your csv file in the same folder with the script
2. Second you must have the list of corresponding files to attach. You can do this with mail merge or other method. The files must have
a naming convention with numbers and leading zeroes. For example certificate_01.pdf, certificate_02.pdf etc. Put these files in the **documents**
subfolder of the script folder. Also **important numbering starts from 01** and not from 00.
3. Now edit the config.ini file the **PRODUCTION** section. Read inside the config file for details. You definetaly must change email settings with
your chosen SMTP email provider. For frequent use and larage number of emails > 500 you might need to use a dedicated SMTP service like sendgrid or mailgun
4. Edit the settings for the csv filename and files naming scheme. Your files must have naming in the certificate_02.pdf format.
Sets the filename of the csv file

    `CONTACTS_CSV = contacts.csv`
    
Folder of the atachment files, leave it default

    `DOCS_FOLDER = documents/`
  
The prefix of your attachment files, i.e. certificate_, invoice_, use an underscore for readability

    `FILE_PREFIX = certificate_`
  
In case you want to rename the sent file, otherwise use the same value as FILE_PREFIX

    `SENT_FILE_PREFIX = certificate_`
  
The numbers of digits in the numberfing, for example 2 means 01, 02, .., 10

    `ZERO_PADDING = 2`
  
The file extesnion of your attachments

    `FILE_TYPE = pdf`
  
5. In the script set the configuration to production mode

    `CONFIG_TYPE = 'PRODUCTION'`
  
6. In the script customize the text message to send in each email. You can also use fields from your csv file like for example tha name of the
receiver
7. TEST AGAIN. Before sending 1000 emails send a couple of emails to real email providers. For example i send the first 3 emails to my gmail
using the gmailusername+1@gmail.com, gmailusername+1@gmail.com etc. This is important so i can check if gmail does not marks the email as spam.
Set the MAX_RECORDS variable to 3 for example and temporarily change the emails in the csv file. Using MAX_RECORDS you limit the amount of emails no matter
how many records exist in the csv file. When you are ready set the MAX_RECORDS to number equal or greater than the total records

    `MAX_RECORDS = 1000`
  
6. Run the script. The script outputs some basic info and does a very basic error handling. If an email fails the record number is put inside a list and printed at the end.

# Problems connecting and sending email
While writing this script i realised that anyhting can go wrong with email. First check your email settings and the recommended settings of your SMTP provider.
I admit this script is not handling all cases. What can i say **IT WORKS ON MY MACHINE**.

# DISCLAIMER
This is a hobby project and use at your own risk. Suggestions and corrections are welcomed.

