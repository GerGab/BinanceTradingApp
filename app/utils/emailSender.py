from config import SmtpConfig
import smtplib
from email.message import EmailMessage

def send_email(message):
    
    msg = EmailMessage()
    msg['Subject'] =message['subject']
    msg['FROM'] = SmtpConfig.MAIL_USERNAME
    msg['To'] = SmtpConfig.MAIL_RECIPIENTS
    msg.set_content(message['content'])

    with smtplib.SMTP_SSL(SmtpConfig.MAIL_SERVER,SmtpConfig.MAIL_PORT) as smtp:
        smtp.login(SmtpConfig.MAIL_USERNAME,SmtpConfig.MAIL_PASSWORD)
        smtp.send_message(msg)
