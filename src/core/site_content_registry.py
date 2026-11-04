"""Registry CMS-секцій → sidebar + proxy admin."""

from __future__ import annotations

from typing import Iterable

from src.core.site_content_registry_base import ContentSection
from src.core.site_content_registry_home import CONTENT_SECTIONS_HOME
from src.core.site_content_registry_pages import CONTENT_SECTIONS_PAGES

CONTENT_SECTIONS: tuple[ContentSection, ...] = CONTENT_SECTIONS_HOME + CONTENT_SECTIONS_PAGES

# Групи сайдбару. Для site-секцій див. _SITE_SECTION_GROUPS нижче.
_SIDEBAR_GROUPS: tuple[tuple[str, frozenset[str]], ...] = (
    ("Головна", frozenset({"home"})),
    ("Про компанію", frozenset({"about"})),
    ("Послуги", frozenset({"services"})),
    ("VI Analysis", frozenset({"analysis"})),
    ("Контакти", frozenset({"contacts"})),
    ("Політика", frozenset({"privacy"})),
    ("Шапка", frozenset({"__site_header__"})),
    ("Підвал", frozenset({"__site_footer__"})),
)

# site/header і site/footer — окремі підменю зліва
_SITE_SECTION_GROUPS: dict[str, str] = {
    "header": "Шапка",
    "footer": "Підвал",
}

# Списки моделей поруч із секціями сторінки: (after_section_slug, item)
_PAGE_LIST_ITEMS: dict[str, tuple[tuple[str, dict], ...]] = {
    "home": (
        (
            "advantages",
            {
                "title": "Картки переваг",
                "icon": "star",
                "link": "/admin/pages/homeadvantage/",
            },
        ),
        (
            "process",
            {
                "title": "Кроки процесу",
                "icon": "format_list_numbered",
                "link": "/admin/pages/homeprocessstep/",
            },
        ),
    ),
    "about": (
        (
            "principles",
            {
                "title": "Принципи (список)",
                "icon": "verified",
                "link": "/admin/pages/aboutprinciple/",
            },
        ),
        (
            "team",
            {
                "title": "Команда (список)",
                "icon": "groups",
                "link": "/admin/pages/teammember/",
            },
        ),
        (
            "stats",
            {
                "title": "Цифри (список)",
                "icon": "pin",
                "link": "/admin/pages/aboutstat/",
            },
        ),
        (
            "process",
            {
                "title": "Кроки процесу",
                "icon": "route",
                "link": "/admin/pages/aboutprocessstep/",
            },
        ),
    ),
    "analysis": (
        (
            "steps",
            {
                "title": "Кроки (список)",
                "icon": "stairs",
                "link": "/admin/pages/analysisstep/",
            },
        ),
        (
            "risks",
            {
                "title": "Ризики (список)",
                "icon": "warning",
                "link": "/admin/pages/analysisrisk/",
            },
        ),
        (
            "include",
            {
                "title": "Що входить (список)",
                "icon": "checklist",
                "link": "/admin/pages/analysisinclude/",
            },
        ),
        (
            "why",
            {
                "title": "Чому вигідно (список)",
                "icon": "thumb_up",
                "link": "/admin/pages/analysiswhy/",
            },
        ),
        (
            "price",
            {
                "title": "Тарифи (список)",
                "icon": "payments",
                "link": "/admin/pages/analysispricerow/",
            },
        ),
    ),
    "services": (
        (
            "style",
            {
                "title": "Послуги (список)",
                "icon": "work",
                "link": "/admin/pages/servicepage/",
            },
        ),
    ),
}


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
    if section.page_slug == "site":
        return _SITE_SECTION_GROUPS.get(section.slug, "Інше")
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


def _build_page_items(page_slug: str, sections: list[ContentSection]) -> list[dict]:
    extras = _PAGE_LIST_ITEMS.get(page_slug, ())
    items: list[dict] = []
    for section in sections:
        items.append(_section_to_item(section))
        for after_slug, extra in extras:
            if after_slug == section.slug:
                items.append(dict(extra))
    return items


def build_content_sidebar_groups() -> list[dict]:
    buckets: dict[str, list[dict]] = {title: [] for title, _ in _SIDEBAR_GROUPS}
    buckets["Інше"] = []

    by_page: dict[str, list[ContentSection]] = {}
    for section in CONTENT_SECTIONS:
        if section.page_slug == "site":
            buckets[_section_group_title(section)].append(_section_to_item(section))
            continue
        by_page.setdefault(section.page_slug, []).append(section)

    for page_slug, sections in by_page.items():
        group_title = _section_group_title(sections[0]) if sections else "Інше"
        buckets[group_title].extend(_build_page_items(page_slug, sections))

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
