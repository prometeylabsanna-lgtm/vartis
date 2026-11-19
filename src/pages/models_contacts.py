from django.db import models

from src.core.fields import WebPImageField
from src.core.models import SingletonModel

from .models_base import SEOFields


class ContactsPage(SingletonModel, SEOFields):
    hero_title = models.CharField('Заголовок першого екрана', max_length=200, default='Контакти')
    hero_text = models.TextField('Текст першого екрана', blank=True)
    hero_image = WebPImageField('Зображення першого екрана', upload_to='pages/contacts/', blank=True)
    cta_primary = models.CharField('Основна кнопка', max_length=80, default='Залишити заявку')
    cta_secondary = models.CharField('Друга кнопка', max_length=80, default='Як звʼязатися')
    info_title = models.CharField('Заголовок блоку', max_length=200, default='Контактні дані')
    phone_label = models.CharField('Підпис телефону', max_length=40, default='Телефон')
    email_label = models.CharField('Підпис email', max_length=40, default='Email')
    facebook_label = models.CharField('Підпис Facebook', max_length=40, default='Facebook')
    whatsapp_label = models.CharField('Підпис WhatsApp', max_length=40, default='WhatsApp')
    signal_label = models.CharField('Підпис Signal', max_length=40, default='Signal')
    telegram_label = models.CharField('Підпис Telegram', max_length=40, default='Telegram')
    phone_hint = models.CharField('Підказка телефону', max_length=120, default='Натисніть, щоб зателефонувати')
    email_hint = models.CharField('Підказка email', max_length=120, default='Відкриє поштову програму')
    whatsapp_hint = models.CharField('Підказка WhatsApp', max_length=120, default='Відкриє чат на номер телефону')
    signal_hint = models.CharField('Підказка Signal', max_length=120, default='Відкриє чат на номер телефону')
    telegram_hint = models.CharField('Підказка Telegram', max_length=120, default='Відкриє чат компанії')
    write_label = models.CharField('Підпис дії месенджера', max_length=40, default='Написати')
    office_label = models.CharField('Підпис адреси', max_length=80, default='Адреса офісу')
    office_note = models.TextField(
        'Примітка про офіс',
        blank=True,
        default='Першу розмову щодо захисту інформації ми радимо проводити поза приміщенням, про яке йдеться.',
    )
    office_cta = models.CharField('Кнопка біля адреси', max_length=80, default='Залишити заявку')

    class Meta:
        verbose_name = 'Контакти'
        verbose_name_plural = 'Контакти'
        constraints = [models.CheckConstraint(condition=models.Q(id=1), name='contactspage_singleton')]

    def __str__(self):
        return 'Контакти'


class PrivacyPage(SingletonModel, SEOFields):
    hero_title = models.CharField('Заголовок першого екрана', max_length=200, default='Політика конфіденційності')
    hero_text = models.TextField(
        'Текст першого екрана',
        blank=True,
        default='Як ми обробляємо та захищаємо персональні дані, які ви залишаєте на сайті',
    )
    body = models.TextField('Текст політики', blank=True)

    class Meta:
        verbose_name = 'Політика конфіденційності'
        verbose_name_plural = 'Політика конфіденційності'
        constraints = [models.CheckConstraint(condition=models.Q(id=1), name='privacypage_singleton')]

    def __str__(self):
        return 'Політика конфіденційності'
