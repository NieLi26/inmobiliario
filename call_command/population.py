import os
import django
from faker import Faker


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
# con esto simulo instalar django para poder usar el ORM
django.setup()

fake = Faker(['es_CL'])


def population():
    for _ in range(15):
        print(fake.name())


if __name__ == "__main__":
    population()

