"""Helpers for page views: SiteBlock values and page shell context."""

from __future__ import annotations

from src.core.block_defaults import get_block_default
from src.core.cms_context import get_site_blocks
from src.core.page_styles import resolve_page_style


def block_value(page: str, key: str, fallback: str = "") -> str:
    blocks = get_site_blocks()
    block = blocks.get(f"{page}.{key}")
    if block is not None and block.text_html:
        return block.text_html
    return fallback or get_block_default(page, key)


def _hex_luminance(color: str) -> float:
    raw = (color or "").strip().lstrip("#")
    if len(raw) == 3:
        raw = "".join(ch * 2 for ch in raw)
    if len(raw) != 6:
        return 0.0
    try:
        r, g, b = (int(raw[i : i + 2], 16) / 255 for i in (0, 2, 4))
    except ValueError:
        return 0.0
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def apply_page_shell(ctx: dict, page_key: str) -> None:
    style = resolve_page_style(page_key)
    bg = style.get("--page-bg", "") or ""
    ctx["page_key"] = page_key
    ctx["page_style"] = style
    ctx["glass"] = style.get("glass_enabled") == "1"
    ctx["shell_theme"] = "light" if _hex_luminance(bg) >= 0.55 else "dark"
    ctx["background_image"] = style.get("background_image_url") or ""
    ctx["shell_bg"] = bg
    ctx["shell_text"] = style.get("--page-text", "")
    ctx["shell_accent"] = style.get("--page-accent", "")
    ctx["seo_title"] = block_value(page_key, "seo_title")
    ctx["seo_description"] = block_value(page_key, "seo_description")
