# Generated by Django 5.1.4 on 2025-01-03 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("partners", "0004_alter_partner_username"),
    ]

    operations = [
        migrations.AlterField(
            model_name="partner",
            name="company_name",
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
