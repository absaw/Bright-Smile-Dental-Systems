from django.contrib.auth import authenticate
from django.utils.deprecation import MiddlewareMixin

class TokenAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header:
            token = auth_header.split(' ')[-1]
            user = authenticate(request, token=token)
            if user:
                request.user = user