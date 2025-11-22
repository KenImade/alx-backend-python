import logging
import time
from collections import defaultdict
from datetime import datetime
from django.http import HttpResponseForbidden, JsonResponse

logging.basicConfig(filename="requests.log", level=logging.INFO, format="%(message)s")


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().time()

        start_time = datetime.strptime("06:00", "%H:%M").time()
        end_time = datetime.strptime("21:00", "%H:%M").time()

        if not (start_time <= now <= end_time):
            return HttpResponseForbidden(
                "Access to messaging is restricted between 9 PM and 6 AM."
            )

        response = self.get_response(request)
        return response


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user.username if request.user.is_authenticated else "Anonymous"

        logging.info(f"{datetime.now()} - User: {user} - Path: {request.path}")

        response = self.get_response(request)
        return response


class RateLimitMessagesMiddleware:
    """
    Limits the number of messages a user can send per minute based on their IP address.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # Dictionary to track messages per IP: {ip: [(timestamp1), (timestamp2), ...]}
        self.ip_message_log = defaultdict(list)
        self.MAX_MESSAGES = 5
        self.TIME_WINDOW = 60  # seconds

    def __call__(self, request):
        # Only apply rate limit to POST requests to messaging endpoints
        if request.method == "POST" and "/api/messages/" in request.path:
            ip = self.get_client_ip(request)
            now = time.time()

            # Remove timestamps older than TIME_WINDOW
            self.ip_message_log[ip] = [
                timestamp
                for timestamp in self.ip_message_log[ip]
                if now - timestamp < self.TIME_WINDOW
            ]

            if len(self.ip_message_log[ip]) >= self.MAX_MESSAGES:
                return JsonResponse(
                    {
                        "error": "Message rate limit exceeded. Max 5 messages per minute."
                    },
                    status=429,
                )

            # Log the new message timestamp
            self.ip_message_log[ip].append(now)

        response = self.get_response(request)
        return response

    @staticmethod
    def get_client_ip(request):
        """Get client IP address from request headers."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
