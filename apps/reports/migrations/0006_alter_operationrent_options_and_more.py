# Generated by Django 4.1.1 on 2023-09-13 21:20

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0005_alter_operationbuyhistory_signature_sales_document'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='operationrent',
            options={'base_manager_name': 'objects', 'verbose_name': 'OperationRent', 'verbose_name_plural': 'OperationRents'},
        ),
        migrations.AlterModelManagers(
            name='operationrent',
            managers=[
                ('active_objects', django.db.models.manager.Manager()),
                ('objects', django.db.models.manager.Manager()),
            ],
        ),
    ]
