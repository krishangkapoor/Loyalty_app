from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Transaction
from transactions.serializers import TransactionSerializer
from customers.models import Customer
from partners.models import Partner

class ScanBarcodeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        customer_id = request.data.get('customer_id')
        partner_id = request.data.get('partner_id')
        amount = request.data.get('amount')
        cashback_rate = request.data.get('cashback_rate')

        # Validate the inputs
        customer = Customer.objects.get(id=customer_id)
        partner = Partner.objects.get(id=partner_id)
        cashback_earned = float(amount) * float(cashback_rate)

        # Create the transaction
        transaction = Transaction.objects.create(
            customer=customer,
            partner=partner,
            amount=amount,
            cashback_earned=cashback_earned
        )

        # Update customer's cashback balance
        customer.cashback_balance += cashback_earned
        customer.save()

        return Response({
            "transaction_id": transaction.id,
            "cashback_earned": cashback_earned,
            "new_balance": customer.cashback_balance
        })
