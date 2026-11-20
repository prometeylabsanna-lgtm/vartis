from modeltranslation.translator import TranslationOptions, register

from src.blog.models import Article, ArticleBlock, BlogPage


@register(BlogPage)
class BlogPageTR(TranslationOptions):
    fields = (
        'seo_title',
        'seo_description',
        'h1',
        'hero_text',
        'crumb',
        'cta_primary',
        'cta_secondary',
        'all_label',
        'feed_title',
        'empty_text',
        'read_label',
        'detail_cta',
        'detail_read',
        'help_title',
        'help_cta',
        'related_title',
        'all_articles_label',
        'read_minutes_template',
    )


@register(Article)
class ArticleTR(TranslationOptions):
    fields = (
        'title',
        'category',
        'excerpt',
        'body',
        'seo_title',
        'seo_description',
        'h1',
    )


@register(ArticleBlock)
class ArticleBlockTR(TranslationOptions):
    fields = (
        'heading',
        'text',
        'list_items',
    )
