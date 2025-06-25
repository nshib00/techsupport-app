from os import getenv
from .base import *


DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1"]

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": getenv("DB_NAME"),
        "USER": getenv("DB_USER"),
        "PASSWORD": getenv("DB_PWD"),
        "HOST": getenv("DB_HOST", "127.0.0.1"),
        "PORT": getenv("DB_PORT", "5432"),
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CELERY_BROKER_URL = 'redis://localhost:6379/0'


