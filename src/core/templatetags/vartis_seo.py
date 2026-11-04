from django import template
from django.utils.safestring import mark_safe

from src.core.seo import (
    article_schema,
    breadcrumb_schema,
    faq_schema,
    json_ld_script,
    media_or_static_absolute,
    person_schema,
    service_schema,
)

register = template.Library()


def _script(data):
    if not data:
        return ''
    return mark_safe(
        f'<script type="application/ld+json">{json_ld_script(data)}</script>'
    )


@register.simple_tag(takes_context=True)
def breadcrumb_json_ld(context, crumbs=None):
    request = context.get('request')
    crumbs = crumbs if crumbs is not None else context.get('crumbs')
    return _script(breadcrumb_schema(request, crumbs))


@register.simple_tag(takes_context=True)
def article_json_ld(context, article=None):
    request = context.get('request')
    article = article or context.get('article')
    if not article:
        return ''
    return _script(article_schema(request, article, context.get('site_settings')))


@register.simple_tag(takes_context=True)
def service_json_ld(context, page=None, path=None):
    request = context.get('request')
    page = page or context.get('page')
    if not page:
        return ''
    return _script(service_schema(request, page, path=path))


@register.simple_tag
def faq_json_ld(faqs):
    return _script(faq_schema(list(faqs) if faqs else None))


@register.simple_tag(takes_context=True)
def team_persons_json_ld(context, members=None):
    request = context.get('request')
    members = members if members is not None else []
    site_settings = context.get('site_settings')
    org = (site_settings.company_name if site_settings else None) or 'VARTIS INTELLIGENCE'
    scripts = []
    for member in members:
        scripts.append(_script(person_schema(request, member, org)))
    return mark_safe(''.join(scripts))


@register.simple_tag(takes_context=True)
def abs_media(context, url):
    request = context.get('request')
    return media_or_static_absolute(request, url or '')