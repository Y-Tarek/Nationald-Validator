from rest_framework import serializers


class NationalIDSerializer(serializers.Serializer):
    country_code = serializers.CharField()
    national_id = serializers.CharField()