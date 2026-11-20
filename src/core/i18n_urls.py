"""Англійські slug і посилання перемикача мов."""

from __future__ import annotations

from urllib.parse import parse_qsl, urlencode, urlsplit

from django.urls import Resolver404, resolve, reverse, translate_url
from django.utils.translation import get_language, override

SERVICE_SLUG_EN = {
    'konsaltynh': 'consulting',
    'kompleksna-dopomoha-biznesu': 'business-support',
    'zbir-ta-analiz-informatsii': 'deep-analytics',
    'zakhyst-vid-vytoku': 'information-leak-protection',
    'kryminalni-provadzhennia': 'criminal-proceedings-support',
}

ARTICLE_SLUG_EN = {
    'perevirka-kontrahenta': 'counterparty-check',
    'osint-dlia-biznesu': 'osint-for-business',
    'zakhyst-komertsiinoi-informatsii': 'protecting-commercial-information',
    'due-diligence': 'due-diligence',
    'pidhotovka-do-perehovoriv': 'preparing-for-negotiations',
    'sudova-istoriia-partnera': 'a-partners-litigation-history',
    'kiberryzyky': 'cyber-risks',
    'nadiinist-postachalnyka': 'supplier-reliability',
    'korporatyvna-bezpeka': 'corporate-security',
}

CATEGORY_EN = {
    'Перевірка контрагентів': 'Counterparty screening',
    'Аналітика': 'Analytics',
    'Корпоративна безпека': 'Corporate security',
    'Консалтинг': 'Consulting',
}
CATEGORY_UK = {en: uk for uk, en in CATEGORY_EN.items()}


def language_code() -> str:
    lang = (get_language() or 'uk').split('-')[0]
    return 'en' if lang == 'en' else 'uk'


def service_public_slug(page) -> str:
    if language_code() == 'en' and getattr(page, 'slug_en', None):
        return page.slug_en
    return page.slug


def article_public_slug(article) -> str:
    if language_code() == 'en' and getattr(article, 'slug_en', None):
        return article.slug_en
    return article.slug


def find_service(slug: str):
    from src.pages.models import ServicePage

    published = ServicePage.objects.filter(is_published=True)
    return published.filter(slug=slug).first() or published.filter(slug_en=slug).first()


def find_article(slug: str):
    from src.blog.models import Article

    published = Article.objects.filter(is_published=True)
    return published.filter(slug=slug).first() or published.filter(slug_en=slug).first()


def resolve_service(slug: str):
    """Повертає (сторінка, slug_для_301). slug_для_301 заповнений, якщо адреса не канонічна."""
    page = find_service(slug)
    if page is None:
        return None, None
    canonical = service_public_slug(page)
    if canonical and canonical != slug:
        return None, canonical
    return page, None


def resolve_article(slug: str):
    article = find_article(slug)
    if article is None:
        return None, None
    canonical = article_public_slug(article)
    if canonical and canonical != slug:
        return None, canonical
    return article, None


def _swap_query(query: str, lang: str) -> str:
    if not query:
        return ''
    pairs = []
    for key, value in parse_qsl(query, keep_blank_values=True):
        if key == 'cat' and value:
            if lang == 'en':
                value = CATEGORY_EN.get(value, value)
            else:
                value = CATEGORY_UK.get(value, value)
        pairs.append((key, value))
    return urlencode(pairs)


def _with_query(path: str, query: str) -> str:
    if not query:
        return path
    return f'{path}?{query}'


def language_url(request, lang: str) -> str:
    """Еквівалент поточної сторінки іншою мовою. Зберігає query, крім перекладу cat."""
    raw = request.get_full_path() if request is not None else '/'
    parts = urlsplit(raw)
    path = parts.path or '/'
    query = _swap_query(parts.query, lang)
    try:
        match = resolve(path)
    except Resolver404:
        try:
            translated = translate_url(path, lang)
        except Exception:
            translated = '/en/' if lang == 'en' else '/'
        return _with_query(translated, query)

    if match.namespace == 'pages' and match.url_name == 'service_detail':
        page = find_service(match.kwargs.get('slug', ''))
        if page is not None:
            slug = page.slug_en if lang == 'en' and page.slug_en else page.slug
            with override(lang):
                return _with_query(
                    reverse('pages:service_detail', kwargs={'slug': slug}),
                    query,
                )
    if match.namespace == 'blog' and match.url_name == 'detail':
        article = find_article(match.kwargs.get('slug', ''))
        if article is not None:
            slug = article.slug_en if lang == 'en' and article.slug_en else article.slug
            with override(lang):
                return _with_query(reverse('blog:detail', kwargs={'slug': slug}), query)
    if match.url_name == 'preview_500':
        return '/en/' if lang == 'en' else '/'

    try:
        # Мова шляху вже активна. override(lang) до translate_url збиває префікс /en/.
        translated = translate_url(path, lang)
    except Exception:
        with override(lang):
            translated = reverse('pages:home')
    return _with_query(translated, query)


def localize_internal_path(path: str) -> str:
    """Перекладає внутрішній шлях на активну мову. Якорі й зовнішні URL не чіпає."""
    if not path or path.startswith('#') or path.startswith('http://') or path.startswith('https://'):
        return path or ''
    base, _, query = path.partition('?')
    try:
        match = resolve(base)
    except Resolver404:
        with override(language_code()):
            try:
                return translate_url(base, language_code())
            except Exception:
                return path
    if match.namespace == 'pages' and match.url_name == 'service_detail':
        page = find_service(match.kwargs.get('slug', ''))
        if page is not None:
            slug = service_public_slug(page)
            translated = reverse('pages:service_detail', kwargs={'slug': slug})
            return f'{translated}?{query}' if query else translated
    if match.namespace == 'blog' and match.url_name == 'detail':
        article = find_article(match.kwargs.get('slug', ''))
        if article is not None:
            slug = article_public_slug(article)
            translated = reverse('blog:detail', kwargs={'slug': slug})
            return f'{translated}?{query}' if query else translated
    with override(language_code()):
        try:
            translated = translate_url(base, language_code())
        except Exception:
            return path
    return f'{translated}?{query}' if query else translated
