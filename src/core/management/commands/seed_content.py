from datetime import date
from pathlib import Path
from shutil import copyfile

from django.core.files import File
from django.core.management.base import BaseCommand

from src.blog.models import Article, ArticleBlock
from src.cases.models import CaseBlock, CaseStat, CaseStudy
from src.core.models import SiteSettings
from src.pages.models import (
    AboutPage,
    AboutPrinciple,
    AboutProcessStep,
    AboutStat,
    AnalysisInclude,
    AnalysisPage,
    AnalysisPriceRow,
    AnalysisRisk,
    AnalysisStep,
    AnalysisWhy,
    ContactsPage,
    HomeAdvantage,
    HomePage,
    HomeProcessStep,
    PrivacyPage,
    ServiceAdvantage,
    ServiceMethodStep,
    ServicePage,
    ServiceScopeItem,
    ServicesIndex,
    TeamMember,
)

STATIC = Path(__file__).resolve().parents[2] / 'static' / 'images'


def assign_image(field, relative):
    src = STATIC / relative
    if not src.exists() or field.name:
        return
    with src.open('rb') as fh:
        field.save(src.name, File(fh), save=False)


class Command(BaseCommand):
    help = 'Idempotent seed of Vartis content from design export'

    def handle(self, *args, **options):
        self.seed_settings()
        self.seed_home()
        self.seed_about()
        self.seed_services()
        self.seed_analysis()
        self.seed_contacts_privacy()
        self.seed_articles()
        self.seed_cases()
        self.stdout.write(self.style.SUCCESS('seed_content OK'))

    def seed_settings(self):
        s = SiteSettings.load()
        s.company_name = 'ТОВ «ВАРТІС ІНТЕЛІДЖЕНС»'
        s.tagline = 'Стратегічна аналітика, OSINT, корпоративна безпека та аналіз ризиків'
        # Як у Home.dc.html — плейсхолдери, доки немає реальних даних
        if s.phone in ('', '+380'):
            s.phone = ''
        if s.email in ('', 'info@vartis.ua'):
            s.email = ''
        if s.address in ('', 'Україна'):
            s.address = ''
        s.facebook_url = s.facebook_url or 'https://facebook.com/vartisintelligence'
        s.save()

    def seed_home(self):
        page = HomePage.load()
        page.seo_title = 'VARTIS INTELLIGENCE — стратегічна аналітика та перевірка контрагентів'
        page.seo_description = (
            'Стратегічна аналітика, перевірка контрагентів та захист бізнесу. '
            'Допомагаємо виявляти приховані ризики й ухвалювати обґрунтовані рішення.'
        )
        page.h1 = 'Інформація, що перетворює ризики на переваги'
        page.hero_title = 'Інформація, що перетворює ризики на переваги'
        page.hero_text = (
            'Стратегічна аналітика, перевірка контрагентів та захист бізнесу. '
            'Допомагаємо виявляти приховані ризики, перевіряти інформацію й ухвалювати обґрунтовані рішення'
        )
        page.services_title = 'Напрями нашої роботи'
        page.advantages_title = 'Переваги компанії'
        page.mission_title = 'Стратегічна інформація для впевнених рішень'
        page.mission_text = (
            'VARTIS INTELLIGENCE працює на перетині стратегічної аналітики, OSINT, '
            'корпоративної безпеки та аналізу ризиків.\n\n'
            'Ми допомагаємо бізнесу отримувати й перевіряти інформацію, оцінювати '
            'обставини та бачити ризики, які можуть впливати на його рішення'
        )
        page.process_title = 'Як ми працюємо?'
        page.blog_title = 'Аналітика та експертні матеріали'
        assign_image(page.hero_image, 'hero.png')
        assign_image(page.mission_image, 'about-bg.png')
        page.save()

        if not page.advantages.exists():
            for i, (title, text, icon) in enumerate([
                ('Аналітичний підхід', 'Рішення на основі перевірених відомостей', 'HiconOutlineScan5'),
                ('Оцінка ризиків', 'Виявлення потенційних загроз до ухвалення важливих рішень', 'HiconOutlineShieldTick'),
                ('Конфіденційність', 'Захист інформації та факту звернення', 'HiconOutlineLock3'),
                ('Експертна підтримка', 'Фаховий аналіз і пояснення отриманих результатів', 'HiconOutlineCalling1'),
            ]):
                HomeAdvantage.objects.create(page=page, title=title, text=text, icon=icon, order=i)

        if not page.process_steps.exists():
            for i, (num, title, text) in enumerate([
                ('01', 'Вивчаємо завдання', "З'ясовуємо, яку інформацію потрібно отримати та на які питання відповісти."),
                ('02', 'Проводимо дослідження', 'Збираємо, перевіряємо й аналізуємо відомості відповідно до погодженого завдання'),
                ('03', 'Формуємо висновки', 'Систематизуємо результати та визначаємо встановлені факти й можливі ризики'),
                ('04', 'Передаємо результат', 'Надаємо матеріали, необхідні для подальшого аналізу та ухвалення рішень'),
            ]):
                HomeProcessStep.objects.create(page=page, number=num, title=title, text=text, order=i)

    def seed_about(self):
        page = AboutPage.load()
        page.seo_title = 'Про компанію — VARTIS INTELLIGENCE'
        page.seo_description = 'Історія, команда, принципи та методологія Vartis Intelligence.'
        page.h1 = 'Про компанію'
        page.hero_title = 'Про компанію'
        page.hero_text = 'Ми допомагаємо бізнесу ухвалювати рішення на основі перевірених фактів'
        page.intro_title = 'Аналітика та безпека для вашого бізнесу'
        page.intro_text = (
            'Ми допомагаємо бізнесу ухвалювати рішення на основі перевірених фактів. '
            'Досліджуємо компанії та людей, бізнес-групи й корпоративні структури, '
            'історію їхніх взаємовідносин і приховані звʼязки. За результатами ви отримуєте '
            'чітку картину ризиків і практичні рекомендації щодо подальшої співпраці.\n\n'
            'Пропонуємо як швидкі рішення на базі власного IT-сервісу, так і глибокі '
            'індивідуальні дослідження, межі яких визначаємо разом із клієнтом.'
        )
        page.principles_title = 'Наші принципи'
        page.team_title = 'Засновники'
        page.science_title = 'Власний сервіс VI Analysis'
        page.science_text = (
            'Інтереси бізнесу не обмежуються кордонами, тож і наша робота теж. '
            'Партнерами Vartis Intelligence є провідні профільні компанії, що '
            'спеціалізуються на пошуку та аналізі інформації.'
        )
        page.stats_title = 'Ключові цифри'
        page.process_title = 'Як ми працюємо'
        assign_image(page.hero_image, 'about-bg.png')
        page.save()

        if not page.principles.exists():
            for i, (title, text) in enumerate([
                ('Законність', 'Усі дані отримуємо виключно законним шляхом — з відкритих джерел, державних реєстрів та інших дозволених законом ресурсів.'),
                ('Конфіденційність', 'Факт звернення, зміст запиту та результати роботи залишаються відомими лише вам.'),
                ('Експертиза', 'Поєднуємо практичний досвід роботи в правоохоронних органах із науковим підходом до аналізу інформації.'),
                ('Практичний результат', 'Не просто збираємо факти, а пояснюємо, що вони означають для вашого бізнесу, і даємо конкретні рекомендації.'),
            ]):
                AboutPrinciple.objects.create(page=page, title=title, text=text, order=i)

        if not page.team.exists():
            for i, (name, role, photo) in enumerate([
                ('В. В. Аброськін', 'Співзасновник', 'team/abroskin.jpg'),
                ('С. В. Тіхонов', 'Співзасновник', 'team/tikhonov.jpg'),
            ]):
                m = TeamMember(page=page, name=name, role=role, order=i)
                assign_image(m.photo, photo)
                m.save()

        if not page.stats.filter(block=AboutStat.BLOCK_INTRO).exists():
            for i, (value, label) in enumerate([
                ('25+', 'років досвіду кожного із засновників у правоохоронній системі'),
                ('6', 'напрямів роботи — від перевірки контрагентів до міжнародної діяльності'),
                ('ЄС', 'партнерська мережа профільних компаній у державах Євросоюзу'),
            ]):
                AboutStat.objects.create(
                    page=page, block=AboutStat.BLOCK_INTRO,
                    value=value, label=label, order=i,
                )

        if not page.stats.filter(block=AboutStat.BLOCK_KEY).exists():
            for i, (value, label) in enumerate([
                ('25+', 'років досвіду засновників'),
                ('1000', 'проведених перевірок'),
                ('50+', 'клієнтів'),
                ('10+', 'реалізованих проєктів'),
            ]):
                AboutStat.objects.create(
                    page=page, block=AboutStat.BLOCK_KEY,
                    value=value, label=label, order=i,
                )

        if not page.process_steps.exists():
            for i, (num, title, text) in enumerate([
                ('01', 'Запит', 'Ви описуєте задачу — у режимі повної конфіденційності.'),
                ('02', 'Визначення обсягу', 'Разом погоджуємо, що саме потрібно встановити, у які строки та в якому форматі.'),
                ('03', 'Дослідження', 'Збираємо та аналізуємо інформацію виключно законними методами.'),
                ('04', 'Висновок', 'Ви отримуєте структурований звіт із виявленими ризиками та рекомендаціями.'),
                ('05', 'Супровід', 'За потреби пояснюємо результати та забезпечуємо подальший моніторинг.'),
            ]):
                AboutProcessStep.objects.create(page=page, number=num, title=title, text=text, order=i)

    def seed_services(self):
        idx = ServicesIndex.load()
        idx.seo_title = 'Послуги — VARTIS INTELLIGENCE'
        idx.seo_description = 'Комплексні рішення для бізнесу — від перевірки інформації до стратегічного аналізу.'
        idx.h1 = 'Послуги'
        idx.hero_title = 'Послуги'
        idx.hero_text = (
            'Комплексні рішення для бізнесу — від перевірки інформації '
            'до стратегічного аналізу та управління ризиками'
        )
        assign_image(idx.hero_image, 'hero.png')
        idx.save()

        services = [
            {
                'slug': 'konsaltynh',
                'title': 'Консалтинг',
                'short': 'Експертна підтримка важливих рішень',
                'icon': 'HiconOutlineCalling1',
                'card': 'services/dir-3.png',
                'card_text': 'Експертна підтримка бізнесу в питаннях аналізу ситуацій, оцінки ризиків і підготовки до важливих рішень',
                'tags': 'Аналіз ситуацій|Оцінка ризиків|Підготовка рішень',
                'hero': 'Експертна підтримка бізнесу в питаннях аналізу ситуацій, оцінки ризиків і підготовки до важливих рішень',
                'scope': 'Консультуємо керівників і команди щодо оцінки ризиків, підготовки до переговорів і ухвалення рішень на основі перевірених відомостей.',
                'order': 0,
            },
            {
                'slug': 'kompleksna-dopomoha-biznesu',
                'title': 'Комплексна допомога бізнесу',
                'short': 'Захист інтересів і контроль інформації',
                'icon': 'HiconOutlineLock3',
                'card': 'services/dir-2.png',
                'card_text': 'Рішення для захисту інтересів компанії, виявлення загроз і збереження контролю над важливою інформацією',
                'tags': 'Захист інтересів|Виявлення загроз|Моніторинг',
                'hero': 'Рішення для захисту інтересів компанії, виявлення загроз і збереження контролю над важливою інформацією',
                'scope': 'Комплексний супровід: від діагностики ризиків до впровадження процедур захисту й постійного моніторингу.',
                'order': 1,
            },
            {
                'slug': 'zbir-ta-analiz-informatsiyi',
                'title': 'Глибока аналітика',
                'short': 'Стратегічна аналітика під ваше завдання',
                'icon': 'HiconOutlineScan5',
                'card': 'services/dir-4.png',
                'card_text': 'Стратегічна аналітика: перевірені відомості про людей, компанії та ринки — для рішень, де помилка коштує дорого',
                'tags': 'Стратегічна аналітика|Факти окремо від припущень|Оплата частинами',
                'hero': (
                    'Стратегічна аналітика: перевірені відомості про людей, компанії та ринки — '
                    'для рішень, де помилка коштує дорого. Ви платите частинами і бачите результат на кожному етапі.'
                ),
                'scope': 'Глибокі індивідуальні дослідження, межі яких визначаємо разом із клієнтом. Факти окремо від припущень.',
                'order': 2,
            },
            {
                'slug': 'zakhyst-vid-vytoku',
                'title': 'Захист від витоку інформації',
                'short': 'Захищені приміщення та переговори',
                'icon': 'HiconOutlineLock3',
                'card': 'blog/lock.jpg',
                'card_text': 'Обстеження приміщень, програма захисту, контроль впровадження та планові перевірки',
                'tags': 'Обстеження|Програма захисту|Планові перевірки',
                'hero': (
                    'Обстеження приміщень, програма захисту, контроль впровадження та планові перевірки'
                ),
                'scope': 'Побудова системи захисту від витоку інформації; документальне оформлення режиму конфіденційності; постійна підтримка.',
                'order': 3,
            },
            {
                'slug': 'kryminalni-provadzhennia',
                'title': 'Інформаційна підтримка у кримінальних провадженнях',
                'short': 'Для адвокатів і юридичних компаній',
                'icon': 'HiconOutlineShieldTick',
                'card': 'blog/law.jpg',
                'card_text': 'Перевірка фактів, альтернативні версії та оцінка доказів для адвокатів і юрфірм',
                'tags': 'Перевірка фактів|Альтернативні версії|Оцінка доказів',
                'hero': (
                    'Перевірка фактів, альтернативні версії та оцінка доказів '
                    'для адвокатів і юрфірм'
                ),
                'scope': 'Перевірка достовірності подій і даних; альтернативні версії; позиція щодо допустимості інформації.',
                'order': 4,
            },
        ]

        from src.pages.design_copy import SERVICES as DESIGN_SERVICES

        for data in services:
            page, created = ServicePage.objects.update_or_create(
                slug=data['slug'],
                defaults={
                    'title': data['title'],
                    'short': data['short'],
                    'icon': data['icon'],
                    'card_text': data['card_text'],
                    'tags': data['tags'],
                    'hero_text': data['hero'],
                    'scope_text': data['scope'],
                    'seo_title': f"{data['title']} — VARTIS INTELLIGENCE",
                    'seo_description': data['card_text'],
                    'h1': data['title'],
                    'order': data['order'],
                    'is_published': True,
                    'order_title': 'Обговорімо вашу задачу',
                    'order_text': (
                        "Опишіть ситуацію — ми зв'яжемося, щоб уточнити завдання. "
                        'Факт звернення залишається конфіденційним.'
                    ),
                },
            )
            assign_image(page.card_image, data['card'])
            assign_image(page.hero_image, data['card'])
            page.save()

            design = DESIGN_SERVICES.get(data['slug'])
            if design:
                page.scope_items.all().delete()
                page.method_steps.all().delete()
                page.advantages.all().delete()
                page.scope_title = design.get('scope_title', page.scope_title)
                page.method_title = design.get('method_title', page.method_title)
                page.advantages_title = design.get('advantages_title', page.advantages_title)
                page.order_title = design.get('order_title', page.order_title).replace('\n', ' ')
                page.order_text = design.get('order_text', page.order_text)
                page.hero_text = design.get('hero_text', page.hero_text)
                page.save()
                for i, text in enumerate(design.get('scope_items', [])):
                    ServiceScopeItem.objects.create(page=page, text=text, order=i)
                for i, (num, title, text) in enumerate(design.get('steps', [])):
                    ServiceMethodStep.objects.create(
                        page=page, number=num, title=title, text=text, order=i,
                    )
                for i, (_icon, title, text) in enumerate(design.get('advantages', [])):
                    ServiceAdvantage.objects.create(
                        page=page, title=title, text=text, order=i,
                    )
            elif created or not page.method_steps.exists():
                page.method_steps.all().delete()
                page.advantages.all().delete()
                page.scope_items.all().delete()
                for i, text in enumerate([
                    'Конфіденційний запит і уточнення завдання',
                    'Збір і перевірка відомостей законними методами',
                    'Структурований висновок із рекомендаціями',
                ]):
                    ServiceScopeItem.objects.create(page=page, text=text, order=i)
                for i, (num, title, text) in enumerate([
                    ('01', 'Запит', 'Описуєте задачу в режимі повної конфіденційності'),
                    ('02', 'Дослідження', 'Збираємо й аналізуємо інформацію'),
                    ('03', 'Висновок', 'Отримуєте звіт і рекомендації'),
                ]):
                    ServiceMethodStep.objects.create(
                        page=page, number=num, title=title, text=text, order=i,
                    )
                for i, (title, text) in enumerate([
                    ('Конфіденційність', 'Факт звернення відомий лише вам'),
                    ('Практичний результат', 'Рекомендації для ухвалення рішень'),
                    ('Законність', 'Лише відкриті та дозволені джерела'),
                ]):
                    ServiceAdvantage.objects.create(page=page, title=title, text=text, order=i)

    def seed_analysis(self):
        page = AnalysisPage.load()
        page.title = 'Експрес-перевірка контрагентів — VI Analysis'
        page.short = 'Збір інформації, ризики, рекомендації'
        page.hero_title = 'VI Analysis'
        page.hero_text = (
            'Експрес-перевірка контрагентів, збір інформації — оцінка ризиків — '
            'рекомендації для бізнесу'
        )
        page.seo_title = 'VI Analysis — експрес-перевірка контрагентів | VARTIS INTELLIGENCE'
        page.seo_description = (
            'Достатньо назви компанії та коду ЄДРПОУ. За лічені хвилини ви бачите, '
            'які ризики з ним повʼязані.'
        )
        page.h1 = 'VI Analysis'
        page.card_text = (
            'Експрес-перевірка контрагентів, збір інформації — оцінка ризиків — '
            'рекомендації для бізнесу'
        )
        page.tags = 'Збір інформації|Оцінка ризиків|Рекомендації'
        page.recommendation_text = (
            'Рекомендаційний модуль перетворює виявлені ризики на конкретний варіант дій '
            'і показує, які саме фактори на нього вплинули.'
        )
        page.result_text = (
            'Замовник отримує оцінку ризиків і рекомендації для ухвалення рішення: '
            'на стандартних умовах, із додатковими умовами або з відмовою від співпраці.'
        )
        page.paket_text = (
            'Для компаній, яким потрібен постійний контроль за партнерською базою. '
            'Ви визначаєте контрагентів — ми перевіряємо й моніторимо зміни.'
        )
        page.order_text = (
            'Надішліть назву компанії або код ЄДРПОУ — ми підготуємо звіт із рекомендацією.'
        )
        assign_image(page.hero_image, 'services/dir-1.png')
        assign_image(page.card_image, 'services/dir-1.png')
        page.save()

        if not page.steps.exists():
            for i, (num, title, text, bullets) in enumerate([
                ('01', 'Збір інформації', 'Система миттєво досліджує контрагента за назвою та кодом ЄДРПОУ.', 'справжні власники та організатори бізнесу\nструктура бізнес-груп'),
                ('02', 'Оцінка ризиків', 'Кожен знайдений факт перевіряється на ризики та отримує рівень небезпеки.', 'категоризація: низький, середній, високий\nуспадковані ризики бізнес-групи'),
                ('03', 'Рекомендація', 'Система формує висновок щодо доцільності співпраці та пропонує її умови.', 'зрозумілий підсумок замість сирих даних\nгнучке налаштування модуля'),
            ]):
                AnalysisStep.objects.create(
                    page=page, number=num, title=title, text=text, bullets=bullets, order=i,
                )

        if not page.risks.exists():
            for i, (title, text) in enumerate([
                ('Правові та регуляторні ризики', 'Кримінальні провадження, санкції та виконавчі провадження.'),
                ('Фінансово-господарські ризики', 'Боргові зобовʼязання, фінансова звітність, ознаки обігу нелегальної продукції.'),
                ('Репутаційні та інші ризики', 'Публікації у ЗМІ, відкриті джерела й додаткові сигнали.'),
            ]):
                AnalysisRisk.objects.create(page=page, title=title, text=text, order=i)

        if not page.includes.exists():
            for i, (title, text) in enumerate([
                ('Доброчесність і відносини з владою', 'Кримінальні та виконавчі провадження, санкції, інші «червоні прапорці».'),
                ('Фінансовий стан та історія звʼязків', 'Борги, звітність, звʼязки зараз і раніше.'),
                ('Явні та приховані ризики', 'У тому числі успадковані від повʼязаних осіб і компаній.'),
                ('Реальні власники та бізнес-групи', 'Групування контрагентів в офіційні та фактичні бізнес-групи.'),
                ('Рекомендації щодо співпраці', 'Стандартні умови, додаткові умови або відмова.'),
                ('Постійний моніторинг реєстрів', 'Повідомлення про суттєві події.'),
            ]):
                AnalysisInclude.objects.create(page=page, title=title, text=text, order=i)

        if not page.why_items.exists():
            for i, (num, title, text) in enumerate([
                ('01', 'Конфіденційність — з першого кроку', 'NDA підписуємо до укладення основної угоди.'),
                ('02', 'Без власного штату перевіряльників', 'Ви платите лише за результат.'),
                ('03', 'Відповідь за хвилини, а не за години', 'Перевірки виконуються в VI Analysis.'),
                ('04', 'Ваші люди на прямому звʼязку', 'Контактні особи отримують інформацію онлайн.'),
            ]):
                AnalysisWhy.objects.create(page=page, number=num, title=title, text=text, order=i)

        if not page.price_rows.exists():
            for i, row in enumerate([
                ('1', 'Підключення', 'разово', 'Первинна перевірка контрагентів і налаштування моніторингу.', '____ грн за кожного контрагента'),
                ('2', 'Абонентська плата', 'щомісяця', 'Моніторинг, повідомлення, перевірки в межах тарифу.', 'за обраним тарифом'),
                ('3', 'Додаткові перевірки', 'за потреби', 'Понад ліміт тарифу.', 'за прайсом'),
                ('4', 'Захищений простір', 'опція', 'Створення та підтримка захищеного інформаційного простору.', 'за окремою угодою'),
            ]):
                AnalysisPriceRow.objects.create(
                    page=page,
                    number=row[0], title=row[1], period=row[2],
                    description=row[3], price_note=row[4], order=i,
                )

    def seed_contacts_privacy(self):
        c = ContactsPage.load()
        c.seo_title = 'Контакти — VARTIS INTELLIGENCE'
        c.seo_description = 'Адреса, телефони, email та форма зворотного звʼязку.'
        c.h1 = 'Контакти'
        c.hero_title = 'Контакти'
        c.hero_text = (
            'Перша консультація допоможе визначити, яке рішення підійде саме вам. '
            'Факт звернення, зміст запиту та результати роботи залишаються відомими лише вам'
        )
        c.info_title = 'Обговорімо вашу задачу'
        assign_image(c.hero_image, 'hero.png')
        c.save()

        p = PrivacyPage.load()
        p.seo_title = 'Політика конфіденційності — VARTIS INTELLIGENCE'
        p.seo_description = 'Політика обробки персональних даних.'
        p.h1 = 'Політика конфіденційності'
        p.hero_title = 'Політика конфіденційності'
        p.body = (
            '<p>Ця Політика конфіденційності описує, як ТОВ «ВАРТІС ІНТЕЛІДЖЕНС» '
            'обробляє персональні дані, отримані через форми на сайті.</p>'
            '<p>Ми збираємо імʼя, номер телефону та адресу електронної пошти лише '
            'для відповіді на ваш запит. Дані не передаються третім особам без '
            'законної підстави.</p>'
            '<p>Ви можете звернутися щодо доступу, виправлення або видалення даних '
            'на email, зазначений у розділі «Контакти».</p>'
        )
        p.save()

    def seed_articles(self):
        from .seed_content_2 import seed_articles
        seed_articles()

    def seed_cases(self):
        from .seed_content_2 import seed_cases
        seed_cases()
