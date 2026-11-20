"""Збирає словники, які вже очікують шаблони, з моделей."""

from __future__ import annotations

from src.pages.models_deep import DeepSnippet


def home_copy(page) -> dict:
    return {
        'h1': page.h1 or page.hero_title,
        'hero_text': page.hero_text,
        'hero_cta': page.hero_cta,
        'services_title': page.services_title,
        'services_lead': page.services_lead,
        'advantages_title': page.advantages_title,
        'advantages_lead': page.advantages_lead,
        'mission_title': page.mission_title,
        'mission_text': page.mission_text,
        'process_title': page.process_title,
        'process_lead': page.process_lead,
        'blog_title': page.blog_title,
        'blog_lead': page.blog_lead,
        'blog_all_label': page.blog_all_label,
    }


def home_advantages(page):
    return [
        {'icon': item.icon, 'title': item.title, 'text': item.text}
        for item in page.advantages.all()
    ]


def home_steps(page):
    return [
        {'num': item.number, 'title': item.title, 'text': item.text}
        for item in page.process_steps.all()
    ]


def _local_href(href: str) -> str:
    from src.core.i18n_urls import localize_internal_path

    return localize_internal_path(href or '#')


def home_directions(page):
    from src.core.public_images import public_image_url

    items = []
    for item in page.directions.filter(is_visible=True):
        items.append({
            'title': item.title,
            'card_text': item.text,
            'href': _local_href(item.href),
            'card_image_url': public_image_url(item.image),
        })
    return items


def service_copy(page) -> dict:
    paragraphs = [item.text for item in page.scope_paragraphs.all()]
    if not paragraphs and page.scope_text:
        paragraphs = [page.scope_text]
    return {
        'h1': page.h1 or page.title,
        'hero_text': page.hero_text,
        'cta_primary': page.cta_primary,
        'cta_secondary': page.cta_secondary,
        'cta_secondary_href': page.cta_secondary_href or '#method',
        'scope_title': page.scope_title,
        'scope_variant': page.scope_variant,
        'scope_feature_title': page.scope_feature_title,
        'scope_feature_text': page.scope_feature_text,
        'scope_paragraphs': paragraphs,
        'scope_items': [item.text for item in page.scope_items.all()],
        'method_title': page.method_title,
        'method_lead': page.method_lead,
        'method_variant': page.method_variant,
        'method_step_prefix': page.method_step_prefix,
        'steps': [(item.number, item.title, item.text) for item in page.method_steps.all()],
        'advantages_title': page.advantages_title,
        'advantages_lead': page.advantages_lead,
        'advantages_dark': page.advantages_dark,
        'advantages': [
            (item.icon or 'HiconOutlineShieldTick', item.title, item.text)
            for item in page.advantages.all()
        ],
        'order_title': page.order_title,
        'order_text': page.order_text,
        'order_variant': page.order_variant,
        'related_title': page.related_title,
    }


def _snippets(deep, kind):
    return list(deep.snippets.filter(kind=kind).order_by('order', 'id'))


def deep_copy(deep) -> dict:
    stats = [(item.value, item.text) for item in _snippets(deep, DeepSnippet.Kind.STAT)]
    return {
        'h1': deep.h1,
        'hero_text': deep.hero_text,
        'cta_primary': deep.cta_primary,
        'cta_secondary': deep.cta_secondary,
        'cta_secondary_href': deep.cta_secondary_href,
        'strategy_eyebrow': deep.strategy_eyebrow,
        'strategy_title': deep.strategy_title,
        'strategy_paragraphs': [item.text for item in _snippets(deep, DeepSnippet.Kind.STRATEGY)],
        'compare_express': {
            'eyebrow': deep.compare_express_eyebrow,
            'title': deep.compare_express_title,
            'text': deep.compare_express_text,
            'link': deep.compare_express_link,
        },
        'compare_deep': {
            'eyebrow': deep.compare_deep_eyebrow,
            'title': deep.compare_deep_title,
            'text': deep.compare_deep_text,
        },
        'steps': [(item.number, item.title, item.text) for item in deep.steps.all()],
        'nda_title': deep.nda_title,
        'nda_text': deep.nda_text,
        'nda_note': deep.nda_note,
        'get_title': deep.get_title,
        'get_lead': deep.get_lead,
        'get_items': [(item.number, item.title, item.text) for item in deep.get_items.all()],
        'example_title': deep.example_title,
        'example_lead': deep.example_lead,
        'ex_frag1': deep.ex_frag1,
        'ex_stats': stats,
        'ex_notes': [item.text for item in _snippets(deep, DeepSnippet.Kind.NOTE)],
        'ex_frag3': deep.ex_frag3,
        'ex_frag3_lead': deep.ex_frag3_lead,
        'ex_facts': [item.text for item in _snippets(deep, DeepSnippet.Kind.FACT)],
        'facts_title': deep.facts_title,
        'conclusion_title': deep.conclusion_title,
        'assumption_label': deep.assumption_label,
        'why_not_label': deep.why_not_label,
        'ex_assumption': deep.ex_assumption,
        'ex_why_not': deep.ex_why_not,
        'ex_frag4': deep.ex_frag4,
        'ex_frag4_lead': deep.ex_frag4_lead,
        'ex_limits': [item.text for item in _snippets(deep, DeepSnippet.Kind.LIMIT)],
        'pay_title': deep.pay_title,
        'pay_lead': deep.pay_lead,
        'pay_stages': [
            {
                'pct': item.pct,
                'when': item.when,
                'paid': item.paid,
                'stage': item.stage,
                'title': item.title,
                'text': item.text,
                'see': item.see,
            }
            for item in deep.pay_stages.all()
        ],
        'paid_label': deep.paid_label,
        'before_pay_label': deep.before_pay_label,
        'guarantee_title': deep.guarantee_title,
        'pay_guar': [item.text for item in _snippets(deep, DeepSnippet.Kind.GUARANTEE)],
        'quality_title': deep.quality_title,
        'quality': [(item.title, item.text) for item in deep.quality_items.all()],
        'faq_title': deep.faq_title,
        'faqs': [(item.question, item.answer) for item in deep.faqs.all()],
        'order_title': deep.order_title,
        'order_text': deep.order_text,
        'related_title': deep.related_title,
    }


def analysis_copy(page) -> dict:
    return {
        'h1': page.h1 or page.hero_title,
        'hero_text': page.hero_text,
        'cta_primary': page.cta_primary,
        'cta_secondary': page.cta_secondary,
        'cta_secondary_href': page.cta_secondary_href,
        'crumb': page.title or page.h1 or 'VI Analysis',
        'steps_eyebrow': page.steps_eyebrow,
        'steps_leads': page.steps_lead_list(),
        'risks_title': page.risks_title,
        'risks_lead': page.risks_lead,
        'risk_types': [
            {'tag': item.tag, 'title': item.title, 'text': item.text}
            for item in page.risks.all()
        ],
        'risk_levels': [
            {'level': item.level, 'tone': item.tone, 'meaning': item.meaning, 'action': item.action}
            for item in page.risk_levels.all()
        ],
        'risks_note_title': page.risks_note_title,
        'risks_note': page.risks_note,
        'recommendation_title': page.recommendation_title,
        'recommendation_text': page.recommendation_text,
        'recs': [
            {'title': item.title, 'tone': item.tone, 'text': item.text}
            for item in page.recs.all()
        ],
        'rec_example': {
            'heading': page.rec_heading,
            'badge': page.rec_badge,
            'code': page.rec_code,
            'verdict': page.rec_verdict,
            'note': page.rec_note,
            'flag': page.rec_flag,
            'accept': page.rec_accept,
            'reject': page.rec_reject,
            'date': page.rec_date,
            'caption': page.rec_caption,
        },
        'result_title': page.result_title,
        'result_text': page.result_text,
        'result_method_prefix': page.result_method_prefix,
        'result_method_suffix': page.result_method_suffix,
        'result_doi_href': page.result_doi_href,
        'result_doi_label': page.result_doi_label,
        'paket_eyebrow': page.paket_eyebrow,
        'paket_title': page.paket_title,
        'paket_lead': page.paket_lead,
        'paket_steps': [
            {'num': item.number, 'title': item.title, 'text': item.text}
            for item in page.paket_steps.all()
        ],
        'include_title': page.include_title,
        'include_lead': page.include_lead,
        'includes': [
            {'title': item.title, 'text': item.text}
            for item in page.includes.all()
        ],
        'include_option_eyebrow': page.include_option_eyebrow,
        'include_option_title': page.include_option_title,
        'include_option_text': page.include_option_text,
        'why_title': page.why_title,
        'why_items': [
            {'num': item.number, 'title': item.title, 'text': item.text}
            for item in page.why_items.all()
        ],
        'price_title': page.price_title,
        'price_lead': page.price_lead,
        'price_parts': [
            {
                'num': item.number,
                'title': item.title,
                'when': item.when,
                'text': item.text,
                'price': item.price,
            }
            for item in page.price_parts.all()
        ],
        'tariffs_title': page.tariffs_title,
        'tariffs': [
            {
                'name': item.name,
                'sub': item.subtitle,
                'featured': item.featured,
                'price': item.price,
                'period': item.period,
                'rows': [{'k': line.label, 'v': line.value} for line in item.lines.all()],
            }
            for item in page.tariffs.all()
        ],
        'pay_terms': [
            {'title': item.title, 'text': item.text}
            for item in page.pay_terms.all()
        ],
        'price_note': page.price_note,
        'order_title': page.order_title,
        'order_text': page.order_text,
        'related_title': page.related_title,
    }
