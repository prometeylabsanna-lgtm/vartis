from django.db import models

from .models_services import ServicePage

DEEP_SLUG = 'zbir-ta-analiz-informatsii'


class DeepAnalytics(models.Model):
    page = models.OneToOneField(ServicePage, on_delete=models.CASCADE, related_name='deep')
    h1 = models.CharField('H1', max_length=200, blank=True, default='Глибока аналітика')
    hero_text = models.TextField('Текст першого екрана', blank=True)
    cta_primary = models.CharField('Основна кнопка', max_length=120, blank=True, default='Обговорити завдання')
    cta_secondary = models.CharField('Друга кнопка', max_length=120, blank=True, default='Приклад звіту')
    cta_secondary_href = models.CharField('Посилання другої кнопки', max_length=80, blank=True, default='#example')
    strategy_eyebrow = models.CharField('Надзаголовок стратегії', max_length=120, blank=True)
    strategy_title = models.CharField('Заголовок стратегії', max_length=200, blank=True)
    compare_express_eyebrow = models.CharField('Надзаголовок експрес', max_length=160, blank=True)
    compare_express_title = models.CharField('Заголовок експрес', max_length=200, blank=True)
    compare_express_text = models.TextField('Текст експрес', blank=True)
    compare_express_link = models.CharField('Посилання експрес', max_length=80, blank=True)
    compare_deep_eyebrow = models.CharField('Надзаголовок глибокої', max_length=160, blank=True)
    compare_deep_title = models.CharField('Заголовок глибокої', max_length=200, blank=True)
    compare_deep_text = models.TextField('Текст глибокої', blank=True)
    nda_title = models.CharField('Заголовок NDA', max_length=200, blank=True)
    nda_text = models.TextField('Текст NDA', blank=True)
    nda_note = models.TextField('Примітка NDA', blank=True)
    get_title = models.CharField('Заголовок результату', max_length=200, blank=True)
    get_lead = models.TextField('Лід результату', blank=True)
    example_title = models.CharField('Заголовок прикладу', max_length=200, blank=True)
    example_lead = models.TextField('Лід прикладу', blank=True)
    ex_frag1 = models.CharField('Фрагмент 1', max_length=200, blank=True)
    ex_frag3 = models.CharField('Фрагмент 3', max_length=200, blank=True)
    ex_frag3_lead = models.TextField('Лід фрагмента 3', blank=True)
    ex_frag4 = models.CharField('Фрагмент 4', max_length=200, blank=True)
    ex_frag4_lead = models.TextField('Лід фрагмента 4', blank=True)
    facts_title = models.CharField('Підпис фактів', max_length=120, default='Встановлені факти')
    conclusion_title = models.CharField('Підпис висновку', max_length=160, default='Висновок і ступінь упевненості')
    assumption_label = models.CharField('Підпис припущення', max_length=40, default='Припущення:')
    why_not_label = models.CharField('Підпис «чому не факт»', max_length=40, default='Чому не факт:')
    ex_assumption = models.TextField('Припущення', blank=True)
    ex_why_not = models.TextField('Чому не факт', blank=True)
    pay_title = models.CharField('Заголовок оплати', max_length=200, blank=True)
    pay_lead = models.TextField('Лід оплати', blank=True)
    paid_label = models.CharField('Підпис «сплачено»', max_length=40, default='Сплачено:')
    before_pay_label = models.CharField('Підпис перед платежем', max_length=80, default='Перед наступним платежем:')
    guarantee_title = models.CharField('Заголовок гарантії', max_length=80, default='Ваша гарантія')
    quality_title = models.CharField('Заголовок якості', max_length=200, blank=True)
    faq_title = models.CharField('Заголовок FAQ', max_length=200, blank=True)
    order_title = models.CharField('Заголовок форми', max_length=200, blank=True)
    order_text = models.TextField('Текст форми', blank=True)
    related_title = models.CharField('Заголовок інших послуг', max_length=120, default='Профільні послуги')

    class Meta:
        verbose_name = 'Глибока аналітика'
        verbose_name_plural = 'Глибока аналітика'

    def __str__(self):
        return 'Глибока аналітика'


class DeepStep(models.Model):
    page = models.ForeignKey(DeepAnalytics, on_delete=models.CASCADE, related_name='steps')
    number = models.CharField('Номер', max_length=8)
    title = models.CharField('Заголовок', max_length=160)
    text = models.CharField('Текст', max_length=240, blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Крок глибокої аналітики'
        verbose_name_plural = 'Кроки глибокої аналітики'

    def __str__(self):
        return f'{self.number} {self.title}'


class DeepGetItem(models.Model):
    page = models.ForeignKey(DeepAnalytics, on_delete=models.CASCADE, related_name='get_items')
    number = models.CharField('Номер', max_length=8)
    title = models.CharField('Заголовок', max_length=160)
    text = models.TextField('Текст', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Пункт результату'
        verbose_name_plural = 'Пункти результату'

    def __str__(self):
        return self.title


class DeepFaq(models.Model):
    page = models.ForeignKey(DeepAnalytics, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField('Питання', max_length=240)
    answer = models.TextField('Відповідь')
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Питання FAQ'
        verbose_name_plural = 'Питання FAQ'

    def __str__(self):
        return self.question


class DeepPayStage(models.Model):
    page = models.ForeignKey(DeepAnalytics, on_delete=models.CASCADE, related_name='pay_stages')
    pct = models.CharField('Частка', max_length=16)
    when = models.CharField('Коли', max_length=80)
    paid = models.CharField('Сплачено', max_length=16)
    stage = models.CharField('Етап', max_length=40)
    title = models.CharField('Заголовок', max_length=160)
    text = models.TextField('Текст', blank=True)
    see = models.TextField('Що бачить клієнт', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Етап оплати'
        verbose_name_plural = 'Етапи оплати'

    def __str__(self):
        return self.title


class DeepQualityItem(models.Model):
    page = models.ForeignKey(DeepAnalytics, on_delete=models.CASCADE, related_name='quality_items')
    title = models.CharField('Заголовок', max_length=160)
    text = models.TextField('Текст', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Аргумент якості'
        verbose_name_plural = 'Аргументи якості'

    def __str__(self):
        return self.title


class DeepSnippet(models.Model):
    class Kind(models.TextChoices):
        STRATEGY = 'strategy', 'Абзац стратегії'
        STAT = 'stat', 'Цифра прикладу'
        NOTE = 'note', 'Примітка прикладу'
        FACT = 'fact', 'Факт'
        LIMIT = 'limit', 'Межа висновку'
        GUARANTEE = 'guarantee', 'Гарантія'

    page = models.ForeignKey(DeepAnalytics, on_delete=models.CASCADE, related_name='snippets')
    kind = models.CharField('Тип', max_length=16, choices=Kind.choices)
    value = models.CharField('Значення', max_length=40, blank=True)
    text = models.TextField('Текст')
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['kind', 'order', 'id']
        verbose_name = 'Фрагмент глибокої аналітики'
        verbose_name_plural = 'Фрагменти глибокої аналітики'

    def __str__(self):
        return f'{self.get_kind_display()}: {self.text[:60]}'
