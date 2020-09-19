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
