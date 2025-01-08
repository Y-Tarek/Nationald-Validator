from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from shared.parser import NationalIDParserFactory
from .models import Service, CountryCode
from .utility import generate_key_pair 
from rest_framework.permissions import IsAuthenticated
from .serializer import CountryCodeSerializer, NationalIDSerializer
from rest_framework import status


class RegisterServiceAPI(APIView):
    """API for creating Srvice Key Pair for a tenant."""
    
    def post(self, request):
        service_name = request.data.get('service_name')
        expires_at = request.data.get('expires_at', None)

        if not service_name:
            return Response({"error": "Service name is required."}, status=status.HTTP_400_BAD_REQUEST)

        public_key, private_key = generate_key_pair()

        api_key = Service.objects.create(
            public_key=public_key,
            private_key=private_key,
            service_name=service_name,
            expires_at=expires_at,
        )

        return Response({
            "service_name": api_key.service_name,
            "public_key": public_key,
            "private_key": private_key,
        }, status=status.HTTP_201_CREATED)

class CountryCodeAPI(ListAPIView):
    """ API list all active country codes to extract validate nationality before national id. """
    serializer_class = CountryCodeSerializer
    queryset = CountryCode.objects.all()


class NationalIDAPI(APIView):
    """ API To Validate and extract info from national id """
    permission_classes = [IsAuthenticated]
    serializer_class = NationalIDSerializer

    def post(self, request):
        country_code = request.data.get("country_code")
        national_id = request.data.get("national_id")

        try:
            parser = NationalIDParserFactory.get_parser(country_code)
            parsed_data = parser.parse(national_id)
            return Response(parsed_data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)