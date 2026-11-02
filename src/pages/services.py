from django.urls import reverse

from .design_copy import HOME
from .models import AnalysisPage, ServicePage


def service_nav_items():
    items = []
    for svc in ServicePage.objects.filter(is_published=True).order_by('order', 'id'):
        items.append({
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
        })
    analysis = AnalysisPage.load()
    analysis_item = {
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
    items.insert(0, analysis_item)
    return items


def home_direction_items():
    by_key = {item['key']: item for item in service_nav_items()}
    ordered = []
    for key in HOME['directions_order']:
        if key in by_key:
            ordered.append(by_key[key])
    return ordered


# Порядок послуг у футері — як у Home.dc.html (SV)
FOOTER_SERVICES_ORDER = (
    'konsaltynh',
    'kompleksna-dopomoha-biznesu',
    'perevirka-kontrahentiv',
    'zbir-ta-analiz-informatsiyi',
    'zakhyst-vid-vytoku',
    'kryminalni-provadzhennia',
)


def footer_service_items():
    by_key = {item['key']: item for item in service_nav_items()}
    # fallback: match by slug fragment if seed slugs differ slightly
    ordered = []
    used = set()
    for key in FOOTER_SERVICES_ORDER:
        if key in by_key:
            ordered.append(by_key[key])
            used.add(key)
    for item in by_key.values():
        if item['key'] not in used:
            ordered.append(item)
    return ordered
