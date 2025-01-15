from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = Customer
        fields = ['id', 'username', 'email', 'password', 'phone', 'barcode']
        extra_kwargs = {
            'password': {'write_only': True},
            'barcode': {'read_only': True}
        }

    def create(self, validated_data):
        customer = Customer.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone=validated_data['phone']
        )
        return customer

class CustomerLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'username', 'email', 'phone', 'barcode']
        read_only_fields = ['email', 'barcode']
