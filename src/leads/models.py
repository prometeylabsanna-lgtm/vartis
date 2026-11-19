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
