from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from shared.parser import NationalIDParserFactory
from rest_framework.permissions import IsAuthenticated
from .serializer import NationalIDSerializer
from rest_framework import status
from django_ratelimit.decorators import is_ratelimited


class NationalIDAPI(APIView):
    """ API To Validate and extract info from national id """
    permission_classes = [IsAuthenticated]
    serializer_class = NationalIDSerializer

    def post(self, request):
        was_limited = is_ratelimited(
            request,
            key='ip',
            rate='5/5m',
            method='POST',
            increment=True,
            group='national id info'
        )

        if was_limited:
            return Response(
                {"detail": "Too many attempts. Please try again later after 5 minutes."},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        country_code = request.data.get("country_code")
        national_id = request.data.get("national_id")

        try:
            parser = NationalIDParserFactory.get_parser(country_code)
            parsed_data = parser.parse(national_id)
            return Response(parsed_data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)