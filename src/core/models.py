from django.db import models

from src.core.models_cms import PageStyle, SiteBlock

__all__ = [
    'SingletonModel',
    'SiteSettings',
    'SiteBlock',
    'PageStyle',
]


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SiteSettings(SingletonModel):
    company_name = models.CharField('Назва компанії', max_length=200, default='ТОВ «ВАРТІС ІНТЕЛІДЖЕНС»')
    tagline = models.CharField(
        'Слоган',
        max_length=300,
        default='Стратегічна аналітика, OSINT, корпоративна безпека та аналіз ризиків',
    )
    logo = models.ImageField(
        'Логотип сайту',
        upload_to='site/',
        blank=True,
        help_text='PNG/SVG/WebP. Якщо порожньо — стандартний логотип із статичних файлів.',
    )
    phone = models.CharField('Телефон', max_length=50, blank=True)
    email = models.EmailField('Email', blank=True)
    address = models.CharField('Адреса', max_length=300, blank=True)
    map_embed_url = models.URLField('URL карти (embed)', blank=True)
    facebook_url = models.URLField('Facebook', blank=True)
    default_seo_title = models.CharField(
        'SEO Title за замовчуванням',
        max_length=200,
        default='Перевірка контрагентів та стратегічна аналітика | VARTIS INTELLIGENCE',
    )
    default_seo_description = models.TextField(
        'SEO Description за замовчуванням',
        default=(
            'Перевірка контрагентів, OSINT і стратегічна аналітика для бізнесу. '
            'Виявляємо приховані ризики та допомагаємо ухвалювати обґрунтовані рішення.'
        ),
    )
    footer_cta_title = models.CharField(
        'Заголовок CTA у футері',
        max_length=120,
        default='Залишити заявку',
    )
    footer_cta_text = models.TextField(
        'Текст CTA у футері',
        default=(
            "Опишіть ситуацію — ми зв'яжемося, щоб уточнити завдання. "
            'Факт звернення залишається конфіденційним.'
        ),
    )

    class Meta:
        verbose_name = 'Налаштування сайту'
        verbose_name_plural = 'Налаштування сайту'
        constraints = [
            models.CheckConstraint(condition=models.Q(id=1), name='sitesettings_singleton'),
        ]

    def __str__(self):
        return self.company_name
