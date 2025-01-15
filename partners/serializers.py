from rest_framework import serializers
from .models import Partner, Product

class PartnerRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = Partner
        fields = ['id', 'username', 'email', 'password', 'company_name', 'company_address', 'phone']

    def create(self, validated_data):
        partner = Partner.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            company_name=validated_data['company_name'],
            company_address=validated_data.get('company_address', ''),
            phone=validated_data['phone']
        )
        return partner

class PartnerLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class PartnerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ['id', 'username', 'email', 'company_name', 'company_address', 'phone']
        read_only_fields = ['email']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'amount', 'cashback_rate']

class PartnerWithProductsSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Partner
        fields = ['id', 'username', 'company_name', 'company_address', 'phone', 'products']
