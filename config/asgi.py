import os

from django.core.asgi import get_asgi_application
from decouple import config

# TODO(prod): default → config.settings.production + обов'язкові env
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    config('DJANGO_SETTINGS_MODULE', default='config.settings.develop'),
)

application = get_asgi_application()

if os.environ.get('VERCEL'):
    try:
        from src.core.bootstrap_vercel import bootstrap_vercel_demo

        bootstrap_vercel_demo()
    except Exception:
        pass
