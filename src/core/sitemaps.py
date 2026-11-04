from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from src.blog.models import Article
from src.cases.models import CaseStudy
from src.pages.models import ServicePage


class StaticSitemap(Sitemap):
    changefreq = 'weekly'

    def items(self):
        # (url_name, priority)
        return [
            ('pages:home', 1.0),
            ('pages:services', 0.9),
            ('pages:analysis', 0.9),
            ('pages:about', 0.7),
            ('pages:contacts', 0.7),
            ('blog:list', 0.6),
            ('cases:list', 0.6),
            ('pages:privacy', 0.3),
        ]

    def location(self, item):
        return reverse(item[0])

    def priority(self, item):
        return item[1]


class ServiceSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return ServicePage.objects.filter(is_published=True)

    def location(self, obj):
        return reverse('pages:service_detail', kwargs={'slug': obj.slug})


class ArticleSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        return Article.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at


class CaseSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return CaseStudy.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at


sitemaps = {
    'static': StaticSitemap,
    'services': ServiceSitemap,
    'articles': ArticleSitemap,
    'cases': CaseSitemap,
}
