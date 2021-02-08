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

input_path = os.path.dirname(os.path.abspath(__file__))
# output_path = os.path.dirname(os.path.abspath(__file__))
print(input_path)
# print(output_path)
pdfname = input_path+"\\Sample_Dashboard.pdf"

# convert all PDF pages to JPEGs
# images = convert_from_path(pdfname, 500)
# i = 1
# len=len(images)
# print("Number of pages in PDF = "+str(len))
# for image in images:
#     image.save('mstr' + str(i) + '.png', 'PNG')
#     i = i + 1

# convert only page 1 of PDF to JPEG
images = convert_from_path(pdfname, 500, single_file=True)
images[0].save('mstr1.png', 'PNG')

print("Screenshot taken and is saved as mstr1.png at", input_path)

# crop image for email embedding
input_image = Image.open(input_path+"\\mstr1.png", "r")

crop_box = (0, 0, 7900, 7900)
output_image_1 = input_image.crop((crop_box))

# resize the image
newsize = (1000, 1000)
output_image = output_image_1.resize(newsize)
output_image.save(input_path+"\\mstr.png", quality=100)

print("Screenshot cropped and is saved as mstr.png at", input_path)

time.sleep(2)

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
# driver.find_element_by_id('mstr55').screenshot('mstr.png')
# print("Code has now taken the full page screenshot...")
#
# time.sleep(2)
#
# print("Screenshot taken and is saved as mstr.png at", fileDir)
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

# "From" address. This address must be verified.
SENDER = 'XXXX@example.com'
SENDERNAME = 'XXXX'

# "To" address. This address must be verified.
# Notice the space between ", "
RECIPIENT  = ['XXX@customer.com', 'XXX@customer.com', 'XXX@customer.com', 'XXX@customer.com']

# Replace with Customer's SMTP details
# Replace smtp_username with your Amazon SES SMTP user name.
USERNAME_SMTP = "AKIAR3ZXXXXXX"

# Replace smtp_password with your Amazon SES SMTP password.
PASSWORD_SMTP = "XXXX"

# Amazon SES endpoint in the appropriate AWS region.
HOST = "email-smtp.us-XXXX.amazonaws.com"
PORT = 587

# The subject line of the email.
SUBJECT = 'Sample Name Dashboard'

# The email body for recipients with non-HTML email clients (if user happen to receive only plain text emails).
BODY_TEXT = ("All,\r\n"
             "Attached is the Sample Dashboard for the week ending last Friday. As always, let us know if you have any questions."
            )

# Encode your image for inline rendering & to avoid SPAM. Important!
encoded = base64.b64encode(open("mstr.png", "rb").read()).decode()

# The HTML body of the email.
BODY_HTML = f"""\
<html>
<body>
<p style="font-size:100%;font-family:Trebuchet MS;">
All,
<br>
Attached is the Sample Dashboard for the week ending last Friday. As always, let us know if you have any questions.
</p>
<img src="data:image/png;base64,{encoded}">
<br>
<p style="font-size:100%;font-family:Trebuchet MS;">
Thanks & Regards,
<br>
XXXX.
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
filename = "Sample_Dashboard.pdf"

# We assume that the file is in the directory where you run your Python script from
with open(filename, "rb") as attachment:
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
    server.login(USERNAME_SMTP, PASSWORD_SMTP)
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

print("Message sent! Messaging script ends here...")