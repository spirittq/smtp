import logging
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .repository import ServiceRepository
from .business_layer.email_sender import EmailSender
from django.db import connections
import json
import smtplib
from django.http import JsonResponse
from django.conf import settings

logger = logging.getLogger(__name__)

def email_info(request):
    try:
        service_repository = ServiceRepository(connections['postgres'].cursor(), logger)
        json_data = service_repository.read_email_info()
        return JsonResponse(json.loads(json_data), safe=False)
    except Exception:
        logger.exception('email_info')
        raise


@require_POST
@csrf_exempt
def send_email(request):
    try:
        content = get_content(request)
        service_repository = ServiceRepository(connections['postgres'].cursor(), logger)
        smtpobj = smtplib.SMTP(settings.SMTP_SERVER_HOST, settings.SMTP_SERVER_PORT)

        email_sender = EmailSender(service_repository, smtpobj, content)
        message_id = email_sender.execute()
        return JsonResponse(message_id, safe=False)
    except Exception:
        logger.exception('send_email')
        raise


def get_content(request):
    body = request.body.decode("utf-8")
    return body

