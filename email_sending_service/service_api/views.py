from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .repository import ServiceRepository
from .business_layer.email_sender import EmailSender
from django.db import connections
import json
import smtplib
from django.http import JsonResponse


def email_info(request):
    service_repository = ServiceRepository(connections['postgres'].cursor())
    json_data = service_repository.read_email_info()
    return JsonResponse(json.loads(json_data), safe=False)


@require_POST
@csrf_exempt
def send_email(request):
    content = get_content(request)
    service_repository = ServiceRepository(connections['postgres'].cursor())
    smtpobj = smtplib.SMTP('localhost', 25)
    email_sender = EmailSender(service_repository, smtpobj)
    email_sender.save_email_raw_data(content)
    email_sender.raw_data_parse(content)
    result_id = email_sender.save_email()
    email_sender.send_email(result_id)
    return JsonResponse(result_id, safe=False)


def get_content(request):
    body = request.body.decode("utf-8")
    return body

