from django.db import models

from src.core.fields import WebPImageField
from src.core.models import SingletonModel

from .models_base import ICON_HELP, SEOFields


class HomePage(SingletonModel, SEOFields):
    hero_title = models.CharField('Заголовок першого екрана', max_length=200, default='Стратегічна аналітика для бізнесу')
    hero_text = models.TextField(
        'Текст першого екрана',
        default='Допомагаємо виявляти приховані ризики й ухвалювати обґрунтовані рішення',
    )
    hero_cta = models.CharField('Кнопка першого екрана', max_length=80, default='Обговорити завдання')
    hero_image = WebPImageField('Зображення першого екрана', upload_to='pages/home/', blank=True)
    services_title = models.CharField('Заголовок напрямів', max_length=200, default='Напрями')
    services_lead = models.TextField('Лід напрямів', blank=True)
    advantages_title = models.CharField('Заголовок переваг', max_length=200, default='Переваги')
    advantages_lead = models.CharField('Лід переваг', max_length=200, blank=True)
    mission_title = models.CharField('Заголовок місії', max_length=200, default='Наша місія')
    mission_text = models.TextField('Текст місії', blank=True)
    mission_image = WebPImageField('Фон місії', upload_to='pages/home/', blank=True)
    process_title = models.CharField('Заголовок процесу', max_length=200, default='Як ми працюємо')
    process_lead = models.CharField('Лід процесу', max_length=200, blank=True)
    blog_title = models.CharField('Заголовок блоку блогу', max_length=200, default='Аналітика')
    blog_lead = models.TextField('Лід блогу', blank=True)
    blog_all_label = models.CharField('Посилання на всі статті', max_length=80, default='Усі статті →')

    class Meta:
        verbose_name = 'Головна'
        verbose_name_plural = 'Головна'
        constraints = [models.CheckConstraint(condition=models.Q(id=1), name='homepage_singleton')]

    def __str__(self):
        return 'Головна'


class HomeAdvantage(models.Model):
    page = models.ForeignKey(HomePage, on_delete=models.CASCADE, related_name='advantages')
    title = models.CharField('Заголовок', max_length=120)
    text = models.CharField('Текст', max_length=300)
    icon = models.CharField('Іконка', max_length=80, blank=True, help_text=ICON_HELP)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Перевага'
        verbose_name_plural = 'Переваги'

    def __str__(self):
        return self.title


class HomeProcessStep(models.Model):
    page = models.ForeignKey(HomePage, on_delete=models.CASCADE, related_name='process_steps')
    number = models.CharField('Номер', max_length=8, default='01')
    title = models.CharField('Заголовок', max_length=120)
    text = models.CharField('Текст', max_length=300)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Крок процесу'
        verbose_name_plural = 'Кроки процесу'

    def __str__(self):
        return f'{self.number} {self.title}'


class HomeDirection(models.Model):
    page = models.ForeignKey(HomePage, on_delete=models.CASCADE, related_name='directions')
    title = models.CharField('Заголовок', max_length=200)
    text = models.TextField('Текст', blank=True)
    image = WebPImageField('Зображення', upload_to='pages/home/directions/', blank=True)
    href = models.CharField('Посилання', max_length=200, blank=True)
    is_visible = models.BooleanField('Показувати на головній', default=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Напрям на головній'
        verbose_name_plural = 'Напрями на головній'

    def __str__(self):
        return self.title
