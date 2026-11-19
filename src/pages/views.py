from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView

from src.blog.models import Article
from src.core.og_image import og_image_from_field
from src.leads.forms import LeadForm

from .models import (
    AboutPage,
    AnalysisPage,
    ContactsPage,
    HomePage,
    PrivacyPage,
    ServicePage,
    ServicesIndex,
)
from .models_deep import DEEP_SLUG, DeepAnalytics
from .present import (
    analysis_copy,
    deep_copy,
    home_advantages,
    home_copy,
    home_directions,
    home_steps,
    service_copy,
)
from .privacy_copy import fill_privacy_placeholders
from .services import service_nav_items


def _crumbs_service(label):
    return [
        {'label': 'Послуги', 'url': reverse('pages:services')},
        {'label': label, 'url': ''},
    ]


def _og_image(request, image_field):
    return og_image_from_field(request, image_field) or None


class HomeView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page = HomePage.load()
        ctx['page'] = page
        ctx['copy'] = home_copy(page)
        ctx['services'] = home_directions(page)
        ctx['advantages'] = home_advantages(page)
        ctx['process_steps'] = home_steps(page)
        ctx['articles'] = Article.objects.filter(is_published=True)[:3]
        ctx['lead_form'] = LeadForm()
        ctx['og_image'] = _og_image(self.request, page.hero_image)
        return ctx


class AboutView(TemplateView):
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page = AboutPage.load()
        ctx['page'] = page
        # #region agent log
        from src.core.middleware_debug_session import _dbg

        _dbg(
            'C',
            'views.py:AboutView',
            'about related counts',
            {
                'intro_len': len(page.intro_text or ''),
                'principles': page.principles.count(),
                'team': page.team.count(),
                'intro_title': page.intro_title,
                'principles_title': page.principles_title,
            },
        )
        # #endregion
        ctx['crumbs'] = [{'label': 'Про компанію', 'url': ''}]
        ctx['lead_form'] = LeadForm()
        ctx['og_image'] = _og_image(self.request, page.hero_image)
        return ctx


class ServicesIndexView(TemplateView):
    template_name = 'pages/services_index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page = ServicesIndex.load()
        ctx['page'] = page
        ctx['catalog'] = service_nav_items()
        ctx['crumbs'] = [{'label': 'Послуги', 'url': ''}]
        ctx['lead_form'] = LeadForm()
        ctx['og_image'] = _og_image(self.request, page.hero_image)
        return ctx


class ServiceDetailView(TemplateView):
    def get_template_names(self):
        if self.kwargs.get('slug') == DEEP_SLUG:
            return ['pages/deep_analytics.html']
        return ['pages/service_detail.html']

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page = get_object_or_404(ServicePage, slug=kwargs['slug'], is_published=True)
        ctx['page'] = page
        ctx['others'] = [s for s in service_nav_items() if s['key'] != page.slug]
        ctx['lead_form'] = LeadForm()
        ctx['og_image'] = _og_image(self.request, page.hero_image)

        if page.slug == DEEP_SLUG:
            if not DeepAnalytics.objects.filter(page=page).exists():
                from .canon_seed import sync_deep
                sync_deep()
            deep = DeepAnalytics.objects.filter(page=page).first()
            ctx['d'] = deep_copy(deep) if deep else {}
            ctx['crumbs'] = _crumbs_service(page.title)
            return ctx

        copy = service_copy(page)
        ctx['crumbs'] = _crumbs_service(page.title)
        ctx['copy'] = copy
        return ctx


class AnalysisView(TemplateView):
    template_name = 'pages/analysis.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page = AnalysisPage.load()
        ctx['page'] = page
        ctx['copy'] = analysis_copy(page)
        ctx['crumbs'] = _crumbs_service(page.title or page.h1)
        ctx['others'] = [s for s in service_nav_items() if not s['is_analysis']]
        ctx['lead_form'] = LeadForm()
        ctx['og_image'] = _og_image(self.request, page.hero_image)
        return ctx


class ContactsView(TemplateView):
    template_name = 'pages/contacts.html'

    def get_context_data(self, **kwargs):
        from src.core.contact_defaults import resolve_public_contacts
        from src.core.models import SiteSettings

        ctx = super().get_context_data(**kwargs)
        ctx['page'] = ContactsPage.load()
        ctx['crumbs'] = [{'label': 'Контакти', 'url': ''}]
        ctx['lead_form'] = LeadForm()

        contacts = resolve_public_contacts(SiteSettings.load())
        ctx['phone_display'] = contacts['phone']
        ctx['phone_href'] = contacts['phone_href']
        ctx['email_display'] = contacts['email']
        ctx['email_href'] = contacts['email_href']
        ctx['address_display'] = contacts['address']
        ctx['facebook_url'] = contacts['facebook_url']
        ctx['facebook_handle'] = contacts['facebook_handle']
        ctx['facebook_hint'] = contacts['facebook_hint']
        ctx['map_embed_url'] = contacts['map_embed_url']
        ctx['telegram_url'] = contacts['telegram_url']
        ctx['whatsapp_url'] = contacts['whatsapp_url']
        ctx['signal_url'] = contacts['signal_url']
        return ctx


class PrivacyView(TemplateView):
    template_name = 'pages/privacy.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page'] = PrivacyPage.load()
        ctx['crumbs'] = [{'label': 'Політика конфіденційності', 'url': ''}]
        ctx['hero_text'] = ctx['page'].hero_text
        ctx['lead_form'] = LeadForm()
        ctx['privacy_body'] = mark_safe(fill_privacy_placeholders(ctx['page'].body))
        return ctx


def page_not_found(request, exception=None):
    return render(request, 'pages/404.html', {'lead_form': LeadForm()}, status=404)
