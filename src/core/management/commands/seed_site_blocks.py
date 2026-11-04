"""Ідемпотентний seed SiteBlock + PageStyle з registry та singleton-моделей."""

from __future__ import annotations

from django.core.management.base import BaseCommand

from src.core.block_defaults import (
    get_block_content_type,
    get_block_default,
    get_block_label,
)
from src.core.models import PageStyle, SiteBlock, SiteSettings
from src.core.page_styles import ensure_all_page_styles
from src.core.site_content_registry import all_registry_block_keys
from src.pages.models import (
    AboutPage,
    AnalysisPage,
    ContactsPage,
    HomePage,
    PrivacyPage,
    ServicesIndex,
)

SINGLETON_FIELD_MAP: dict[tuple[str, str], tuple[type, str]] = {}


def _map_page(model, page: str, fields: list[str]) -> None:
    for field in fields:
        SINGLETON_FIELD_MAP[(page, field)] = (model, field)


_map_page(
    HomePage,
    "home",
    [
        "seo_title",
        "seo_description",
        "h1",
        "hero_title",
        "hero_text",
        "hero_image",
        "services_title",
        "advantages_title",
        "mission_title",
        "mission_text",
        "mission_image",
        "process_title",
        "blog_title",
    ],
)
_map_page(
    AboutPage,
    "about",
    [
        "seo_title",
        "seo_description",
        "h1",
        "hero_title",
        "hero_text",
        "hero_image",
        "intro_title",
        "intro_text",
        "principles_title",
        "team_title",
        "team_lead",
        "science_eyebrow",
        "science_title",
        "science_text",
        "science_doi_url",
        "science_doi_label",
        "partners_eyebrow",
        "partners_title",
        "partners_text",
        "stats_title",
        "process_title",
    ],
)
_map_page(
    ServicesIndex,
    "services",
    ["seo_title", "seo_description", "h1", "hero_title", "hero_text", "hero_image"],
)
_map_page(
    AnalysisPage,
    "analysis",
    [
        "seo_title",
        "seo_description",
        "h1",
        "title",
        "hero_title",
        "hero_text",
        "hero_image",
        "short",
        "steps_title",
        "risks_title",
        "recommendation_title",
        "recommendation_text",
        "result_title",
        "result_text",
        "paket_title",
        "paket_subtitle",
        "paket_text",
        "include_title",
        "why_title",
        "price_title",
        "order_title",
        "order_text",
    ],
)
_map_page(
    ContactsPage,
    "contacts",
    ["seo_title", "seo_description", "h1", "hero_title", "hero_text", "hero_image", "info_title"],
)
_map_page(
    PrivacyPage,
    "privacy",
    ["seo_title", "seo_description", "h1", "hero_title", "body"],
)

SITE_SETTINGS_MAP = {
    ("site", "footer_cta_title"): "footer_cta_title",
    ("site", "footer_cta_text"): "footer_cta_text",
}


class Command(BaseCommand):
    help = "Ідемпотентний seed SiteBlock з registry"

    def handle(self, *args, **options):
        created = 0
        copied = 0
        for page, key in all_registry_block_keys():
            ctype = get_block_content_type(page, key)
            defaults = {
                "label": get_block_label(page, key),
                "content_type": ctype,
                "text_html": get_block_default(page, key) if ctype == "text" else "",
                "is_active": True,
            }
            if ctype == "url":
                defaults["link_url"] = get_block_default(page, key)
            block, was_created = SiteBlock.objects.get_or_create(page=page, key=key, defaults=defaults)
            if was_created:
                created += 1
            if self._copy_legacy(block):
                copied += 1

        styles_created = ensure_all_page_styles()
        self.stdout.write(
            self.style.SUCCESS(
                f"seed_site_blocks: +{created} blocks, copied {copied}, +{styles_created} PageStyle"
            )
        )

    def _copy_legacy(self, block: SiteBlock) -> bool:
        pair = (block.page, block.key)
        updated = False

        if pair in SITE_SETTINGS_MAP and not (block.text_html or block.link_url):
            attr = SITE_SETTINGS_MAP[pair]
            solo = SiteSettings.load()
            val = getattr(solo, attr, "") or ""
            if val:
                block.text_html = val
                block.save(update_fields=["text_html"])
                return True

        spec = SINGLETON_FIELD_MAP.get(pair)
        if not spec:
            return updated
        model, field_name = spec
        try:
            obj = model.load()
        except Exception:
            return False
        val = getattr(obj, field_name, None)
        if val is None:
            return False
        if hasattr(val, "read"):
            if block.image:
                return False
            if not val.name:
                return False
            block.image = val
            block.content_type = SiteBlock.ContentType.IMAGE
            block.save(update_fields=["image", "content_type"])
            return True
        text = str(val or "").strip()
        if not text or block.text_html:
            return False
        ctype = get_block_content_type(block.page, block.key)
        if ctype == "url":
            block.link_url = text
            block.text_html = text
            block.content_type = SiteBlock.ContentType.URL
            block.save(update_fields=["link_url", "text_html", "content_type"])
        else:
            block.text_html = text
            block.save(update_fields=["text_html"])
        return True
