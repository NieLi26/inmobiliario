# Generated by Django 4.1.1 on 2023-01-19 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_alter_pricing_price_alter_subscription_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="phone",
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name="customuser",
            name="rut",
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name="pricing",
            name="price",
            field=models.PositiveIntegerField(verbose_name="Precio"),
        ),
    ]
