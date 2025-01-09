from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from shared.parser import NationalIDParserFactory
from rest_framework.permissions import IsAuthenticated
from .serializer import NationalIDSerializer
from rest_framework import status


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