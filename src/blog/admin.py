from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from unfold.admin import ModelAdmin

from src.core.admin_mixins import TopDropdownFiltersMixin
from src.core.admin_site_content_widgets import CmsTinyMCEWidget

from .models import Article, BlogArticleBanner, BlogPage


@admin.register(Article)
class ArticleAdmin(TopDropdownFiltersMixin, ModelAdmin):
    list_display = ('title', 'category', 'published_at', 'read_minutes', 'is_published')
    list_filter = ('category', 'is_published')
    search_fields = ('title', 'slug', 'excerpt', 'body')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Стаття — Стаття', {
            'classes': ['tab'],
            'fields': (
                'title', 'slug', 'category', 'published_at', 'read_minutes',
                'image', 'excerpt', 'body', 'is_published',
            ),
        }),
        ('Стаття — SEO', {
            'classes': ['tab'],
            'fields': ('seo_title', 'seo_description', 'h1'),
        }),
    )

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'body':
            kwargs['widget'] = CmsTinyMCEWidget(
                attrs={'class': 'cms-tinymce--article', 'rows': 22},
            )
        return super().formfield_for_dbfield(db_field, request, **kwargs)


class _SingletonRedirectAdmin(ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        self.model.load()
        return redirect(
            reverse(
                f'admin:{self.model._meta.app_label}_{self.model._meta.model_name}_change',
                args=[1],
            )
        )


@admin.register(BlogPage)
class BlogPageAdmin(_SingletonRedirectAdmin):
    fieldsets = (
        ('Сторінка блогу — Сторінка', {
            'classes': ['tab'],
            'fields': (
                'h1', 'hero_text', 'crumb', 'cta_primary', 'cta_secondary',
                'all_label', 'feed_title', 'empty_text', 'read_label',
                'detail_cta', 'detail_read', 'related_title', 'all_articles_label',
            ),
        }),
        ('Сторінка блогу — SEO', {
            'classes': ['tab'],
            'fields': ('seo_title', 'seo_description'),
        }),
    )


@admin.register(BlogArticleBanner)
class BlogArticleBannerAdmin(_SingletonRedirectAdmin):
    fields = ('help_title', 'help_cta')

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change=change, **kwargs)
        form.base_fields['help_title'].label = 'Текст'
        form.base_fields['help_cta'].label = 'Кнопка'
        return form
