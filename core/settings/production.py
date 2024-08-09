from decouple import config
# import dj_database_url

from .base import *
from . import pymysql_init


## ALLOWED HOSTS
ALLOWED_HOSTS = ['www.harisrealestate.com', 'harisrealestate.com', '67.223.119.66']

## CSRF TOKEN CLEARANCE
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_DOMAIN = '.harisrealestate.com'
CSRF_TRUSTED_ORIGINS = ['https://harisrealestate.com', 'https://www.harisrealestate.com']

## Secure-Only Session Cookie
SESSION_COOKIE_SECURE = True

## HTTPS
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_SSL_REDIRECT = True


DATABASE_URL = os.getenv("DATABASE_URL")

DATABASES = {
	'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
    #       MYSQL CONNECTION

    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': config("DB_NAME"),
    #     'USER': config("DB_USER"),
    #     'PASSWORD': config("DB_PASSWORD"),
    #     'HOST': config("DB_HOST"),
    #     'PORT': config("DB_PORT"),
    # }
	
    #       POSTGRESQL CONNECTION ONE WAY

    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': config("DB_NAME"),
    #     'USER': config("DB_USER"),
    #     'PASSWORD': config("DB_PASSWORD"),
    #     'HOST': config("DB_HOST"),
    #     'PORT': config("DB_PORT"),
    # }

    #       POSTGRESQL CONNECTION ANOTHER WAY

    # 'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=1800),
}


# Media
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Static Configuration
STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'staticfiles')
]