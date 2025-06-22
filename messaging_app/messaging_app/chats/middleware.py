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


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_counts = {}
        self.rate_limit = 5
        self.time_window = 60

    def __call__(self, request):
        if request.method == "POST" and request.path == '/api/chats/messages':
            ip_address = self.get_client_ip(request)

            current_time = time()
            if ip_address not in self.message_counts:
                self.message_counts[ip_address] = []
            self.message_counts[ip_address] = [
                t for t in self.message_counts[ip_address] if current_time -t < self.time_window
            ]
            if len(self.message_counts[ip_address]) >= self.rate_limit:
                return HttpResponseForbidden("Message limit exceeded: 5 per minute")
            self.message_counts[ip_address].append(current_time)
        response = self.get_response(request)
        return response
    
    def get_client_ip(self, request):
        """Safely extract client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    

class RolePermissionMiddleware:
    # Initialize middleware with get_response callable
    def __init__(self, get_response):
        # Store get_response to pass request to next middleware or view
        self.get_response = get_response
        # Define restricted paths (e.g., admin actions)
        self.restricted_paths = ['/api/chats/admin/']

    def __call__(self, request: HttpRequest):
        if any(request.path.startswith(path) for path in self.restricted_paths
        ):
            if not request.user.is_authenticated:
                # Return 403 Forbidden if user is not logged in
                return HttpResponseForbidden("Authentication required")
            if not hasattr(request.user, 'role') or request.user.role not in [
            'admin', 'moderator']:
                # Return 403 Forbidden if user is not admin or moderator
                return HttpResponseForbidden("Admin or moderator role required")
        # Alternative: Use Django groups for role checks
        # Pass request to next middleware or view
        response = self.get_response(request)
        # Return the response to continue the cycle
        return response
