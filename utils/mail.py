import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
import json
import os

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

import utils.config as cfg



class Mail:
    def __init__(self, ):
        self.sender_email = cfg.EMAIL_SENDER
        self.receiver_email = cfg.EMAIL_RECEIVER1
        self.receiver_email2 = cfg.EMAIL_RECEIVER2
        self.password = cfg.EMAIL_PASSWORD
        self.smtp_server = cfg.EMAIL_SMTP_SERVER
        self.smtp_port = cfg.EMAIL_SMTP_PORT
        self.server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        self.server.starttls()
        self.server.login(self.sender_email, self.password)

    def send(self, username, data, body):
        try:
            # Set up email addresses and login credentials
            with open("output.json", "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False)
                file.close()
            with open("output.json", "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            os.remove("output.json")
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {username}",
            )
            message = MIMEMultipart()
            message['From'] = self.sender_email
            message['To'] = self.receiver_email
            message['Subject'] = 'An Account is Registering'
            message.attach(part)

            # Add body to email
            message.attach(MIMEText(body, 'plain'))
            # Send email
            text = message.as_string()
            self.server.sendmail(self.sender_email, self.receiver_email, text)
            message['To'] = self.receiver_email2
            self.server.sendmail(self.sender_email, self.receiver_email2, text)

            # Close SMTP session
            # self.server.quit()
        except Exception as e:
            print(e)
