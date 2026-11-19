"""Оновлення вже збережених текстів, слагів і контактів на наявній базі."""

from __future__ import annotations

import re

from src.blog.models import Article, ArticleBlock
from src.core.contact_defaults import apply_official_contacts
from src.core.models import SiteSettings
from src.core.models_cms import SiteBlock
from src.core.slug_renames import (
    ARTICLE_SLUGS,
    SERVICE_SLUGS,
    rename_slugs,
)
from src.pages.models import ServicePage

_APOSTROPHE = re.compile(r"([А-Яа-яІіЇїЄєҐґ])['\u2019\u02bc]([А-Яа-яІіЇїЄєҐґ])")


def _normalize(value: str) -> str:
    return _APOSTROPHE.sub(lambda match: match.group(1) + '\u02bc' + match.group(2), value or '')


def _normalize_obj(obj, fields: tuple[str, ...]) -> None:
    changed = []
    for name in fields:
        current = getattr(obj, name, '') or ''
        if not isinstance(current, str):
            continue
        updated = _normalize(current)
        if updated != current:
            setattr(obj, name, updated)
            changed.append(name)
    if changed:
        obj.save(update_fields=changed)


def _text_fields(model) -> tuple[str, ...]:
    from django.db import models

    names = []
    for field in model._meta.fields:
        if isinstance(field, (models.CharField, models.TextField)):
            names.append(field.name)
    return tuple(names)


def _normalize_queryset(model) -> None:
    from django.db.utils import OperationalError

    fields = _text_fields(model)
    if not fields:
        return
    try:
        rows = list(model.objects.all())
    except OperationalError:
        return
    for row in rows:
        _normalize_obj(row, fields)


def sync_editorial() -> None:
    rename_slugs(Article, ARTICLE_SLUGS)
    rename_slugs(ServicePage, SERVICE_SLUGS)

    from src.core.management.commands.seed_content_2 import seed_articles

    seed_articles()

    settings_row = SiteSettings.objects.filter(pk=1).first()
    if settings_row is not None:
        apply_official_contacts(settings_row)
        settings_row.save()

    for row in SiteSettings.objects.all():
        _normalize_obj(row, (
            'company_name', 'tagline', 'address', 'footer_cta_title', 'footer_cta_text',
            'default_seo_title', 'default_seo_description',
        ))
    for row in SiteBlock.objects.all():
        _normalize_obj(row, ('label', 'text_html', 'link_label'))
    for row in Article.objects.all():
        _normalize_obj(row, ('title', 'excerpt', 'body', 'seo_title', 'seo_description', 'h1'))
    for row in ArticleBlock.objects.all():
        _normalize_obj(row, ('heading', 'text', 'list_items'))

    from django.apps import apps

    for model in apps.get_app_config('pages').get_models():
        _normalize_queryset(model)
