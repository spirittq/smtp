import json


class EmailSender:
    def __init__(self, service_repository, smtpobj, content):
        self.sender = None
        self.recipient = None
        self.subject = None
        self.message = None
        self.raw_id = None
        self.service_repository = service_repository
        self.smtpobj = smtpobj
        self.content = content

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

    def send_email(self, message_id):
        try:
            message = 'Subject: {}\n\n{}'.format(self.subject, self.message)
            self.smtpobj.sendmail(self.sender, self.recipient, message)
            self.set_status_success(message_id)
            print("Successfully sent email")
        except Exception:
            self.set_status_failed(message_id)
            print("Error: unable to send email")

    def set_status_success(self, message_id):
        self.service_repository.set_status_success(message_id)

    def set_status_failed(self, message_id):
        self.service_repository.set_status_failed(message_id)

    def execute(self):
        self.save_email_raw_data(self.content)
        self.raw_data_parse(self.content)
        message_id = self.save_email()
        self.send_email(message_id)
        return message_id
