import os

from django.core.wsgi import get_wsgi_application
from decouple import config

# TODO(prod): default → config.settings.production + обов'язкові env
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    config('DJANGO_SETTINGS_MODULE', default='config.settings.develop'),
)

application = get_wsgi_application()

# TODO(prod): прибрати — auto-migrate + seed + demo admin лише для Vercel (SQLite /tmp)
if os.environ.get('VERCEL'):
    try:
        from src.core.bootstrap_vercel import bootstrap_vercel_demo

        bootstrap_vercel_demo()
    except Exception:
        pass
