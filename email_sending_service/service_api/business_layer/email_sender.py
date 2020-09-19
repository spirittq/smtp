import json
import smtplib


class EmailSender:
    def __init__(self, service_repository):
        self.sender = None
        self.recipient = None
        self.subject = None
        self.message = None
        self.raw_id = None
        self.service_repository = service_repository

    def save_email_raw_data(self, content):
        self.raw_id = self.service_repository.save_email_raw_data(content)

    def raw_data_parse(self, raw_data):
        json_data = json.loads(raw_data)
        self.sender = json_data['sender']
        self.recipient = json_data['recipient']
        self.subject = json_data['subject']
        self.message = json_data['message']

    def save_email(self):
        email_id = self.service_repository.save_email(self.raw_id, self.sender, self.recipient, self.subject, self.message)
        return email_id

    def send_email(self):
        try:
            message = f""
            smtpObj = smtplib.SMTP('localhost', 25)
            smtpObj.sendmail(self.sender, self.receiver, self.message)
            print("Successfully sent email")
        except Exception:
            print("Error: unable to send email")