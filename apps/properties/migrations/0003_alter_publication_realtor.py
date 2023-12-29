# Generated by Django 4.1.1 on 2023-12-29 00:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('properties', '0002_alter_publication_realtor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='realtor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='publications_realtor', to=settings.AUTH_USER_MODEL, verbose_name='Agente'),
        ),
    ]