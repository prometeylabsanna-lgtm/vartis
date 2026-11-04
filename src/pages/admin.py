from django import forms
from django.contrib import admin
from unfold.admin import ModelAdmin, StackedInline, TabularInline
from unfold.widgets import UnfoldAdminFileFieldWidget

from src.core.admin_site_content_widgets import CmsTinyMCEWidget

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


class ServicePageForm(forms.ModelForm):
    class Meta:
        model = ServicePage
        fields = '__all__'
        widgets = {
            **{name: CmsTinyMCEWidget(attrs={'rows': 10}) for name in SERVICE_RICH_FIELDS},
            **{name: UnfoldAdminFileFieldWidget() for name in SERVICE_IMAGE_FIELDS},
        }


class ServiceScopeItemInline(TabularInline):
    model = ServiceScopeItem
    extra = 0


class ServiceMethodStepInline(TabularInline):
    model = ServiceMethodStep
    extra = 0


class ServiceAdvantageInline(TabularInline):
    model = ServiceAdvantage
    extra = 0


@admin.register(ServicePage)
class ServicePageAdmin(ModelAdmin):
    form = ServicePageForm
    list_display = ('title', 'slug', 'order', 'is_published')
    list_editable = ('order', 'is_published')
    prepopulated_fields = {}
    inlines = [ServiceScopeItemInline, ServiceMethodStepInline, ServiceAdvantageInline]
    fieldsets = (
        ('SEO', {'fields': ('seo_title', 'seo_description', 'h1')}),
        ('Основне', {
            'fields': (
                'slug', 'title', 'short', 'order', 'is_published',
                'icon', 'tags', 'card_image', 'card_text',
            ),
        }),
        ('Hero', {'fields': ('hero_text', 'hero_image')}),
        ('Блоки', {
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
        widgets = {
            'bio': CmsTinyMCEWidget(attrs={'rows': 10}),
            'photo': UnfoldAdminFileFieldWidget(),
        }


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
