"""System files for crawlers: robots.txt and llms.txt."""

from __future__ import annotations

from django.http import HttpResponse
from django.urls import reverse
from django.views import View

from src.core.seo import absolute_url, get_public_origin, seo_indexing_allowed
from src.pages.models import ServicePage
from src.pages.services import service_nav_items


class RobotsTxtView(View):
    def get(self, request, *args, **kwargs):
        origin = get_public_origin(request)
        sitemap_url = f'{origin}{reverse("sitemap")}'
        lines: list[str] = [
            '# VARTIS INTELLIGENCE',
            f'# Host: {origin}',
            '',
        ]

        if not seo_indexing_allowed(request):
            lines.extend(
                [
                    'User-agent: *',
                    'Disallow: /',
                    '',
                    '# Staging/preview: повна заборона індексації.',
                    '# На проді встановіть PUBLIC_SITE_URL і SEO_ALLOW_INDEXING=True.',
                    '',
                    f'Sitemap: {sitemap_url}',
                    '',
                ]
            )
            return HttpResponse('\n'.join(lines), content_type='text/plain; charset=utf-8')

        lines.extend(
            [
                'User-agent: *',
                'Allow: /',
                'Disallow: /admin/',
                'Disallow: /leads/',
                '',
                'User-agent: GPTBot',
                'Allow: /',
                'Disallow: /admin/',
                'Disallow: /leads/',
                '',
                'User-agent: ChatGPT-User',
                'Allow: /',
                'Disallow: /admin/',
                'Disallow: /leads/',
                '',
                'User-agent: Google-Extended',
                'Allow: /',
                'Disallow: /admin/',
                'Disallow: /leads/',
                '',
                'User-agent: anthropic-ai',
                'Allow: /',
                'Disallow: /admin/',
                'Disallow: /leads/',
                '',
                'User-agent: ClaudeBot',
                'Allow: /',
                'Disallow: /admin/',
                'Disallow: /leads/',
                '',
                'User-agent: PerplexityBot',
                'Allow: /',
                'Disallow: /admin/',
                'Disallow: /leads/',
                '',
                f'Sitemap: {sitemap_url}',
                '',
            ]
        )
        return HttpResponse('\n'.join(lines), content_type='text/plain; charset=utf-8')


class LlmsTxtView(View):
    """llms.txt — AI-ready site map for LLM crawlers (https://llmstxt.org/)."""

    def get(self, request, *args, **kwargs):
        origin = get_public_origin(request)

        def u(name, **kw):
            path = reverse(name, kwargs=kw) if kw else reverse(name)
            return absolute_url(request, path)

        services_lines = []
        try:
            for item in service_nav_items():
                href = item.get('href') or ''
                title = item.get('title') or ''
                short = item.get('short') or item.get('card_text') or ''
                if href:
                    line = f'- [{title}]({absolute_url(request, href)})'
                    if short:
                        line = f'{line}: {short}'
                    services_lines.append(line)
        except Exception:
            for page in ServicePage.objects.filter(is_published=True).order_by('order', 'id'):
                path = reverse('pages:service_detail', kwargs={'slug': page.slug})
                desc = (page.seo_description or page.card_text or '')[:160]
                line = f'- [{page.title}]({absolute_url(request, path)})'
                if desc:
                    line = f'{line}: {desc}'
                services_lines.append(line)

        body = f"""# VARTIS INTELLIGENCE

> Стратегічна аналітика, перевірка контрагентів (VI Analysis), OSINT, корпоративна безпека
> та аналіз ризиків для бізнесу в Україні. Допомагаємо виявляти приховані загрози
> й ухвалювати обґрунтовані рішення на основі перевіреної інформації.

Site: {origin}/
Language: uk-UA
Contact: {u('pages:contacts')}

## Головні сторінки

- [Головна]({u('pages:home')}): огляд компанії, напрямів роботи та процесу досліджень
- [Про компанію]({u('pages:about')}): історія, принципи, команда, методологія
- [Послуги]({u('pages:services')}): каталог послуг Vartis Intelligence
- [VI Analysis]({u('pages:analysis')}): експрес-перевірка контрагентів за ЄДРПОУ
- [Блог]({u('blog:list')}): аналітика та експертні матеріали
- [Кейси]({u('cases:list')}): приклади реалізованих проєктів
- [Контакти]({u('pages:contacts')}): звʼязок і форма заявки
- [Політика конфіденційності]({u('pages:privacy')}): обробка персональних даних

## Послуги

{chr(10).join(services_lines) if services_lines else '- Каталог послуг доступний на /posluhy/'}

## Пріоритет для сканування

1. Головна, Послуги, VI Analysis, Глибока аналітика
2. Про компанію, Контакти
3. Блог і кейси (опубліковані матеріали)
4. Sitemap: {origin}{reverse('sitemap')}

## Обмеження

- Не індексувати /admin/ та /leads/
- Staging/preview (*.vercel.app) — noindex до продакшену
- Канонічний домен задається через PUBLIC_SITE_URL

## Optional

- [robots.txt]({origin}/robots.txt)
- [sitemap.xml]({origin}{reverse('sitemap')})
"""
        return HttpResponse(body, content_type='text/plain; charset=utf-8')
