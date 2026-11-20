"""Очищення HTML з TinyMCE для публічних сторінок."""

from __future__ import annotations

import re

from django.utils.html import escape
from django.utils.safestring import mark_safe

_ALLOWED = frozenset(
    {
        'p', 'br', 'strong', 'b', 'em', 'i', 'u', 'ul', 'ol', 'li',
        'a', 'span', 'h2', 'h3', 'blockquote',
    }
)
_TAG = re.compile(r'</?([a-z0-9]+)((?:\s[^>]*)?)>', re.IGNORECASE)
_HAS_HTML = re.compile(
    r'</?(?:p|br|strong|b|em|i|u|ul|ol|li|a|span|h2|h3|blockquote)\b',
    re.I,
)
_NOTE_CLASS = 'art-note'
_ATTR = re.compile(r'([a-z0-9:-]+)\s*=\s*("([^"]*)"|\'([^\']*)\')', re.I)
_STYLE_PROP = re.compile(
    r'^\s*(color|background-color|font-size|font-family|font-weight|text-decoration)\s*:\s*(.+)$',
    re.I,
)
_UNSAFE_CSS = re.compile(r'url\s*\(|expression|javascript|@import|behavior', re.I)
_SAFE_HREF = re.compile(r'^(https?:|mailto:|#|/)', re.I)


def _clean_style(raw: str) -> str:
    kept = []
    for part in (raw or '').split(';'):
        match = _STYLE_PROP.match(part.strip())
        if not match:
            continue
        value = match.group(2).strip()
        if not value or _UNSAFE_CSS.search(value):
            continue
        kept.append(f'{match.group(1).lower()}: {value}')
    return '; '.join(kept)


def _clean_href(raw: str) -> str:
    href = (raw or '').strip()
    if not href or not _SAFE_HREF.match(href):
        return ''
    if href.startswith('/') and not href.startswith('//'):
        from src.core.i18n_urls import localize_internal_path

        return localize_internal_path(href)
    return href


def _rebuild_open(tag: str, attr_blob: str) -> str:
    attrs = []
    for match in _ATTR.finditer(attr_blob or ''):
        name = match.group(1).lower()
        value = match.group(3) if match.group(3) is not None else (match.group(4) or '')
        if name.startswith('on'):
            continue
        if tag == 'a' and name == 'href':
            href = _clean_href(value)
            if href:
                attrs.append(f'href="{escape(href)}"')
        elif tag == 'a' and name in {'target', 'rel', 'title'}:
            attrs.append(f'{name}="{escape(value)}"')
        elif name == 'style' and tag in {'p', 'span', 'li', 'ul', 'ol'}:
            style = _clean_style(value)
            if style:
                attrs.append(f'style="{escape(style)}"')
        elif tag == 'blockquote' and name == 'class':
            classes = [token for token in value.split() if token == _NOTE_CLASS]
            if classes:
                attrs.append(f'class="{" ".join(classes)}"')
    extra = (' ' + ' '.join(attrs)) if attrs else ''
    if tag == 'br':
        return '<br>'
    return f'<{tag}{extra}>'


def sanitize_html(value: str) -> str:
    if not value:
        return ''
    if not _HAS_HTML.search(value):
        return escape(value).replace('\n', '<br>')

    def replace(match: re.Match) -> str:
        tag = match.group(1).lower()
        if tag not in _ALLOWED:
            return ''
        blob = match.group(0)
        if blob.startswith('</'):
            return '' if tag == 'br' else f'</{tag}>'
        return _rebuild_open(tag, match.group(2) or '')

    return _TAG.sub(replace, value)


def render_rich(value: str) -> str:
    return mark_safe(sanitize_html(value or ''))
