from model_repository.models import EmailInfo
from django.core import serializers


class ServiceRepository:
    def __init__(self, cursor, logger):
        self.cursor = cursor
        self.logger = logger

    def read_email_info(self):
        try:
            email_info = EmailInfo.objects.using('postgres').all()
            json_data = serializers.serialize("json", email_info)
            return json_data
        except Exception:
            self.logger.exception('read_email_info')
            raise

    def save_email_raw_data(self, raw_data):
        try:
            self.cursor.callproc('save_email_raw_data', [raw_data, ])
            new_id = self.cursor.fetchone()[0]
            return new_id
        except Exception:
            self.logger.exception("save_email_raw_data")
            raise

    def save_email(self, raw_id, sender, recipient, subject, message):
        try:
            self.cursor.callproc('save_email_data', [
                raw_id,
                sender,
                recipient,
                subject,
                message,
            ])
            new_id = self.cursor.fetchone()[0]
            return new_id
        except Exception:
            self.logger.exception("save_email")
            raise

    def set_status_success(self, result_id):
        try:
            self.cursor.callproc('set_status_success', [result_id, ])
            new_id = self.cursor.fetchone()[0]
            return new_id
        except Exception:
            self.logger.exception("set_status_success")
            raise

    def set_status_failed(self, result_id):
        try:
            self.cursor.callproc('set_status_failed', [result_id, ])
            new_id = self.cursor.fetchone()[0]
            return new_id
        except Exception:
            self.logger.exception("set_status_failed")
            raise