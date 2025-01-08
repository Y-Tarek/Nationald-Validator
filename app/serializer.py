from rest_framework import serializers

class CountryCodeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    code = serializers.CharField()

class NationalIDSerializer(serializers.Serializer):
    country_code = serializers.CharField()
    national_id = serializers.CharField()