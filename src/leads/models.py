from django.core.validators import MaxLengthValidator
from django.db import models

LEAD_MESSAGE_MAX_LENGTH = 2000


class Lead(models.Model):
    class Status(models.TextChoices):
        NEW = 'new', 'Новий лід'
        IN_PROGRESS = 'in_progress', 'В роботі'
        DONE = 'done', 'Оброблено'
        SPAM = 'spam', 'Спам'

    name = models.CharField("Імʼя", max_length=120)
    phone = models.CharField('Телефон', max_length=40)
    email = models.EmailField('Email')
    message = models.TextField(
        'Повідомлення',
        blank=True,
        validators=[MaxLengthValidator(LEAD_MESSAGE_MAX_LENGTH)],
    )
    consent = models.BooleanField('Згода на обробку даних', default=False)
    source_page = models.CharField('Сторінка-джерело', max_length=200, blank=True)
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
    )
    created_at = models.DateTimeField('Створено', auto_now_add=True)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.phone}'


class LeadModal(models.Model):
    title = models.CharField('Заголовок вікна', max_length=120, default='Залишити заявку')
    lead = models.TextField(
        'Лід вікна',
        default=(
            "Опишіть ситуацію — ми звʼяжемося, щоб уточнити завдання. "
            'Факт звернення залишається конфіденційним.'
        ),
    )
    name_label = models.CharField('Підпис імені', max_length=80, default="Імʼя")
    phone_label = models.CharField('Підпис телефону', max_length=80, default='Телефон')
    email_label = models.CharField('Підпис email', max_length=80, default='Email')
    message_label = models.CharField('Підпис повідомлення', max_length=120, default='Коротко про завдання')
    phone_placeholder = models.CharField('Плейсхолдер телефону', max_length=40, blank=True, default='+380 XX XXX XX XX')
    email_placeholder = models.CharField('Плейсхолдер email', max_length=80, blank=True, default='user@domain.com')
    message_placeholder = models.CharField('Плейсхолдер повідомлення', max_length=160, blank=True)
    consent_prefix = models.CharField(
        'Текст згоди',
        max_length=240,
        default='Погоджуюся на обробку персональних даних відповідно до',
    )
    submit_label = models.CharField('Кнопка надсилання', max_length=80, default='Надіслати заявку')
    thanks_title = models.CharField('Заголовок подяки', max_length=120, default='Дякуємо за заявку')
    thanks_text = models.TextField(
        'Текст подяки',
        default=(
            'Ми отримали ваше звернення і звʼяжемося найближчим часом. '
            'Факт звернення залишається конфіденційним.'
        ),
    )

    class Meta:
        verbose_name = 'Вікно заявки'
        verbose_name_plural = 'Вікно заявки'

    def __str__(self):
        return self.title or 'Вікно заявки'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
