from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from src.core.admin_mixins import TopDropdownFiltersMixin

from .models import CaseBlock, CaseStat, CaseStudy


class CaseStatInline(TabularInline):
    model = CaseStat
    extra = 0


class CaseBlockInline(TabularInline):
    model = CaseBlock
    extra = 0
    fields = (
        'order', 'heading', 'text', 'list_items',
        'facts', 'assumption', 'why', 'quotes',
    )


@admin.register(CaseStudy)
class CaseStudyAdmin(TopDropdownFiltersMixin, ModelAdmin):
    list_display = ('title', 'category', 'is_demo', 'is_published')
    list_filter = ('category', 'is_demo', 'is_published')
    search_fields = ('title', 'slug', 'excerpt')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [CaseStatInline, CaseBlockInline]
    fieldsets = (
        (None, {
            'fields': (
                'title', 'slug', 'category', 'image', 'excerpt',
                'client', 'service', 'scope', 'is_demo', 'is_published',
            ),
        }),
        ('SEO', {
            'fields': ('seo_title', 'seo_description', 'h1'),
        }),
    )
