from rest_framework import serializers
from customers.models import Customer
from partners.models import Partner, Product
from .models import Transaction, BarcodeScanLog

class TransactionSerializer(serializers.ModelSerializer):
    barcode = serializers.CharField(write_only=True)
    company_name = serializers.CharField(write_only=True)
    product_name = serializers.CharField(write_only=True)

    class Meta:
        model = Transaction
        fields = [
            'id', 'barcode', 'company_name', 'product_name',
            'amount', 'cashback_earned', 'created_at'
        ]
        read_only_fields = ['amount', 'cashback_earned', 'created_at']

    def validate(self, data):
        barcode = data.get('barcode')
        company_name = data.get('company_name')
        product_name = data.get('product_name')

        try:
            customer = Customer.objects.get(barcode=barcode)
        except Customer.DoesNotExist:
            raise serializers.ValidationError({"barcode": "Invalid barcode. Customer not found."})

        try:
            partner = Partner.objects.get(company_name=company_name)
        except Partner.DoesNotExist:
            raise serializers.ValidationError({"company_name": "Invalid company name. Partner not found."})

        try:
            product = Product.objects.get(name=product_name, partner=partner)
        except Product.DoesNotExist:
            raise serializers.ValidationError({"product_name": "Invalid product name. Product not found for this partner."})

        data['customer'] = customer
        data['partner'] = partner
        data['product'] = product

        return data

    def create(self, validated_data):
        customer = validated_data.pop('customer')
        partner = validated_data.pop('partner')
        product = validated_data.pop('product')

        cashback_earned = product.amount * (product.cashback_rate / 100)

        customer.cashback_balance += cashback_earned
        customer.save()

        transaction = Transaction.objects.create(
            customer=customer,
            partner=partner,
            amount=product.amount,
            cashback_earned=cashback_earned,
            product_name=product.name
        )

        return transaction


class BarcodeScanLogSerializer(serializers.ModelSerializer):
    customer_username = serializers.CharField(source='customer.username', read_only=True)
    partner_company_name = serializers.CharField(source='partner.company_name', read_only=True)

    class Meta:
        model = BarcodeScanLog
        fields = ['id', 'customer_username', 'partner_company_name', 'product_name', 'amount', 'cashback_earned', 'scanned_at']
        read_only_fields = fields
