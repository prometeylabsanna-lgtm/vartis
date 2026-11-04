"""Демо-контакти для здачі/превʼю, доки клієнт не заповнить реальні в адмінці."""

from __future__ import annotations

from typing import Any

DEMO_PHONE = '+380 44 123 45 67'
DEMO_EMAIL = 'info@vartis.ua'
DEMO_ADDRESS = 'Київ, вул. Хрещатик, 1'
DEMO_FACEBOOK_URL = 'https://facebook.com/vartisintelligence'
DEMO_MAP_EMBED_URL = (
    'https://maps.google.com/maps?q=%D0%9A%D0%B8%D1%97%D0%B2,+%D0%B2%D1%83%D0%BB.+'
    '%D0%A5%D1%80%D0%B5%D1%89%D0%B0%D1%82%D0%B8%D0%BA,+1&hl=uk&z=16&output=embed'
)


def _strip(value: Any) -> str:
    return (value or '').strip() if isinstance(value, str) else ''


def resolve_public_contacts(site_settings=None) -> dict[str, str]:
    """Завжди повертає заповнені контакти для публічних панелей сайту."""
    phone = _strip(getattr(site_settings, 'phone', None)) or DEMO_PHONE
    email = _strip(getattr(site_settings, 'email', None)) or DEMO_EMAIL
    address = _strip(getattr(site_settings, 'address', None)) or DEMO_ADDRESS
    facebook_url = _strip(getattr(site_settings, 'facebook_url', None)) or DEMO_FACEBOOK_URL
    map_embed_url = _strip(getattr(site_settings, 'map_embed_url', None)) or DEMO_MAP_EMBED_URL
    handle = facebook_url.rstrip('/').split('/')[-1] or 'vartisintelligence'
    phone_tel = ''.join(ch for ch in phone if ch.isdigit() or ch == '+')

    return {
        'phone': phone,
        'email': email,
        'address': address,
        'facebook_url': facebook_url,
        'facebook_handle': handle,
        'facebook_hint': f'facebook.com/{handle}',
        'map_embed_url': map_embed_url,
        'phone_href': f'tel:{phone_tel}' if phone_tel else '',
        'email_href': f'mailto:{email}' if email else '',
    }
