from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import TemplateView

from src.blog.models import Article
from src.leads.forms import LeadForm

from . import design_copy
from .cms import apply_page_shell
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

_HOME_ADVANTAGES_FALLBACK = [
    {'icon': 'HiconOutlineScan5', 'title': 'Аналітичний підхід', 'text': 'Рішення на основі перевірених відомостей'},
    {'icon': 'HiconOutlineShieldTick', 'title': 'Оцінка ризиків', 'text': 'Виявлення потенційних загроз до ухвалення важливих рішень'},
    {'icon': 'HiconOutlineLock3', 'title': 'Конфіденційність', 'text': 'Захист інформації та факту звернення'},
    {'icon': 'HiconOutlineCalling1', 'title': 'Експертна підтримка', 'text': 'Фаховий аналіз і пояснення отриманих результатів'},
]

_HOME_PROCESS_FALLBACK = [
    {'num': '01', 'title': 'Вивчаємо завдання', 'text': "З'ясовуємо, яку інформацію потрібно отримати та на які питання відповісти."},
    {'num': '02', 'title': 'Проводимо дослідження', 'text': 'Збираємо, перевіряємо й аналізуємо відомості відповідно до погодженого завдання'},
    {'num': '03', 'title': 'Формуємо висновки', 'text': 'Систематизуємо результати та визначаємо встановлені факти й можливі ризики'},
    {'num': '04', 'title': 'Передаємо результат', 'text': 'Надаємо матеріали, необхідні для подальшого аналізу та ухвалення рішень'},
]


def _crumbs_service(label):
    return [
        {'label': 'Послуги', 'url': reverse('pages:services')},
        {'label': label, 'url': ''},
    ]


class HomeView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page = HomePage.load()
        apply_page_shell(ctx, 'home')
        ctx['page'] = page
        ctx['services'] = home_direction_items()
        db_adv = [
            {'icon': a.icon or 'HiconOutlineScan5', 'title': a.title, 'text': a.text}
            for a in page.advantages.all()
        ]
        ctx['advantages'] = db_adv or _HOME_ADVANTAGES_FALLBACK
        db_steps = [
            {'num': s.number, 'title': s.title, 'text': s.text}
            for s in page.process_steps.all()
        ]
        ctx['process_steps'] = db_steps or _HOME_PROCESS_FALLBACK
        ctx['articles'] = Article.objects.filter(is_published=True)[:3]
        ctx['lead_form'] = LeadForm()
        return ctx


class AboutView(TemplateView):
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        apply_page_shell(ctx, 'about')
        ctx['page'] = AboutPage.load()
        ctx['crumbs'] = [{'label': 'Про компанію', 'url': ''}]
        ctx['lead_form'] = LeadForm()
        return ctx


class ServicesIndexView(TemplateView):
    template_name = 'pages/services_index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        apply_page_shell(ctx, 'services')
        ctx['page'] = ServicesIndex.load()
        ctx['catalog'] = service_nav_items()
        ctx['crumbs'] = [{'label': 'Послуги', 'url': ''}]
        ctx['lead_form'] = LeadForm()
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
        apply_page_shell(ctx, 'analysis')
        ctx['page'] = page
        ctx['copy'] = a
        ctx['crumbs'] = _crumbs_service(a['crumb'])
        ctx['others'] = [s for s in service_nav_items() if not s['is_analysis']]
        ctx['lead_form'] = LeadForm()
        return ctx


class ContactsView(TemplateView):
    template_name = 'pages/contacts.html'

    MAP_EMBED_DEFAULT = (
        'https://maps.google.com/maps?q=%D0%9A%D0%B8%D1%97%D0%B2,+%D0%B2%D1%83%D0%BB.+'
        '%D0%A5%D1%80%D0%B5%D1%89%D0%B0%D1%82%D0%B8%D0%BA,+1&hl=uk&z=16&output=embed'
    )
    FB_DEFAULT = 'https://facebook.com/vartisintelligence'

    def get_context_data(self, **kwargs):
        from src.core.models import SiteSettings

        ctx = super().get_context_data(**kwargs)
        apply_page_shell(ctx, 'contacts')
        ctx['page'] = ContactsPage.load()
        ctx['crumbs'] = [{'label': 'Контакти', 'url': ''}]
        ctx['lead_form'] = LeadForm()

        s = SiteSettings.load()
        phone = (s.phone or '').strip()
        email = (s.email or '').strip()
        address = (s.address or '').strip()
        fb = (s.facebook_url or '').strip() or self.FB_DEFAULT
        handle = fb.rstrip('/').split('/')[-1] or 'vartisintelligence'

        ctx['phone_display'] = phone or '[Телефон]'
        ctx['phone_href'] = (
            f"tel:{''.join(ch for ch in phone if ch.isdigit() or ch == '+')}"
            if phone else ''
        )
        ctx['email_display'] = email or '[Email]'
        ctx['email_href'] = f'mailto:{email}' if email else ''
        ctx['address_display'] = address or '[Адреса офісу]'
        ctx['facebook_url'] = fb
        ctx['facebook_handle'] = handle
        ctx['facebook_hint'] = f'facebook.com/{handle}'
        ctx['map_embed_url'] = (s.map_embed_url or '').strip() or self.MAP_EMBED_DEFAULT
        return ctx


class PrivacyView(TemplateView):
    template_name = 'pages/privacy.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        apply_page_shell(ctx, 'privacy')
        ctx['page'] = PrivacyPage.load()
        ctx['crumbs'] = [{'label': 'Політика конфіденційності', 'url': ''}]
        ctx['lead_form'] = LeadForm()
        return ctx


def page_not_found(request, exception=None):
    return render(request, 'pages/404.html', {'lead_form': LeadForm()}, status=404)
