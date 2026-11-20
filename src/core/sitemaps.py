from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from src.blog.models import Article
from src.pages.models import ServicePage


class StaticSitemap(Sitemap):
    i18n = True
    alternates = True
    x_default = True
    def changefreq(self, item):
        if item[0] == 'pages:privacy':
            return 'yearly'
        return 'weekly'

    def items(self):
        # (url_name, priority) — лише сторінки з дизайн-збірки
        return [
            ('pages:home', 1.0),
            ('pages:services', 0.9),
            ('pages:analysis', 0.9),
            ('pages:about', 0.7),
            ('pages:contacts', 0.7),
            ('blog:list', 0.6),
            ('pages:privacy', 0.3),
        ]

    def location(self, item):
        return reverse(item[0])

    def priority(self, item):
        return item[1]


class ServiceSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8
    i18n = True
    alternates = True
    x_default = True

    def items(self):
        return ServicePage.objects.filter(is_published=True)

    def location(self, obj):
        from django.utils.translation import get_language

        slug = obj.slug
        if (get_language() or '').startswith('en') and obj.slug_en:
            slug = obj.slug_en
        return reverse('pages:service_detail', kwargs={'slug': slug})


class ArticleSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6
    i18n = True
    alternates = True
    x_default = True

    def items(self):
        return Article.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.published_at


sitemaps = {
    'static': StaticSitemap,
    'services': ServiceSitemap,
    'articles': ArticleSitemap,
}
