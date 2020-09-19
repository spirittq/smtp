from model_repository.models import EmailInfo
from django.core import serializers
import json


class ServiceRepository:
    def __init__(self, cursor):
        self.cursor = cursor
        # self.app_logger = app_logger

    def read_email_info(self):
        email_info = EmailInfo.objects.using('postgres').all()
        json_data = serializers.serialize("json", email_info)
        return json_data

    def save_email_raw_data(self, raw_data):
        self.cursor.callproc('save_email_raw_data', [raw_data, ])
        new_id = self.cursor.fetchone()[0]
        return new_id

    def save_email(self, raw_id, sender, recipient, subject, message):
        self.cursor.callproc('save_email_data', [
            raw_id,
            sender,
            recipient,
            subject,
            message,
        ])
        new_id = self.cursor.fetchone()[0]
        return new_id

    def change_status(self, result_id, condition):
        self.cursor.callproc('change_status_code', [result_id, condition, ])
        new_id = self.cursor.fetchone()[0]
        return new_id