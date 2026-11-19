from django.db import models

from src.core.fields import WebPImageField
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
    logo = WebPImageField(
        'Логотип сайту',
        upload_to='site/',
        blank=True,
        help_text='PNG/JPG → WebP автоматично. SVG без змін. Якщо порожньо — логотип зі static.',
    )
    phone = models.CharField('Телефон', max_length=50, blank=True)
    email = models.EmailField('Email', blank=True)
    address = models.CharField('Адреса', max_length=300, blank=True)
    map_embed_url = models.URLField('URL карти (embed)', blank=True)
    facebook_url = models.URLField('Facebook', blank=True)
    telegram_chat_url = models.URLField(
        'Telegram: посилання на чат компанії',
        blank=True,
        help_text=(
            'Посилання, яке відкриває чат компанії в Telegram, напр. https://t.me/назва_чату. '
            'Якщо порожньо — використовується запасне посилання нижче (за номером). '
            'Номер на сайті не показується.'
        ),
    )
    telegram_url = models.URLField(
        'Telegram: запасне посилання (за номером)',
        blank=True,
        help_text=(
            'Використовується, лише якщо поле «Telegram: посилання на чат компанії» порожнє. '
            'Номер на сайті не показується.'
        ),
    )
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
            "Опишіть ситуацію — ми звʼяжемося, щоб уточнити завдання. "
            'Факт звернення залишається конфіденційним.'
        ),
    )
    nav_about = models.CharField('Пункт «Про компанію»', max_length=80, default='Про компанію')
    nav_services = models.CharField('Пункт «Послуги»', max_length=80, default='Послуги')
    nav_cases = models.CharField('Пункт «Кейси»', max_length=80, default='Кейси')
    nav_blog = models.CharField('Пункт «Блог»', max_length=80, default='Блог')
    nav_contacts = models.CharField('Пункт «Контакти»', max_length=80, default='Контакти')
    header_cta = models.CharField('Кнопка в шапці', max_length=80, default='Залишити заявку')
    mobile_lead = models.CharField(
        'Текст у мобільному меню',
        max_length=200,
        default='Стратегічна аналітика, перевірка контрагентів та захист бізнесу',
    )
    mobile_cta_secondary = models.CharField('Друга кнопка меню', max_length=80, default='Обговорити завдання')
    footer_col_company = models.CharField('Колонка «Компанія»', max_length=80, default='Компанія')
    footer_col_services = models.CharField('Колонка «Послуги»', max_length=80, default='Послуги')
    footer_phone_label = models.CharField('Підпис телефону', max_length=40, default='Тел')
    footer_email_label = models.CharField('Підпис email', max_length=40, default='Email')
    footer_address_label = models.CharField('Підпис адреси', max_length=40, default='Адреса')
    footer_whatsapp_label = models.CharField('Підпис WhatsApp', max_length=40, default='WhatsApp')
    footer_signal_label = models.CharField('Підпис Signal', max_length=40, default='Signal')
    footer_telegram_label = models.CharField('Підпис Telegram', max_length=40, default='Telegram')
    footer_write_label = models.CharField('Підпис дії месенджера', max_length=40, default='Написати')
    privacy_link_label = models.CharField(
        'Посилання на політику',
        max_length=80,
        default='Політика конфіденційності',
    )

    class Meta:
        verbose_name = 'Налаштування сайту'
        verbose_name_plural = 'Налаштування сайту'
        constraints = [
            models.CheckConstraint(condition=models.Q(id=1), name='sitesettings_singleton'),
        ]

    def __str__(self):
        return self.company_name


from src.core import cms_proxies as _cms_proxies  # noqa: E402,F401
