from .base import *


ALLOWED_HOSTS = []


DATABASES = {

    #       SQLITE3 DATABASE CONNECTION

    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}