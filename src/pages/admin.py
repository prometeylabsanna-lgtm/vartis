from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

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
    ContactsPage,
    HomeAdvantage,
    HomePage,
    HomeProcessStep,
    PrivacyPage,
    ServiceAdvantage,
    ServiceMethodStep,
    ServicePage,
    ServiceScopeItem,
    ServicesIndex,
    TeamMember,
)


class SingletonAdmin(ModelAdmin):
    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        self.model.load()
        return super().changelist_view(request, extra_context)


class HomeAdvantageInline(TabularInline):
    model = HomeAdvantage
    extra = 0


class HomeProcessStepInline(TabularInline):
    model = HomeProcessStep
    extra = 0


@admin.register(HomePage)
class HomePageAdmin(SingletonAdmin):
    inlines = [HomeAdvantageInline, HomeProcessStepInline]
    fieldsets = (
        ('SEO', {'fields': ('seo_title', 'seo_description', 'h1')}),
        ('Hero', {'fields': ('hero_title', 'hero_text', 'hero_image')}),
        ('Секції', {
            'fields': (
                'services_title', 'advantages_title',
                'mission_title', 'mission_text', 'mission_image',
                'process_title', 'blog_title',
            ),
        }),
    )


class AboutPrincipleInline(TabularInline):
    model = AboutPrinciple
    extra = 0


class TeamMemberInline(TabularInline):
    model = TeamMember
    extra = 0


class AboutStatInline(TabularInline):
    model = AboutStat
    extra = 0
    fields = ('block', 'value', 'label', 'order')


class AboutProcessStepInline(TabularInline):
    model = AboutProcessStep
    extra = 0


@admin.register(AboutPage)
class AboutPageAdmin(SingletonAdmin):
    inlines = [
        AboutPrincipleInline, TeamMemberInline,
        AboutStatInline, AboutProcessStepInline,
    ]
    fieldsets = (
        ('SEO', {'fields': ('seo_title', 'seo_description', 'h1')}),
        ('Hero', {'fields': ('hero_title', 'hero_text', 'hero_image')}),
        ('Контент', {
            'fields': (
                'intro_title', 'intro_text', 'principles_title',
                'team_title', 'science_title', 'science_text',
                'stats_title', 'process_title',
            ),
        }),
    )


@admin.register(ServicesIndex)
class ServicesIndexAdmin(SingletonAdmin):
    fieldsets = (
        ('SEO', {'fields': ('seo_title', 'seo_description', 'h1')}),
        ('Hero', {'fields': ('hero_title', 'hero_text', 'hero_image')}),
    )


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


class AnalysisStepInline(TabularInline):
    model = AnalysisStep
    extra = 0


class AnalysisRiskInline(TabularInline):
    model = AnalysisRisk
    extra = 0


class AnalysisIncludeInline(TabularInline):
    model = AnalysisInclude
    extra = 0


class AnalysisWhyInline(TabularInline):
    model = AnalysisWhy
    extra = 0


class AnalysisPriceRowInline(TabularInline):
    model = AnalysisPriceRow
    extra = 0


@admin.register(AnalysisPage)
class AnalysisPageAdmin(SingletonAdmin):
    inlines = [
        AnalysisStepInline, AnalysisRiskInline, AnalysisIncludeInline,
        AnalysisWhyInline, AnalysisPriceRowInline,
    ]
    fieldsets = (
        ('SEO', {'fields': ('seo_title', 'seo_description', 'h1')}),
        ('Картка / меню', {
            'fields': ('title', 'short', 'icon', 'tags', 'card_image', 'card_text'),
        }),
        ('Hero', {'fields': ('hero_title', 'hero_text', 'hero_image')}),
        ('Секції', {
            'fields': (
                'steps_title', 'risks_title',
                'recommendation_title', 'recommendation_text',
                'result_title', 'result_text',
                'paket_title', 'paket_subtitle', 'paket_text',
                'include_title', 'why_title', 'price_title',
                'order_title', 'order_text',
            ),
        }),
    )


@admin.register(ContactsPage)
class ContactsPageAdmin(SingletonAdmin):
    fieldsets = (
        ('SEO', {'fields': ('seo_title', 'seo_description', 'h1')}),
        ('Hero', {'fields': ('hero_title', 'hero_text', 'hero_image')}),
        ('Контент', {'fields': ('info_title',)}),
    )


@admin.register(PrivacyPage)
class PrivacyPageAdmin(SingletonAdmin):
    fieldsets = (
        ('SEO', {'fields': ('seo_title', 'seo_description', 'h1')}),
        ('Контент', {'fields': ('hero_title', 'body')}),
    )
