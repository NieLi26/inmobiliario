# Generated by Django 4.1.1 on 2023-01-31 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0005_customuser_terms"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="terms",
            field=models.BooleanField(
                default=False, verbose_name="Declaro conocer y aceptar"
            ),
        ),
    ]
