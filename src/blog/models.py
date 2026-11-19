import re

from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse

_STRIP_TAGS = re.compile(r"<[^>]+>")

from src.core.fields import WebPImageField
from src.core.models import SingletonModel


class Article(models.Model):
    slug = models.SlugField('Slug', unique=True, max_length=160)
    title = models.CharField('Заголовок', max_length=300)
    category = models.CharField('Категорія', max_length=120)
    published_at = models.DateField('Дата публікації')
    image = WebPImageField('Зображення', upload_to='blog/', blank=True)
    excerpt = models.TextField('Короткий опис')
    body = models.TextField('Текст', blank=True)
    seo_title = models.CharField('SEO Title', max_length=200, blank=True)
    seo_description = models.TextField('SEO Description', blank=True)
    h1 = models.CharField('H1', max_length=300, blank=True)
    is_published = models.BooleanField('Опубліковано', default=True)
    read_minutes = models.PositiveIntegerField(
        'Хвилин читання',
        default=6,
        validators=[MinValueValidator(1)],
        help_text='Скільки хвилин показувати біля статті.',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Стаття'
        verbose_name_plural = 'Статті'
        ordering = ['-published_at', '-id']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})

    @property
    def display_h1(self):
        return self.h1 or self.title

    @property
    def read_label(self):
        minutes = self.read_minutes or 1
        return f'{minutes} хв читання'

    def estimate_read_minutes(self):
        words = len((self.excerpt or '').split())
        body_text = _STRIP_TAGS.sub(' ', self.body or '')
        words += len(body_text.split())
        if not body_text:
            for block in self.blocks.all():
                words += len((block.heading or '').split())
                words += len((block.text or '').split())
                words += len((block.list_items or '').split())
        if not words:
            return 6
        return max(1, round(words / 180))


class ArticleBlock(models.Model):
    class BlockType(models.TextChoices):
        PARAGRAPH = 'p', 'Абзац'
        HEADING = 'h', 'Підзаголовок'
        LIST = 'list', 'Список'
        NOTE = 'note', 'Примітка'

    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='blocks')
    block_type = models.CharField('Тип', max_length=10, choices=BlockType.choices)
    heading = models.CharField('Підзаголовок', max_length=300, blank=True)
    text = models.TextField('Текст', blank=True)
    list_items = models.TextField('Пункти списку (рядок = пункт)', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Блок статті'
        verbose_name_plural = 'Блоки статті'

    def items(self):
        return [i.strip() for i in self.list_items.splitlines() if i.strip()]

    def __str__(self):
        return f'{self.article_id}: {self.block_type}'


class BlogPage(SingletonModel):
    seo_title = models.CharField(
        'SEO Title',
        max_length=200,
        blank=True,
        default='Блог про перевірку контрагентів і OSINT | VARTIS INTELLIGENCE',
    )
    seo_description = models.TextField(
        'SEO Description',
        blank=True,
        default=(
            'Експертні матеріали: перевірка контрагентів, стратегічна розвідка, '
            'корпоративна безпека та управління ризиками.'
        ),
    )
    h1 = models.CharField('H1', max_length=200, default='Блог')
    hero_text = models.TextField(
        'Текст першого екрана',
        blank=True,
        default=(
            'Аналітика та експертні матеріали про перевірку контрагентів, '
            'стратегічну розвідку, корпоративну безпеку та управління ризиками'
        ),
    )
    crumb = models.CharField('Крихта', max_length=80, default='Блог')
    cta_primary = models.CharField('Основна кнопка', max_length=80, default='Залишити заявку')
    cta_secondary = models.CharField('Друга кнопка', max_length=80, default='До статей')
    all_label = models.CharField('Підпис «усі»', max_length=40, default='Усі')
    feed_title = models.CharField('Заголовок стрічки', max_length=120, default='Усі публікації')
    empty_text = models.CharField('Порожня стрічка', max_length=200, default='У цій темі ще немає публікацій.')
    read_label = models.CharField('Кнопка статті', max_length=80, default='Читати статтю')
    detail_cta = models.CharField('Кнопка в статті', max_length=80, default='Обговорити завдання')
    detail_read = models.CharField('Друга кнопка статті', max_length=80, default='Читати')
    help_title = models.CharField('Банер у статті', max_length=200, default='Потрібна допомога з подібним завданням?')
    help_cta = models.CharField('Кнопка банера', max_length=80, default='Обговорити завдання')
    related_title = models.CharField('Заголовок «читайте також»', max_length=80, default='Читайте також')
    all_articles_label = models.CharField('Посилання на всі статті', max_length=80, default='Усі статті →')

    class Meta:
        verbose_name = 'Сторінка блогу'
        verbose_name_plural = 'Сторінка блогу'
        constraints = [models.CheckConstraint(condition=models.Q(id=1), name='blogpage_singleton')]

    def __str__(self):
        return 'Сторінка блогу'


class BlogArticleBanner(BlogPage):
    class Meta:
        proxy = True
        verbose_name = 'Банер у статті'
        verbose_name_plural = 'Банер у статті'
