"""Registry CMS-секцій → sidebar + proxy admin."""

from __future__ import annotations

from typing import Iterable

from src.core.site_content_registry_base import ContentSection
from src.core.site_content_registry_home import CONTENT_SECTIONS_HOME
from src.core.site_content_registry_pages import CONTENT_SECTIONS_PAGES

CONTENT_SECTIONS: tuple[ContentSection, ...] = CONTENT_SECTIONS_HOME + CONTENT_SECTIONS_PAGES

_SIDEBAR_GROUPS: tuple[tuple[str, frozenset[str]], ...] = (
    ("Головна", frozenset({"home"})),
    ("Про компанію", frozenset({"about"})),
    ("Послуги", frozenset({"services"})),
    ("VI Analysis", frozenset({"analysis"})),
    ("Контакти", frozenset({"contacts"})),
    ("Політика", frozenset({"privacy"})),
    ("Оболонка", frozenset({"site"})),
)


def get_section(page_slug: str, section_slug: str) -> ContentSection | None:
    for section in CONTENT_SECTIONS:
        if section.page_slug == page_slug and section.slug == section_slug:
            return section
    return None


def all_registry_block_keys() -> list[tuple[str, str]]:
    keys: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for section in CONTENT_SECTIONS:
        for pair in section.blocks:
            if pair not in seen:
                seen.add(pair)
                keys.append(pair)
    return keys


def _sidebar_item_title(section: ContentSection) -> str:
    return section.sidebar_title or section.title


def _section_group_title(section: ContentSection) -> str:
    for group_title, page_slugs in _SIDEBAR_GROUPS:
        if section.page_slug in page_slugs:
            return group_title
    return "Інше"


def _section_to_item(section: ContentSection) -> dict:
    # Рядок, не reverse_lazy: Vercel серіалізує UNFOLD settings до apps ready.
    path = f"/admin/core/{section.admin_model_name}/"
    return {
        "title": _sidebar_item_title(section),
        "icon": section.sidebar_icon,
        "link": path,
    }


def build_content_sidebar_groups() -> list[dict]:
    buckets: dict[str, list[dict]] = {title: [] for title, _ in _SIDEBAR_GROUPS}
    buckets["Інше"] = []

    for section in CONTENT_SECTIONS:
        buckets[_section_group_title(section)].append(_section_to_item(section))

    groups: list[dict] = []
    first = True
    for title, _ in _SIDEBAR_GROUPS:
        items = buckets[title]
        if not items:
            continue
        groups.append({
            "title": title,
            "separator": first,
            "collapsible": True,
            "items": items,
        })
        first = False

    if buckets["Інше"]:
        groups.append({
            "title": "Інше",
            "separator": first,
            "collapsible": True,
            "items": buckets["Інше"],
        })
    return groups


def iter_section_blocks(section: ContentSection) -> Iterable[tuple[str, str]]:
    return section.blocks
