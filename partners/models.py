from django.contrib.auth.models import AbstractUser
from django.db import models

class Partner(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='partner_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='partner_user_permissions',
        blank=True
    )

    company_name = models.CharField(max_length=255, unique=True)
    company_address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.company_name

class Product(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    cashback_rate = models.DecimalField(max_digits=4, decimal_places=2, help_text="Enter cashback rate as a percentage (e.g., 5.0 for 5%)")

    def __str__(self):
        return f"{self.name} - {self.partner.company_name}"
