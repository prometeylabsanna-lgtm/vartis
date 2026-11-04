"""Реєстрація proxy CMS-секцій у Django admin."""

from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from unfold.admin import ModelAdmin

from src.core import cms_proxies
from src.core.admin_site_content import site_content_section_view
from src.core.models import SiteSettings


class SingletonModelAdminMixin:
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = SiteSettings.load()
        return redirect(
            reverse(f"admin:{obj._meta.app_label}_{self.model._meta.model_name}_change", args=[obj.pk])
        )


_SECTION_MODELS = (
    (cms_proxies.HomeHeroSettings, "home", "hero"),
    (cms_proxies.HomeStyleSettings, "home", "style"),
    (cms_proxies.HomeServicesSettings, "home", "services"),
    (cms_proxies.HomeAdvantagesSettings, "home", "advantages"),
    (cms_proxies.HomeMissionSettings, "home", "mission"),
    (cms_proxies.HomeProcessSettings, "home", "process"),
    (cms_proxies.HomeBlogSettings, "home", "blog"),
    (cms_proxies.SiteFooterSettings, "site", "footer"),
    (cms_proxies.AboutHeroSettings, "about", "hero"),
    (cms_proxies.AboutIntroSettings, "about", "intro"),
    (cms_proxies.AboutPrinciplesSettings, "about", "principles"),
    (cms_proxies.AboutTeamSettings, "about", "team"),
    (cms_proxies.AboutScienceSettings, "about", "science"),
    (cms_proxies.AboutPartnersSettings, "about", "partners"),
    (cms_proxies.AboutStatsSettings, "about", "stats"),
    (cms_proxies.AboutProcessSettings, "about", "process"),
    (cms_proxies.ServicesHeroSettings, "services", "hero"),
    (cms_proxies.AnalysisHeroSettings, "analysis", "hero"),
    (cms_proxies.AnalysisStepsSettings, "analysis", "steps"),
    (cms_proxies.AnalysisRisksSettings, "analysis", "risks"),
    (cms_proxies.AnalysisRecommendationSettings, "analysis", "recommendation"),
    (cms_proxies.AnalysisResultSettings, "analysis", "result"),
    (cms_proxies.AnalysisPaketSettings, "analysis", "paket"),
    (cms_proxies.AnalysisIncludeSettings, "analysis", "include"),
    (cms_proxies.AnalysisWhySettings, "analysis", "why"),
    (cms_proxies.AnalysisPriceSettings, "analysis", "price"),
    (cms_proxies.AnalysisOrderSettings, "analysis", "order"),
    (cms_proxies.ContactsHeroSettings, "contacts", "hero"),
    (cms_proxies.PrivacyHeroSettings, "privacy", "hero"),
)


class SiteContentSectionAdmin(SingletonModelAdminMixin, ModelAdmin):
    page_slug: str = ""
    section_slug: str = ""

    def change_view(self, request, object_id, form_url="", extra_context=None):
        return site_content_section_view(
            request,
            self.page_slug,
            self.section_slug,
            model_admin=self,
        )


def register_site_content_section_admins(site=None):
    admin_site = site or admin.site
    for model, page_slug, section_slug in _SECTION_MODELS:
        if admin_site.is_registered(model):
            continue
        admin_class = type(
            f"{model.__name__}Admin",
            (SiteContentSectionAdmin,),
            {"page_slug": page_slug, "section_slug": section_slug},
        )
        admin_site.register(model, admin_class)
