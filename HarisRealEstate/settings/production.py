import dj_database_url

from .base import *


## ALLOWED HOSTS
ALLOWED_HOSTS = ['127.0.0.1', 'harisrealestate.up.railway.app', 'harisrealestate.com', 'www.harisrealestate.com']


## CSRF TOKEN CLEARANCE
CSRF_COOKIE_DOMAIN = 'www.harisrealestate.com'
CSRF_TRUSTED_ORIGINS = ['https://harisrealestate.up.railway.app', 'https://www.harisrealestate.com', 'https://harisrealestate.com']


## HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True


DATABASE_URL = os.getenv("DATABASE_URL")

DATABASES = {
    #       POSTGRESQL CONNECTION ONE WAY

    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': os.getenv("DB_NAME"),
    #     'USER': os.getenv("DB_USER"),
    #     'PASSWORD': os.getenv("DB_PASSWORD"),
    #     'HOST': os.getenv("DB_HOST"),
    #     'PORT': os.getenv("DB_PORT"),
    # }

    #       POSTGRESQL CONNECTION ANOTHER WAY

    'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=1800),
}
