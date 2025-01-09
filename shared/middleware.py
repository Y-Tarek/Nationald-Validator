from rest_framework.exceptions import AuthenticationFailed
from app.models import Service
from django.http import JsonResponse

class ServiceAuthenticationMiddleware:
    """Middleware for Service Authentication using public keys."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/'):
            return self.get_response(request)

        public_key = request.headers.get('X-PUBLIC-KEY')

        if not public_key:
            return JsonResponse({'detail': 'Public key is required.'}, status=400)

        try:
            service = Service.objects.get(public_key=public_key)

            if not service.is_authenticated:
                return JsonResponse({'detail': 'Service is not authenticated or has expired.'}, status=401)

            request.service = service
        except Service.DoesNotExist:
            return JsonResponse({'detail': 'Invalid API Key.'}, status=401)

        return self.get_response(request)