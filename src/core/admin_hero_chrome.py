"""Вкладка «Баннер» на Першому екрані. Не в Оформленні."""

from __future__ import annotations

from django import forms
from unfold.widgets import INPUT_CLASSES

from src.core.admin_site_content_widgets import CmsAdminColorWidget
from src.core.hero_chrome import DEFAULT_HERO_OPACITY, DEFAULT_HERO_PANEL, DEFAULT_HERO_TEXT
from src.core.models_cms import PageStyle

HERO_PAGE = {
    "HomeHeroSettings": "home",
    "AboutHeroSettings": "about",
    "ServicesHeroSettings": "services",
    "AnalysisHeroSettings": "analysis",
    "ContactsHeroSettings": "contacts",
    "PrivacyHeroSettings": "privacy",
}

HERO_CHROME_FIELDS = ("hero_text_color", "hero_panel_color", "hero_panel_opacity")

_OPACITY_CLASS = " ".join([*INPUT_CLASSES, "cms-hero-opacity"])


class HeroChromeAdminMixin:
    hero_page = ""

    def get_form(self, request, obj=None, **kwargs):
        fields = kwargs.get("fields")
        if fields:
            kwargs["fields"] = [name for name in fields if name not in HERO_CHROME_FIELDS]
        base = super().get_form(request, obj, **kwargs)
        page_key = self.hero_page
        if not page_key:
            return base

        class HeroChromeForm(base):
            hero_text_color = forms.CharField(
                required=False,
                label="Колір тексту на баннері",
                help_text="Лише банер. Не змінює текст сторінки нижче.",
                widget=CmsAdminColorWidget(default_color=DEFAULT_HERO_TEXT),
            )
            hero_panel_color = forms.CharField(
                required=False,
                label="Колір скла баннера",
                help_text="Відтінок напівпрозорої панелі на фото.",
                widget=CmsAdminColorWidget(default_color=DEFAULT_HERO_PANEL),
            )
            hero_panel_opacity = forms.IntegerField(
                required=False,
                min_value=0,
                max_value=100,
                label="Щільність скла, %",
                help_text="10 — як у макеті. 80+ майже непрозора панель.",
                widget=forms.NumberInput(
                    attrs={
                        "class": _OPACITY_CLASS,
                        "min": 0,
                        "max": 100,
                        "step": 1,
                        "inputmode": "numeric",
                    },
                ),
            )

            def __init__(self, *args, **kw):
                super().__init__(*args, **kw)
                style = PageStyle.for_page(page_key)
                self.fields["hero_text_color"].initial = style.effective_hero_text
                self.fields["hero_panel_color"].initial = style.effective_hero_panel
                self.fields["hero_panel_opacity"].initial = style.effective_hero_opacity

        return HeroChromeForm

    def get_fieldsets(self, request, obj=None):
        sets = list(super().get_fieldsets(request, obj) or [])
        if not self.hero_page:
            return sets
        banner = (
            f"{self.tab_title} — Баннер",
            {"classes": ["tab"], "fields": HERO_CHROME_FIELDS},
        )
        if len(sets) > 1:
            sets.insert(1, banner)
        else:
            sets.append(banner)
        return sets

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not self.hero_page:
            return
        style = PageStyle.for_page(self.hero_page)
        style.hero_text_color = (form.cleaned_data.get("hero_text_color") or "").strip()
        style.hero_panel_color = (form.cleaned_data.get("hero_panel_color") or "").strip()
        opacity = form.cleaned_data.get("hero_panel_opacity")
        style.hero_panel_opacity = (
            DEFAULT_HERO_OPACITY if opacity is None else opacity
        )
        style.save(update_fields=[
            "hero_text_color", "hero_panel_color", "hero_panel_opacity",
        ])
