from django.db import models

class Partner(models.Model):
    business_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=255)  # Store hashed passwords in production

    def __str__(self):
        return self.business_name
