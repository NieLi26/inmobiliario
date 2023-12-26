# Generated by Django 4.1.1 on 2023-12-26 03:55

import apps.reports.utils
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('properties', '0001_initial'),
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OperationRent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.BooleanField(default=True, verbose_name='Estado')),
                ('created', models.DateField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('modified', models.DateField(auto_now=True, verbose_name='Fecha de Modificaión')),
                ('deleted', models.DateField(blank=True, null=True, verbose_name='Fecha de Eliminacion')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('guarantee_value', models.PositiveIntegerField(default=0, verbose_name='Valor de Garantia')),
                ('guarantee_document', models.FileField(blank=True, null=True, upload_to=apps.reports.utils.operation_rent_guarantee_document_files_directory_path, validators=[django.core.validators.FileExtensionValidator(['pdf'])], verbose_name='Documento de Garantia')),
                ('lease_agreement', models.FileField(blank=True, null=True, upload_to=apps.reports.utils.operation_rent_lease_files_directory_path, validators=[django.core.validators.FileExtensionValidator(['pdf'])], verbose_name='Contrato de Arriendo')),
                ('signature_lease_agreement', models.DateField(blank=True, null=True, verbose_name='Fecha Firma Contrato de Arriendo')),
                ('lease_start_date', models.DateField(blank=True, null=True, verbose_name='Fecha Inicio Contrato Arriendo')),
                ('lease_final_date', models.DateField(blank=True, null=True, verbose_name='Fecha Termino Contrato Arriendo')),
                ('monthly_total', models.PositiveIntegerField(default=0, verbose_name='Total Arriendo Mensual')),
                ('is_lease_commission_paid', models.BooleanField(default=False, verbose_name='Comisión por Contrato Pagada')),
                ('monthly_commission', models.PositiveIntegerField(default=0, verbose_name='Total Comision')),
                ('is_completed', models.BooleanField(default=False)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='operations_rent', to='crm.client')),
                ('publication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='operations_rent', to='properties.publication')),
            ],
            options={
                'verbose_name': 'OperationRent',
                'verbose_name_plural': 'OperationRents',
                'default_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='PaymentRent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.BooleanField(default=True, verbose_name='Estado')),
                ('created', models.DateField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('modified', models.DateField(auto_now=True, verbose_name='Fecha de Modificaión')),
                ('deleted', models.DateField(blank=True, null=True, verbose_name='Fecha de Eliminacion')),
                ('total_payment', models.PositiveIntegerField(default=0, verbose_name='Total')),
                ('payment_date', models.DateField(verbose_name='Fecha de Pago')),
                ('is_commission_paid', models.BooleanField(default=False, verbose_name='Comisión Pagada')),
                ('is_partial_payment', models.BooleanField(default=False, verbose_name='Pago Parcial')),
                ('operation_rent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments_rent', to='reports.operationrent')),
            ],
            options={
                'verbose_name': 'PaymentRent',
                'verbose_name_plural': 'PaymentRents',
                'ordering': ('-payment_date',),
            },
        ),
        migrations.CreateModel(
            name='OperationBuyHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.BooleanField(default=True, verbose_name='Estado')),
                ('created', models.DateField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('modified', models.DateField(auto_now=True, verbose_name='Fecha de Modificaión')),
                ('deleted', models.DateField(blank=True, null=True, verbose_name='Fecha de Eliminacion')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('purchase_sale_advance', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Anticipo de Compra/Venta')),
                ('purchase_sale_agreement', models.FileField(blank=True, null=True, upload_to=apps.reports.utils.operation_buy_purchase_sale_files_directory_path, validators=[django.core.validators.FileExtensionValidator(['pdf'])], verbose_name='Promesa de Compra/Venta')),
                ('signature_purchase_sale_agreement', models.DateField(blank=True, null=True, verbose_name='Fecha Firma Promesa de Compra/Venta')),
                ('sales_document', models.FileField(blank=True, null=True, upload_to=apps.reports.utils.operation_buy_sales_document_files_directory_path, validators=[django.core.validators.FileExtensionValidator(['pdf'])], verbose_name='Contrato de Compra/Venta')),
                ('signature_sales_document', models.DateField(blank=True, null=True, verbose_name='Fecha Firma Contrato de Pago')),
                ('total', models.PositiveIntegerField(default=0, verbose_name='Total')),
                ('total_commission', models.PositiveIntegerField(default=0, verbose_name='Total Comision')),
                ('is_commission_paid', models.BooleanField(default=False, verbose_name='Comisión Pagada')),
                ('has_promise', models.BooleanField(default=False)),
                ('is_completed', models.BooleanField(default=False)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='operations_buy', to='crm.client')),
                ('publication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='operations_buy', to='properties.publication')),
            ],
            options={
                'verbose_name': 'OperationBuyHistory',
                'verbose_name_plural': 'OperationsBuyHistory',
            },
        ),
    ]
