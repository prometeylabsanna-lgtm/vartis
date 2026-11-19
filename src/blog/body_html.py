"""Збірка HTML тіла статті з блоків (міграція / seed)."""

from __future__ import annotations

from django.utils.html import escape


def _p(text: str) -> str:
    value = (text or "").strip()
    return f"<p>{escape(value)}</p>" if value else ""


def _h2(text: str) -> str:
    value = (text or "").strip()
    return f"<h2>{escape(value)}</h2>" if value else ""


def _ul(raw: str) -> str:
    items = [line.strip() for line in (raw or "").splitlines() if line.strip()]
    if not items:
        return ""
    lis = "".join(f"<li>{escape(item)}</li>" for item in items)
    return f"<ul>{lis}</ul>"


def _note(text: str) -> str:
    value = (text or "").strip()
    if not value:
        return ""
    return f'<blockquote class="art-note">{escape(value)}</blockquote>'


def article_blocks_to_html(blocks) -> str:
    parts: list[str] = []
    for block in blocks:
        kind = getattr(block, "block_type", "") or ""
        heading = getattr(block, "heading", "") or ""
        text = getattr(block, "text", "") or ""
        items = getattr(block, "list_items", "") or ""
        if kind == "h":
            parts.append(_h2(heading))
            parts.append(_p(text))
            parts.append(_ul(items))
        elif kind == "list":
            parts.append(_ul(items))
        elif kind == "note":
            parts.append(_note(text))
        else:
            parts.append(_p(text))
    return "".join(part for part in parts if part)
