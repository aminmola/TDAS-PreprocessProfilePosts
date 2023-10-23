import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
import json
import os


class Mail:
    def __init__(self, ):
        self.sender_email = 'kukalamolaei@gmail.com'
        self.receiver_email = '0059sharifloo@gmail.com'
        self.receiver_email2 = 'saramoody1997@gmail.com'
        self.password = 'poresbnqbpwlftdi'
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587
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
