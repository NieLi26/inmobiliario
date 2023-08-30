import os
import django
from django.core.management import call_command

# Configurar la variable de entorno DJANGO_SETTINGS_MODULE
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# Configurar Django
django.setup()

# Llamar a call_command para ejecutar el comando dumpdata
call_command('dbbackup')



