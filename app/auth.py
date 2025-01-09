from django.http import JsonResponse
from .models import Service
from .utility import verify_request_signature
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

class SignatureAuthentication(BaseAuthentication):
    """
    Custom authentication class to authenticate API requests
    using a public key and signature.
    """
    
    def authenticate(self, request):
        public_key = request.headers.get("X-PUBLIC-KEY")
        signature = request.headers.get("X-SIGNATURE")

        if not public_key or not signature:
            return None
      
        try:
            api_key = Service.objects.get(public_key=public_key, is_active=True)
            
            if not verify_request_signature(signature, api_key.public_key):
                raise AuthenticationFailed({"error": "Invalid signature"})
            
            return (api_key, None) 
        except Service.DoesNotExist:
            raise AuthenticationFailed({"error": "Invalid API key"})