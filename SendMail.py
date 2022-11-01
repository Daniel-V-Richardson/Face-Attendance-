import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from decouple import config
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from datetime import datetime, timedelta
from email.mime.text import MIMEText


AttPath = "Attendance CSV"
now = datetime.now()
current_date= now.date()
current_date_string = str(current_date)
extension =".csv"
Attendance = 'Attendance_'+ current_date_string + extension


emailfrom = config('EMAIL_FROM')
emailto = config('EMAIL_TO')
print('Email sent to:- '+emailto)
fileToSend = f'{AttPath}/{Attendance}'
print(fileToSend)
filename= f'{Attendance}'
print(filename)
username = config('SMTP_USERNAME')
password = config('SMTP_PASSWORD')


msg = MIMEMultipart()
msg["From"] = emailfrom
msg["To"] = emailto
msg["Subject"] = "Attendance for the Date: "+f'{current_date}'
msg.preamble = "Attendance for the Date: "+f'{current_date}'

ctype, encoding = mimetypes.guess_type(fileToSend)
if ctype is None or encoding is not None:
    ctype = "application/octet-stream"

maintype, subtype = ctype.split("/", 1)

if maintype == "text":
    fp = open(fileToSend)
    # Note: we should handle calculating the charset
    attachment = MIMEText(fp.read(), _subtype=subtype)
    fp.close()
elif maintype == "image":
    fp = open(fileToSend, "rb")
    attachment = MIMEImage(fp.read(), _subtype=subtype)
    fp.close()
elif maintype == "audio":
    fp = open(fileToSend, "rb")
    attachment = MIMEAudio(fp.read(), _subtype=subtype)
    fp.close()
else:
    fp = open(fileToSend, "rb")
    attachment = MIMEBase(maintype, subtype)
    attachment.set_payload(fp.read())
    fp.close()
    encoders.encode_base64(attachment)
attachment.add_header("Content-Disposition", "attachment", filename=filename)
msg.attach(attachment)

server = smtplib.SMTP("smtp.gmail.com:587")
server.starttls()
server.login(username,password)
server.sendmail(emailfrom, emailto, msg.as_string())
server.quit()