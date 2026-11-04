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
            "glass_enabled": "0",
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
        _, was_created = PageStyle.objects.get_or_create(
            page=value,
            defaults={"glass_enabled": False},
        )
        if was_created:
            created += 1
    return created


def reset_page_styles_to_layout_defaults() -> int:
    """Повертає стилі до світлого макета (якщо адмін не задав власні кольори)."""
    updated = 0
    for row in PageStyle.objects.all():
        changed = False
        if row.glass_enabled:
            row.glass_enabled = False
            changed = True
        # Порожні кольори вже беруть нові світлі DEFAULT_*;
        # якщо лишились старі темні дефолти як збережені значення — скидаємо.
        if (row.background_color or "").strip().lower() in {"#0b1626", "0b1626"}:
            row.background_color = ""
            changed = True
        if (row.text_color or "").strip().lower() in {"#f6f0e6", "f6f0e6", "#e8edf4", "e8edf4"}:
            row.text_color = ""
            changed = True
        if changed:
            row.save(update_fields=["glass_enabled", "background_color", "text_color"])
            updated += 1
    return updated
