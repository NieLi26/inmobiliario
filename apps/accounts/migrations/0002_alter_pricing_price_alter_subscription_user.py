# Generated by Django 4.1.1 on 2023-01-17 17:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pricing",
            name="price",
            field=models.PositiveIntegerField(default=0, verbose_name="Precio"),
        ),
        migrations.AlterField(
            model_name="subscription",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
