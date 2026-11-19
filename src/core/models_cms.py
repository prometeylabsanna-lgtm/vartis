"""CMS: SiteBlock та PageStyle."""

from __future__ import annotations

from django.core.cache import cache
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from src.core.fields import WebPImageField
from src.core.hero_chrome import (
    DEFAULT_HERO_OPACITY as HERO_OPACITY_DEFAULT,
    DEFAULT_HERO_PANEL as HERO_PANEL_DEFAULT,
    DEFAULT_HERO_TEXT as HERO_TEXT_DEFAULT,
    clamp_opacity,
    hex_to_rgba,
)

SITE_BLOCKS_CACHE_KEY = 'vartis_site_blocks_v1'


def clear_site_blocks_cache() -> None:
    cache.delete(SITE_BLOCKS_CACHE_KEY)


class SiteBlock(models.Model):
    class ContentType(models.TextChoices):
        TEXT = 'text', 'Текст'
        IMAGE = 'image', 'Зображення'
        URL = 'url', 'Посилання'
        VIDEO = 'video', 'Відео'

    class Page(models.TextChoices):
        HOME = 'home', 'Головна'
        ABOUT = 'about', 'Про компанію'
        SERVICES = 'services', 'Послуги'
        ANALYSIS = 'analysis', 'VI Analysis'
        CONTACTS = 'contacts', 'Контакти'
        PRIVACY = 'privacy', 'Політика'
        SITE = 'site', 'Сайт'
        BLOG = 'blog', 'Блог'
        CASES = 'cases', 'Кейси'

    page = models.CharField('Сторінка', max_length=32, choices=Page.choices)
    key = models.CharField('Ключ блоку', max_length=64)
    label = models.CharField('Назва в адмінці', max_length=128, blank=True)
    content_type = models.CharField(
        'Тип',
        max_length=16,
        choices=ContentType.choices,
        default=ContentType.TEXT,
    )
    text_html = models.TextField('Текст', blank=True)
    image = WebPImageField('Зображення', upload_to='blocks/', blank=True)
    link_url = models.CharField('URL посилання', max_length=512, blank=True)
    link_label = models.CharField('Текст посилання', max_length=128, blank=True)
    sort_order = models.PositiveSmallIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активний', default=True)

    class Meta:
        ordering = ['page', 'sort_order', 'key']
        verbose_name = 'Блок контенту'
        verbose_name_plural = 'Блоки контенту'
        constraints = [
            models.UniqueConstraint(fields=['page', 'key'], name='unique_vartis_site_block_page_key'),
        ]

    def __str__(self) -> str:
        return f'{self.page}.{self.key}'

    @property
    def cache_key(self) -> str:
        return f'{self.page}.{self.key}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        clear_site_blocks_cache()


class PageStyle(models.Model):
    # Світла тема як у макеті Home.dc (білий фон + темний текст).
    DEFAULT_BACKGROUND = '#ffffff'
    DEFAULT_TEXT = '#12263a'
    DEFAULT_ACCENT = '#b58b4a'
    DEFAULT_HERO_TEXT = HERO_TEXT_DEFAULT
    DEFAULT_HERO_PANEL = HERO_PANEL_DEFAULT
    DEFAULT_HERO_OPACITY = HERO_OPACITY_DEFAULT

    page = models.CharField(
        'Сторінка',
        max_length=32,
        choices=SiteBlock.Page.choices,
        unique=True,
    )
    background_color = models.CharField(
        'Колір фону',
        max_length=32,
        blank=True,
        help_text='HEX. Порожнє — дефолт сайту.',
    )
    text_color = models.CharField(
        'Колір тексту',
        max_length=32,
        blank=True,
        help_text='HEX. Порожнє — дефолт сайту.',
    )
    accent_color = models.CharField(
        'Колір акценту',
        max_length=32,
        blank=True,
        help_text='HEX. Порожнє — дефолт сайту.',
    )
    background_image = WebPImageField(
        'Фонове зображення',
        upload_to='blocks/page-style/',
        blank=True,
    )
    glass_enabled = models.BooleanField('Скло (glass)', default=False)
    hero_text_color = models.CharField(
        'Колір тексту на баннері',
        max_length=32,
        blank=True,
        help_text='Лише баннер. Порожнє — білий як у макеті.',
    )
    hero_panel_color = models.CharField(
        'Колір скла баннера',
        max_length=32,
        blank=True,
        help_text='Лише баннер. Порожнє — біле скло макета.',
    )
    hero_panel_opacity = models.PositiveSmallIntegerField(
        'Прозорість скла, %',
        default=DEFAULT_HERO_OPACITY,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text='10 — скло як у макеті. 80+ виглядає як суцільна панель.',
    )

    class Meta:
        ordering = ['page']
        verbose_name = 'Стиль сторінки'
        verbose_name_plural = 'Стилі сторінок'

    def __str__(self) -> str:
        return f'Стиль: {self.get_page_display()}'

    @classmethod
    def for_page(cls, page: str) -> PageStyle:
        obj, _ = cls.objects.get_or_create(
            page=page,
            defaults={'glass_enabled': False},
        )
        return obj

    @property
    def effective_background(self) -> str:
        return (self.background_color or '').strip() or self.DEFAULT_BACKGROUND

    @property
    def effective_text(self) -> str:
        return (self.text_color or '').strip() or self.DEFAULT_TEXT

    @property
    def effective_accent(self) -> str:
        return (self.accent_color or '').strip() or self.DEFAULT_ACCENT

    @property
    def effective_hero_text(self) -> str:
        return (self.hero_text_color or '').strip() or self.DEFAULT_HERO_TEXT

    @property
    def effective_hero_panel(self) -> str:
        return (self.hero_panel_color or '').strip() or self.DEFAULT_HERO_PANEL

    @property
    def effective_hero_opacity(self) -> int:
        return clamp_opacity(self.hero_panel_opacity)

    def hero_panel_rgba(self) -> str:
        return hex_to_rgba(self.effective_hero_panel, self.effective_hero_opacity)

    def hero_text_muted_rgba(self) -> str:
        return hex_to_rgba(self.effective_hero_text, 75, fallback=self.DEFAULT_HERO_TEXT)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        clear_site_blocks_cache()
