"""Кольори баннера окремо від Оформлення сторінки."""

from __future__ import annotations

import re

_HEX = re.compile(r'^#?[0-9a-fA-F]{3}([0-9a-fA-F]{3})?$')

DEFAULT_HERO_TEXT = '#ffffff'
DEFAULT_HERO_PANEL = '#ffffff'
DEFAULT_HERO_OPACITY = 10


def normalize_hex(value: str, fallback: str = DEFAULT_HERO_TEXT) -> str:
    raw = (value or '').strip()
    if not raw:
        return fallback
    if not raw.startswith('#'):
        raw = f'#{raw}'
    if not _HEX.match(raw):
        return fallback
    if len(raw) == 4:
        raw = '#' + ''.join(ch * 2 for ch in raw[1:])
    return raw.lower()


def clamp_opacity(value) -> int:
    try:
        return max(0, min(100, int(value)))
    except (TypeError, ValueError):
        return DEFAULT_HERO_OPACITY


def hex_to_rgba(value: str, opacity_pct: int, fallback: str = DEFAULT_HERO_PANEL) -> str:
    color = normalize_hex(value, fallback)
    red = int(color[1:3], 16)
    green = int(color[3:5], 16)
    blue = int(color[5:7], 16)
    alpha = clamp_opacity(opacity_pct) / 100
    if alpha == 1:
        return f'rgba({red}, {green}, {blue}, 1)'
    alpha_s = f'{alpha:.2f}'.rstrip('0').rstrip('.')
    return f'rgba({red}, {green}, {blue}, {alpha_s})'
