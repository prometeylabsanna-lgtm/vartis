from django.conf import settings

from .models import SiteSettings
from .seo import (
    absolute_url,
    get_public_origin,
    json_ld_script,
    media_or_static_absolute,
    organization_schema,
    robots_meta_content,
    seo_indexing_allowed,
    website_schema,
)


def site_settings(request):
    path = getattr(request, 'path', '') or ''
    is_admin = path.startswith('/admin/')

    try:
        settings_obj = SiteSettings.load()
    except Exception:
        settings_obj = None

    services = []
    footer_services = []
    lead_form = None

    if not is_admin:
        try:
            from src.pages.services import footer_service_items, service_nav_items

            services = service_nav_items()
            footer_services = footer_service_items()
        except Exception:
            services = []
            footer_services = []

        try:
            from src.leads.forms import LeadForm

            lead_form = LeadForm()
        except Exception:
            lead_form = None

    default_og = media_or_static_absolute(
        request,
        f'{settings.STATIC_URL}images/og-default.webp',
    )

    return {
        'site_settings': settings_obj,
        'nav_services': services,
        'footer_services': footer_services,
        'gtm_id': settings.GTM_ID,
        'lead_form': lead_form,
        'canonical_url': absolute_url(request),
        'public_origin': get_public_origin(request),
        'seo_robots': robots_meta_content(request),
        'seo_allow_indexing': seo_indexing_allowed(request),
        'og_image_default': default_og,
        'org_json_ld': json_ld_script(organization_schema(request, settings_obj)),
        'website_json_ld': json_ld_script(website_schema(request)),
    }
