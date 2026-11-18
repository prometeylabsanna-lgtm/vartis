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
