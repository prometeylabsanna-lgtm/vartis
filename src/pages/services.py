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


def _analysis_nav_item():
    analysis = AnalysisPage.load()
    return {
        'key': 'perevirka-kontrahentiv',
        'title': analysis.title or 'Експрес-перевірка контрагентів — VI Analysis',
        'short': analysis.short or 'Збір інформації, ризики, рекомендації',
        'icon': analysis.icon or 'HiconOutlineShieldTick',
        'href': reverse('pages:analysis'),
        'card_image': analysis.card_image,
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
