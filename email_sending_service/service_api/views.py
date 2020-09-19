from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .repository import ServiceRepository
from django.db import connections
import json
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
    raw_id = service_repository.save_email_raw_data(content)
    result = {"raw_id": raw_id}
    return JsonResponse(result)


def get_content(request):
    body = request.body.decode("utf-8")
    return body