from django.db import models
from customers.models import Customer
from partners.models import Partner

class Transaction(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='transactions')
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    cashback_earned = models.DecimalField(max_digits=10, decimal_places=2)
    product_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
                                      
    def __str__(self):
        return f"Transaction {self.id} - {self.customer.username} with {self.partner.company_name}"


class BarcodeScanLog(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='barcode_logs')
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='barcode_logs')
    product_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    cashback_earned = models.DecimalField(max_digits=10, decimal_places=2)
    scanned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.username} scanned by {self.partner.company_name} on {self.scanned_at}"
