import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json


def pySendEmail(smtp_server, port,subject,body, sender_email, receiver_email, password, emailAttachement):

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  

    message.attach(MIMEText(body, "plain"))
    filename = emailAttachement  # In same directory as script

    with open(filename, "rb") as attachment:
         part = MIMEBase("text", "plain")
         part.set_payload(attachment.read())

    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    try:
         server = smtplib.SMTP(smtp_server,port)
         server.ehlo() # Can be omitted
         server.starttls(context=context) # Secure the connection
         server.ehlo() # Can be omitted
         server.login(sender_email, password)
         server.sendmail(sender_email, receiver_email, text)
    except Exception as e:
         print(e)
    finally:
         server.quit()

# if __name__ == '__main__':
#      json_file = open("config.json")
#      jsonVars = json.load(json_file)
#      json_file.close()
#
#      body="Bacup log attached"
#      pySendEmail(jsonVars["Smtp"]["Server"], jsonVars["Smtp"]["Port"], jsonVars["Smtp"]["Subject"], body, \
#                  jsonVars["Smtp"]["SenderAddress"], jsonVars["Smtp"]["ToAddress"], jsonVars["Smtp"]["Password"], \
#                  "pymysqldump.log")



