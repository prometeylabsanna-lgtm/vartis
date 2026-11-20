"""Заливає англійські поля статей і збирає HTML тіла."""

from types import SimpleNamespace

from src.blog.body_html import article_blocks_to_html
from src.blog.models import Article
from src.core.i18n_seed.articles_a import ARTICLES_A
from src.core.i18n_seed.articles_b import ARTICLES_B
from src.core.i18n_seed.articles_c import ARTICLES_C
from src.core.i18n_seed.fill import fill_en
from src.core.i18n_urls import ARTICLE_SLUG_EN


def _html(blocks):
    objects = []
    for block in blocks:
        if 'note' in block and 'h' not in block:
            kind, heading, text, items = 'note', '', block['note'], ''
        elif 'h' in block:
            kind = 'h'
            heading = block.get('h') or ''
            text = block.get('p') or ''
            items = '\n'.join(block.get('list') or [])
        elif 'list' in block:
            kind, heading, text = 'list', '', ''
            items = '\n'.join(block['list'])
        else:
            kind, heading, text, items = 'p', '', block.get('p') or '', ''
        objects.append(SimpleNamespace(
            block_type=kind, heading=heading, text=text, list_items=items,
        ))
    return article_blocks_to_html(objects)


def _row(block):
    if 'note' in block and 'h' not in block:
        return {'heading': '', 'text': block['note'], 'list_items': ''}
    if 'h' in block:
        return {
            'heading': block.get('h') or '',
            'text': block.get('p') or '',
            'list_items': '\n'.join(block.get('list') or []),
        }
    if 'list' in block:
        return {'heading': '', 'text': '', 'list_items': '\n'.join(block['list'])}
    return {'heading': '', 'text': block.get('p') or '', 'list_items': ''}


def seed_articles() -> None:
    catalog = {}
    catalog.update(ARTICLES_A)
    catalog.update(ARTICLES_B)
    catalog.update(ARTICLES_C)
    for slug, copy in catalog.items():
        article = Article.objects.filter(slug=slug).first()
        if article is None:
            continue
        if not article.slug_en:
            article.slug_en = ARTICLE_SLUG_EN.get(slug, '')
            if article.slug_en:
                article.save(update_fields=['slug_en'])
        blocks = copy['blocks']
        fill_en(
            article,
            title=copy['title'],
            category=copy['category'],
            excerpt=copy['excerpt'],
            seo_title=copy['title'],
            seo_description=copy['seo'],
            h1=copy['title'],
            body=_html(blocks),
        )
        stored = list(article.blocks.order_by('order', 'id'))
        for item, block in zip(stored, blocks):
            fill_en(item, **_row(block))
