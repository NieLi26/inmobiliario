# Generated by Django 4.1.1 on 2023-02-11 01:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0005_cellar_num_enclosure_industrial_num_cellars"),
    ]

    operations = [
        migrations.RenameField(
            model_name="cellar", old_name="num_enclosure", new_name="num_enclosures",
        ),
    ]
