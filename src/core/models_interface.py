"""Тексти інтерфейсу, яких немає в контентних моделях сторінок."""

from django.db import models

from src.core.models import SingletonModel


class InterfaceCopy(SingletonModel):
    lang_switch_aria = models.CharField('Підпис перемикача мов', max_length=80, default='Мова')
    cookie_title = models.CharField('Заголовок cookie', max_length=80, default='Файли cookie')
    cookie_body = models.TextField(
        'Текст cookie',
        default=(
            'Ми використовуємо файли cookie для аналітики відвідувань і роботи сайту. '
            'Натискаючи «Прийняти», ви погоджуєтесь на їх використання. Деталі — у'
        ),
    )
    cookie_more_label = models.CharField('Кнопка «Детальніше»', max_length=80, default='Детальніше')
    cookie_accept_label = models.CharField('Кнопка «Прийняти»', max_length=80, default='Прийняти')
    cookie_settings_label = models.CharField(
        'Налаштування cookie', max_length=80, default='Налаштування cookie',
    )
    cookie_again_label = models.CharField(
        'Показати банер знову', max_length=120, default='Показати банер cookie знову',
    )
    developed_label = models.CharField('Підпис розробника', max_length=40, default='Розроблено')
    back_to_top = models.CharField('Кнопка вгору', max_length=40, default='Вгору')
    back_to_top_aria = models.CharField(
        'Підказка кнопки вгору', max_length=80, default='Повернутися вгору',
    )
    crumb_home = models.CharField('Крихта «Головна»', max_length=40, default='Головна')
    crumbs_aria = models.CharField('Підпис крихт', max_length=80, default='Хлібні крихти')
    logo_home_aria = models.CharField(
        'Підпис логотипа', max_length=120, default='VARTIS INTELLIGENCE — на головну',
    )
    nav_main_aria = models.CharField('Підпис навігації', max_length=80, default='Основна навігація')
    services_list_aria = models.CharField('Підпис списку послуг', max_length=80, default='Список послуг')
    menu_open_aria = models.CharField('Підпис меню', max_length=80, default='Відкрити меню')
    footer_nav_aria = models.CharField(
        'Підпис навігації у футері', max_length=80, default='Навігація у футері',
    )
    footer_services_aria = models.CharField(
        'Підпис послуг у футері', max_length=80, default='Послуги у футері',
    )
    mobile_nav_aria = models.CharField(
        'Підпис мобільного меню', max_length=80, default='Мобільна навігація',
    )
    photo_lightbox_aria = models.CharField('Підпис перегляду фото', max_length=80, default='Перегляд фото')
    photo_close_aria = models.CharField('Закрити фото', max_length=40, default='Закрити')
    modal_close_aria = models.CharField('Закрити вікно', max_length=40, default='Закрити')
    form_aria = models.CharField('Підпис форми', max_length=80, default='Форма заявки у вікні')
    pagination_aria = models.CharField('Підпис пагінації', max_length=40, default='Сторінки')
    feed_filter_aria = models.CharField('Підпис фільтра', max_length=80, default='Фільтр за темою')
    dir_prev_aria = models.CharField('Попередні послуги', max_length=80, default='Попередні послуги')
    dir_next_aria = models.CharField('Наступні послуги', max_length=80, default='Наступні послуги')
    profile_services_aria = models.CharField(
        'Профільні послуги', max_length=80, default='Профільні послуги',
    )
    map_title = models.CharField('Підпис карти', max_length=120, default='Карта розташування офісу')
    article_section_aria = models.CharField('Підпис статті', max_length=80, default='Текст статті')
    feed_section_aria = models.CharField('Підпис стрічки', max_length=80, default='Стрічка статей')
    catalog_aria = models.CharField('Підпис каталогу', max_length=80, default='Каталог послуг')
    privacy_section_aria = models.CharField('Підпис політики', max_length=80, default='Текст політики')
    share_label = models.CharField('Поділитися', max_length=40, default='Поділитися')
    copy_link_label = models.CharField(
        'Скопіювати посилання', max_length=80, default='Скопіювати посилання',
    )
    copied_label = models.CharField('Скопійовано', max_length=40, default='Скопійовано')
    new_badge = models.CharField('Бейдж «Нове»', max_length=40, default='Нове')
    cover_alt_prefix = models.CharField('Alt обкладинки', max_length=40, default='Обкладинка:')
    service_alt_prefix = models.CharField(
        'Alt ілюстрації послуги', max_length=80, default='Ілюстрація послуги:',
    )
    direction_alt_prefix = models.CharField('Alt фото напряму', max_length=80, default='Фото напряму:')
    err404_meta_title = models.CharField(
        'Title 404', max_length=160, default='Сторінку не знайдено — VARTIS INTELLIGENCE',
    )
    err404_title = models.CharField('Заголовок 404', max_length=120, default='Сторінку не знайдено')
    err404_text = models.TextField(
        'Текст 404',
        default=(
            'Можливо, адресу введено з помилкою або сторінку було переміщено. '
            'Поверніться на головну або оберіть потрібний розділ у меню.'
        ),
    )
    err404_primary = models.CharField('Кнопка 404', max_length=80, default='На головну')
    err404_secondary = models.CharField('Друга кнопка 404', max_length=80, default='Наші послуги')

    class Meta:
        verbose_name = 'Інтерфейс'
        verbose_name_plural = 'Інтерфейс'
        constraints = [
            models.CheckConstraint(condition=models.Q(id=1), name='interfacecopy_singleton'),
        ]

    def __str__(self):
        return 'Інтерфейс'
