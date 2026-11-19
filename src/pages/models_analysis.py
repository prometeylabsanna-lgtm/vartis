from django.db import models

from src.core.fields import WebPImageField
from src.core.models import SingletonModel

from .models_base import ICON_HELP, SEOFields


class AnalysisPage(SingletonModel, SEOFields):
    title = models.CharField('Назва', max_length=200, default='VI Analysis')
    hero_title = models.CharField('Заголовок першого екрана', max_length=200, default='VI Analysis')
    hero_text = models.TextField(
        'Текст першого екрана',
        default='Власний сервіс швидкої перевірки контрагентів',
    )
    hero_image = WebPImageField('Зображення першого екрана', upload_to='pages/analysis/', blank=True)
    cta_primary = models.CharField('Основна кнопка', max_length=120, default='Замовити перевірку')
    cta_secondary = models.CharField('Друга кнопка', max_length=120, default='Пакетне обслуговування')
    cta_secondary_href = models.CharField('Посилання другої кнопки', max_length=80, default='#paket')
    steps_eyebrow = models.CharField('Надзаголовок кроків', max_length=200, blank=True)
    steps_leads = models.TextField('Ліди кроків (абзац = порожній рядок)', blank=True)
    steps_title = models.CharField('Заголовок кроків', max_length=200, default='Три кроки від реквізитів до рішення')
    risks_title = models.CharField('Заголовок ризиків', max_length=200, default='Що перевіряє VI ANALYSIS')
    risks_lead = models.TextField('Лід ризиків', blank=True)
    risks_note_title = models.CharField('Заголовок примітки', max_length=160, blank=True)
    risks_note = models.TextField('Примітка про ризики', blank=True)
    recommendation_title = models.CharField('Заголовок рекомендації', max_length=200, default='Рекомендація щодо співпраці')
    recommendation_text = models.TextField('Текст рекомендації', blank=True)
    rec_heading = models.CharField('Заголовок макета', max_length=80, blank=True, default='Рекомендації')
    rec_badge = models.CharField('Бейдж макета', max_length=80, blank=True)
    rec_code = models.CharField('Код макета', max_length=16, blank=True)
    rec_verdict = models.CharField('Вердикт макета', max_length=160, blank=True)
    rec_note = models.CharField('Примітка макета', max_length=240, blank=True)
    rec_flag = models.CharField('Ознака макета', max_length=160, blank=True)
    rec_accept = models.CharField('Кнопка прийняти', max_length=40, blank=True, default='Прийняти')
    rec_reject = models.CharField('Кнопка відхилити', max_length=40, blank=True, default='Відхилити')
    rec_date = models.CharField('Дата макета', max_length=80, blank=True)
    rec_caption = models.CharField('Підпис макета', max_length=160, blank=True)
    result_title = models.CharField('Заголовок результату', max_length=200, default='Що отримує замовник')
    result_text = models.TextField('Текст результату', blank=True)
    result_method_prefix = models.TextField('Текст перед DOI', blank=True)
    result_method_suffix = models.CharField('Текст після DOI', max_length=40, blank=True, default=').')
    result_doi_href = models.URLField('DOI посилання', blank=True)
    result_doi_label = models.CharField('DOI підпис', max_length=200, blank=True)
    paket_eyebrow = models.CharField('Надзаголовок пакета', max_length=240, blank=True)
    paket_title = models.CharField('Заголовок пакета', max_length=200, default='Пакетне обслуговування')
    paket_subtitle = models.CharField('Підзаголовок пакета', max_length=200, default='для постійних клієнтів')
    paket_lead = models.TextField('Лід пакета', blank=True)
    paket_text = models.TextField('Текст пакета', blank=True)
    include_title = models.CharField('Заголовок «Що входить»', max_length=200, default='Що входить до пакета')
    include_lead = models.TextField('Лід «Що входить»', blank=True)
    include_option_eyebrow = models.CharField('Надзаголовок опції', max_length=80, blank=True)
    include_option_title = models.CharField('Заголовок опції', max_length=200, blank=True)
    include_option_text = models.TextField('Текст опції', blank=True)
    why_title = models.CharField('Заголовок «Чому вигідно»', max_length=200, default='Чому це вигідно')
    price_title = models.CharField('Заголовок вартості', max_length=200, default='Скільки це коштує')
    price_lead = models.TextField('Лід вартості', blank=True)
    tariffs_title = models.CharField('Заголовок тарифів', max_length=200, blank=True)
    price_note = models.TextField('Примітка про ціну', blank=True)
    order_title = models.CharField('Заголовок форми', max_length=200, default='Перевірте контрагента до підписання договору')
    order_text = models.TextField('Текст форми', blank=True)
    related_title = models.CharField('Заголовок інших послуг', max_length=120, default='Профільні послуги')
    short = models.CharField('Короткий опис у меню', max_length=200, blank=True)
    card_image = WebPImageField('Зображення картки', upload_to='pages/analysis/', blank=True)
    card_text = models.TextField('Текст картки', blank=True)
    tags = models.CharField('Теги (через |)', max_length=300, blank=True)
    icon = models.CharField('Іконка', max_length=80, blank=True, default='HiconOutlineShieldTick', help_text=ICON_HELP)

    class Meta:
        verbose_name = 'VI Analysis'
        verbose_name_plural = 'VI Analysis'
        constraints = [models.CheckConstraint(condition=models.Q(id=1), name='analysispage_singleton')]

    def __str__(self):
        return 'VI Analysis'

    def tag_list(self):
        return [t.strip() for t in self.tags.split('|') if t.strip()]

    def steps_lead_list(self):
        return [part.strip() for part in (self.steps_leads or '').split('\n\n') if part.strip()]
