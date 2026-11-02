from django.db import models
from django.urls import reverse


class Article(models.Model):
    slug = models.SlugField('Slug', unique=True, max_length=160)
    title = models.CharField('Заголовок', max_length=300)
    category = models.CharField('Категорія', max_length=120)
    published_at = models.DateField('Дата публікації')
    image = models.ImageField('Зображення', upload_to='blog/', blank=True)
    excerpt = models.TextField('Короткий опис')
    seo_title = models.CharField('SEO Title', max_length=200, blank=True)
    seo_description = models.TextField('SEO Description', blank=True)
    h1 = models.CharField('H1', max_length=300, blank=True)
    is_published = models.BooleanField('Опубліковано', default=True)
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
