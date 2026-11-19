"""Заповнює моделі поточними текстами, не чіпаючи вже змінені поля."""

from __future__ import annotations

import re

from django.utils.html import strip_tags

from src.core.models import SiteBlock
from src.pages import design_copy
from src.pages.models import (
    AnalysisInclude,
    AnalysisPage,
    AnalysisPaketStep,
    AnalysisPayTerm,
    AnalysisPricePart,
    AnalysisRec,
    AnalysisRisk,
    AnalysisRiskLevel,
    AnalysisTariff,
    AnalysisTariffLine,
    AnalysisWhy,
    DeepAnalytics,
    DeepFaq,
    DeepGetItem,
    DeepPayStage,
    DeepQualityItem,
    DeepSnippet,
    DeepStep,
    HomeAdvantage,
    HomePage,
    HomeProcessStep,
    ServiceAdvantage,
    ServiceMethodStep,
    ServicePage,
    ServiceScopeItem,
    ServiceScopeParagraph,
)
from src.pages.models_deep import DEEP_SLUG

_HOME_ADVANTAGES = (
    ('HiconOutlineScan5', 'Аналітичний підхід', 'Рішення на основі перевірених відомостей'),
    ('HiconOutlineShieldTick', 'Оцінка ризиків', 'Виявлення потенційних загроз до ухвалення важливих рішень'),
    ('HiconOutlineLock3', 'Конфіденційність', 'Захист інформації та факту звернення'),
    ('HiconOutlineCalling1', 'Експертна підтримка', 'Фаховий аналіз і пояснення отриманих результатів'),
)
_HOME_STEPS = (
    ('01', 'Вивчаємо завдання', 'Зʼясовуємо, яку інформацію потрібно отримати та на які питання відповісти'),
    ('02', 'Проводимо дослідження', 'Збираємо, перевіряємо й аналізуємо відомості відповідно до погодженого завдання'),
    ('03', 'Формуємо висновки', 'Систематизуємо результати та визначаємо встановлені факти й можливі ризики'),
    ('04', 'Передаємо результат', 'Надаємо матеріали, необхідні для подальшого аналізу та ухвалення рішень'),
)


def _default(obj, name):
    field = obj._meta.get_field(name)
    default = field.default
    return default() if callable(default) else default


def _plain(value: str) -> str:
    return re.sub(r'\s+', ' ', strip_tags(value or '')).strip()


def _open(obj, name, *legacy) -> bool:
    current = getattr(obj, name)
    if current is None:
        current = ''
    allowed = {_default(obj, name), '', *legacy}
    return current in allowed


def adopt(obj, name, value, *legacy) -> bool:
    if value is None:
        return False
    if not _open(obj, name, *legacy):
        return False
    if getattr(obj, name) == value:
        return False
    setattr(obj, name, value)
    return True


def adopt_block(obj, name, page: str, key: str, *legacy) -> bool:
    block = SiteBlock.objects.filter(page=page, key=key).first()
    if block is None or not (block.text_html or '').strip():
        return False
    text = strip_tags(block.text_html).strip()
    from src.core.block_defaults import BLOCK_DEFAULTS

    if _plain(text) == _plain(BLOCK_DEFAULTS.get((page, key), '')):
        return False
    return adopt(obj, name, text, *legacy)


def _save(obj, dirty: bool):
    if dirty:
        obj.save()


def sync_home() -> None:
    page = HomePage.load()
    home = design_copy.HOME
    h1_seed = 'Інформація, що перетворює ризики на переваги'
    hero_seed = (
        'Стратегічна аналітика, перевірка контрагентів та захист бізнесу. '
        'Допомагаємо виявляти приховані ризики, перевіряти інформацію й ухвалювати обґрунтовані рішення'
    )
    mission_seed = 'Стратегічна інформація для впевнених рішень'
    dirty = False
    dirty |= adopt_block(page, 'h1', 'home', 'h1', h1_seed)
    dirty |= adopt(page, 'h1', home['h1'], h1_seed)
    dirty |= adopt_block(page, 'hero_title', 'home', 'hero_title', h1_seed)
    dirty |= adopt(page, 'hero_title', home['h1'], h1_seed)
    dirty |= adopt_block(page, 'hero_text', 'home', 'hero_text', hero_seed)
    dirty |= adopt(page, 'hero_text', home['hero_text'], hero_seed)
    dirty |= adopt(page, 'hero_cta', home['hero_cta'])
    for key in (
        'services_title', 'services_lead', 'advantages_title', 'advantages_lead',
        'process_title', 'process_lead', 'blog_title', 'blog_lead',
    ):
        dirty |= adopt_block(page, key, 'home', key, 'Напрями', 'Переваги', 'Як ми працюємо', 'Аналітика')
        dirty |= adopt(page, key, home[key], 'Напрями', 'Переваги', 'Як ми працюємо', 'Аналітика')
    dirty |= adopt_block(page, 'mission_title', 'home', 'mission_title', mission_seed, 'Наша місія')
    dirty |= adopt(page, 'mission_title', home['mission_title'], mission_seed, 'Наша місія')
    dirty |= adopt_block(page, 'mission_text', 'home', 'mission_text')
    dirty |= adopt(page, 'mission_text', home['mission_text'])
    dirty |= adopt(page, 'blog_all_label', 'Усі статті →')
    _save(page, dirty)
    if not page.advantages.exists():
        for i, (icon, title, text) in enumerate(_HOME_ADVANTAGES):
            HomeAdvantage.objects.create(page=page, icon=icon, title=title, text=text, order=i)
    if not page.process_steps.exists():
        for i, (num, title, text) in enumerate(_HOME_STEPS):
            HomeProcessStep.objects.create(page=page, number=num, title=title, text=text, order=i)
    from src.pages.home_directions_seed import seed_home_directions

    seed_home_directions(page)


def sync_service(page: ServicePage, design: dict) -> None:
    dirty = False
    space_order = (design.get('order_title') or '').replace('\n', ' ')
    for field, key in (
        ('hero_text', 'hero_text'),
        ('cta_primary', 'cta_primary'),
        ('cta_secondary', 'cta_secondary'),
        ('cta_secondary_href', 'cta_secondary_href'),
        ('scope_title', 'scope_title'),
        ('scope_variant', 'scope_variant'),
        ('scope_feature_title', 'scope_feature_title'),
        ('scope_feature_text', 'scope_feature_text'),
        ('method_title', 'method_title'),
        ('method_lead', 'method_lead'),
        ('method_variant', 'method_variant'),
        ('advantages_title', 'advantages_title'),
        ('advantages_lead', 'advantages_lead'),
        ('order_text', 'order_text'),
        ('order_variant', 'order_variant'),
    ):
        if key in design:
            dirty |= adopt(page, field, design[key], space_order)
    if 'order_title' in design:
        dirty |= adopt(page, 'order_title', design['order_title'], space_order)
    if 'advantages_dark' in design and _open(page, 'advantages_dark'):
        page.advantages_dark = bool(design['advantages_dark'])
        dirty = True
    _save(page, dirty)
    if not page.scope_paragraphs.exists():
        for i, text in enumerate(design.get('scope_paragraphs') or []):
            ServiceScopeParagraph.objects.create(page=page, text=text, order=i)
    if not page.scope_items.exists():
        for i, text in enumerate(design.get('scope_items') or []):
            ServiceScopeItem.objects.create(page=page, text=text[:400], order=i)
    if not page.method_steps.exists():
        for i, (num, title, text) in enumerate(design.get('steps') or []):
            ServiceMethodStep.objects.create(page=page, number=num, title=title, text=text, order=i)
    icons = {title: icon for icon, title, _text in design.get('advantages') or []}
    if not page.advantages.exists():
        for i, (icon, title, text) in enumerate(design.get('advantages') or []):
            ServiceAdvantage.objects.create(page=page, icon=icon, title=title, text=text, order=i)
    else:
        for item in page.advantages.all():
            icon = icons.get(item.title)
            if icon and not item.icon:
                item.icon = icon
                item.save(update_fields=['icon'])


def sync_services() -> None:
    for slug, design in design_copy.SERVICES.items():
        page = ServicePage.objects.filter(slug=slug).first()
        if page is not None:
            sync_service(page, design)


def _snippet(page, kind, rows):
    if page.snippets.filter(kind=kind).exists():
        return
    for i, row in enumerate(rows):
        if isinstance(row, tuple):
            value, text = row
        else:
            value, text = '', row
        DeepSnippet.objects.create(page=page, kind=kind, value=value, text=text, order=i)


def sync_deep() -> None:
    service = ServicePage.objects.filter(slug=DEEP_SLUG).first()
    if service is None:
        return
    data = design_copy.DEEP_ANALYTICS
    deep, _created = DeepAnalytics.objects.get_or_create(page=service)
    express = data['compare_express']
    compare = data['compare_deep']
    mapping = {
        'h1': data['h1'],
        'hero_text': data['hero_text'],
        'cta_primary': data['cta_primary'],
        'cta_secondary': data['cta_secondary'],
        'cta_secondary_href': data['cta_secondary_href'],
        'strategy_eyebrow': data['strategy_eyebrow'],
        'strategy_title': data['strategy_title'],
        'compare_express_eyebrow': express['eyebrow'],
        'compare_express_title': express['title'],
        'compare_express_text': express['text'],
        'compare_express_link': express['link'],
        'compare_deep_eyebrow': compare['eyebrow'],
        'compare_deep_title': compare['title'],
        'compare_deep_text': compare['text'],
        'nda_title': data['nda_title'],
        'nda_text': data['nda_text'],
        'nda_note': data['nda_note'],
        'get_title': data['get_title'],
        'get_lead': data['get_lead'],
        'example_title': data['example_title'],
        'example_lead': data['example_lead'],
        'ex_frag1': data['ex_frag1'],
        'ex_frag3': data['ex_frag3'],
        'ex_frag3_lead': data['ex_frag3_lead'],
        'ex_frag4': data['ex_frag4'],
        'ex_frag4_lead': data['ex_frag4_lead'],
        'ex_assumption': data['ex_assumption'],
        'ex_why_not': data['ex_why_not'],
        'pay_title': data['pay_title'],
        'pay_lead': data['pay_lead'],
        'quality_title': data['quality_title'],
        'faq_title': data['faq_title'],
        'order_title': data['order_title'],
        'order_text': data['order_text'],
    }
    dirty = False
    for name, value in mapping.items():
        dirty |= adopt(deep, name, value)
    _save(deep, dirty)
    if not deep.steps.exists():
        for i, (num, title, text) in enumerate(data['steps']):
            DeepStep.objects.create(page=deep, number=num, title=title, text=text, order=i)
    if not deep.get_items.exists():
        for i, (num, title, text) in enumerate(data['get_items']):
            DeepGetItem.objects.create(page=deep, number=num, title=title, text=text, order=i)
    if not deep.faqs.exists():
        for i, (question, answer) in enumerate(data['faqs']):
            DeepFaq.objects.create(page=deep, question=question, answer=answer, order=i)
    if not deep.pay_stages.exists():
        for i, row in enumerate(data['pay_stages']):
            DeepPayStage.objects.create(page=deep, order=i, **row)
    if not deep.quality_items.exists():
        for i, (title, text) in enumerate(data['quality']):
            DeepQualityItem.objects.create(page=deep, title=title, text=text, order=i)
    _snippet(deep, DeepSnippet.Kind.STRATEGY, data['strategy_paragraphs'])
    _snippet(deep, DeepSnippet.Kind.STAT, data['ex_stats'])
    _snippet(deep, DeepSnippet.Kind.NOTE, data['ex_notes'])
    _snippet(deep, DeepSnippet.Kind.FACT, data['ex_facts'])
    _snippet(deep, DeepSnippet.Kind.LIMIT, data['ex_limits'])
    _snippet(deep, DeepSnippet.Kind.GUARANTEE, data['pay_guar'])


def sync_analysis() -> None:
    page = AnalysisPage.load()
    data = design_copy.ANALYSIS
    example = data['rec_example']
    scalar = {
        'h1': data['h1'],
        'hero_title': data['h1'],
        'hero_text': data['hero_text'],
        'cta_primary': data['cta_primary'],
        'cta_secondary': data['cta_secondary'],
        'cta_secondary_href': data['cta_secondary_href'],
        'steps_eyebrow': data['steps_eyebrow'],
        'steps_leads': '\n\n'.join(data['steps_leads']),
        'risks_title': data['risks_title'],
        'risks_lead': data['risks_lead'],
        'risks_note_title': data['risks_note_title'],
        'risks_note': data['risks_note'],
        'recommendation_title': data['recommendation_title'],
        'recommendation_text': data['recommendation_text'],
        'rec_heading': example['heading'],
        'rec_badge': example['badge'],
        'rec_code': example['code'],
        'rec_verdict': example['verdict'],
        'rec_note': example['note'],
        'rec_flag': example['flag'],
        'rec_accept': example['accept'],
        'rec_reject': example['reject'],
        'rec_date': example['date'],
        'rec_caption': example['caption'],
        'result_title': data['result_title'],
        'result_text': data['result_text'],
        'result_method_prefix': data['result_method_prefix'],
        'result_method_suffix': data['result_method_suffix'],
        'result_doi_href': data['result_doi_href'],
        'result_doi_label': data['result_doi_label'],
        'paket_eyebrow': data['paket_eyebrow'],
        'paket_title': data['paket_title'],
        'paket_lead': data['paket_lead'],
        'include_title': data['include_title'],
        'include_lead': data['include_lead'],
        'include_option_eyebrow': data['include_option_eyebrow'],
        'include_option_title': data['include_option_title'],
        'include_option_text': data['include_option_text'],
        'why_title': data['why_title'],
        'price_title': data['price_title'],
        'price_lead': data['price_lead'],
        'tariffs_title': data['tariffs_title'],
        'price_note': data['price_note'],
        'order_title': data['order_title'],
        'order_text': data['order_text'],
    }
    short_rec = (
        'Рекомендаційний модуль перетворює виявлені ризики на конкретний варіант дій '
        'і показує, які саме фактори на нього вплинули.'
    )
    short_result = (
        'Замовник отримує оцінку ризиків і рекомендації для ухвалення рішення: '
        'на стандартних умовах, із додатковими умовами або з відмовою від співпраці.'
    )
    short_order = 'Надішліть назву компанії або код ЄДРПОУ — ми підготуємо звіт із рекомендацією.'
    hero_seed = (
        'Експрес-перевірка контрагентів, збір інформації — оцінка ризиків — '
        'рекомендації для бізнесу'
    )
    dirty = False
    for name, value in scalar.items():
        dirty |= adopt(
            page, name, value,
            short_rec, short_result, short_order, hero_seed,
            'Власний сервіс швидкої перевірки контрагентів',
            'Що перевіряє VI ANALYSIS',
            'Рекомендація щодо співпраці',
            'Що отримує замовник',
            'Пакетне обслуговування',
            'для постійних клієнтів',
            'Що входить до пакета',
            'Чому це вигідно',
            'Скільки це коштує',
            'Перевірте контрагента до підписання договору',
        )
    _save(page, dirty)
    if not page.risk_levels.exists():
        for i, row in enumerate(data['risk_levels']):
            AnalysisRiskLevel.objects.create(page=page, order=i, **row)
    if not page.recs.exists():
        for i, row in enumerate(data['recs']):
            AnalysisRec.objects.create(page=page, order=i, **row)
    if not page.paket_steps.exists():
        for i, row in enumerate(data['paket_steps']):
            AnalysisPaketStep.objects.create(
                page=page, number=row['num'], title=row['title'], text=row['text'], order=i,
            )
    if not page.price_parts.exists():
        for i, row in enumerate(data['price_parts']):
            AnalysisPricePart.objects.create(
                page=page, number=row['num'], title=row['title'], when=row['when'],
                text=row['text'], price=row['price'], order=i,
            )
    if not page.tariffs.exists():
        for i, row in enumerate(data['tariffs']):
            tariff = AnalysisTariff.objects.create(
                page=page, name=row['name'], subtitle=row['sub'], featured=row['featured'],
                price=row['price'], period=row['period'], order=i,
            )
            for n, line in enumerate(row['rows']):
                AnalysisTariffLine.objects.create(
                    tariff=tariff, label=line['k'], value=line['v'], order=n,
                )
    if not page.pay_terms.exists():
        for i, row in enumerate(data['pay_terms']):
            AnalysisPayTerm.objects.create(page=page, title=row['title'], text=row['text'], order=i)
    risk_seed = {
        'Правові та регуляторні ризики': 'Кримінальні провадження, санкції та виконавчі провадження.',
        'Фінансово-господарські ризики': 'Боргові зобовʼязання, фінансова звітність, ознаки обігу нелегальної продукції.',
        'Репутаційні та інші ризики': 'Публікації у ЗМІ, відкриті джерела й додаткові сигнали.',
    }
    by_title = {row['title']: row for row in data['risk_types']}
    if not page.risks.exists():
        for i, row in enumerate(data['risk_types']):
            AnalysisRisk.objects.create(
                page=page, tag=row['tag'], title=row['title'], text=row['text'], order=i,
            )
    else:
        for risk in page.risks.all():
            source = by_title.get(risk.title)
            if source is None:
                continue
            changed = []
            if not risk.tag:
                risk.tag = source['tag']
                changed.append('tag')
            if risk.text in ('', risk_seed.get(risk.title, '')):
                risk.text = source['text']
                changed.append('text')
            if changed:
                risk.save(update_fields=changed)
    _refresh_titled(page.includes, data['includes'], AnalysisInclude, page, _INCLUDE_SEED)
    _refresh_why(page, data['why_items'])


_INCLUDE_SEED = {
    'Доброчесність і відносини з владою': 'Кримінальні та виконавчі провадження, санкції, інші «червоні прапорці».',
    'Фінансовий стан та історія звʼязків': 'Борги, звітність, звʼязки зараз і раніше.',
    'Явні та приховані ризики': 'У тому числі успадковані від повʼязаних осіб і компаній.',
    'Реальні власники та бізнес-групи': 'Групування контрагентів в офіційні та фактичні бізнес-групи.',
    'Рекомендації щодо співпраці': 'Стандартні умови, додаткові умови або відмова.',
    'Постійний моніторинг реєстрів': 'Повідомлення про суттєві події.',
}
_WHY_SEED = {
    'Конфіденційність — з першого кроку': 'NDA підписуємо до укладення основної угоди.',
    'Без власного штату перевіряльників': 'Ви платите лише за результат.',
    'Відповідь за хвилини, а не за години': 'Перевірки виконуються в VI Analysis.',
    'Ваші люди на прямому звʼязку': 'Контактні особи отримують інформацію онлайн.',
}


def _refresh_titled(qs, rows, model, page, legacy):
    if not qs.exists():
        for i, row in enumerate(rows):
            model.objects.create(page=page, title=row['title'], text=row['text'], order=i)
        return
    full = {row['title']: row['text'] for row in rows}
    for item in qs.all():
        if item.title in full and item.text in ('', legacy.get(item.title, '')):
            item.text = full[item.title]
            item.save(update_fields=['text'])


def _refresh_why(page, rows):
    if not page.why_items.exists():
        for i, row in enumerate(rows):
            AnalysisWhy.objects.create(
                page=page, number=row['num'], title=row['title'], text=row['text'], order=i,
            )
        return
    full = {row['title']: row['text'] for row in rows}
    for item in page.why_items.all():
        if item.title in full and item.text in ('', _WHY_SEED.get(item.title, '')):
            item.text = full[item.title]
            item.save(update_fields=['text'])


def sync_all() -> None:
    from src.blog.models import BlogPage
    from src.leads.models import LeadModal
    from src.pages.models import AboutPage, ContactsPage, PrivacyPage, ServicesIndex

    sync_home()
    sync_services()
    sync_deep()
    sync_analysis()
    BlogPage.load()
    LeadModal.load()
    AboutPage.load()
    ContactsPage.load()
    PrivacyPage.load()
    ServicesIndex.load()
