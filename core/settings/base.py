import os
from pathlib import Path
from django.urls import reverse_lazy
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load .env file for variables and key
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", False)
DEBUG_PROPAGATE_EXCEPTIONS = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # External PACKAGES
    'phonenumber_field',
    'django_cleanup.apps.CleanupConfig',
    'mptt',
    'django_mptt_admin',
    # Internal APPS
    'account',
    'listing',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
	"whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'listing.context_processors.searchForm',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

DATETIME_FORMAT="%Y-%m-%d%H:%M:%S"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/



# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Account App Configuration
LOGIN_REDIRECT_URL = reverse_lazy('listing:index')
AUTH_USER_MODEL = 'account.User'
AUTH_PROFILE_MODULE = 'account.Profile'
LOGIN_URL = '/account/login'

PASSWORD_RESET_TIMEOUT_DAYS = 2



# Email Backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# SMTP Configuration for Gmail
EMAIL_HOST: str = 'django.core.mail.backends.smtp.EmailBackend'  # or the SMTP server provided by your email service
EMAIL_PORT: int = 587  # or the appropriate port for your email service
EMAIL_HOST: str = os.getenv('EMAIL_HOST')
EMAIL_HOST_USER: str = os.getenv('EMAIL_HOST_USER')  # your Gmail or email service username
EMAIL_HOST_PASSWORD: str = os.getenv('EMAIL_HOST_PASSWORD')  # your Gmail or email service password
EMAIL_USE_TLS: bool = True  # or False if your email service does not support TLS/SSL
