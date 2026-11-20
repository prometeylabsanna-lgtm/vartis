"""Перший сід карток напрямів на головній з поточного сайту."""

from __future__ import annotations

from pathlib import Path

from django.core.files import File

from src.pages.models import HomeDirection, HomePage

_HOME_DIRECTION_FALLBACK = (
    (
        'perevirka-kontrahentiv',
        'Експрес-перевірка контрагентів — VI Analysis',
        'Експрес-перевірка контрагентів, збір інформації — оцінка ризиків — рекомендації для бізнесу',
        'images/services/dir-1.webp',
        '/posluhy/perevirka-kontrahentiv/',
    ),
    (
        'kompleksna-dopomoha-biznesu',
        'Комплексна допомога бізнесу',
        'Рішення для захисту інтересів компанії, виявлення загроз і збереження контролю над важливою інформацією',
        'images/services/dir-2.webp',
        '/posluhy/kompleksna-dopomoha-biznesu/',
    ),
    (
        'konsaltynh',
        'Консалтинг',
        'Експертна підтримка бізнесу в питаннях аналізу ситуацій, оцінки ризиків і підготовки до важливих рішень',
        'images/services/dir-3.webp',
        '/posluhy/konsaltynh/',
    ),
    (
        'zbir-ta-analiz-informatsii',
        'Глибока аналітика',
        'Стратегічна аналітика: перевірені відомості про людей, компанії та ринки — для рішень, де помилка коштує дорого',
        'images/services/dir-4.webp',
        '/posluhy/zbir-ta-analiz-informatsii/',
    ),
)


def _attach_static_image(field, static_rel: str) -> None:
    src = Path(__file__).resolve().parents[1] / 'core' / 'static' / static_rel
    if not src.exists() or field.name:
        return
    with src.open('rb') as fh:
        field.save(src.name, File(fh), save=False)


def seed_home_directions(page: HomePage | None = None) -> None:
    from django.db.utils import OperationalError, ProgrammingError

    page = page or HomePage.load()
    try:
        if page.directions.exists():
            return
    except (OperationalError, ProgrammingError):
        return
    from src.pages.services import service_nav_items

    by_key = {item['key']: item for item in service_nav_items()}
    for i, (key, title, text, static_rel, href) in enumerate(_HOME_DIRECTION_FALLBACK):
        live = by_key.get(key) or {}
        live_title = (live.get('title') or '').strip()
        if live_title in {'', 'VI Analysis'}:
            live_title = title
        card = HomeDirection(
            page=page,
            title=live_title,
            text=live.get('card_text') or text,
            href=href,
            is_visible=True,
            order=i,
        )
        source = live.get('card_image')
        copied = False
        if source and getattr(source, 'name', ''):
            try:
                if source.storage.exists(source.name):
                    with source.open('rb') as fh:
                        card.image.save(source.name.rsplit('/', 1)[-1], fh, save=False)
                    copied = True
            except (ValueError, OSError):
                copied = False
        if not copied:
            _attach_static_image(card.image, static_rel)
        card.save()
