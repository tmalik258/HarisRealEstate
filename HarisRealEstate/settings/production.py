from decouple import config
import dj_database_url

from .base import *


## ALLOWED HOSTS
ALLOWED_HOSTS = ['13.231.223.105', '127.0.0.1', '.harisrealestate.com']

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


# AWS S3 Storage

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = config('AWS_S3_CUSTOM_DOMAIN')
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'
AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME')
AWS_S3_SIGNATURE_NAME = config('AWS_S3_SIGNATURE_NAME')
AWS_S3_FILE_OVERWRITE = True

STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'