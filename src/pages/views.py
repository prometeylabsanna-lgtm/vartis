from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import TemplateView

from src.blog.models import Article
from src.core.seo import media_or_static_absolute
from src.core.seo_copy import SERVICE_SEO
from src.leads.forms import LeadForm

from . import design_copy
from .models import (
    AboutPage,
    AnalysisPage,
    ContactsPage,
    HomePage,
    PrivacyPage,
    ServicePage,
    ServicesIndex,
)
from .services import home_direction_items, service_nav_items

DEEP_SLUG = 'zbir-ta-analiz-informatsiyi'


def _crumbs_service(label):
    return [
        {'label': 'Послуги', 'url': reverse('pages:services')},
        {'label': label, 'url': ''},
    ]


def _og_image(request, image_field):
    if image_field:
        return media_or_static_absolute(request, image_field.url)
    return None


class HomeView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page = HomePage.load()
        copy = design_copy.HOME
        ctx['page'] = page
        ctx['copy'] = copy
        ctx['services'] = home_direction_items()
        ctx['advantages'] = [
            {'icon': 'HiconOutlineScan5', 'title': 'Аналітичний підхід', 'text': 'Рішення на основі перевірених відомостей'},
            {'icon': 'HiconOutlineShieldTick', 'title': 'Оцінка ризиків', 'text': 'Виявлення потенційних загроз до ухвалення важливих рішень'},
            {'icon': 'HiconOutlineLock3', 'title': 'Конфіденційність', 'text': 'Захист інформації та факту звернення'},
            {'icon': 'HiconOutlineCalling1', 'title': 'Експертна підтримка', 'text': 'Фаховий аналіз і пояснення отриманих результатів'},
        ]
        ctx['process_steps'] = [
            {'num': '01', 'title': 'Вивчаємо завдання', 'text': "З'ясовуємо, яку інформацію потрібно отримати та на які питання відповісти."},
            {'num': '02', 'title': 'Проводимо дослідження', 'text': 'Збираємо, перевіряємо й аналізуємо відомості відповідно до погодженого завдання'},
            {'num': '03', 'title': 'Формуємо висновки', 'text': 'Систематизуємо результати та визначаємо встановлені факти й можливі ризики'},
            {'num': '04', 'title': 'Передаємо результат', 'text': 'Надаємо матеріали, необхідні для подальшого аналізу та ухвалення рішень'},
        ]
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
        svc_seo = SERVICE_SEO.get(page.slug)
        if svc_seo:
            page.seo_title = svc_seo['title']
            page.seo_description = svc_seo['description']

        if page.slug == DEEP_SLUG:
            ctx['d'] = design_copy.DEEP_ANALYTICS
            ctx['crumbs'] = _crumbs_service(
                design_copy.DEEP_ANALYTICS.get('crumb') or page.title
            )
        else:
            copy = dict(design_copy.SERVICES.get(page.slug, {}))
            ctx['crumbs'] = _crumbs_service(copy.get('crumb') or page.title)
            if 'h1' not in copy:
                copy['h1'] = page.h1 or page.title
            if 'hero_text' not in copy:
                copy['hero_text'] = page.hero_text
            if 'cta_primary' not in copy:
                copy['cta_primary'] = 'Обговорити завдання'
            if 'cta_secondary' not in copy:
                copy['cta_secondary'] = 'Як ми працюємо'
            if 'cta_secondary_href' not in copy:
                copy['cta_secondary_href'] = '#method'
            if 'scope_title' not in copy:
                copy['scope_title'] = page.scope_title or 'Що входить'
            if 'scope_paragraphs' not in copy:
                copy['scope_paragraphs'] = [page.scope_text] if page.scope_text else []
            if 'scope_items' not in copy:
                copy['scope_items'] = [i.text for i in page.scope_items.all()]
            if 'method_title' not in copy:
                copy['method_title'] = page.method_title or 'Методологія'
            if 'method_lead' not in copy:
                copy['method_lead'] = ''
            if 'steps' not in copy:
                copy['steps'] = [
                    (s.number, s.title, s.text) for s in page.method_steps.all()
                ]
            if 'advantages_title' not in copy:
                copy['advantages_title'] = page.advantages_title or 'Переваги для клієнта'
            if 'advantages_lead' not in copy:
                copy['advantages_lead'] = ''
            if 'advantages' not in copy:
                copy['advantages'] = [
                    ('HiconOutlineShieldTick', a.title, a.text)
                    for a in page.advantages.all()
                ]
            if 'order_title' not in copy:
                copy['order_title'] = page.order_title or 'Обговорімо\nвашу задачу'
            if 'order_text' not in copy:
                copy['order_text'] = page.order_text
            ctx['copy'] = copy
        return ctx


class AnalysisView(TemplateView):
    template_name = 'pages/analysis.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page = AnalysisPage.load()
        a = design_copy.ANALYSIS
        ctx['page'] = page
        ctx['copy'] = a
        ctx['crumbs'] = _crumbs_service(a['crumb'])
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
        return ctx


class PrivacyView(TemplateView):
    template_name = 'pages/privacy.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page'] = PrivacyPage.load()
        ctx['crumbs'] = [{'label': 'Політика конфіденційності', 'url': ''}]
        ctx['hero_text'] = (
            'Як ми обробляємо та захищаємо персональні дані, які ви залишаєте на сайті'
        )
        ctx['lead_form'] = LeadForm()
        return ctx


def page_not_found(request, exception=None):
    return render(request, 'pages/404.html', {'lead_form': LeadForm()}, status=404)
