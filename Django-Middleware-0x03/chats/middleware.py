import logging
from datetime import datetime, time
from django.http import HttpRequest, HttpResponseForbidden

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('request.log')
formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        timestamp = datetime.now()

        user = request.user if  request.user.is_authenticated else 'Anonymous'
        log_message = f"{timestamp} - User: {user} - Path: {request.path}"
        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().time()

        restricted_start = time(21, 0)
        restricted_end = time(6, 0)

        if (
            now >= restricted_start or
            now <= restricted_end
        ):
            return HttpResponseForbidden("Access to the messaging app is restricted between 9PM and 6AM.")
        return self.get_response(request)
