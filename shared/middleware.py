from django.utils.timezone import now
from rest_framework.exceptions import AuthenticationFailed
from app.models import Service

class ServiceAuthenticationMiddleware:
    """ Middleware for Service Authentication using public keys. """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/'):
            return self.get_response(request)
        
        public_key = request.headers.get('X-PUBLIC-KEY')

        if not public_key:
            raise AuthenticationFailed('Public key is required.')

        try:
            service = Service.objects.get(public_key=public_key)

            if not service.is_authenticated:
                raise AuthenticationFailed('Service is not authenticated or has expired.')

            request.service = service
        except Service.DoesNotExist:
            raise AuthenticationFailed('Invalid public key.')

        return self.get_response(request)
