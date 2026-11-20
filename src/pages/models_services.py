from django.db import models

from src.core.fields import WebPImageField

from .models_base import ICON_HELP, SEOFields
from src.core.models import SingletonModel

SERVICE_SLUGS = [
    ('konsaltynh', 'Консалтинг'),
    ('kompleksna-dopomoha-biznesu', 'Комплексна допомога бізнесу'),
    ('zbir-ta-analiz-informatsii', 'Глибока аналітика'),
    ('zakhyst-vid-vytoku', 'Захист від витоку інформації'),
    ('kryminalni-provadzhennia', 'Інформаційна підтримка у кримінальних провадженнях'),
]

SCOPE_VARIANTS = [('', 'Список'), ('bento', 'Бенто')]
METHOD_VARIANTS = [('cards', 'Картки'), ('timeline', 'Таймлайн')]
ORDER_VARIANTS = [('', 'Темна'), ('light', 'Світла')]


class ServicesIndex(SingletonModel, SEOFields):
    hero_title = models.CharField('Заголовок першого екрана', max_length=200, default='Послуги')
    hero_text = models.TextField(
        'Текст першого екрана',
        default=(
            'Комплексні рішення для бізнесу — від перевірки інформації '
            'до стратегічного аналізу та управління ризиками'
        ),
    )
    hero_image = WebPImageField('Зображення першого екрана', upload_to='pages/services/', blank=True)
    cta_primary = models.CharField('Основна кнопка', max_length=80, default='Залишити заявку')
    cta_secondary = models.CharField('Друга кнопка', max_length=80, default='Усі напрями')
    card_more_label = models.CharField('Підпис картки', max_length=80, default='Детальніше')

    class Meta:
        verbose_name = 'Каталог послуг'
        verbose_name_plural = 'Каталог послуг'
        constraints = [models.CheckConstraint(condition=models.Q(id=1), name='servicesindex_singleton')]

    def __str__(self):
        return 'Каталог послуг'


class ServicePage(SEOFields):
    slug = models.SlugField('Slug', unique=True, choices=SERVICE_SLUGS)
    slug_en = models.SlugField('Slug (EN)', max_length=80, unique=True, null=True, blank=True)
    title = models.CharField('Назва', max_length=200)
    short = models.CharField('Короткий опис', max_length=200, blank=True)
    hero_text = models.TextField('Текст першого екрана', blank=True)
    hero_image = WebPImageField('Зображення першого екрана', upload_to='pages/services/', blank=True)
    cta_primary = models.CharField('Основна кнопка', max_length=120, blank=True, default='Обговорити завдання')
    cta_secondary = models.CharField('Друга кнопка', max_length=120, blank=True, default='Як ми працюємо')
    cta_secondary_href = models.CharField('Посилання другої кнопки', max_length=80, blank=True, default='#method')
    scope_title = models.CharField('Заголовок опису', max_length=200, default='Опис напряму')
    scope_text = models.TextField('Текст опису', blank=True)
    scope_variant = models.CharField('Вигляд опису', max_length=16, choices=SCOPE_VARIANTS, blank=True, default='')
    scope_feature_title = models.CharField('Заголовок акценту', max_length=300, blank=True)
    scope_feature_text = models.TextField('Текст акценту', blank=True)
    method_title = models.CharField('Заголовок методології', max_length=200, default='Методологія')
    method_lead = models.CharField('Лід методології', max_length=200, blank=True)
    method_variant = models.CharField('Вигляд кроків', max_length=16, choices=METHOD_VARIANTS, default='cards')
    method_step_prefix = models.CharField('Префікс етапу', max_length=40, blank=True, default='Етап')
    advantages_title = models.CharField('Заголовок переваг', max_length=200, default='Переваги для клієнта')
    advantages_lead = models.CharField('Лід переваг', max_length=200, blank=True)
    advantages_dark = models.BooleanField('Темний блок переваг', default=False)
    order_title = models.CharField('Заголовок форми', max_length=200, default='Обговорімо вашу задачу')
    order_text = models.TextField('Текст форми', blank=True)
    order_variant = models.CharField('Вигляд форми', max_length=16, choices=ORDER_VARIANTS, blank=True, default='')
    related_title = models.CharField('Заголовок інших послуг', max_length=120, default='Профільні послуги')
    is_published = models.BooleanField('Опубліковано', default=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    icon = models.CharField('Іконка', max_length=80, blank=True, help_text=ICON_HELP)
    card_image = WebPImageField('Зображення картки', upload_to='pages/services/', blank=True)
    card_text = models.TextField('Текст картки', blank=True)
    tags = models.CharField('Теги (через |)', max_length=300, blank=True)

    class Meta:
        verbose_name = 'Послуга'
        verbose_name_plural = 'Послуги'
        ordering = ['order', 'id']

    def __str__(self):
        return self.title

    def tag_list(self):
        return [t.strip() for t in self.tags.split('|') if t.strip()]


class ServiceScopeParagraph(models.Model):
    page = models.ForeignKey(ServicePage, on_delete=models.CASCADE, related_name='scope_paragraphs')
    text = models.TextField('Абзац')
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Абзац опису'
        verbose_name_plural = 'Абзаци опису'

    def __str__(self):
        return self.text[:80]


class ServiceScopeItem(models.Model):
    page = models.ForeignKey(ServicePage, on_delete=models.CASCADE, related_name='scope_items')
    text = models.CharField('Пункт', max_length=400)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Пункт опису'
        verbose_name_plural = 'Пункти опису'

    def __str__(self):
        return self.text


class ServiceMethodStep(models.Model):
    page = models.ForeignKey(ServicePage, on_delete=models.CASCADE, related_name='method_steps')
    number = models.CharField('Номер', max_length=8, default='01')
    title = models.CharField('Заголовок', max_length=120)
    text = models.TextField('Текст', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Крок методології'
        verbose_name_plural = 'Кроки методології'

    def __str__(self):
        return f'{self.number} {self.title}'


class ServiceAdvantage(models.Model):
    page = models.ForeignKey(ServicePage, on_delete=models.CASCADE, related_name='advantages')
    icon = models.CharField('Іконка', max_length=80, blank=True, help_text=ICON_HELP)
    title = models.CharField('Заголовок', max_length=120)
    text = models.TextField('Текст', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Перевага послуги'
        verbose_name_plural = 'Переваги послуги'

    def __str__(self):
        return self.title
