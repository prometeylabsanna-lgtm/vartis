import os

from django.core.wsgi import get_wsgi_application
from decouple import config

# TODO(prod): default → config.settings.production + обов'язкові env
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    config('DJANGO_SETTINGS_MODULE', default='config.settings.develop'),
)

application = get_wsgi_application()

# TODO(prod): прибрати — auto-migrate лише для демо на Vercel (SQLite /tmp)
if os.environ.get('VERCEL'):
    try:
        from django.core.management import call_command

        call_command('migrate', interactive=False, run_syncdb=True, verbosity=0)
    except Exception:
        pass
