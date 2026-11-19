from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from src.core.admin_mixins import TopDropdownFiltersMixin

from .models import Article, ArticleBlock, BlogPage


class ArticleBlockInline(TabularInline):
    model = ArticleBlock
    extra = 0
    fields = ('order', 'block_type', 'heading', 'text', 'list_items')


@admin.register(Article)
class ArticleAdmin(TopDropdownFiltersMixin, ModelAdmin):
    list_display = ('title', 'category', 'published_at', 'read_minutes', 'is_published')
    list_filter = ('category', 'is_published')
    search_fields = ('title', 'slug', 'excerpt')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ArticleBlockInline]
    fieldsets = (
        (None, {
            'fields': (
                'title', 'slug', 'category', 'published_at', 'read_minutes',
                'image', 'excerpt', 'is_published',
            ),
        }),
        ('SEO', {
            'fields': ('seo_title', 'seo_description', 'h1'),
        }),
    )


@admin.register(BlogPage)
class BlogPageAdmin(ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        from django.shortcuts import redirect
        from django.urls import reverse

        BlogPage.load()
        return redirect(reverse("admin:blog_blogpage_change", args=[1]))
