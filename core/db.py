from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


# mysqlclient
MYSQL = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'propieda3_propiedades_web',
        'USER': 'propieda3',
        'PASSWORD': 'Mac@526_1705Gf',
        'HOST': '104.194.10.147',
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    }
}


SQLITE = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
