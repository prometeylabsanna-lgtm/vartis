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
    if not src.exists():
        return
    # Перезаписати, якщо в БД є шлях, а файлу в storage немає (типово після /tmp на Vercel)
    if field.name:
        try:
            if field.storage.exists(field.name):
                return
        except (ValueError, OSError):
            pass
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
        from django.core.management import call_command
        call_command('seed_site_blocks')
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
            s.address = 'Київ, вул. Хрещатик, 1'
        s.facebook_url = s.facebook_url or 'https://facebook.com/vartisintelligence'
        s.map_embed_url = (
            'https://maps.google.com/maps?q=%D0%9A%D0%B8%D1%97%D0%B2,+%D0%B2%D1%83%D0%BB.+'
            '%D0%A5%D1%80%D0%B5%D1%89%D0%B0%D1%82%D0%B8%D0%BA,+1&hl=uk&z=16&output=embed'
        )
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
        page.team_lead = (
            'Поєднуємо практичний досвід роботи в правоохоронних органах '
            'із науковим підходом до аналізу інформації'
        )
        page.science_eyebrow = 'Наукова основа'
        page.science_title = 'Власний сервіс VI Analysis'
        page.science_text = (
            'Методологічна основа сервісу швидкої перевірки контрагентів викладена '
            'у статті засновників компанії В. В. Аброськіна та С. В. Тіхонова '
            '«Цифрова екосистема перевірки контрагентів…» («Право і суспільство», № 1/2026).'
        )
        page.science_doi_url = 'https://doi.org/10.32842/2078-3736/2026.1.1.28'
        page.science_doi_label = 'doi.org/10.32842/2078-3736/2026.1.1.28'
        page.partners_eyebrow = 'Міжнародна діяльність'
        page.partners_title = 'Для бізнесу з інтересами за межами України'
        page.partners_text = (
            'Інтереси бізнесу не обмежуються кордонами, тож і наша робота теж. '
            'Партнерами Vartis Intelligence є провідні профільні компанії, що '
            'спеціалізуються на пошуку та аналізі інформації в інтересах фізичних '
            'і юридичних осіб. Вони працюють виключно у спосіб, дозволений '
            'національним законодавством держав Європейського Союзу.'
        )
        page.stats_title = 'Ключові цифри'
        page.process_title = 'Як ми працюємо'
        assign_image(page.hero_image, 'about-bg.png')
        page.save()

        principles = [
            ('HiconOutlineShieldTick', 'Законність',
             'Усі дані отримуємо виключно законним шляхом — з відкритих джерел, державних реєстрів та інших дозволених законом ресурсів.'),
            ('HiconOutlineLock3', 'Конфіденційність',
             'Факт звернення, зміст запиту та результати роботи залишаються відомими лише вам.'),
            ('HiconOutlineScan5', 'Експертиза',
             'Поєднуємо практичний досвід роботи в правоохоронних органах із науковим підходом до аналізу інформації.'),
            ('HiconOutlineCalling1', 'Практичний результат',
             'Не просто збираємо факти, а пояснюємо, що вони означають для вашого бізнесу, і даємо конкретні рекомендації.'),
        ]
        if not page.principles.exists():
            for i, (icon, title, text) in enumerate(principles):
                AboutPrinciple.objects.create(
                    page=page, icon=icon, title=title, text=text, order=i,
                )
        else:
            for i, (icon, title, text) in enumerate(principles):
                AboutPrinciple.objects.filter(page=page, title=title).update(
                    icon=icon, text=text, order=i,
                )

        team_data = [
            {
                'name': 'В’ячеслав Аброськін',
                'photo': 'team/abroskin.jpg',
                'photo_position': '50% 20%',
                'email': 'vaceslavabroskin46@gmail.com',
                'role': 'Співзасновник і директор ТОВ «ВАРТІС ІНТЕЛІДЖЕНС»',
                'regalia': (
                    'Кандидат юридичних наук · Адвокат, партнер FOMIN PARTNERS · '
                    'Генерал поліції ІІ рангу у відставці'
                ),
                'bio': (
                    'Понад 25 років професійного досвіду в правоохоронній системі, а також у сферах '
                    'державного управління, військової служби, юридичної практики, кримінального '
                    'аналізу та корпоративної безпеки. Обіймав посаду першого заступника Голови '
                    'Національної поліції — керівника кримінальної поліції; був ініціатором '
                    'створення підрозділів кримінального аналізу.'
                ),
                'expertise': [
                    'Кримінальний аналіз і робота з інформацією',
                    'Протидія організованій злочинності та оперативно-розшукова діяльність',
                    'Корпоративна безпека й оцінка безпекових ризиків',
                    'Корпоративне право, захист інтересів бізнесу та управління юридичними ризиками',
                    'Забезпечення публічної безпеки в кризових умовах',
                ],
                'career_path': [
                    {'t': 'Співзасновник і директор ТОВ «ВАРТІС ІНТЕЛІДЖЕНС»', 'y': 'Нині'},
                    {'t': 'Адвокат, партнер FOMIN PARTNERS', 'y': 'Нині'},
                    {'t': 'Збройні Сили України, підполковник', 'y': '2022–2024'},
                    {'t': 'Ректор Одеського державного університету внутрішніх справ', 'y': '2019–2021'},
                    {
                        't': 'Перший заступник Голови Національної поліції України — керівник кримінальної поліції',
                        'y': '2017–2019',
                    },
                    {'t': 'Начальник ГУ Національної поліції в Донецькій області', 'y': '2014–2017'},
                    {'t': 'Карний розшук органів внутрішніх справ', 'y': 'З 1994'},
                ],
            },
            {
                'name': 'Сергій Тіхонов',
                'photo': 'team/tikhonov.jpg',
                'photo_position': '50% 15%',
                'email': 'tikhonov31@gmail.com',
                'role': 'Співзасновник ТОВ «ВАРТІС ІНТЕЛІДЖЕНС»',
                'regalia': 'Доктор філософії у галузі права · Генерал поліції ІІІ рангу у відставці',
                'bio': (
                    'Понад 25 років досвіду в правоохоронній системі — від оперативника до керівника '
                    'центрального підрозділу карного розшуку, служби загальнодержавного рівня. '
                    'Колишній завідувач кафедри оперативно-розшукової діяльності Національної '
                    'академії внутрішніх справ.'
                ),
                'expertise': [
                    'Пошук, перевірка та аналіз інформації',
                    'Оперативно-розшукова діяльність і карний розшук',
                    'Криміналістика',
                    'Правове регулювання та реформування правоохоронної діяльності',
                    'Методичне забезпечення практичної діяльності',
                ],
                'career_path': [
                    {'t': 'Співзасновник ТОВ «ВАРТІС ІНТЕЛІДЖЕНС»', 'y': 'Нині'},
                    {'t': 'Завідувач кафедри оперативно-розшукової діяльності НАВС', 'y': ''},
                    {'t': 'Керівник центрального підрозділу карного розшуку', 'y': ''},
                    {'t': 'Підрозділи карного розшуку', 'y': ''},
                ],
            },
        ]
        existing_team = list(page.team.all())
        if not existing_team:
            for i, row in enumerate(team_data):
                m = TeamMember(
                    page=page,
                    name=row['name'],
                    role=row['role'],
                    regalia=row['regalia'],
                    email=row['email'],
                    bio=row['bio'],
                    photo_position=row['photo_position'],
                    expertise=row['expertise'],
                    career_path=row['career_path'],
                    order=i,
                )
                assign_image(m.photo, row['photo'])
                m.save()
        else:
            for i, row in enumerate(team_data):
                m = existing_team[i] if i < len(existing_team) else TeamMember(page=page)
                m.name = row['name']
                m.role = row['role']
                m.regalia = row['regalia']
                m.email = row['email']
                m.bio = row['bio']
                m.photo_position = row['photo_position']
                m.expertise = row['expertise']
                m.career_path = row['career_path']
                m.order = i
                if not m.photo:
                    assign_image(m.photo, row['photo'])
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

        key_metrics = [
            ('25+', 'років досвіду засновників'),
            ('1000', 'проведених перевірок'),
            ('50+', 'клієнтів'),
            ('10+', 'реалізованих проєктів'),
        ]
        existing_key = list(page.stats.filter(block=AboutStat.BLOCK_KEY))
        for i, (value, label) in enumerate(key_metrics):
            if i < len(existing_key):
                row = existing_key[i]
                row.value = value
                row.label = label
                row.order = i
                row.save(update_fields=['value', 'label', 'order'])
            else:
                AboutStat.objects.create(
                    page=page, block=AboutStat.BLOCK_KEY,
                    value=value, label=label, order=i,
                )

        process_steps = [
            ('01', 'Запит', 'Ви описуєте задачу — у режимі повної конфіденційності.'),
            ('02', 'Визначення обсягу', 'Разом погоджуємо, що саме потрібно встановити, у які строки та в якому форматі.'),
            ('03', 'Дослідження', 'Збираємо та аналізуємо інформацію виключно законними методами.'),
            ('04', 'Висновок', 'Ви отримуєте структурований звіт із виявленими ризиками та рекомендаціями.'),
            ('05', 'Супровід', 'За потреби пояснюємо результати, відповідаємо на запитання та забезпечуємо подальший моніторинг.'),
        ]
        existing_steps = list(page.process_steps.all())
        if not existing_steps:
            for i, (num, title, text) in enumerate(process_steps):
                AboutProcessStep.objects.create(
                    page=page, number=num, title=title, text=text, order=i,
                )
        else:
            for i, (num, title, text) in enumerate(process_steps):
                if i < len(existing_steps):
                    step = existing_steps[i]
                    step.number = num
                    step.title = title
                    step.text = text
                    step.order = i
                    step.save(update_fields=['number', 'title', 'text', 'order'])
                else:
                    AboutProcessStep.objects.create(
                        page=page, number=num, title=title, text=text, order=i,
                    )

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

        steps_data = [
            (
                '01', 'Збір інформації',
                'Система миттєво досліджує контрагента за назвою та кодом ЄДРПОУ, зводить дані з різних джерел.',
                'дає змогу встановити справжніх власників і організаторів бізнесу\n'
                'допомагає структурувати компанії за належністю до бізнес-груп',
            ),
            (
                '02', 'Оцінка ризиків',
                'Кожен знайдений факт перевіряється на ризики та отримує рівень небезпеки.',
                'категоризація: низький, середній, високий\n'
                'окремо показано ризики, успадковані від бізнес-групи — проблеми '
                'пов’язаних компаній не залишаться поза увагою',
            ),
            (
                '03', 'Рекомендація',
                'На основі виявлених ризиків система формує висновок щодо доцільності '
                'співпраці та пропонує її умови.',
                'зрозумілий підсумок замість сирих даних\n'
                'гнучке налаштування рекомендаційного модуля дозволяє адаптувати '
                'визначення ризику під особливості бізнесу',
            ),
        ]
        for i, (num, title, text, bullets) in enumerate(steps_data):
            AnalysisStep.objects.update_or_create(
                page=page, number=num,
                defaults={'title': title, 'text': text, 'bullets': bullets, 'order': i},
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
        p.seo_description = (
            'Політика конфіденційності ТОВ «ВАРТІС ІНТЕЛІДЖЕНС»: '
            'які дані ми збираємо, як їх використовуємо та захищаємо.'
        )
        p.h1 = 'Політика конфіденційності'
        p.hero_title = 'Політика конфіденційності'
        p.body = (
            '<p>Редакція від [дата]. Тимчасовий текст — буде замінено на затверджену редакцію.</p>'
            '<div class="privacy-block">'
            '<h2><span class="privacy-block__num">01</span> Загальні положення</h2>'
            '<p>Ця Політика пояснює, як ТОВ «ВАРТІС ІНТЕЛІДЖЕНС» збирає, використовує та '
            'захищає персональні дані відвідувачів сайту. Надсилаючи форму на сайті, ви '
            'погоджуєтеся з умовами цієї Політики.</p></div>'
            '<div class="privacy-block">'
            '<h2><span class="privacy-block__num">02</span> Які дані ми збираємо</h2>'
            '<p>Ім\'я, номер телефону, адресу електронної пошти та текст повідомлення, які ви '
            'самостійно вказуєте у формі заявки. Також технічні дані: IP-адреса, тип браузера, '
            'сторінки, які ви переглядали.</p></div>'
            '<div class="privacy-block">'
            '<h2><span class="privacy-block__num">03</span> Мета обробки</h2>'
            '<p>Дані використовуються лише для того, щоб зв\'язатися з вами щодо вашого звернення, '
            'підготувати пропозицію та покращувати роботу сайту.</p></div>'
            '<div class="privacy-block">'
            '<h2><span class="privacy-block__num">04</span> Передача третім особам</h2>'
            '<p>Ми не продаємо і не передаємо ваші дані третім особам, крім випадків, передбачених '
            'законодавством України, та сервісів, що забезпечують роботу сайту '
            '(хостинг, CRM, аналітика).</p></div>'
            '<div class="privacy-block">'
            '<h2><span class="privacy-block__num">05</span> Зберігання та захист</h2>'
            '<p>Дані зберігаються не довше, ніж це потрібно для мети обробки. Ми застосовуємо '
            'організаційні та технічні заходи захисту, зокрема захищене з\'єднання (SSL).</p></div>'
            '<div class="privacy-block">'
            '<h2><span class="privacy-block__num">06</span> Ваші права</h2>'
            '<p>Ви маєте право дізнатися, які дані про вас зберігаються, вимагати їх виправлення '
            'або видалення, а також відкликати згоду на обробку, написавши нам.</p></div>'
            '<div class="privacy-block">'
            '<h2><span class="privacy-block__num">07</span> Файли cookie</h2>'
            '<p>Сайт використовує файли cookie для аналітики (Google Analytics 4). Ви можете '
            'вимкнути cookie в налаштуваннях браузера.</p></div>'
            '<div class="privacy-block">'
            '<h2><span class="privacy-block__num">08</span> Контакти</h2>'
            '<p>З питань обробки персональних даних звертайтеся: [Email], [Телефон], '
            '[Адреса офісу].</p></div>'
        )
        p.save()

    def seed_articles(self):
        from .seed_content_2 import seed_articles
        seed_articles()

    def seed_cases(self):
        from .seed_content_2 import seed_cases
        seed_cases()
