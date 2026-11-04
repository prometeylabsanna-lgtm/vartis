from django.db import models

from src.core.models import SingletonModel


class SEOFields(models.Model):
    seo_title = models.CharField('SEO Title', max_length=200, blank=True)
    seo_description = models.TextField('SEO Description', blank=True)
    h1 = models.CharField('H1', max_length=200, blank=True)

    class Meta:
        abstract = True


class HomePage(SingletonModel, SEOFields):
    hero_title = models.CharField('Hero заголовок', max_length=200, default='Стратегічна аналітика для бізнесу')
    hero_text = models.TextField(
        'Hero текст',
        default='Допомагаємо виявляти приховані ризики й ухвалювати обґрунтовані рішення',
    )
    hero_image = models.ImageField('Hero зображення', upload_to='pages/home/', blank=True)
    services_title = models.CharField('Заголовок напрямів', max_length=200, default='Напрями')
    advantages_title = models.CharField('Заголовок переваг', max_length=200, default='Переваги')
    mission_title = models.CharField('Заголовок місії', max_length=200, default='Наша місія')
    mission_text = models.TextField('Текст місії', blank=True)
    mission_image = models.ImageField('Фон місії', upload_to='pages/home/', blank=True)
    process_title = models.CharField('Заголовок процесу', max_length=200, default='Як ми працюємо')
    blog_title = models.CharField('Заголовок блоку блогу', max_length=200, default='Аналітика')

    class Meta:
        verbose_name = 'Головна'
        verbose_name_plural = 'Головна'
        constraints = [models.CheckConstraint(condition=models.Q(id=1), name='homepage_singleton')]

    def __str__(self):
        return 'Головна'


class HomeAdvantage(models.Model):
    page = models.ForeignKey(HomePage, on_delete=models.CASCADE, related_name='advantages')
    title = models.CharField('Заголовок', max_length=120)
    text = models.CharField('Текст', max_length=300)
    icon = models.CharField('Іконка', max_length=80, blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Перевага'
        verbose_name_plural = 'Переваги'

    def __str__(self):
        return self.title


class HomeProcessStep(models.Model):
    page = models.ForeignKey(HomePage, on_delete=models.CASCADE, related_name='process_steps')
    number = models.CharField('Номер', max_length=8, default='01')
    title = models.CharField('Заголовок', max_length=120)
    text = models.CharField('Текст', max_length=300)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Крок процесу'
        verbose_name_plural = 'Кроки процесу'

    def __str__(self):
        return f'{self.number} {self.title}'


class AboutPage(SingletonModel, SEOFields):
    hero_title = models.CharField('Hero заголовок', max_length=200, default='Про компанію')
    hero_text = models.TextField('Hero текст', blank=True)
    hero_image = models.ImageField('Hero зображення', upload_to='pages/about/', blank=True)
    intro_title = models.CharField('Заголовок «Про нас»', max_length=200, default='Про нас')
    intro_text = models.TextField('Текст «Про нас»', blank=True)
    principles_title = models.CharField('Заголовок принципів', max_length=200, default='Принципи')
    team_title = models.CharField('Заголовок команди', max_length=200, default='Команда')
    team_lead = models.TextField('Лід команди', blank=True)
    science_eyebrow = models.CharField('Eyebrow науки', max_length=80, blank=True, default='Наукова основа')
    science_title = models.CharField(
        'Заголовок методології',
        max_length=200,
        default='Методологія та партнери',
    )
    science_text = models.TextField('Текст методології', blank=True)
    science_doi_url = models.URLField('DOI посилання', blank=True)
    science_doi_label = models.CharField('DOI підпис', max_length=200, blank=True)
    partners_eyebrow = models.CharField(
        'Eyebrow партнерів',
        max_length=80,
        blank=True,
        default='Міжнародна діяльність',
    )
    partners_title = models.CharField('Заголовок партнерів', max_length=200, blank=True)
    partners_text = models.TextField('Текст партнерів', blank=True)
    stats_title = models.CharField('Заголовок цифр', max_length=200, default='Ключові цифри')
    process_title = models.CharField('Заголовок процесу', max_length=200, default='Як ми працюємо')

    class Meta:
        verbose_name = 'Про компанію'
        verbose_name_plural = 'Про компанію'
        constraints = [models.CheckConstraint(condition=models.Q(id=1), name='aboutpage_singleton')]

    def __str__(self):
        return 'Про компанію'

    @property
    def intro_figures(self):
        return self.stats.filter(block=AboutStat.BLOCK_INTRO)

    @property
    def key_stats(self):
        return self.stats.filter(block=AboutStat.BLOCK_KEY)


class AboutPrinciple(models.Model):
    page = models.ForeignKey(AboutPage, on_delete=models.CASCADE, related_name='principles')
    icon = models.CharField(
        'Іконка',
        max_length=64,
        default='HiconOutlineShieldTick',
        help_text='Ключ з vartis_icons',
    )
    title = models.CharField('Заголовок', max_length=120)
    text = models.TextField('Текст')
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Принцип'
        verbose_name_plural = 'Принципи'

    def __str__(self):
        return self.title


class TeamMember(models.Model):
    page = models.ForeignKey(AboutPage, on_delete=models.CASCADE, related_name='team')
    name = models.CharField("Ім'я", max_length=120)
    role = models.CharField('Посада', max_length=300)
    regalia = models.CharField('Регалії', max_length=400, blank=True)
    email = models.EmailField('Email', blank=True)
    bio = models.TextField('Біографія', blank=True)
    photo = models.ImageField('Фото', upload_to='pages/team/', blank=True)
    photo_position = models.CharField('Позиція фото', max_length=32, blank=True, default='50% 20%')
    expertise = models.JSONField('Ключова експертиза', default=list, blank=True)
    career_path = models.JSONField('Професійний шлях', default=list, blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Член команди'
        verbose_name_plural = 'Команда'

    def __str__(self):
        return self.name


class AboutStat(models.Model):
    BLOCK_INTRO = 'intro'
    BLOCK_KEY = 'key'
    BLOCK_CHOICES = (
        (BLOCK_INTRO, 'Про нас (стрічка)'),
        (BLOCK_KEY, 'Ключові цифри'),
    )

    page = models.ForeignKey(AboutPage, on_delete=models.CASCADE, related_name='stats')
    block = models.CharField(
        'Блок',
        max_length=16,
        choices=BLOCK_CHOICES,
        default=BLOCK_KEY,
        db_index=True,
    )
    value = models.CharField('Значення', max_length=40)
    label = models.CharField('Підпис', max_length=160)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Цифра'
        verbose_name_plural = 'Цифри'

    def __str__(self):
        return f'{self.value} {self.label}'


class AboutProcessStep(models.Model):
    page = models.ForeignKey(AboutPage, on_delete=models.CASCADE, related_name='process_steps')
    number = models.CharField('Номер', max_length=8, default='01')
    title = models.CharField('Заголовок', max_length=120)
    text = models.CharField('Текст', max_length=300)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Крок процесу (про нас)'
        verbose_name_plural = 'Кроки процесу (про нас)'

    def __str__(self):
        return f'{self.number} {self.title}'


class ServicesIndex(SingletonModel, SEOFields):
    hero_title = models.CharField('Hero заголовок', max_length=200, default='Послуги')
    hero_text = models.TextField(
        'Hero текст',
        default=(
            'Комплексні рішення для бізнесу — від перевірки інформації '
            'до стратегічного аналізу та управління ризиками'
        ),
    )
    hero_image = models.ImageField('Hero зображення', upload_to='pages/services/', blank=True)

    class Meta:
        verbose_name = 'Каталог послуг'
        verbose_name_plural = 'Каталог послуг'
        constraints = [
            models.CheckConstraint(condition=models.Q(id=1), name='servicesindex_singleton'),
        ]

    def __str__(self):
        return 'Каталог послуг'


SERVICE_SLUGS = [
    ('konsaltynh', 'Консалтинг'),
    ('kompleksna-dopomoha-biznesu', 'Комплексна допомога бізнесу'),
    ('zbir-ta-analiz-informatsiyi', 'Глибока аналітика'),
    ('zakhyst-vid-vytoku', 'Захист від витоку інформації'),
    ('kryminalni-provadzhennia', 'Інформаційна підтримка у кримінальних провадженнях'),
]


class ServicePage(SEOFields):
    slug = models.SlugField('Slug', unique=True, choices=SERVICE_SLUGS)
    title = models.CharField('Назва', max_length=200)
    short = models.CharField('Короткий опис', max_length=200, blank=True)
    hero_text = models.TextField('Hero текст', blank=True)
    hero_image = models.ImageField('Hero зображення', upload_to='pages/services/', blank=True)
    scope_title = models.CharField('Заголовок опису', max_length=200, default='Опис напряму')
    scope_text = models.TextField('Текст опису', blank=True)
    method_title = models.CharField('Заголовок методології', max_length=200, default='Методологія')
    advantages_title = models.CharField(
        'Заголовок переваг',
        max_length=200,
        default='Переваги для клієнта',
    )
    order_title = models.CharField('Заголовок форми', max_length=200, default='Обговорімо вашу задачу')
    order_text = models.TextField('Текст форми', blank=True)
    is_published = models.BooleanField('Опубліковано', default=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    icon = models.CharField('Іконка', max_length=80, blank=True)
    card_image = models.ImageField('Зображення картки', upload_to='pages/services/', blank=True)
    card_text = models.TextField('Текст картки', blank=True)
    tags = models.CharField('Теги (через |)', max_length=300, blank=True)

    class Meta:
        verbose_name = 'Послуга'
        verbose_name_plural = 'Послуги'
        ordering = ['order', 'id']

    def __str__(self):
        return self.title

    def tag_list(self):
        return [t.strip() for t in self.tags.split('|') if t.strip()]


class ServiceScopeItem(models.Model):
    page = models.ForeignKey(ServicePage, on_delete=models.CASCADE, related_name='scope_items')
    text = models.CharField('Пункт', max_length=300)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Пункт опису'
        verbose_name_plural = 'Пункти опису'

    def __str__(self):
        return self.text


class ServiceMethodStep(models.Model):
    page = models.ForeignKey(ServicePage, on_delete=models.CASCADE, related_name='method_steps')
    number = models.CharField('Номер', max_length=8, default='01')
    title = models.CharField('Заголовок', max_length=120)
    text = models.TextField('Текст', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Крок методології'
        verbose_name_plural = 'Кроки методології'

    def __str__(self):
        return f'{self.number} {self.title}'


class ServiceAdvantage(models.Model):
    page = models.ForeignKey(ServicePage, on_delete=models.CASCADE, related_name='advantages')
    title = models.CharField('Заголовок', max_length=120)
    text = models.TextField('Текст', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Перевага послуги'
        verbose_name_plural = 'Переваги послуги'

    def __str__(self):
        return self.title


class AnalysisPage(SingletonModel, SEOFields):
    title = models.CharField('Назва', max_length=200, default='VI Analysis')
    hero_title = models.CharField(
        'Hero заголовок',
        max_length=200,
        default='VI Analysis',
    )
    hero_text = models.TextField(
        'Hero текст',
        default='Власний сервіс швидкої перевірки контрагентів',
    )
    hero_image = models.ImageField('Hero зображення', upload_to='pages/analysis/', blank=True)
    steps_title = models.CharField(
        'Заголовок кроків',
        max_length=200,
        default='Три кроки від реквізитів до рішення',
    )
    risks_title = models.CharField('Заголовок ризиків', max_length=200, default='Що перевіряє VI ANALYSIS')
    recommendation_title = models.CharField(
        'Заголовок рекомендації',
        max_length=200,
        default='Рекомендація щодо співпраці',
    )
    recommendation_text = models.TextField('Текст рекомендації', blank=True)
    result_title = models.CharField(
        'Заголовок результату',
        max_length=200,
        default='Що отримує замовник',
    )
    result_text = models.TextField('Текст результату', blank=True)
    paket_title = models.CharField(
        'Заголовок пакета',
        max_length=200,
        default='Пакетне обслуговування',
    )
    paket_subtitle = models.CharField(
        'Підзаголовок пакета',
        max_length=200,
        default='для постійних клієнтів',
    )
    paket_text = models.TextField('Текст пакета', blank=True)
    include_title = models.CharField(
        'Заголовок «Що входить»',
        max_length=200,
        default='Що входить до пакета',
    )
    why_title = models.CharField('Заголовок «Чому вигідно»', max_length=200, default='Чому це вигідно')
    price_title = models.CharField('Заголовок вартості', max_length=200, default='Скільки це коштує')
    order_title = models.CharField(
        'Заголовок форми',
        max_length=200,
        default='Перевірте контрагента до підписання договору',
    )
    order_text = models.TextField('Текст форми', blank=True)
    short = models.CharField('Короткий опис у меню', max_length=200, blank=True)
    card_image = models.ImageField('Зображення картки', upload_to='pages/analysis/', blank=True)
    card_text = models.TextField('Текст картки', blank=True)
    tags = models.CharField('Теги (через |)', max_length=300, blank=True)
    icon = models.CharField('Іконка', max_length=80, blank=True, default='HiconOutlineShieldTick')

    class Meta:
        verbose_name = 'VI Analysis'
        verbose_name_plural = 'VI Analysis'
        constraints = [
            models.CheckConstraint(condition=models.Q(id=1), name='analysispage_singleton'),
        ]

    def __str__(self):
        return 'VI Analysis'

    def tag_list(self):
        return [t.strip() for t in self.tags.split('|') if t.strip()]


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
    title = models.CharField('Заголовок', max_length=160)
    text = models.TextField('Текст', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Ризик VI Analysis'
        verbose_name_plural = 'Ризики VI Analysis'

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


class AnalysisPriceRow(models.Model):
    page = models.ForeignKey(AnalysisPage, on_delete=models.CASCADE, related_name='price_rows')
    number = models.CharField('№', max_length=8, default='1')
    title = models.CharField('Складова', max_length=120)
    period = models.CharField('Період', max_length=80, blank=True)
    description = models.TextField('Що входить', blank=True)
    price_note = models.CharField('Як рахується', max_length=200, blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Тариф VI Analysis'
        verbose_name_plural = 'Тарифи VI Analysis'

    def __str__(self):
        return self.title


class ContactsPage(SingletonModel, SEOFields):
    hero_title = models.CharField('Hero заголовок', max_length=200, default='Контакти')
    hero_text = models.TextField('Hero текст', blank=True)
    hero_image = models.ImageField('Hero зображення', upload_to='pages/contacts/', blank=True)
    info_title = models.CharField('Заголовок блоку', max_length=200, default='Контактні дані')

    class Meta:
        verbose_name = 'Контакти'
        verbose_name_plural = 'Контакти'
        constraints = [
            models.CheckConstraint(condition=models.Q(id=1), name='contactspage_singleton'),
        ]

    def __str__(self):
        return 'Контакти'


class PrivacyPage(SingletonModel, SEOFields):
    hero_title = models.CharField(
        'Hero заголовок',
        max_length=200,
        default='Політика конфіденційності',
    )
    body = models.TextField('Текст політики', blank=True)

    class Meta:
        verbose_name = 'Політика конфіденційності'
        verbose_name_plural = 'Політика конфіденційності'
        constraints = [
            models.CheckConstraint(condition=models.Q(id=1), name='privacypage_singleton'),
        ]

    def __str__(self):
        return 'Політика конфіденційності'
