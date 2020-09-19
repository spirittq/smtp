import json
import logging

logger = logging.getLogger(__name__)


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
        try:
            self.raw_id = self.service_repository.save_email_raw_data(content)
        except Exception:
            logger.exception('save_email_raw_data')
            raise

    def raw_data_parse(self, raw_data):
        try:
            json_data = json.loads(raw_data+'oojoij')
            self.sender = json_data['sender']
            self.recipient = json_data['recipient']
            self.subject = json_data['subject']
            self.message = json_data['message']
        except Exception:
            logger.exception('raw_data_parse')
            raise

    def save_email(self):
        try:
            email_id = self.service_repository.save_email(self.raw_id, self.sender, self.recipient, self.subject, self.message)
            return email_id
        except Exception:
            logger.exception('save_email')
            raise

    def send_email(self, message_id):
        try:
            message = 'Subject: {}\n\n{}'.format(self.subject, self.message)
            self.smtpobj.sendmail(self.sender, self.recipient, message)
            self.set_status_success(message_id)
            print("Successfully sent email")
        except Exception:
            self.set_status_failed(message_id)
            logger.exception('send_email')
            raise

    def set_status_success(self, message_id):
        try:
            self.service_repository.set_status_success(message_id)
        except Exception:
            logger.exception('set_status_success')
            raise

    def set_status_failed(self, message_id):
        try:
            self.service_repository.set_status_failed(message_id)
        except Exception:
            logger.exception('set_status_failed')
            raise

    def execute(self):
        try:
            self.save_email_raw_data(self.content)
            self.raw_data_parse(self.content)
            message_id = self.save_email()
            self.send_email(message_id)
            return message_id
        except Exception:
            logger.exception('execute')
            raise