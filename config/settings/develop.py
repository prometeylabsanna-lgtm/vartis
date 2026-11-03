import os

from decouple import config

from .base import *  # noqa: F401,F403

DEBUG = True

# TODO(prod): прибрати insecure default
SECRET_KEY = config('SECRET_KEY', default='dev-only-insecure-key-do-not-use-in-prod')

ALLOWED_HOSTS = ['*']

# Форми / CSRF на https://*.vercel.app (URL ще невідомий)
CSRF_TRUSTED_ORIGINS = [
    'https://*.vercel.app',
    'http://127.0.0.1:8000',
    'http://localhost:8000',
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Vercel: файлова система read-only → SQLite у /tmp (ефемерно, ок для демо)
if os.environ.get('VERCEL'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': '/tmp/vartis-demo.sqlite3',
        }
    }

STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
    },
}

CONTENT_SECURITY_POLICY = {
    'DIRECTIVES': {
        'default-src': ["'self'"],
        'script-src': ["'self'", "'unsafe-inline'", 'https://www.googletagmanager.com'],
        'style-src': ["'self'", "'unsafe-inline'", 'https://fonts.googleapis.com'],
        'font-src': ["'self'", 'https://fonts.gstatic.com', 'data:'],
        'img-src': ["'self'", 'data:', 'https:'],
        'frame-src': ["'self'", 'https://www.google.com', 'https://maps.google.com'],
        'connect-src': ["'self'"],
    }
}
