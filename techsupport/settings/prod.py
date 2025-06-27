from os import getenv
from .base import *


DEBUG = False

ALLOWED_HOSTS = getenv("ALLOWED_HOSTS", "").split(",")

CORS_ALLOWED_ORIGINS = getenv("CORS_ALLOWED_ORIGINS", "").split(",")


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': getenv('POSTGRES_DB'),
        'USER': getenv('POSTGRES_USER'),
        'PASSWORD': getenv('POSTGRES_PASSWORD'),
        'HOST': getenv('POSTGRES_HOST'),
        'PORT': getenv('POSTGRES_PORT'),
    }
}

CORS_ALLOWED_ORIGINS = getenv('CORS_ALLOWED_ORIGINS', '').split(',')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = getenv('EMAIL_HOST')
EMAIL_PORT = int(getenv('EMAIL_PORT', 587))
EMAIL_HOST_USER = getenv('EMAIL_USER')
EMAIL_HOST_PASSWORD = getenv('EMAIL_PWD')
EMAIL_USE_TLS = True

CELERY_BROKER_URL = getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')