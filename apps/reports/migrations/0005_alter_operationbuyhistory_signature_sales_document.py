# Generated by Django 4.1.1 on 2023-09-13 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0004_alter_paymentrent_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operationbuyhistory',
            name='signature_sales_document',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha Firma Contrato de Pago'),
        ),
    ]