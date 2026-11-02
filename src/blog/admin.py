from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from .models import Article, ArticleBlock


class ArticleBlockInline(TabularInline):
    model = ArticleBlock
    extra = 0
    fields = ('order', 'block_type', 'heading', 'text', 'list_items')


@admin.register(Article)
class ArticleAdmin(ModelAdmin):
    list_display = ('title', 'category', 'published_at', 'is_published')
    list_filter = ('category', 'is_published')
    search_fields = ('title', 'slug', 'excerpt')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ArticleBlockInline]
    fieldsets = (
        (None, {
            'fields': (
                'title', 'slug', 'category', 'published_at',
                'image', 'excerpt', 'is_published',
            ),
        }),
        ('SEO', {
            'fields': ('seo_title', 'seo_description', 'h1'),
        }),
    )
