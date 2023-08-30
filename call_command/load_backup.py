import os
import django
from django.core import management

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

django.setup()

FILE_NAME = 'backup_test.json'


def main():

    management.call_command('migrate')
    management.call_command('loaddata', FILE_NAME)


if __name__ == "__main__":
    main()