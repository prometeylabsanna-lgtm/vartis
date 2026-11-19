"""Перейменування старих транслітів на систему як у kryminalni-provadzhennia."""

from __future__ import annotations

ARTICLE_SLUGS = {
    'osint-dlya-biznesu': 'osint-dlia-biznesu',
    'zakhyst-komertsiynoyi-informatsiyi': 'zakhyst-komertsiinoi-informatsii',
    'sudova-istoriya-partnera': 'sudova-istoriia-partnera',
    'nadiynist-postachalnyka': 'nadiinist-postachalnyka',
}

SERVICE_SLUGS = {
    'zbir-ta-analiz-informatsiyi': 'zbir-ta-analiz-informatsii',
}


def rename_slugs(model, mapping: dict[str, str]) -> None:
    for old, new in mapping.items():
        if old == new:
            continue
        old_rows = model.objects.filter(slug=old)
        if model.objects.filter(slug=new).exists():
            old_rows.delete()
            continue
        old_rows.update(slug=new)
