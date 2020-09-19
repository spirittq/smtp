import json


class EmailSender:
    def __init__(self, service_repository, smtpobj):
        self.sender = None
        self.recipient = None
        self.subject = None
        self.message = None
        self.raw_id = None
        self.service_repository = service_repository
        self.smtpobj = smtpobj

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

    def send_email(self, result_id):
        try:
            message = 'Subject: {}\n\n{}'.format(self.subject, self.message)
            self.smtpobj.sendmail(self.sender, self.recipient, message)
            self.change_status(result_id, True)
            print("Successfully sent email")
        except Exception:
            self.change_status(result_id, False)
            print("Error: unable to send email")

    def change_status(self, result_id, condition):
        self.service_repository.change_status(result_id, condition)
