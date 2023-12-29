# Generated by Django 4.1.1 on 2023-12-28 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agentprofile',
            name='end_contract',
            field=models.DateField(verbose_name='Termino Contrato'),
        ),
        migrations.AlterField(
            model_name='agentprofile',
            name='start_contract',
            field=models.DateField(verbose_name='Inicio Contrato'),
        ),
        migrations.AlterField(
            model_name='agentprofile',
            name='zone',
            field=models.TextField(verbose_name='Zona'),
        ),
    ]