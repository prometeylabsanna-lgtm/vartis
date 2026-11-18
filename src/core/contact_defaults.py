"""Демо-контакти для здачі/превʼю, доки клієнт не заповнить реальні в адмінці."""

from __future__ import annotations

from typing import Any
from urllib.parse import unquote

DEMO_PHONE = '+380 75 535 99 18'
DEMO_EMAIL = 'info@vartis.in.ua'
DEMO_ADDRESS = '04070, м. Київ, вулиця Ігорівська, буд. 11Б (Бізнес-Центр Ігорівський)'
DEMO_FACEBOOK_URL = 'https://facebook.com/vartisintelligence'
DEMO_TELEGRAM_URL = 'https://t.me/+380733088462'
DEMO_MAP_EMBED_URL = (
    'https://maps.google.com/maps?q=04070,+%D0%9A%D0%B8%D1%97%D0%B2,+%D0%B2%D1%83%D0%BB%D0%B8%D1%86%D1%8F+'
    '%D0%86%D0%B3%D0%BE%D1%80%D1%96%D0%B2%D1%81%D1%8C%D0%BA%D0%B0,+11%D0%91&hl=uk&z=16&output=embed'
)
LEGACY_PHONES = {'', '+380', '[Телефон]', '+380 44 123 45 67', '+380441234567'}
LEGACY_EMAILS = {'', '[Email]', 'info@vartis.ua'}
LEGACY_ADDRESSES = {'', 'Україна', '[Адреса офісу]', 'Київ, вул. Хрещатик, 1'}
LEGACY_MAPS = {
    '',
    (
        'https://maps.google.com/maps?q=%D0%9A%D0%B8%D1%97%D0%B2,+%D0%B2%D1%83%D0%BB.+'
        '%D0%A5%D1%80%D0%B5%D1%89%D0%B0%D1%82%D0%B8%D0%BA,+1&hl=uk&z=16&output=embed'
    ),
}


def apply_official_contacts(site_settings) -> None:
    """Підставляє офіційні контакти замість порожніх і старих демо-значень."""
    if _strip(getattr(site_settings, 'phone', None)) in LEGACY_PHONES:
        site_settings.phone = DEMO_PHONE
    if _strip(getattr(site_settings, 'email', None)) in LEGACY_EMAILS:
        site_settings.email = DEMO_EMAIL
    if _strip(getattr(site_settings, 'address', None)) in LEGACY_ADDRESSES:
        site_settings.address = DEMO_ADDRESS
    if _is_legacy_map(getattr(site_settings, 'map_embed_url', None)):
        site_settings.map_embed_url = DEMO_MAP_EMBED_URL
    if not _strip(getattr(site_settings, 'facebook_url', None)):
        site_settings.facebook_url = DEMO_FACEBOOK_URL
    if not _strip(getattr(site_settings, 'telegram_url', None)):
        site_settings.telegram_url = DEMO_TELEGRAM_URL


def _strip(value: Any) -> str:
    return (value or '').strip() if isinstance(value, str) else ''


def _is_legacy_map(value: Any) -> bool:
    raw = _strip(value)
    if raw in LEGACY_MAPS:
        return True
    decoded = unquote(raw)
    return 'Хрещатик' in decoded or 'Khreshchatyk' in decoded


def _phone_digits(phone: str) -> str:
    return ''.join(ch for ch in phone if ch.isdigit())


def resolve_public_contacts(site_settings=None) -> dict[str, str]:
    """Завжди повертає заповнені контакти для публічних панелей сайту."""
    phone = _strip(getattr(site_settings, 'phone', None)) or DEMO_PHONE
    email = _strip(getattr(site_settings, 'email', None)) or DEMO_EMAIL
    address = _strip(getattr(site_settings, 'address', None)) or DEMO_ADDRESS
    facebook_url = _strip(getattr(site_settings, 'facebook_url', None)) or DEMO_FACEBOOK_URL
    stored_map = getattr(site_settings, 'map_embed_url', None)
    map_embed_url = DEMO_MAP_EMBED_URL if _is_legacy_map(stored_map) else (_strip(stored_map) or DEMO_MAP_EMBED_URL)
    telegram_url = _strip(getattr(site_settings, 'telegram_url', None)) or DEMO_TELEGRAM_URL
    handle = facebook_url.rstrip('/').split('/')[-1] or 'vartisintelligence'
    phone_tel = ''.join(ch for ch in phone if ch.isdigit() or ch == '+')
    digits = _phone_digits(phone_tel)

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
        'telegram_url': telegram_url,
        'whatsapp_url': f'https://wa.me/{digits}' if digits else '',
        'signal_url': f'https://signal.me/#p/+{digits}' if digits else '',
    }
