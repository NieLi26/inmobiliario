# Generated by Django 4.1.1 on 2023-01-30 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_customuser_phone_customuser_rut_alter_pricing_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="phone",
            field=models.CharField(max_length=10, null=True, verbose_name="Telefono"),
        ),
    ]
