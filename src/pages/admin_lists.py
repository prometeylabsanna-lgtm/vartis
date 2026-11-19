"""Списки, яких не було в попередній адмінці секцій."""

from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from src.pages.models import (
    AnalysisPaketStep,
    AnalysisPayTerm,
    AnalysisPricePart,
    AnalysisRec,
    AnalysisRiskLevel,
    AnalysisTariff,
    AnalysisTariffLine,
    DeepAnalytics,
    DeepFaq,
    DeepGetItem,
    DeepPayStage,
    DeepQualityItem,
    DeepSnippet,
    DeepStep,
    ServiceScopeParagraph,
)


class _BindPage:
    parent_model = None

    def save_model(self, request, obj, form, change):
        if self.parent_model is not None and not getattr(obj, "page_id", None):
            obj.page = self.parent_model.load()
        super().save_model(request, obj, form, change)

    def get_exclude(self, request, obj=None):
        excluded = list(super().get_exclude(request, obj) or [])
        if "page" not in excluded:
            excluded.append("page")
        return excluded


class AnalysisTariffLineInline(TabularInline):
    model = AnalysisTariffLine
    extra = 0
    fields = ("order", "label", "value")


@admin.register(AnalysisTariff)
class AnalysisTariffAdmin(_BindPage, ModelAdmin):
    from src.pages.models import AnalysisPage

    parent_model = AnalysisPage
    list_display = ("name", "price", "featured", "order")
    list_editable = ("order",)
    ordering = ("order", "id")
    inlines = [AnalysisTariffLineInline]


@admin.register(AnalysisRiskLevel)
class AnalysisRiskLevelAdmin(_BindPage, ModelAdmin):
    from src.pages.models import AnalysisPage

    parent_model = AnalysisPage
    list_display = ("level", "tone", "order")
    ordering = ("order", "id")


@admin.register(AnalysisRec)
class AnalysisRecAdmin(_BindPage, ModelAdmin):
    from src.pages.models import AnalysisPage

    parent_model = AnalysisPage
    list_display = ("title", "order")
    ordering = ("order", "id")


@admin.register(AnalysisPaketStep)
class AnalysisPaketStepAdmin(_BindPage, ModelAdmin):
    from src.pages.models import AnalysisPage

    parent_model = AnalysisPage
    list_display = ("title", "order")
    ordering = ("order", "id")


@admin.register(AnalysisPricePart)
class AnalysisPricePartAdmin(_BindPage, ModelAdmin):
    from src.pages.models import AnalysisPage

    parent_model = AnalysisPage
    list_display = ("title", "order")
    ordering = ("order", "id")


@admin.register(AnalysisPayTerm)
class AnalysisPayTermAdmin(_BindPage, ModelAdmin):
    from src.pages.models import AnalysisPage

    parent_model = AnalysisPage
    list_display = ("title", "order")
    ordering = ("order", "id")


@admin.register(ServiceScopeParagraph)
class ServiceScopeParagraphAdmin(ModelAdmin):
    list_display = ("page", "order")
    list_filter = ("page",)
    ordering = ("page", "order", "id")


@admin.register(DeepAnalytics)
class DeepAnalyticsAdmin(ModelAdmin):
    list_display = ("page", "h1")


class _DeepChild(ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not getattr(obj, "page_id", None):
            parent = DeepAnalytics.objects.first()
            if parent is not None:
                obj.page = parent
        super().save_model(request, obj, form, change)


@admin.register(DeepStep)
class DeepStepAdmin(_DeepChild):
    list_display = ("title", "order")
    ordering = ("order", "id")


@admin.register(DeepGetItem)
class DeepGetItemAdmin(_DeepChild):
    list_display = ("title", "order")
    ordering = ("order", "id")


@admin.register(DeepFaq)
class DeepFaqAdmin(_DeepChild):
    list_display = ("question", "order")
    ordering = ("order", "id")


@admin.register(DeepPayStage)
class DeepPayStageAdmin(_DeepChild):
    list_display = ("title", "order")
    ordering = ("order", "id")


@admin.register(DeepQualityItem)
class DeepQualityItemAdmin(_DeepChild):
    list_display = ("title", "order")
    ordering = ("order", "id")


@admin.register(DeepSnippet)
class DeepSnippetAdmin(_DeepChild):
    list_display = ("kind", "order")
    ordering = ("order", "id")
