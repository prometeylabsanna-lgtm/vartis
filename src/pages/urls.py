from django.conf import settings
from django.urls import path
from django.utils.translation import gettext_lazy as _

from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path(_('pro-kompaniiu/'), views.AboutView.as_view(), name='about'),
    path(_('posluhy/'), views.ServicesIndexView.as_view(), name='services'),
    path(
        _('posluhy/perevirka-kontrahentiv/'),
        views.AnalysisView.as_view(),
        name='analysis',
    ),
    path(_('posluhy/<slug:slug>/'), views.ServiceDetailView.as_view(), name='service_detail'),
    path(_('kontakty/'), views.ContactsView.as_view(), name='contacts'),
    path(_('polityka-konfidentsiinosti/'), views.PrivacyView.as_view(), name='privacy'),
]

if settings.DEBUG:
    urlpatterns += [
        path('500/', views.server_error, name='preview_500'),
    ]
