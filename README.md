# Real state

## Installation

### Migrate and Migrations

Crear la estructura de los `models`

```bash
$ python manage.py makemigrations
```

Migrela a su `BBDD`

```bash
$ python manage.py migrate
```

### Population Data

#### Utilize el siguientes comandos para insertar datos dentro de sus tablas:
 
Regiones de chile con sus respectivas comunas

```bash
$ python manage.py load_data
```

### Create Super User

Crea tu superusuario

```bash
$ python manage.py createsuperuser
```

