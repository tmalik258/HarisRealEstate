from decouple import config
# import dj_database_url

from .base import *


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


# STATIC_URL = '/static/'

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_SIGNATURE_NAME = 's3v4',
AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME')
AWS_S3_CUSTOM_DOMAIN = F'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
AWS_DEFAULT_ACL =  None
AWS_S3_VERITY = True

AWS_LOCATION = 'static'

# Media
DEFAULT_FILE_STORAGE = 'core.storages.MediaStore'

# Static Configuration S3
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'