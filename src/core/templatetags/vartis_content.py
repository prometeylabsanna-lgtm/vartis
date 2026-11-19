"""Templatetags для CMS-блоків (лише UK)."""

from __future__ import annotations

import re

from django import template
from django.templatetags.static import static
from django.utils.html import escape
from django.utils.safestring import mark_safe

from src.core.block_defaults import STATIC_FALLBACKS, get_block_default
from src.core.models import SiteBlock
from src.core.richtext import sanitize_html as _sanitize_html

register = template.Library()

_STRIP_TAGS = re.compile(r"<[^>]+>")


def _block(context, page: str, key: str) -> SiteBlock | None:
    blocks = context.get("site_blocks") or {}
    return blocks.get(f"{page}.{key}")


def _is_visible(block: SiteBlock | None) -> bool:
    if block is None:
        return True
    if not block.is_active:
        return False
    if block.text_html in {"0", "false", "False"}:
        return False
    return True


@register.filter
def cms_rich(value):
    return mark_safe(_sanitize_html(value or ""))


@register.simple_tag(takes_context=True)
def section_visible(context, page: str, visibility_key: str) -> bool:
    block = _block(context, page, visibility_key)
    if block is None:
        default = get_block_default(page, visibility_key)
        return default not in {"0", "false", "False", ""}
    return _is_visible(block)


def _text_value(context, page: str, key: str, fallback: str = "") -> str:
    block = _block(context, page, key)
    if block is not None and block.text_html:
        return block.text_html
    return fallback or get_block_default(page, key)


@register.simple_tag(takes_context=True)
def block_text(context, page: str, key: str, fallback: str = "") -> str:
    return _text_value(context, page, key, fallback=fallback)


@register.simple_tag(takes_context=True)
def block_plain(context, page: str, key: str, fallback: str = "") -> str:
    raw = _text_value(context, page, key, fallback=fallback)
    return _STRIP_TAGS.sub("", raw).strip()


@register.simple_tag(takes_context=True)
def block_html(context, page: str, key: str, fallback: str = "") -> str:
    return block_rich(context, page, key, fallback=fallback)


@register.simple_tag(takes_context=True)
def block_rich(context, page: str, key: str, fallback: str = "") -> str:
    raw = _text_value(context, page, key, fallback=fallback)
    return mark_safe(_sanitize_html(raw))


@register.simple_tag(takes_context=True)
def block_image_url(context, page: str, key: str, fallback_static: str = "") -> str:
    block = _block(context, page, key)
    if block is not None and block.image:
        try:
            return block.image.url
        except Exception:
            pass
    static_path = fallback_static or STATIC_FALLBACKS.get((page, key), "")
    if static_path:
        return static(static_path)
    return ""


@register.filter
def gold_tail(value):
    text = str(value or "").strip()
    if " " not in text:
        return escape(text)
    head, tail = text.rsplit(" ", 1)
    return mark_safe(f'{escape(head)} <span class="gold-text">{escape(tail)}</span>')
