"""Демо-бутстрап для Vercel (ефемерний SQLite в /tmp). Не для прод з постійною БД."""

from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

DEMO_USERNAME = 'admin'
DEMO_PASSWORD = 'admin'
DEMO_EMAIL = 'admin@vartis.local'


def ensure_demo_superuser() -> None:
    if not os.environ.get('VERCEL'):
        return
    from django.contrib.auth import get_user_model

    user_model = get_user_model()
    user, created = user_model.objects.get_or_create(
        username=DEMO_USERNAME,
        defaults={
            'email': DEMO_EMAIL,
            'is_staff': True,
            'is_superuser': True,
            'is_active': True,
        },
    )
    changed = created
    if not user.is_staff or not user.is_superuser or not user.is_active:
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        changed = True
    # Завжди синхронізуємо демо-пароль: /tmp БД нова на cold start
    user.set_password(DEMO_PASSWORD)
    if not user.email:
        user.email = DEMO_EMAIL
    user.save()
    logger.info('vercel demo superuser %s (%s)', DEMO_USERNAME, 'created' if created else 'updated')
    if changed:
        pass


def bootstrap_vercel_demo() -> None:
    if not os.environ.get('VERCEL'):
        return
    from django.core.management import call_command

    try:
        call_command('migrate', interactive=False, run_syncdb=True, verbosity=0)
    except Exception:
        logger.exception('vercel migrate failed')

    try:
        ensure_demo_superuser()
    except Exception:
        logger.exception('vercel demo superuser failed')

    try:
        from src.pages.models import HomePage

        if not HomePage.objects.exists():
            call_command('seed_content', verbosity=0)
    except Exception:
        logger.exception('vercel seed_content failed')

    try:
        call_command('seed_site_blocks', verbosity=0)
    except Exception:
        logger.exception('vercel seed_site_blocks failed')
