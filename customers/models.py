from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class Customer(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customer_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customer_user_permissions',
        blank=True
    )

    phone = models.CharField(max_length=15, unique=True)
    address = models.TextField(null=True, blank=True)
    cashback_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    barcode = models.CharField(max_length=100, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.barcode:
            self.barcode = f"CUST-{uuid.uuid4().hex[:12].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
