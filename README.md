# Mass mail attach and send
Send multiple emails with attachements. Use after mail merge to send the created documents by email
## What this script does
Based on a number of files and a list of contacts csv file, it sends an email to each contact with the corresponding file attachement.
## But you can do that with libreoffice!
I know and i have used it before. The problem is it does not work always and it's extremely buggy. You can do the same with MS Word
but as far as i know you need paid plugins. If you know basic python you will find this script more fun to use and you can easily customise to it
for more complex scenarios.
## How to use it
###

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



all contactd with 
You want for example to send certificates to a number of students. Using mail merge with MS Office or LibreOffice
you can easily create the certificates based on csv file with names and other data fields. The problem is that
MS Word does not support mail 
