"""Підказки для CMS-полів (мінімальні заглушки)."""

from __future__ import annotations


def help_for_key(key: str, *, page: str = "") -> str:
    if key.endswith("_image"):
        return "Завантажте зображення або залиште порожнім для стандартного фото сайту."
    if key.endswith("_section_visible"):
        return "Якщо вимкнено — секція не показується на сайті."
    if key in {"seo_title", "seo_description"}:
        return "Мета-теги для пошукових систем."
    return ""


def help_for_section(page_slug: str, section_slug: str) -> str:
    return ""
