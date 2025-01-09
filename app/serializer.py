from rest_framework import serializers


class NationalIDSerializer(serializers.Serializer):
    country_code = serializers.CharField()
    national_id = serializers.CharField()

class ServiceSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    service_name = serializers.CharField()
    is_active = serializers.BooleanField()

class ServiceTransactionSerializer(serializers.Serializer):
    transaction_id = serializers.CharField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2,)
    status = serializers.CharField()
    service = ServiceSerializer()