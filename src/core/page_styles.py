"""Допоміжні функції стилів сторінок."""

from __future__ import annotations

from src.core.models import PageStyle, SiteBlock


def resolve_page_style(page: str) -> dict[str, str]:
    """CSS-змінні для сторінки (порожні рядки = дефолт у шаблоні)."""
    try:
        row = PageStyle.objects.get(page=page)
    except PageStyle.DoesNotExist:
        row = None
    if row is None:
        return {
            "--page-bg": PageStyle.DEFAULT_BACKGROUND,
            "--page-text": PageStyle.DEFAULT_TEXT,
            "--page-accent": PageStyle.DEFAULT_ACCENT,
            "glass_enabled": "1",
            "background_image_url": "",
        }
    bg_url = ""
    if row.background_image:
        try:
            bg_url = row.background_image.url
        except Exception:
            bg_url = ""
    return {
        "--page-bg": row.effective_background,
        "--page-text": row.effective_text,
        "--page-accent": row.effective_accent,
        "glass_enabled": "1" if row.glass_enabled else "0",
        "background_image_url": bg_url,
    }


def ensure_all_page_styles() -> int:
    created = 0
    for value, _label in SiteBlock.Page.choices:
        _, was_created = PageStyle.objects.get_or_create(page=value, defaults={"glass_enabled": True})
        if was_created:
            created += 1
    return created
