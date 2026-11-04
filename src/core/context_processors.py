from django.conf import settings

from .models import SiteSettings


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

    return {
        'site_settings': settings_obj,
        'nav_services': services,
        'footer_services': footer_services,
        'gtm_id': settings.GTM_ID,
        'lead_form': lead_form,
    }
