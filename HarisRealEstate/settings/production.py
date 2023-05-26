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

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = F'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
AWS_DEFAULT_ACL = 'public-read'
# AWS_REGION_NAME = config('AWS_REGION_NAME')
# AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME')

AWS_LOCATION = 'static'

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'