from django.db import models


class EmailInfo(models.Model):
    id = models.IntegerField(blank=True, null=False, primary_key=True)
    sender = models.CharField(max_length=150, blank=True, null=True)
    recipient = models.CharField(max_length=150, blank=True, null=True)
    subject = models.CharField(max_length=150, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    raw_data = models.TextField(blank=True, null=True)
    status_code = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'email_info'

