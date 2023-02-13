# Generated by Django 4.1.1 on 2023-02-11 01:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0004_shop_builded_year"),
    ]

    operations = [
        migrations.AddField(
            model_name="cellar",
            name="num_enclosure",
            field=models.CharField(
                choices=[
                    ("", "Selecione una opción"),
                    ("0", "0"),
                    ("1", "1"),
                    ("2", "2"),
                    ("3", "3"),
                    ("4", "4"),
                    ("5", "5"),
                    ("6", "6"),
                    ("7", "7"),
                    ("8", "8"),
                    ("9", "9"),
                    ("10", "10"),
                    ("11", "11"),
                    ("12", "12"),
                    ("13", "13"),
                    ("14", "14"),
                    ("15", "15"),
                ],
                default=datetime.datetime(
                    2023, 2, 11, 1, 29, 8, 550892, tzinfo=datetime.timezone.utc
                ),
                max_length=2,
                verbose_name="Recintos",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="industrial",
            name="num_cellars",
            field=models.CharField(
                choices=[
                    ("", "Selecione una opción"),
                    ("0", "0"),
                    ("1", "1"),
                    ("2", "2"),
                    ("3", "3"),
                    ("4", "4"),
                    ("5", "5"),
                    ("6", "6"),
                    ("7", "7"),
                    ("8", "8"),
                    ("9", "9"),
                    ("10", "10"),
                    ("11", "11"),
                    ("12", "12"),
                    ("13", "13"),
                    ("14", "14"),
                    ("15", "15"),
                ],
                default=datetime.datetime(
                    2023, 2, 11, 1, 29, 12, 223214, tzinfo=datetime.timezone.utc
                ),
                max_length=2,
                verbose_name="Bodegas",
            ),
            preserve_default=False,
        ),
    ]
