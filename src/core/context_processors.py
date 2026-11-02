from django.conf import settings

from .models import SiteSettings


def site_settings(request):
    try:
        settings_obj = SiteSettings.load()
    except Exception:
        settings_obj = None

    services = []
    footer_services = []
    try:
        from src.pages.services import footer_service_items, service_nav_items
        services = service_nav_items()
        footer_services = footer_service_items()
    except Exception:
        services = []
        footer_services = []

    from src.leads.forms import LeadForm

    return {
        'site_settings': settings_obj,
        'nav_services': services,
        'footer_services': footer_services,
        'gtm_id': settings.GTM_ID,
        'lead_form': LeadForm(),
    }
