from django.db import models

from src.core.fields import WebPImageField
from src.core.models import SingletonModel

from .models_base import ICON_HELP, SEOFields


class AboutPage(SingletonModel, SEOFields):
    hero_title = models.CharField('Заголовок першого екрана', max_length=200, default='Про компанію')
    hero_text = models.TextField('Текст першого екрана', blank=True)
    hero_image = WebPImageField('Зображення першого екрана', upload_to='pages/about/', blank=True)
    hero_cta = models.CharField('Основна кнопка', max_length=80, default='Обговорити завдання')
    hero_cta_secondary = models.CharField('Друга кнопка', max_length=80, default='Наша команда')
    hero_cta_secondary_href = models.CharField('Посилання другої кнопки', max_length=80, default='#team')
    intro_title = models.CharField('Заголовок «Про нас»', max_length=200, default='Про нас')
    intro_text = models.TextField('Текст «Про нас»', blank=True)
    principles_title = models.CharField('Заголовок принципів', max_length=200, default='Принципи')
    team_title = models.CharField('Заголовок команди', max_length=200, default='Команда')
    team_lead = models.TextField('Лід команди', blank=True)
    expertise_label = models.CharField('Підпис експертизи', max_length=80, default='Ключова експертиза')
    career_label = models.CharField('Підпис шляху', max_length=80, default='Професійний шлях')
    science_eyebrow = models.CharField('Надзаголовок науки', max_length=80, blank=True, default='Наукова основа')
    science_title = models.CharField('Заголовок методології', max_length=200, default='Методологія та партнери')
    science_text = models.TextField('Текст методології', blank=True)
    science_doi_url = models.URLField('DOI посилання', blank=True)
    science_doi_label = models.CharField('DOI підпис', max_length=200, blank=True)
    partners_eyebrow = models.CharField('Надзаголовок партнерів', max_length=80, blank=True, default='Міжнародна діяльність')
    partners_title = models.CharField('Заголовок партнерів', max_length=200, blank=True)
    partners_text = models.TextField('Текст партнерів', blank=True)
    stats_title = models.CharField('Заголовок цифр', max_length=200, default='Ключові цифри')
    process_title = models.CharField('Заголовок процесу', max_length=200, default='Як ми працюємо')

    class Meta:
        verbose_name = 'Про компанію'
        verbose_name_plural = 'Про компанію'
        constraints = [models.CheckConstraint(condition=models.Q(id=1), name='aboutpage_singleton')]

    def __str__(self):
        return 'Про компанію'

    @property
    def intro_figures(self):
        return self.stats.filter(block=AboutStat.BLOCK_INTRO)

    @property
    def key_stats(self):
        return self.stats.filter(block=AboutStat.BLOCK_KEY)


class AboutPrinciple(models.Model):
    page = models.ForeignKey(AboutPage, on_delete=models.CASCADE, related_name='principles')
    icon = models.CharField('Іконка', max_length=64, default='HiconOutlineShieldTick', help_text=ICON_HELP)
    title = models.CharField('Заголовок', max_length=120)
    text = models.TextField('Текст')
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Принцип'
        verbose_name_plural = 'Принципи'

    def __str__(self):
        return self.title


class TeamMember(models.Model):
    page = models.ForeignKey(AboutPage, on_delete=models.CASCADE, related_name='team')
    name = models.CharField("Імʼя", max_length=120)
    role = models.CharField('Посада', max_length=300)
    regalia = models.CharField('Регалії', max_length=400, blank=True)
    email = models.EmailField('Email', blank=True)
    bio = models.TextField('Біографія', blank=True)
    photo = WebPImageField('Фото', upload_to='pages/team/', blank=True)
    photo_position = models.CharField('Позиція фото', max_length=32, blank=True, default='50% 20%')
    expertise = models.JSONField('Ключова експертиза', default=list, blank=True)
    career_path = models.JSONField('Професійний шлях', default=list, blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Член команди'
        verbose_name_plural = 'Команда'

    def __str__(self):
        return self.name


class AboutStat(models.Model):
    BLOCK_INTRO = 'intro'
    BLOCK_KEY = 'key'
    BLOCK_CHOICES = (
        (BLOCK_INTRO, 'Про нас (стрічка)'),
        (BLOCK_KEY, 'Ключові цифри'),
    )

    page = models.ForeignKey(AboutPage, on_delete=models.CASCADE, related_name='stats')
    block = models.CharField('Блок', max_length=16, choices=BLOCK_CHOICES, default=BLOCK_KEY, db_index=True)
    value = models.CharField('Значення', max_length=40)
    label = models.CharField('Підпис', max_length=160)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Цифра'
        verbose_name_plural = 'Цифри'

    def __str__(self):
        return f'{self.value} {self.label}'


class AboutIntroStat(AboutStat):
    class Meta:
        proxy = True
        verbose_name = 'Цифра стрічки'
        verbose_name_plural = 'Цифри стрічки «Про нас»'


class AboutKeyStat(AboutStat):
    class Meta:
        proxy = True
        verbose_name = 'Ключова цифра'
        verbose_name_plural = 'Ключові цифри'


class AboutProcessStep(models.Model):
    page = models.ForeignKey(AboutPage, on_delete=models.CASCADE, related_name='process_steps')
    number = models.CharField('Номер', max_length=8, default='01')
    title = models.CharField('Заголовок', max_length=120)
    text = models.CharField('Текст', max_length=300)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Крок процесу (про нас)'
        verbose_name_plural = 'Кроки процесу (про нас)'

    def __str__(self):
        return f'{self.number} {self.title}'
