# Generated by Django 4.1.1 on 2023-09-10 19:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0012_apartment_deleted_cellar_deleted_commune_deleted_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publication',
            name='operation',
        ),
    ]