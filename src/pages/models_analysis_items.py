from django.db import models

from .models_analysis import AnalysisPage


class AnalysisStep(models.Model):
    page = models.ForeignKey(AnalysisPage, on_delete=models.CASCADE, related_name='steps')
    number = models.CharField('Номер', max_length=8, default='01')
    title = models.CharField('Заголовок', max_length=120)
    text = models.TextField('Текст', blank=True)
    bullets = models.TextField('Пункти (рядок = пункт)', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Крок VI Analysis'
        verbose_name_plural = 'Кроки VI Analysis'

    def bullet_list(self):
        return [b.strip() for b in self.bullets.splitlines() if b.strip()]

    def __str__(self):
        return f'{self.number} {self.title}'


class AnalysisRisk(models.Model):
    page = models.ForeignKey(AnalysisPage, on_delete=models.CASCADE, related_name='risks')
    tag = models.CharField('Мітка', max_length=120, blank=True)
    title = models.CharField('Заголовок', max_length=160)
    text = models.TextField('Текст', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Ризик VI Analysis'
        verbose_name_plural = 'Ризики VI Analysis'

    def __str__(self):
        return self.title


class AnalysisRiskLevel(models.Model):
    page = models.ForeignKey(AnalysisPage, on_delete=models.CASCADE, related_name='risk_levels')
    level = models.CharField('Рівень', max_length=40)
    tone = models.CharField('Тон', max_length=16, default='mid')
    meaning = models.CharField('Значення', max_length=200)
    action = models.CharField('Дія', max_length=120)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Рівень ризику'
        verbose_name_plural = 'Рівні ризику'

    def __str__(self):
        return self.level


class AnalysisRec(models.Model):
    page = models.ForeignKey(AnalysisPage, on_delete=models.CASCADE, related_name='recs')
    title = models.CharField('Заголовок', max_length=80)
    tone = models.CharField('Тон', max_length=16, default='ok')
    text = models.CharField('Текст', max_length=200)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Варіант рекомендації'
        verbose_name_plural = 'Варіанти рекомендації'

    def __str__(self):
        return self.title


class AnalysisInclude(models.Model):
    page = models.ForeignKey(AnalysisPage, on_delete=models.CASCADE, related_name='includes')
    title = models.CharField('Заголовок', max_length=160)
    text = models.TextField('Текст', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Що входить (VI Analysis)'
        verbose_name_plural = 'Що входить (VI Analysis)'

    def __str__(self):
        return self.title


class AnalysisPaketStep(models.Model):
    page = models.ForeignKey(AnalysisPage, on_delete=models.CASCADE, related_name='paket_steps')
    number = models.CharField('Номер', max_length=8, default='01')
    title = models.CharField('Заголовок', max_length=120)
    text = models.TextField('Текст', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Крок пакета'
        verbose_name_plural = 'Кроки пакета'

    def __str__(self):
        return f'{self.number} {self.title}'


class AnalysisWhy(models.Model):
    page = models.ForeignKey(AnalysisPage, on_delete=models.CASCADE, related_name='why_items')
    number = models.CharField('Номер', max_length=8, default='01')
    title = models.CharField('Заголовок', max_length=160)
    text = models.TextField('Текст', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Чому вигідно (VI Analysis)'
        verbose_name_plural = 'Чому вигідно (VI Analysis)'

    def __str__(self):
        return f'{self.number} {self.title}'


class AnalysisPricePart(models.Model):
    page = models.ForeignKey(AnalysisPage, on_delete=models.CASCADE, related_name='price_parts')
    number = models.CharField('№', max_length=8, default='1')
    title = models.CharField('Назва', max_length=120)
    when = models.CharField('Коли', max_length=80, blank=True)
    text = models.TextField('Текст', blank=True)
    price = models.CharField('Ціна', max_length=120, blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Складова ціни'
        verbose_name_plural = 'Складові ціни'

    def __str__(self):
        return self.title


class AnalysisTariff(models.Model):
    page = models.ForeignKey(AnalysisPage, on_delete=models.CASCADE, related_name='tariffs')
    name = models.CharField('Назва', max_length=80)
    subtitle = models.CharField('Підзаголовок', max_length=120, blank=True)
    featured = models.BooleanField('Акцентний', default=False)
    price = models.CharField('Ціна', max_length=80, blank=True)
    period = models.CharField('Період', max_length=80, blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Тариф VI Analysis'
        verbose_name_plural = 'Тарифи VI Analysis'

    def __str__(self):
        return self.name


class AnalysisTariffLine(models.Model):
    tariff = models.ForeignKey(AnalysisTariff, on_delete=models.CASCADE, related_name='lines')
    label = models.CharField('Параметр', max_length=160)
    value = models.CharField('Значення', max_length=80)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Рядок тарифу'
        verbose_name_plural = 'Рядки тарифу'

    def __str__(self):
        return f'{self.label}: {self.value}'


class AnalysisPayTerm(models.Model):
    page = models.ForeignKey(AnalysisPage, on_delete=models.CASCADE, related_name='pay_terms')
    title = models.CharField('Заголовок', max_length=120)
    text = models.TextField('Текст', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Умова оплати'
        verbose_name_plural = 'Умови оплати'

    def __str__(self):
        return self.title


class AnalysisPriceRow(models.Model):
    """Залишено для вже збережених рядків. На сайті використовуються складові ціни й тарифи."""

    page = models.ForeignKey(AnalysisPage, on_delete=models.CASCADE, related_name='price_rows')
    number = models.CharField('№', max_length=8, default='1')
    title = models.CharField('Складова', max_length=120)
    period = models.CharField('Період', max_length=80, blank=True)
    description = models.TextField('Що входить', blank=True)
    price_note = models.CharField('Як рахується', max_length=200, blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Старий рядок тарифу'
        verbose_name_plural = 'Старі рядки тарифу'

    def __str__(self):
        return self.title
