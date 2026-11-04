from django import forms
from django.contrib import admin
from django.db import models
from unfold.admin import ModelAdmin, StackedInline
from src.core.admin_guidelines import image_profile_for_key, text_limit_for_key
from src.core.admin_site_content_widgets import (
    CmsAdminTextInputWidget,
    CmsAdminTextareaWidget,
    CmsImageFieldWidget,
    CmsTinyMCEWidget,
)

from .models import (
    AboutPage,
    AboutPrinciple,
    AboutProcessStep,
    AboutStat,
    AnalysisInclude,
    AnalysisPage,
    AnalysisPriceRow,
    AnalysisRisk,
    AnalysisStep,
    AnalysisWhy,
    HomeAdvantage,
    HomePage,
    HomeProcessStep,
    ServiceAdvantage,
    ServiceMethodStep,
    ServicePage,
    ServiceScopeItem,
    TeamMember,
)


class _ParentPageMixin:
    """Автоматично прив'язує ListItem до singleton-сторінки."""

    parent_model = None
    parent_field = 'page'

    def save_model(self, request, obj, form, change):
        if self.parent_model is not None and not getattr(obj, f'{self.parent_field}_id', None):
            setattr(obj, self.parent_field, self.parent_model.load())
        super().save_model(request, obj, form, change)

    def get_exclude(self, request, obj=None):
        excluded = list(super().get_exclude(request, obj) or [])
        if self.parent_field not in excluded:
            excluded.append(self.parent_field)
        return excluded


SERVICE_RICH_FIELDS = (
    'hero_text',
    'scope_text',
    'order_text',
    'card_text',
)

SERVICE_IMAGE_FIELDS = (
    'hero_image',
    'card_image',
)

SERVICE_TEXT_LIMITS = {
    'seo_title': 70,
    'seo_description': 160,
    'h1': 90,
    'title': 90,
    'short': 160,
    'scope_title': 80,
    'method_title': 80,
    'advantages_title': 80,
    'order_title': 80,
    'tags': 120,
    'icon': 40,
}


def _preview_url(file_field) -> str:
    if not file_field:
        return ''
    try:
        return file_field.url
    except Exception:
        return ''


class ServicePageForm(forms.ModelForm):
    class Meta:
        model = ServicePage
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        for name in SERVICE_RICH_FIELDS:
            if name not in self.fields:
                continue
            limit = text_limit_for_key(name) or text_limit_for_key(name.replace('hero_', '').replace('card_', ''))
            max_chars = limit.max_chars if limit else 900
            self.fields[name].widget = CmsTinyMCEWidget(
                attrs={'rows': 10},
                max_chars=max_chars,
                hard_limit=False,
            )
            self.fields[name].help_text = (
                f'Рекомендовано до {max_chars} символів (щоб не зламати верстку).'
            )

        for name, max_chars in SERVICE_TEXT_LIMITS.items():
            if name not in self.fields:
                continue
            field = self.fields[name]
            if isinstance(field.widget, forms.Textarea):
                field.widget = CmsAdminTextareaWidget(
                    attrs={'rows': 3},
                    max_chars=max_chars,
                    hard_limit=True,
                )
            else:
                field.widget = CmsAdminTextInputWidget(max_chars=max_chars, hard_limit=True)
            field.help_text = f'Максимум {max_chars} символів.'
            field.max_length = max_chars

        for name in SERVICE_IMAGE_FIELDS:
            if name not in self.fields:
                continue
            profile = image_profile_for_key(name)
            preview = _preview_url(getattr(instance, name, None) if instance else None)
            self.fields[name].widget = CmsImageFieldWidget(
                hint=profile.hint,
                preview_url=preview,
            )
            self.fields[name].help_text = profile.hint


class _CountableInlineForm(forms.ModelForm):
    """Inline з лімітами й лічильником для Char/Text полів."""

    text_limits: dict[str, int] = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, max_chars in self.text_limits.items():
            if name not in self.fields:
                continue
            field = self.fields[name]
            if isinstance(self._meta.model._meta.get_field(name), models.TextField):
                field.widget = CmsAdminTextareaWidget(
                    attrs={'rows': 3},
                    max_chars=max_chars,
                    hard_limit=False,
                )
                field.help_text = f'Рекомендовано до {max_chars} символів.'
            else:
                field.widget = CmsAdminTextInputWidget(max_chars=max_chars, hard_limit=True)
                field.help_text = f'Максимум {max_chars} символів.'
                field.max_length = max_chars


class ServiceScopeItemForm(_CountableInlineForm):
    text_limits = {'text': 160}

    class Meta:
        model = ServiceScopeItem
        fields = '__all__'


class ServiceMethodStepForm(_CountableInlineForm):
    text_limits = {'number': 8, 'title': 80, 'text': 400}

    class Meta:
        model = ServiceMethodStep
        fields = '__all__'


class ServiceAdvantageForm(_CountableInlineForm):
    text_limits = {'title': 80, 'text': 280}

    class Meta:
        model = ServiceAdvantage
        fields = '__all__'


class ServiceScopeItemInline(StackedInline):
    model = ServiceScopeItem
    form = ServiceScopeItemForm
    extra = 0
    fields = (('text', 'order'),)
    classes = ['vartis-inline-card']


class ServiceMethodStepInline(StackedInline):
    model = ServiceMethodStep
    form = ServiceMethodStepForm
    extra = 0
    fields = (('number', 'title', 'order'), 'text')
    classes = ['vartis-inline-card']


class ServiceAdvantageInline(StackedInline):
    model = ServiceAdvantage
    form = ServiceAdvantageForm
    extra = 0
    fields = (('title', 'order'), 'text')
    classes = ['vartis-inline-card']


@admin.register(ServicePage)
class ServicePageAdmin(ModelAdmin):
    form = ServicePageForm
    list_display = ('title', 'slug', 'order', 'is_published')
    list_editable = ('order', 'is_published')
    prepopulated_fields = {}
    inlines = [ServiceScopeItemInline, ServiceMethodStepInline, ServiceAdvantageInline]
    fieldsets = (
        ('SEO', {
            'classes': ('tab',),
            'fields': ('seo_title', 'seo_description', 'h1'),
        }),
        ('Основне', {
            'classes': ('tab',),
            'fields': (
                'slug', 'title', 'short', 'order', 'is_published',
                'icon', 'tags', 'card_image', 'card_text',
            ),
        }),
        ('Hero', {
            'classes': ('tab',),
            'fields': ('hero_text', 'hero_image'),
        }),
        ('Блоки', {
            'classes': ('tab',),
            'fields': (
                'scope_title', 'scope_text', 'method_title',
                'advantages_title', 'order_title', 'order_text',
            ),
        }),
    )


@admin.register(HomeAdvantage)
class HomeAdvantageAdmin(_ParentPageMixin, ModelAdmin):
    parent_model = HomePage
    list_display = ('title', 'order', 'icon')
    list_editable = ('order',)
    ordering = ('order', 'id')
    search_fields = ('title',)


@admin.register(HomeProcessStep)
class HomeProcessStepAdmin(_ParentPageMixin, ModelAdmin):
    parent_model = HomePage
    list_display = ('number', 'title', 'order')
    list_editable = ('order',)
    ordering = ('order', 'id')
    search_fields = ('title',)


@admin.register(AboutPrinciple)
class AboutPrincipleAdmin(_ParentPageMixin, ModelAdmin):
    parent_model = AboutPage
    list_display = ('title', 'order', 'icon')
    list_editable = ('order',)
    ordering = ('order', 'id')


class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if 'bio' in self.fields:
            self.fields['bio'].widget = CmsTinyMCEWidget(
                attrs={'rows': 10},
                max_chars=2000,
                hard_limit=False,
            )
            self.fields['bio'].help_text = 'Рекомендовано до 2000 символів.'
        if 'photo' in self.fields:
            profile = image_profile_for_key('team_photo')
            self.fields['photo'].widget = CmsImageFieldWidget(
                hint=profile.hint,
                preview_url=_preview_url(getattr(instance, 'photo', None) if instance else None),
            )
            self.fields['photo'].help_text = profile.hint
        for name, max_chars in (('name', 80), ('role', 120), ('regalia', 200)):
            if name in self.fields:
                self.fields[name].widget = CmsAdminTextInputWidget(
                    max_chars=max_chars,
                    hard_limit=True,
                )
                self.fields[name].help_text = f'Максимум {max_chars} символів.'


@admin.register(TeamMember)
class TeamMemberAdmin(_ParentPageMixin, ModelAdmin):
    parent_model = AboutPage
    form = TeamMemberForm
    list_display = ('name', 'role', 'order')
    list_editable = ('order',)
    ordering = ('order', 'id')
    search_fields = ('name', 'role')


@admin.register(AboutStat)
class AboutStatAdmin(_ParentPageMixin, ModelAdmin):
    parent_model = AboutPage
    list_display = ('value', 'label', 'block', 'order')
    list_editable = ('order',)
    ordering = ('order', 'id')


@admin.register(AboutProcessStep)
class AboutProcessStepAdmin(_ParentPageMixin, ModelAdmin):
    parent_model = AboutPage
    list_display = ('number', 'title', 'order')
    list_editable = ('order',)
    ordering = ('order', 'id')


@admin.register(AnalysisStep)
class AnalysisStepAdmin(_ParentPageMixin, ModelAdmin):
    parent_model = AnalysisPage
    list_display = ('number', 'title', 'order')
    list_editable = ('order',)
    ordering = ('order', 'id')


@admin.register(AnalysisRisk)
class AnalysisRiskAdmin(_ParentPageMixin, ModelAdmin):
    parent_model = AnalysisPage
    list_display = ('title', 'order')
    list_editable = ('order',)
    ordering = ('order', 'id')


@admin.register(AnalysisInclude)
class AnalysisIncludeAdmin(_ParentPageMixin, ModelAdmin):
    parent_model = AnalysisPage
    list_display = ('title', 'order')
    list_editable = ('order',)
    ordering = ('order', 'id')


@admin.register(AnalysisWhy)
class AnalysisWhyAdmin(_ParentPageMixin, ModelAdmin):
    parent_model = AnalysisPage
    list_display = ('title', 'order')
    list_editable = ('order',)
    ordering = ('order', 'id')


@admin.register(AnalysisPriceRow)
class AnalysisPriceRowAdmin(_ParentPageMixin, ModelAdmin):
    parent_model = AnalysisPage
    list_display = ('number', 'title', 'price_note', 'order')
    list_editable = ('order',)
    ordering = ('order', 'id')
