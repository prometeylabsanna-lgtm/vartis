from django.templatetags.static import static
from django.urls import reverse

from .design_copy import HOME
from .models import AnalysisPage, ServicePage


# Порядок послуг у меню/футері — як у .dc.html
SERVICES_NAV_ORDER = (
    'konsaltynh',
    'kompleksna-dopomoha-biznesu',
    'perevirka-kontrahentiv',
    'zbir-ta-analiz-informatsiyi',
    'zakhyst-vid-vytoku',
    'kryminalni-provadzhennia',
)

# Статичні запасні зображення карток (як у seed_content), якщо media відсутнє
CARD_IMAGE_STATIC = {
    'perevirka-kontrahentiv': 'images/services/dir-1.webp',
    'kompleksna-dopomoha-biznesu': 'images/services/dir-2.webp',
    'konsaltynh': 'images/services/dir-3.webp',
    'zbir-ta-analiz-informatsiyi': 'images/services/dir-4.webp',
    'zakhyst-vid-vytoku': 'images/blog/lock.webp',
    'kryminalni-provadzhennia': 'images/blog/law.webp',
}


def _is_seed_card_filename(name: str) -> bool:
    """Seed/design-файли (dir-1…4, lock/law) — завжди зі static, не з /tmp media."""
    base = (name or '').rsplit('/', 1)[-1].lower()
    if base in {'lock.jpg', 'law.jpg', 'lock.jpeg', 'law.jpeg'}:
        return True
    for i in ('1', '2', '3', '4'):
        if base == f'dir-{i}.png' or base.startswith(f'dir-{i}_'):
            return True
    return False


def _card_image_url(field, key):
    """
    Картки напрямів з дизайну — зі static (надійно на Vercel).
    Кастомний upload з адмінки — з media, якщо файл є.
    """
    path = CARD_IMAGE_STATIC.get(key)
    if field and getattr(field, 'name', None) and not _is_seed_card_filename(field.name):
        try:
            if field.storage.exists(field.name):
                return field.url
        except (ValueError, OSError):
            pass
    return static(path) if path else ''


def _analysis_nav_item():
    analysis = AnalysisPage.load()
    key = 'perevirka-kontrahentiv'
    return {
        'key': key,
        'title': analysis.title or 'Експрес-перевірка контрагентів — VI Analysis',
        'short': analysis.short or 'Збір інформації, ризики, рекомендації',
        'icon': analysis.icon or 'HiconOutlineShieldTick',
        'href': reverse('pages:analysis'),
        'card_image': analysis.card_image,
        'card_image_url': _card_image_url(analysis.card_image, key),
        'card_text': analysis.card_text or analysis.short,
        'tags': analysis.tag_list(),
        'is_analysis': True,
        'obj': analysis,
    }


def _service_nav_item(svc):
    return {
        'key': svc.slug,
        'title': svc.title,
        'short': svc.short,
        'icon': svc.icon,
        'href': reverse('pages:service_detail', kwargs={'slug': svc.slug}),
        'card_image': svc.card_image,
        'card_image_url': _card_image_url(svc.card_image, svc.slug),
        'card_text': svc.card_text or svc.short,
        'tags': svc.tag_list(),
        'is_analysis': False,
        'obj': svc,
    }


def service_nav_items():
    by_key = {
        svc.slug: _service_nav_item(svc)
        for svc in ServicePage.objects.filter(is_published=True)
    }
    by_key['perevirka-kontrahentiv'] = _analysis_nav_item()

    ordered = []
    used = set()
    for key in SERVICES_NAV_ORDER:
        if key in by_key:
            ordered.append(by_key[key])
            used.add(key)
    for key, item in by_key.items():
        if key not in used:
            ordered.append(item)
    return ordered


def home_direction_items():
    by_key = {item['key']: item for item in service_nav_items()}
    ordered = []
    for key in HOME['directions_order']:
        if key in by_key:
            ordered.append(by_key[key])
    return ordered


FOOTER_SERVICES_ORDER = SERVICES_NAV_ORDER


def footer_service_items():
    return service_nav_items()
