"""Реєстр дефолтів SiteBlock."""

from __future__ import annotations

BLOCK_CONTENT_TYPES: dict[tuple[str, str], str] = {}
BLOCK_LABELS: dict[tuple[str, str], str] = {}
BLOCK_DEFAULTS: dict[tuple[str, str], str] = {}
STATIC_FALLBACKS: dict[tuple[str, str], str] = {}
INLINE_KEYS: set[tuple[str, str]] = set()
MULTILINE_KEYS: set[tuple[str, str]] = set()
RICHTEXT_KEYS: set[tuple[str, str]] = set()
IMAGE_KEYS: set[tuple[str, str]] = set()


def _reg(
    page: str,
    key: str,
    default: str = "",
    *,
    label: str = "",
    content_type: str = "text",
    inline: bool = False,
    multiline: bool = False,
    richtext: bool = False,
) -> None:
    pair = (page, key)
    BLOCK_DEFAULTS[pair] = default
    BLOCK_LABELS[pair] = label or key
    BLOCK_CONTENT_TYPES[pair] = content_type
    if content_type == "image":
        IMAGE_KEYS.add(pair)
    if inline:
        INLINE_KEYS.add(pair)
    if multiline:
        MULTILINE_KEYS.add(pair)
    if richtext:
        RICHTEXT_KEYS.add(pair)
        MULTILINE_KEYS.add(pair)


def get_block_default(page: str, key: str) -> str:
    return BLOCK_DEFAULTS.get((page, key), "")


def get_block_label(page: str, key: str) -> str:
    return BLOCK_LABELS.get((page, key), key)


def get_block_content_type(page: str, key: str) -> str:
    return BLOCK_CONTENT_TYPES.get((page, key), "text")


def is_richtext_key(page: str, key: str) -> bool:
    return (page, key) in RICHTEXT_KEYS


def is_visibility_key(key: str) -> bool:
    return key.endswith("_visible") or key.endswith("_section_visible")


from src.core.block_defaults_home import register_home_blocks  # noqa: E402
from src.core.block_defaults_pages import register_page_blocks  # noqa: E402

register_home_blocks()
register_page_blocks()
