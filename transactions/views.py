from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from customers.models import Customer
from partners.models import Partner, Product
from .models import Transaction, BarcodeScanLog
from .serializers import TransactionSerializer, BarcodeScanLogSerializer


class ScanBarcodeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            transaction = serializer.save()
            BarcodeScanLog.objects.create(
                customer=transaction.customer,
                partner=transaction.partner,
                product_name=transaction.product_name,
                amount=transaction.amount,
                cashback_earned=transaction.cashback_earned
            )
            return Response({
                "message": "Transaction successful",
                "transaction_id": transaction.id,
                "cashback_earned": transaction.cashback_earned,
                "new_balance": transaction.customer.cashback_balance
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BarcodeScanHistoryView(ListAPIView):
    serializer_class = BarcodeScanLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if isinstance(user, Customer):
            return BarcodeScanLog.objects.filter(customer=user)
        
        if isinstance(user, Partner):
            return BarcodeScanLog.objects.filter(partner=user)
        
        return BarcodeScanLog.objects.none()