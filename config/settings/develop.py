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

# Vercel: файлова система read-only → SQLite + media у /tmp (ефемерно, ок для демо)
if os.environ.get('VERCEL'):
    from pathlib import Path as _Path

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': '/tmp/vartis-demo.sqlite3',
        }
    }
    MEDIA_ROOT = _Path('/tmp/vartis-media')
    MEDIA_ROOT.mkdir(parents=True, exist_ok=True)

    SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
    },
}

CONTENT_SECURITY_POLICY = {
    # Unfold Alpine (x-show/openModal) ламається без eval → оверлей блокує login.
    'EXCLUDE_URL_PREFIXES': ('/admin/',),
    'DIRECTIVES': {
        'default-src': ["'self'"],
        'script-src': [
            "'self'",
            "'unsafe-inline'",
            'https://www.googletagmanager.com',
            'https://cdn.jsdelivr.net',
        ],
        'style-src': [
            "'self'",
            "'unsafe-inline'",
            'https://fonts.googleapis.com',
            'https://cdn.jsdelivr.net',
        ],
        'font-src': ["'self'", 'https://fonts.gstatic.com', 'data:'],
        'img-src': ["'self'", 'data:', 'https:'],
        'frame-src': ["'self'", 'https://www.google.com', 'https://maps.google.com'],
        'connect-src': ["'self'"],
    },
}
