from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from src.core.sitemaps import sitemaps
from src.core.views_seo import LlmsTxtView, RobotsTxtView
from src.pages.views import page_not_found

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('src.pages.urls')),
    path('blog/', include('src.blog.urls')),
    path('keysy/', include('src.cases.urls')),
    path('leads/', include('src.leads.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('robots.txt', RobotsTxtView.as_view(), name='robots'),
    path('llms.txt', LlmsTxtView.as_view(), name='llms'),
]

handler404 = page_not_found

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path('404/', page_not_found, name='preview_404'),
    ]
