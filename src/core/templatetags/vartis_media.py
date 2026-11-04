"""Публічні URL зображень (static fallback для design/seed на Vercel)."""

from __future__ import annotations

from django import template

from src.core.public_images import public_image_url

register = template.Library()


@register.simple_tag
def public_img(field, fallback: str = '') -> str:
    return public_image_url(field, fallback_static=fallback or None)
