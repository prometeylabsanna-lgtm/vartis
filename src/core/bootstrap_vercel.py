"""Демо-бутстрап для Vercel (ефемерний SQLite в /tmp). Не для прод з постійною БД."""

from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

DEMO_USERNAME = 'admin'
DEMO_PASSWORD = 'admin'
DEMO_EMAIL = 'admin@vartis.local'
# Фіксований salt → однаковий password hash на кожному cold start,
# інакше Django інвалідує cookie-сесію (_auth_user_hash) і викидає на login.
_DEMO_PASSWORD_SALT = 'vartisdemofixed01'


def _demo_password_hash() -> str:
    from django.contrib.auth.hashers import make_password

    return make_password(DEMO_PASSWORD, salt=_DEMO_PASSWORD_SALT, hasher='pbkdf2_sha256')


def ensure_demo_superuser() -> None:
    if not os.environ.get('VERCEL'):
        return
    from django.contrib.auth import get_user_model

    user_model = get_user_model()
    desired_hash = _demo_password_hash()
    user, created = user_model.objects.get_or_create(
        username=DEMO_USERNAME,
        defaults={
            'email': DEMO_EMAIL,
            'is_staff': True,
            'is_superuser': True,
            'is_active': True,
            'password': desired_hash,
        },
    )
    changed = created
    if not user.is_staff or not user.is_superuser or not user.is_active:
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        changed = True
    if user.password != desired_hash:
        user.password = desired_hash
        changed = True
    if not user.email:
        user.email = DEMO_EMAIL
        changed = True
    if changed:
        user.save()
    logger.info(
        'vercel demo superuser %s (%s)',
        DEMO_USERNAME,
        'created' if created else ('updated' if changed else 'ok'),
    )


def _demo_content_snapshot():
    from src.pages.models import AboutPrinciple, HomePage, ServicePage
    from src.pages.models_about import AboutPage
    from src.pages.models_contacts import PrivacyPage

    about = AboutPage.load()
    return {
        'home_exists': HomePage.objects.exists(),
        'service_count': ServicePage.objects.filter(is_published=True).count(),
        'principle_count': AboutPrinciple.objects.count(),
        'intro_len': len(about.intro_text or ''),
        'privacy_len': len(PrivacyPage.load().body or ''),
    }


def _demo_content_missing(snap=None) -> bool:
    data = snap if snap is not None else _demo_content_snapshot()
    return (
        not data['home_exists']
        or data['service_count'] < 1
        or data['principle_count'] < 1
        or data['privacy_len'] < 1
    )


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
        from src.core.middleware_debug_session import _dbg

        snap = _demo_content_snapshot()
        home_gate = bool(snap['home_exists'])
        needs_seed = _demo_content_missing(snap)
        # #region agent log
        _dbg(
            'A',
            'bootstrap_vercel.py:after-migrate',
            'vercel content snapshot before seed',
            {**snap, 'home_gate_skip': home_gate, 'needs_seed': needs_seed},
        )
        # #endregion
        if needs_seed:
            call_command('seed_content', verbosity=0)
            # #region agent log
            _dbg(
                'A',
                'bootstrap_vercel.py:after-seed',
                'vercel content snapshot after seed',
                {**_demo_content_snapshot(), 'seeded': True, 'phase': 'post-fix'},
            )
            # #endregion
        else:
            # #region agent log
            _dbg(
                'A',
                'bootstrap_vercel.py:skip-seed',
                'vercel seed_content skipped',
                snap,
            )
            # #endregion
    except Exception:
        logger.exception('vercel seed_content failed')

    try:
        call_command('seed_site_blocks', verbosity=0)
    except Exception:
        logger.exception('vercel seed_site_blocks failed')

    try:
        from src.core.page_styles import reset_page_styles_to_layout_defaults

        reset_page_styles_to_layout_defaults()
    except Exception:
        logger.exception('vercel page style reset failed')
