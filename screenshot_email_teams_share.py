# import packages for taking screenshot from PDF
from pdf2image import convert_from_path

# import packages for cropping screenshot
from PIL import Image

# import packages for taking screenshot from web
# from selenium import webdriver
# from selenium.webdriver import ChromeOptions
import time

# import packages to move your PNG files
import shutil, os, glob, sys

# import packages for configuring email
import smtplib
import email.utils
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64

# import packages for sending messages on MSFT Teams
# import pymsteams

##########################################################
########### PART - I.a - TAKING PDF SCREENSHOT ###########
##########################################################
print("Initiating screenshot sequence... now...\n")

script_path = os.path.dirname(os.path.abspath(__file__))
print("Your Python script is placed at: ", script_path)

parentDir = os.path.dirname(script_path)
pdf_path = os.path.join(parentDir, "XXXX")
print("Your PDF is placed in: ", pdf_path)
pdf_to_read = os.path.join(pdf_path, "XXXX.pdf")
# print("Name of your PDF is: ", pdf_to_read)

image_output_path = os.path.join(parentDir, "XXXX")
# print("Your screenshot will be saved at: ", image_output_path)

# convert only page 1 of PDF to JPEG
images = convert_from_path(pdf_to_read, 500, single_file=True, output_folder=image_output_path, fmt="PNG", output_file="XXXX")

print("Screenshot taken and is saved at: ", image_output_path)

time.sleep(2)

##########################################################
########### PART - I.a.1 - CROPPING SCREENSHOT #############
##########################################################

image_to_crop = Image.open(os.path.join(image_output_path, "XXXX.png"), "r")

# (https://pillow.readthedocs.io/en/stable/handbook/concepts.html#coordinate-system)
crop_box = (200, 300, 7900, 7800) #(left, upper, right, lower)

output_image_intermediate = image_to_crop.crop((crop_box))
newsize = (1680, 1680)
output_image = output_image_intermediate.resize(newsize)
output_image.save(os.path.join(image_output_path, "XXXX.png"), quality=100)

print("Screenshot is cropped and saved at: ", image_output_path)

##########################################################
########### PART - I.b - TAKING WEB SCREENSHOT ###########
##########################################################

# print("Initiating screenshot sequence... now...\n")
#
# # URL to open exact dashboard (please pass &uid &pwd in the URL, not so secured)
# mstr_conn = "https://XXXX/MicroStrategyXXX/servlet/mstrWeb?evt=2048001&src=mstrWeb.2048001&documentID=XXXX&currentViewMedia=1&visMode=0&Server=XXXX&Port=0&share=1&uid=XXXX&pwd=XXXX"
# print("MicroStrategy Connection established... please wait... for 10 seconds")
#
# options = ChromeOptions()
# options.headless = True
#
# # (width x height) This is critical to avoid horizontal & vertical scrolls
# options.add_argument('window-size=1653x1500')
#
# driver = webdriver.Chrome(options=options)
# driver.get(mstr_conn)
#
# time.sleep(10)
# print("Accessing the dashboard now...")
#
# fileDir = os.path.dirname(os.path.abspath(__file__))
#
# S = lambda X: driver.execute_script('return document.body.parentNode.scroll' + X)
# driver.set_window_size(S('Width'), S('Height'))
#
# # Select the div class id, you want to include in your screenshot
# driver.find_element_by_id('mstr55').screenshot('XXXX.png')
# print("Code has now taken the full page screenshot...")
#
# time.sleep(2)
#
# print("Screenshot taken and is saved as XXXX.png at", fileDir)
#
# time.sleep(2)
#
# # print("Now copying your PNG files to I - Server location")
# # source_dir = fileDir
# # dest_dir = "C:\\Users\\XXXX\\XXXX"
# #
# # files = glob.iglob(os.path.join(source_dir, "*.png"))
# # print (files)
# # for file in files:
# #     if os.path.isfile(file):
# #         shutil.copy2(file, dest_dir)
# # print("Screenshot copied as mstr.png at", dest_dir)
#
# # # this code below will delete PNG files from source_dir
# # test = os.listdir(dest_dir)
# # for item in test:
# #     if item.endswith(".png"):
# #         os.remove(item)
#
# driver.quit()
# # driver.close()
# print("Taking screenshot script ends here...")

##########################################################
############## PART - II - SENDING EMAIL #################
##########################################################

image_to_read = os.path.join(image_output_path, "XXXX.png")

date_path = os.path.join(parentDir, "XXXX")
date_to_read_inter = open(os.path.join(date_path, "date.txt"), "r").readlines()
date_to_read = date_to_read_inter[1]


# "From" address. This address must be verified (for AWS SES).
SENDER = 'MXXXX@XXXX.com'
SENDERNAME = 'MicroStrategy Distribution Service'

# "To" address. These address must be verified (for AWS SES).
RECIPIENT  = ['xxxx@xxxx.com', 'xxxx@xxxx.com', 'xxxx@xxxx.com', 'xxxx@xxxx.com']

# Replace with client's SMTP details
# Replace smtp_username with your Amazon SES SMTP user name.
USERNAME_SMTP = "AKIAR3ZTJSLKH4GRXXXX"

# Replace smtp_password with your Amazon SES SMTP password.
PASSWORD_SMTP = "BC4HL1goasn0N7+FLTEYDkdcQehCdf7mWhOP/R1kXXXX"

# Amazon SES endpoint in the appropriate AWS region.
# HOST = "email-smtp.us-xxxx-2.amazonaws.com"
# PORT = 587
HOST = "xxxx.xxxx.com"
PORT = 25

# The subject line of the email.
SUBJECT = 'XXXX'

# The email body for recipients with non-HTML email clients (if user happen to receive only plain text emails).
BODY_TEXT = ("All,\r\n"
             "\n"
             "Attached is the XXXX report for the week ending last Friday. As always, let us know if you have any questions."
            )

# Encode your image for inline rendering & to avoid SPAM. Important!
encoded = base64.b64encode(open(image_to_read, "rb").read()).decode()

# The HTML body of the email.
BODY_HTML = f"""\
<html>
<body>
<p style="font-size:100%;font-family:Trebuchet MS;">
All,
<br>
<br>
Attached is the XXXX report for the week ending: <span>{date_to_read:}</span>. As always, let us know if you have any questions.
</p>
<img src="data:image/png;base64,{encoded}">
<br>
<p style="font-size:100%;font-family:Trebuchet MS;">
Thanks & Regards,
<br>
XXXX Team
</p>
<br>
<p style="font-size:100%;font-family:Trebuchet MS;">
<i>Please do not reply to this email. Mailbox MicroStrategyDS@XXXX.com is not monitored</i>
</p>

</body>
</html>
"""

# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = SUBJECT
msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
msg['To'] = ", ".join(RECIPIENT)


# Record the MIME types of both parts - text/plain and text/html.
part1 = MIMEText(BODY_TEXT, 'plain')
part2 = MIMEText(BODY_HTML, 'html')

# Open PDF file in binary mode
filename = "XXXX.pdf"

# We assume that the file is in the directory where you run your Python script from
with open(pdf_to_read, "rb") as attachment:
    # The content type "application/octet-stream" means that a MIME attachment is a binary file
    part3 = MIMEBase("application", "octet-stream")
    part3.set_payload(attachment.read())

# Encode PDF to base64 to avoid SPAM. Important!
encoders.encode_base64(part3)

# Add header
part3.add_header(
    "Content-Disposition",
    f"attachment; filename= {filename}",
)

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case the HTML message, is best and preferred.
msg.attach(part1)
msg.attach(part2)
msg.attach(part3)
text = msg.as_string()

# Try to send the message.
try:
    server = smtplib.SMTP(HOST, PORT)
    server.ehlo()
    server.starttls()
    # stmplib docs recommend calling ehlo() before & after starttls()
    server.ehlo()
    # server.login(USERNAME_SMTP, PASSWORD_SMTP)
    server.sendmail(SENDER, RECIPIENT, msg.as_string())
    server.close()
# Display an error message if something goes wrong.
except Exception as e:
    print ("Error: ", e)
else:
    print ("Email sent! Emailing script ends here")

##########################################################
####### PART - III - SENDING MESSAGE ON MSFT TEAMS #######
##########################################################

# You must create the connectorcard object with the Microsoft Webhook URL
# myTeamsMessage = pymsteams.connectorcard("https://outlook.office.com/webhook/XXXX/IncomingWebhook/XX/XXXX")
#
# # Add text to the message.
# myTeamsMessage.text("All, Attached is the Sample Dashboard for the week ending last Friday. As always, let us know if you have any questions.")
#
# myMessageSection = pymsteams.cardsection()
# myMessageSection.activityImage("http://i.imgur.com/c4jt321l.png")
#
# myTeamsMessage.addSection(myMessageSection)
#
# # send the message.
# myTeamsMessage.send()

# print("Message sent! Messaging script ends here...")