import os
import re

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, re_path

from src.core.sitemaps import sitemaps
from src.core.views_media import media_serve
from src.core.views_seo import LlmsTxtView, RobotsTxtView
from src.pages.views import page_not_found

urlpatterns = [
    path('admin/', admin.site.urls),
    path('leads/', include('src.leads.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('robots.txt', RobotsTxtView.as_view(), name='robots'),
    path('llms.txt', LlmsTxtView.as_view(), name='llms'),
]

urlpatterns += i18n_patterns(
    path('', include('src.pages.urls')),
    path('blog/', include('src.blog.urls')),
    prefix_default_language=False,
)

handler404 = page_not_found
handler500 = 'src.pages.views.server_error'

# django.conf.urls.static.static() при DEBUG=False повертає [] — тому serve напряму.
# Потрібно і локально (DEBUG), і на Vercel (media в /tmp).
if settings.DEBUG or os.environ.get('VERCEL'):
    media_url = settings.MEDIA_URL if settings.MEDIA_URL.endswith('/') else f'{settings.MEDIA_URL}/'
    urlpatterns += [
        re_path(
            r'^%s(?P<path>.*)$' % re.escape(media_url.lstrip('/')),
            media_serve,
        ),
    ]

if settings.DEBUG:
    urlpatterns += [
        path('404/', page_not_found, name='preview_404'),
    ]
