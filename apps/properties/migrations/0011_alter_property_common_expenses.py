# Generated by Django 4.1.1 on 2023-08-25 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0010_alter_property_common_expenses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='common_expenses',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Gastos comunes'),
        ),
    ]
