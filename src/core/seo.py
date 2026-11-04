"""SEO helpers: canonical URLs, indexing policy, JSON-LD."""

from __future__ import annotations

import json
from typing import Any
from urllib.parse import urljoin

from django.conf import settings
from django.utils.safestring import mark_safe

STAGING_HOST_MARKERS = ('vercel.app', 'localhost', '127.0.0.1')


def get_public_origin(request) -> str:
    configured = (getattr(settings, 'PUBLIC_SITE_URL', '') or '').rstrip('/')
    if configured:
        return configured
    host = request.get_host()
    forwarded = (request.META.get('HTTP_X_FORWARDED_PROTO') or '').split(',')[0].strip()
    if request.is_secure() or forwarded == 'https' or 'vercel.app' in host.lower():
        scheme = 'https'
    else:
        scheme = request.scheme or 'http'
    return f'{scheme}://{host}'.rstrip('/')


def absolute_url(request, path: str | None = None) -> str:
    origin = get_public_origin(request)
    if path is None:
        path = request.path or '/'
    path = path.split('?', 1)[0]
    if not path.startswith('/'):
        path = f'/{path}'
    return f'{origin}{path}'


def media_or_static_absolute(request, url: str | None) -> str:
    if not url:
        return ''
    if url.startswith('http://') or url.startswith('https://'):
        return url
    return urljoin(get_public_origin(request) + '/', url.lstrip('/'))


def seo_indexing_allowed(request) -> bool:
    """Staging/preview hosts stay noindex until PUBLIC_SITE_URL + SEO_ALLOW_INDEXING."""
    flag = getattr(settings, 'SEO_ALLOW_INDEXING', None)
    if flag is not None:
        return bool(flag)
    host = request.get_host().split(':')[0].lower()
    return not any(marker in host for marker in STAGING_HOST_MARKERS)


def robots_meta_content(request) -> str:
    if seo_indexing_allowed(request):
        return 'index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1'
    return 'noindex, nofollow'


def json_ld_script(data: dict[str, Any] | list[Any]) -> str:
    payload = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    return mark_safe(payload)


def organization_schema(request, site_settings) -> dict[str, Any]:
    origin = get_public_origin(request)
    logo = ''
    if site_settings and getattr(site_settings, 'logo', None) and site_settings.logo:
        logo = media_or_static_absolute(request, site_settings.logo.url)
    else:
        logo = media_or_static_absolute(request, f"{settings.STATIC_URL}images/logo-sm.webp")

    data: dict[str, Any] = {
        '@context': 'https://schema.org',
        '@type': 'ProfessionalService',
        'name': (site_settings.company_name if site_settings else None) or 'VARTIS INTELLIGENCE',
        'alternateName': 'Vartis Intelligence',
        'url': origin + '/',
        'description': (
            (site_settings.tagline if site_settings else None)
            or 'Стратегічна аналітика, OSINT, корпоративна безпека та аналіз ризиків'
        ),
        'logo': {
            '@type': 'ImageObject',
            'url': logo,
        },
        'image': media_or_static_absolute(request, f"{settings.STATIC_URL}images/og-default.webp"),
        'areaServed': {
            '@type': 'Country',
            'name': 'UA',
        },
        'knowsLanguage': ['uk', 'en'],
        'priceRange': '$$',
    }
    from src.core.contact_defaults import resolve_public_contacts

    contacts = resolve_public_contacts(site_settings)
    data['telephone'] = contacts['phone']
    data['email'] = contacts['email']
    data['address'] = {
        '@type': 'PostalAddress',
        'streetAddress': contacts['address'],
        'addressLocality': 'Київ',
        'addressCountry': 'UA',
    }
    data['sameAs'] = [contacts['facebook_url']]
    return data


def website_schema(request) -> dict[str, Any]:
    return {
        '@context': 'https://schema.org',
        '@type': 'WebSite',
        'name': 'VARTIS INTELLIGENCE',
        'url': get_public_origin(request) + '/',
        'inLanguage': 'uk-UA',
    }


def breadcrumb_schema(request, crumbs: list[dict[str, str]] | None) -> dict[str, Any] | None:
    if not crumbs:
        return None
    items = [
        {
            '@type': 'ListItem',
            'position': 1,
            'name': 'Головна',
            'item': absolute_url(request, '/'),
        }
    ]
    for index, crumb in enumerate(crumbs, start=2):
        entry: dict[str, Any] = {
            '@type': 'ListItem',
            'position': index,
            'name': crumb.get('label') or '',
        }
        url = crumb.get('url') or ''
        if url:
            entry['item'] = absolute_url(request, url)
        items.append(entry)
    return {
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        'itemListElement': items,
    }


def article_schema(request, article, site_settings) -> dict[str, Any]:
    origin = get_public_origin(request)
    image = ''
    if getattr(article, 'image', None) and article.image:
        image = media_or_static_absolute(request, article.image.url)
    publisher_logo = media_or_static_absolute(request, f"{settings.STATIC_URL}images/logo-sm.webp")
    if site_settings and getattr(site_settings, 'logo', None) and site_settings.logo:
        publisher_logo = media_or_static_absolute(request, site_settings.logo.url)

    data: dict[str, Any] = {
        '@context': 'https://schema.org',
        '@type': 'Article',
        'headline': article.title,
        'description': (article.seo_description or article.excerpt or '')[:300],
        'datePublished': article.published_at.isoformat(),
        'dateModified': article.updated_at.date().isoformat(),
        'inLanguage': 'uk-UA',
        'mainEntityOfPage': {
            '@type': 'WebPage',
            '@id': absolute_url(request, article.get_absolute_url()),
        },
        'author': {
            '@type': 'Organization',
            'name': (site_settings.company_name if site_settings else None) or 'VARTIS INTELLIGENCE',
            'url': origin + '/',
        },
        'publisher': {
            '@type': 'Organization',
            'name': 'VARTIS INTELLIGENCE',
            'logo': {
                '@type': 'ImageObject',
                'url': publisher_logo,
            },
        },
    }
    if image:
        data['image'] = [image]
    return data


def service_schema(request, page, path: str | None = None) -> dict[str, Any]:
    from django.urls import reverse

    if path:
        service_path = path
    else:
        service_path = reverse('pages:service_detail', kwargs={'slug': page.slug})

    name = getattr(page, 'title', None) or getattr(page, 'h1', None) or 'Послуга'
    description = (
        getattr(page, 'seo_description', None)
        or getattr(page, 'hero_text', None)
        or getattr(page, 'card_text', None)
        or ''
    )[:300]
    data: dict[str, Any] = {
        '@context': 'https://schema.org',
        '@type': 'Service',
        'name': name,
        'description': description,
        'url': absolute_url(request, service_path),
        'provider': {
            '@type': 'Organization',
            'name': 'VARTIS INTELLIGENCE',
            'url': get_public_origin(request) + '/',
        },
        'areaServed': {
            '@type': 'Country',
            'name': 'UA',
        },
        'serviceType': name,
    }
    hero = getattr(page, 'hero_image', None)
    if hero:
        data['image'] = media_or_static_absolute(request, hero.url)
    return data


def faq_schema(faqs: list[tuple[str, str]] | None) -> dict[str, Any] | None:
    if not faqs:
        return None
    return {
        '@context': 'https://schema.org',
        '@type': 'FAQPage',
        'mainEntity': [
            {
                '@type': 'Question',
                'name': question,
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': answer,
                },
            }
            for question, answer in faqs
        ],
    }


def person_schema(request, member, organization_name: str = 'VARTIS INTELLIGENCE') -> dict[str, Any]:
    data: dict[str, Any] = {
        '@context': 'https://schema.org',
        '@type': 'Person',
        'name': member.name,
        'jobTitle': member.role,
        'worksFor': {
            '@type': 'Organization',
            'name': organization_name,
            'url': get_public_origin(request) + '/',
        },
    }
    if member.bio:
        data['description'] = member.bio[:300]
    if member.email:
        data['email'] = member.email
    if getattr(member, 'photo', None) and member.photo:
        data['image'] = media_or_static_absolute(request, member.photo.url)
    return data
