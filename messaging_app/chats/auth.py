from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomJWTAuthentication(JWTAuthentication):
    """Custom JWT authentication class for chats app"""

    def authenticate(self, request):
        return super().authenticate(request)
