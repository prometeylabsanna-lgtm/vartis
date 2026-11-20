from datetime import date

from django.test import TestCase
from django.urls import reverse

from src.blog.models import Article


def _article(index, day):
    return Article.objects.create(
        slug=f'stattya-{index}',
        title=f'Стаття {index}',
        category='Аналітика',
        published_at=date(2026, 1, day),
        excerpt='Короткий опис',
    )


class ArticleEditorTests(TestCase):
    def setUp(self):
        from django.contrib.auth import get_user_model

        from src.blog.models import ArticleBlock, BlogPage

        get_user_model().objects.create_superuser('adm', 'a@example.com', 'pw')
        self.client.force_login(get_user_model().objects.get(username='adm'))
        self.article = Article.objects.create(
            slug='perevirka',
            title='Перевірка',
            category='Аналітика',
            published_at=date(2026, 1, 1),
            excerpt='Короткий опис',
            body=(
                '<h2>Крок 1</h2><p>Абзац тексту</p>'
                '<blockquote class="art-note">Окремі факти рідко дають повну картину.</blockquote>'
            ),
        )
        ArticleBlock.objects.create(
            article=self.article,
            block_type='note',
            text='старий блок',
            order=0,
        )
        BlogPage.load()

    def test_admin_uses_tinymce_not_block_inline(self):
        response = self.client.get(f'/admin/blog/article/{self.article.pk}/change/')
        self.assertEqual(response.status_code, 200)
        body = response.content.decode()
        self.assertIn('cms-tinymce--article', body)
        self.assertIn('js/admin/cms_tinymce.js', body)
        self.assertNotIn('name="blocks-0-text"', body)
        self.assertNotIn('Пункти списку', body)

    def test_public_renders_heading_and_frame(self):
        response = self.client.get(self.article.get_absolute_url())
        self.assertContains(response, '<h2>Крок 1</h2>', html=True)
        self.assertContains(response, 'art-note')
        self.assertContains(response, 'Окремі факти рідко дають повну картину.')
        self.assertNotContains(response, 'старий блок')
        self.assertContains(response, 'Потрібна допомога з подібним завданням?')

    def test_article_banner_admin(self):
        response = self.client.get('/admin/blog/blogarticlebanner/1/change/')
        self.assertEqual(response.status_code, 200)
        body = response.content.decode()
        self.assertIn('name="help_title"', body)
        self.assertIn('name="help_cta"', body)

    def test_rich_list_then_heading_keeps_spacing_rule(self):
        from pathlib import Path

        self.article.body = (
            '<ul><li>who can see the client base</li>'
            '<li>how people are hired and how they leave</li></ul>'
            '<h2>Step 2. Short rules</h2><p>Write the few rules.</p>'
        )
        self.article.save(update_fields=['body'])
        response = self.client.get(self.article.get_absolute_url())
        self.assertContains(response, '<ul>')
        self.assertContains(response, '<h2>Step 2. Short rules</h2>', html=True)
        css = Path('src/core/static/css/article-detail.css').read_text(encoding='utf-8')
        self.assertIn('.art-body .art-body__rich > ul + h2', css)
        self.assertIn('margin-top: 32px', css)

    def test_blocks_to_html(self):
        from src.blog.body_html import article_blocks_to_html
        from src.blog.models import ArticleBlock

        html = article_blocks_to_html(ArticleBlock.objects.filter(article=self.article))
        self.assertIn('blockquote class="art-note"', html)
        self.assertIn('старий блок', html)


class BlogPaginationTests(TestCase):
    def setUp(self):
        Article.objects.all().delete()

    def test_pager_hidden_when_second_page_has_no_articles(self):
        for index in range(1, 6):
            _article(index, index)
        response = self.client.get(reverse('blog:list'))
        self.assertNotContains(response, 'class="pagination"')

    def test_second_page_link_opens_articles_not_footer(self):
        for index in range(1, 7):
            _article(index, index)
        response = self.client.get(reverse('blog:list'))
        self.assertContains(response, 'href="/blog/?page=2"')
        self.assertContains(response, 'show:#feed:top')
        page_two = self.client.get(reverse('blog:list') + '?page=2')
        self.assertContains(page_two, 'Стаття 1')
        self.assertContains(page_two, 'id="feed-partial"')

    def test_article_uses_admin_read_minutes(self):
        article = _article(1, 1)
        article.read_minutes = 9
        article.save(update_fields=['read_minutes'])
        response = self.client.get(article.get_absolute_url())
        self.assertContains(response, '9 хв читання')
        self.assertNotContains(response, '6 хв читання')
