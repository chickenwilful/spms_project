import json
from django.http import HttpResponse


def json_success(request, data):
    return json_response({
        'success': 1,
        'data': data,
    })


def json_fail(request, data):
    return json_response({
        'success': 0,
        'data': data,
    })


def json_response(data):
    return HttpResponse(json.dumps(data), content_type='application/json')
