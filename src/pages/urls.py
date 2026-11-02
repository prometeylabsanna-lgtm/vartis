from django.urls import path

from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('pro-kompaniyu/', views.AboutView.as_view(), name='about'),
    path('posluhy/', views.ServicesIndexView.as_view(), name='services'),
    path('posluhy/perevirka-kontrahentiv/', views.AnalysisView.as_view(), name='analysis'),
    path('posluhy/<slug:slug>/', views.ServiceDetailView.as_view(), name='service_detail'),
    path('kontakty/', views.ContactsView.as_view(), name='contacts'),
    path('polityka-konfidentsiynosti/', views.PrivacyView.as_view(), name='privacy'),
]
