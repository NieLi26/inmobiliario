import os
import json
import django
from django.core import management

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

django.setup()

FILE_NAME = 'backup_test.json'
FORMAT = 'json'
INDENT = 2


def main():
    with open(FILE_NAME, 'w', encoding='utf-8') as f:
        management.call_command('dumpdata', format=FORMAT, indent=INDENT, stdout=f)


    # with open(FILE_NAME, 'r') as f:
    #     data = json.load(f)
    #     print(data)


if __name__ == "__main__":
    main()