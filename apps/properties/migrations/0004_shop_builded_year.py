# Generated by Django 4.1.1 on 2023-02-11 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0003_cellar_num_bathrooms_industrial_num_bathrooms_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="shop",
            name="builded_year",
            field=models.PositiveIntegerField(
                blank=True, null=True, verbose_name="Año de Construcción"
            ),
        ),
    ]