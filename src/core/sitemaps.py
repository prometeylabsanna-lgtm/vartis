from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from src.blog.models import Article
from src.cases.models import CaseStudy
from src.pages.models import ServicePage


class StaticSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return [
            'pages:home',
            'pages:about',
            'pages:services',
            'pages:analysis',
            'pages:contacts',
            'pages:privacy',
            'blog:list',
            'cases:list',
        ]

    def location(self, item):
        return reverse(item)


class ServiceSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

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
    priority = 0.6

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
