from django.contrib.auth.models import User
from django.contrib.auth.backends import BaseBackend

class TokenAuthBackend(BaseBackend):
    def authenticate(self, request, token=None):
        if not token:
            return None
        try:
            user = User.objects.get(auth_token__key=token)
            return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None