import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from configparser import ConfigParser
# from email import encoders
# import os.path

file = 'oms_config.ini'
config = ConfigParser()
config.read(file)

def send_email(email_sender_account, email_sender_password, email_recipients, email_subject, email_message):

    # msg = MIMEMultipart()
    # msg['From'] = email_sender_account
    # msg['To'] = email_recipients
    # msg['Subject'] = email_subject

    # msg.attach(MIMEText(email_message, 'plain'))

    sub = email_subject
    body = email_message
    msg = f"Subject: {sub}\n\n{body}"
    # try:
    # for email_recipient in email_recipients:
    #     print(email_recipient)
    with smtplib.SMTP(config['outlook_credentials']['server'], 587) as server:
        # server = smtplib.SMTP(config['outlook_credentials']['server'], 587)
        server.ehlo()
        server.starttls()
        server.login(email_sender_account, email_sender_password)
        # print(msg, type(msg))
        # text = msg.as_string()
        # for email_recipient in email_recipients:
        server.sendmail(email_sender_account, email_recipients, msg)
        print('email sent')
        server.quit()
    # except:
    #     print("SMTP server connection error")
    return True

print(list(config['outlook_credentials']['recepients'].split(',')))
# send_email(config['outlook_credentials']['account'], config['outlook_credentials']['pwd'], list(config['outlook_credentials']['recepients'].split(',')), 'Trail Run', 'Trail Run Successful!!')
