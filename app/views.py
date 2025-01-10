from app.constants import FAILED, SUCCESSFUL
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from shared.parser import NationalIDParserFactory
from rest_framework.permissions import IsAuthenticated
from .serializer import NationalIDSerializer, ServiceTransactionSerializer
from rest_framework import status
from django_ratelimit.decorators import is_ratelimited
from .models import Transaction
import uuid

class NationalIDAPI(APIView):
    """ API To Validate and extract info from national id """
    permission_classes = [IsAuthenticated]
    serializer_class = NationalIDSerializer

    def post(self, request):
        if self.is_rate_limited(request):
            return self.handle_rate_limit_failure(request)

        response_data, status_code, status_value = self.process_national_id(request)

        self.log_transaction(request, status_value)

        return Response(response_data, status=status_code)

    @staticmethod
    def is_rate_limited(request):
        """Check if the request exceeds the rate limit."""
        return is_ratelimited(
            request,
            key='ip',
            rate='5/5m',
            method='POST',
            increment=True,
            group='national id info'
        )

    def handle_rate_limit_failure(self, request):
        """Handle the case where the rate limit is exceeded."""
        response_data = {"detail": "Too many attempts. Please try again later after 5 minutes."}
        self.log_transaction(request, FAILED)
        return Response(response_data, status=status.HTTP_429_TOO_MANY_REQUESTS)

    def process_national_id(self, request):
        """Process the national ID and return response data, status code, and status."""
        country_code = request.data.get("country_code")
        national_id = request.data.get("national_id")

        try:
            parser = NationalIDParserFactory.get_parser(country_code)
            parsed_data = parser.parse(national_id)
            return parsed_data, status.HTTP_200_OK, SUCCESSFUL
        except ValueError as e:
            return {"error": str(e)}, status.HTTP_400_BAD_REQUEST, FAILED

    def log_transaction(self, request, status_value):
        """Log the transaction in the database."""
        Transaction.objects.create(
            service=getattr(request, 'service', None),
            transaction_id=str(uuid.uuid4()),
            amount=50.0,
            status=status_value,
        )
    
class ServiceTransactionAPI(ListAPIView):
    """ API to List Service Transactions """
    permission_classes = [IsAuthenticated]
    serializer_class = ServiceTransactionSerializer
    queryset = Transaction.objects.all()

    def get_queryset(self):
        return self.queryset.filter(
            service = self.request.service
        ).select_related('service').order_by('-id')