from datetime import date
from pathlib import Path
import json

from src.blog.models import Article, ArticleBlock
from .seed_content import assign_image

ARTICLES_JSON = Path(__file__).resolve().parents[2] / 'data' / 'articles.json'


def _blocks_from_js(body):
    """Convert articles.js body items into ArticleBlock kwargs list."""
    out = []
    for i, item in enumerate(body):
        if 'note' in item and len(item) == 1:
            out.append({'block_type': 'note', 'heading': '', 'text': item['note'], 'list_items': '', 'order': i})
            continue
        if 'p' in item and 'h' not in item and 'list' not in item and 'note' not in item:
            out.append({'block_type': 'p', 'heading': '', 'text': item['p'], 'list_items': '', 'order': i})
            continue
        if 'h' in item:
            list_items = '\n'.join(item['list']) if item.get('list') else ''
            out.append({
                'block_type': 'h',
                'heading': item.get('h') or '',
                'text': item.get('p') or '',
                'list_items': list_items,
                'order': i,
            })
            continue
        if 'list' in item:
            out.append({
                'block_type': 'list',
                'heading': '',
                'text': '',
                'list_items': '\n'.join(item['list']),
                'order': i,
            })
            continue
        if 'note' in item:
            out.append({'block_type': 'note', 'heading': '', 'text': item['note'], 'list_items': '', 'order': i})
            continue
        if 'p' in item:
            out.append({'block_type': 'p', 'heading': '', 'text': item['p'], 'list_items': '', 'order': i})
    return out


def seed_articles():
    from src.blog.models import Article
    from src.core.slug_renames import ARTICLE_SLUGS, rename_slugs

    rename_slugs(Article, ARTICLE_SLUGS)
    articles = json.loads(ARTICLES_JSON.read_text(encoding='utf-8'))
    for data in articles:
        art, created = Article.objects.update_or_create(
            slug=data['slug'],
            defaults={
                'title': data['title'],
                'category': data['cat'],
                'published_at': date.fromisoformat(data['date']),
                'excerpt': data['excerpt'],
                'seo_title': data.get('seo_title') or data['title'],
                'seo_description': data.get('seo_description') or data['excerpt'],
                'h1': data['title'],
                'is_published': True,
            },
        )
        assign_image(art.image, data['img'])
        art.save()
        art.blocks.all().delete()
        for kwargs in _blocks_from_js(data['body']):
            ArticleBlock.objects.create(article=art, **kwargs)
        if created:
            art.read_minutes = art.estimate_read_minutes()
            art.save(update_fields=['read_minutes'])
