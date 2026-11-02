from django.db import models
from django.urls import reverse


class CaseStudy(models.Model):
    slug = models.SlugField('Slug', unique=True, max_length=160)
    title = models.CharField('Заголовок', max_length=300)
    category = models.CharField('Категорія', max_length=120)
    image = models.ImageField('Зображення', upload_to='cases/', blank=True)
    excerpt = models.TextField('Короткий опис')
    client = models.CharField('Клієнт', max_length=200, blank=True)
    service = models.CharField('Послуга', max_length=200, blank=True)
    scope = models.CharField('Охоплення', max_length=200, blank=True)
    seo_title = models.CharField('SEO Title', max_length=200, blank=True)
    seo_description = models.TextField('SEO Description', blank=True)
    h1 = models.CharField('H1', max_length=300, blank=True)
    is_published = models.BooleanField('Опубліковано', default=True)
    is_demo = models.BooleanField('Демонстраційний', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Кейс'
        verbose_name_plural = 'Кейси'
        ordering = ['-id']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('cases:detail', kwargs={'slug': self.slug})

    @property
    def display_h1(self):
        return self.h1 or self.title


class CaseStat(models.Model):
    case = models.ForeignKey(CaseStudy, on_delete=models.CASCADE, related_name='stats')
    value = models.CharField('Значення', max_length=40)
    label = models.CharField('Підпис', max_length=200)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Цифра кейсу'
        verbose_name_plural = 'Цифри кейсу'

    def __str__(self):
        return f'{self.value} — {self.label}'


class CaseBlock(models.Model):
    case = models.ForeignKey(CaseStudy, on_delete=models.CASCADE, related_name='blocks')
    heading = models.CharField('Заголовок', max_length=300, blank=True)
    text = models.TextField('Текст', blank=True)
    list_items = models.TextField('Список (рядок = пункт)', blank=True)
    facts = models.TextField('Факти (рядок = факт)', blank=True)
    assumption = models.TextField('Припущення', blank=True)
    why = models.TextField('Чому', blank=True)
    quotes = models.TextField('Цитати (рядок = цитата)', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Блок кейсу'
        verbose_name_plural = 'Блоки кейсу'

    def items(self):
        return [i.strip() for i in self.list_items.splitlines() if i.strip()]

    def fact_list(self):
        return [i.strip() for i in self.facts.splitlines() if i.strip()]

    def quote_list(self):
        return [i.strip() for i in self.quotes.splitlines() if i.strip()]

    def __str__(self):
        return self.heading or f'Блок {self.pk}'
