"""Реєстрація proxy-секцій: поля моделі, вкладки Контент і SEO."""

from django.contrib import admin
from django.templatetags.static import static
from django.db import models
from django.shortcuts import redirect
from django.urls import reverse
from unfold.admin import ModelAdmin

from src.core import cms_proxies
from src.core.admin_site_content_widgets import (
    CmsAdminColorWidget,
    CmsAdminIconWidget,
    CmsAdminImageWidget,
    CmsTinyMCEWidget,
)
from src.core.admin_hero_chrome import HERO_PAGE, HeroChromeAdminMixin
from src.core.admin_i18n import expand_fieldsets
from src.core.models_cms import PageStyle

_SEO = ("seo_title", "seo_description", "h1")

_SPECS = (
    (cms_proxies.HomeHeroSettings, "Перший екран", ("hero_title", "hero_text", "hero_cta", "hero_image"), True),
    (cms_proxies.HomeServicesSettings, "Напрями", ("services_title", "services_lead"), False),
    (cms_proxies.HomeAdvantagesSettings, "Переваги", ("advantages_title", "advantages_lead"), False),
    (cms_proxies.HomeMissionSettings, "Місія", ("mission_title", "mission_text", "mission_image"), False),
    (cms_proxies.HomeProcessSettings, "Процес", ("process_title", "process_lead"), False),
    (cms_proxies.HomeBlogSettings, "Блог на головній", ("blog_title", "blog_lead", "blog_all_label"), False),
    (
        cms_proxies.SiteHeaderSettings,
        "Шапка",
        (
            "nav_about", "nav_services", "nav_blog", "nav_contacts",
            "header_cta", "mobile_lead", "mobile_cta_secondary",
        ),
        False,
    ),
    (
        cms_proxies.SiteFooterSettings,
        "Підвал",
        (
            "footer_cta_title", "footer_cta_text",
            "footer_col_company", "footer_col_services",
            "footer_phone_label", "footer_email_label", "footer_address_label",
            "footer_whatsapp_label", "footer_signal_label", "footer_telegram_label",
            "footer_write_label", "privacy_link_label",
        ),
        False,
    ),
    (
        cms_proxies.AboutHeroSettings,
        "Перший екран",
        (
            "hero_title", "hero_text", "hero_cta", "hero_cta_secondary",
            "hero_cta_secondary_href", "hero_image",
        ),
        True,
    ),
    (cms_proxies.AboutIntroSettings, "Про нас", ("intro_title", "intro_text"), False),
    (cms_proxies.AboutPrinciplesSettings, "Принципи", ("principles_title",), False),
    (
        cms_proxies.AboutTeamSettings,
        "Команда",
        ("team_title", "team_lead", "expertise_label", "career_label"),
        False,
    ),
    (
        cms_proxies.AboutScienceSettings,
        "Наука",
        ("science_eyebrow", "science_title", "science_text", "science_doi_url", "science_doi_label"),
        False,
    ),
    (
        cms_proxies.AboutPartnersSettings,
        "Партнери",
        ("partners_eyebrow", "partners_title", "partners_text"),
        False,
    ),
    (cms_proxies.AboutStatsSettings, "Цифри", ("stats_title",), False),
    (cms_proxies.AboutProcessSettings, "Процес", ("process_title",), False),
    (
        cms_proxies.ServicesHeroSettings,
        "Перший екран",
        ("hero_title", "hero_text", "hero_image", "cta_primary", "cta_secondary", "card_more_label"),
        True,
    ),
    (
        cms_proxies.AnalysisHeroSettings,
        "Перший екран",
        (
            "hero_title", "hero_text", "hero_image",
            "cta_primary", "cta_secondary", "cta_secondary_href",
        ),
        True,
    ),
    (
        cms_proxies.AnalysisStepsSettings,
        "Кроки",
        ("steps_eyebrow", "steps_title", "steps_leads"),
        False,
    ),
    (
        cms_proxies.AnalysisRisksSettings,
        "Ризики",
        ("risks_title", "risks_lead", "risks_note_title", "risks_note"),
        False,
    ),
    (
        cms_proxies.AnalysisRecommendationSettings,
        "Рекомендація",
        (
            "recommendation_title", "recommendation_text",
            "rec_heading", "rec_badge", "rec_code", "rec_verdict", "rec_note",
            "rec_flag", "rec_accept", "rec_reject", "rec_date", "rec_caption",
        ),
        False,
    ),
    (
        cms_proxies.AnalysisResultSettings,
        "Результат",
        (
            "result_title", "result_text", "result_method_prefix", "result_method_suffix",
            "result_doi_href", "result_doi_label",
        ),
        False,
    ),
    (
        cms_proxies.AnalysisPaketSettings,
        "Пакет",
        ("paket_eyebrow", "paket_title", "paket_subtitle", "paket_lead", "paket_text"),
        False,
    ),
    (
        cms_proxies.AnalysisIncludeSettings,
        "Що входить",
        ("include_title", "include_lead", "include_option_eyebrow", "include_option_title", "include_option_text"),
        False,
    ),
    (cms_proxies.AnalysisWhySettings, "Чому вигідно", ("why_title",), False),
    (
        cms_proxies.AnalysisPriceSettings,
        "Вартість",
        ("price_title", "price_lead", "tariffs_title", "price_note"),
        False,
    ),
    (cms_proxies.AnalysisOrderSettings, "Заявка", ("order_title", "order_text", "related_title"), False),
    (
        cms_proxies.ContactsHeroSettings,
        "Перший екран",
        (
            "hero_title", "hero_text", "hero_image", "cta_primary", "cta_secondary",
            "info_title", "phone_label", "email_label", "facebook_label",
            "whatsapp_label", "signal_label", "telegram_label",
            "phone_hint", "email_hint", "whatsapp_hint", "signal_hint", "telegram_hint",
            "write_label", "office_label", "office_note", "office_cta",
        ),
        True,
    ),
    (cms_proxies.PrivacyHeroSettings, "Перший екран", ("hero_title", "hero_text", "body"), True),
)

_IMAGE_FALLBACKS = {
    ("HomeHeroSettings", "hero_image"): "images/hero.webp",
    ("HomeMissionSettings", "mission_image"): "images/about-bg.webp",
    ("AboutHeroSettings", "hero_image"): "images/about-bg.webp",
    ("ServicesHeroSettings", "hero_image"): "images/hero.webp",
    ("AnalysisHeroSettings", "hero_image"): "images/services/dir-1.webp",
    ("ContactsHeroSettings", "hero_image"): "images/hero.webp",
}

_STYLE_FIELDS = (
    "background_color", "text_color", "accent_color", "background_image",
)


class SectionAdmin(ModelAdmin):
    tab_title = "Контент"
    section_fields = ()
    with_seo = False

    class Media:
        js = ("js/admin/cms_image_preview.js", "js/admin/cms_nested_tabs.js")
        css = {"all": ("css/admin/cms_tabs.css",)}

    def get_fieldsets(self, request, obj=None):
        sets = [(
            f"{self.tab_title} — Сторінка",
            {"classes": ["tab"], "fields": self.section_fields},
        )]
        if self.with_seo:
            sets.append((
                f"{self.tab_title} — SEO",
                {"classes": ["tab"], "fields": _SEO},
            ))
        return expand_fieldsets(sets, self.model)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if isinstance(db_field, models.TextField):
            kwargs["widget"] = CmsTinyMCEWidget()
        elif isinstance(db_field, models.ImageField):
            fallback = _IMAGE_FALLBACKS.get((self.model.__name__, db_field.name), "")
            kwargs["widget"] = CmsAdminImageWidget(
                fallback_url=static(fallback) if fallback else "",
            )
        elif db_field.name == "icon":
            kwargs["widget"] = CmsAdminIconWidget()
        elif db_field.name.endswith("color"):
            defaults = {
                "background_color": PageStyle.DEFAULT_BACKGROUND,
                "text_color": PageStyle.DEFAULT_TEXT,
                "accent_color": PageStyle.DEFAULT_ACCENT,
            }
            kwargs["widget"] = CmsAdminColorWidget(
                default_color=defaults.get(db_field.name, PageStyle.DEFAULT_ACCENT),
            )
        return super().formfield_for_dbfield(db_field, request, **kwargs)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        self.model.load()
        url = reverse(
            f"admin:{self.model._meta.app_label}_{self.model._meta.model_name}_change",
            args=[1],
        )
        return redirect(url)


class HeroSectionAdmin(HeroChromeAdminMixin, SectionAdmin):
    pass


class StyleSectionAdmin(SectionAdmin):
    tab_title = "Оформлення"
    section_fields = _STYLE_FIELDS
    style_page = "home"
    exclude = (
        "glass_enabled",
        "hero_text_color",
        "hero_panel_color",
        "hero_panel_opacity",
    )

    def get_fields(self, request, obj=None):
        return list(self.section_fields)

    def get_fieldsets(self, request, obj=None):
        return [(
            "Оформлення — Кольори",
            {"classes": ["tab"], "fields": self.section_fields},
        )]

    def save_model(self, request, obj, form, change):
        obj.glass_enabled = False
        super().save_model(request, obj, form, change)

    def changelist_view(self, request, extra_context=None):
        obj = PageStyle.for_page(self.style_page)
        url = reverse(
            f"admin:{self.model._meta.app_label}_{self.model._meta.model_name}_change",
            args=[obj.pk],
        )
        return redirect(url)


def register_site_content_section_admins(site=None):
    admin_site = site or admin.site
    for model, tab, fields, seo in _SPECS:
        if admin_site.is_registered(model):
            continue
        is_hero = tab == "Перший екран" and model.__name__ in HERO_PAGE
        attrs = {"tab_title": tab, "section_fields": fields, "with_seo": seo}
        if is_hero:
            attrs["hero_page"] = HERO_PAGE[model.__name__]
        admin_site.register(model, type(
            f"{model.__name__}Admin",
            (HeroSectionAdmin if is_hero else SectionAdmin,),
            attrs,
        ))
    for name, page in cms_proxies.STYLE_PAGE.items():
        model = getattr(cms_proxies, name)
        if admin_site.is_registered(model):
            continue
        admin_site.register(model, type(
            f"{name}Admin",
            (StyleSectionAdmin,),
            {"style_page": page},
        ))
    from src.core.apps import CoreConfig
    CoreConfig._bind_translation_proxies()
