from datetime import date
from pathlib import Path
import json

from src.blog.models import Article, ArticleBlock
from src.cases.models import CaseBlock, CaseStat, CaseStudy
from .seed_content import assign_image

ARTICLES_JSON = Path(__file__).resolve().parents[2] / 'data' / 'articles.json'


def _blocks_from_js(body):
    """Convert articles.js body items into ArticleBlock kwargs list."""
    out = []
    for i, item in enumerate(body):
        if 'note' in item and len(item) == 1:
            out.append({'block_type': 'note', 'heading': '', 'text': item['note'], 'list_items': '', 'order': i})
            continue
        if 'p' in item and 'h' not in item and 'list' not in item and 'note' not in item:
            out.append({'block_type': 'p', 'heading': '', 'text': item['p'], 'list_items': '', 'order': i})
            continue
        if 'h' in item:
            list_items = '\n'.join(item['list']) if item.get('list') else ''
            out.append({
                'block_type': 'h',
                'heading': item.get('h') or '',
                'text': item.get('p') or '',
                'list_items': list_items,
                'order': i,
            })
            continue
        if 'list' in item:
            out.append({
                'block_type': 'list',
                'heading': '',
                'text': '',
                'list_items': '\n'.join(item['list']),
                'order': i,
            })
            continue
        if 'note' in item:
            out.append({'block_type': 'note', 'heading': '', 'text': item['note'], 'list_items': '', 'order': i})
            continue
        if 'p' in item:
            out.append({'block_type': 'p', 'heading': '', 'text': item['p'], 'list_items': '', 'order': i})
    return out


def seed_articles():
    from src.blog.models import Article
    from src.core.slug_renames import ARTICLE_SLUGS, rename_slugs

    rename_slugs(Article, ARTICLE_SLUGS)
    articles = json.loads(ARTICLES_JSON.read_text(encoding='utf-8'))
    for data in articles:
        art, _created = Article.objects.update_or_create(
            slug=data['slug'],
            defaults={
                'title': data['title'],
                'category': data['cat'],
                'published_at': date.fromisoformat(data['date']),
                'excerpt': data['excerpt'],
                'seo_title': data.get('seo_title') or data['title'],
                'seo_description': data.get('seo_description') or data['excerpt'],
                'h1': data['title'],
                'is_published': True,
            },
        )
        assign_image(art.image, data['img'])
        art.save()
        art.blocks.all().delete()
        for kwargs in _blocks_from_js(data['body']):
            ArticleBlock.objects.create(article=art, **kwargs)


def seed_cases():
    from src.core.slug_renames import CASE_SLUGS, rename_slugs

    rename_slugs(CaseStudy, CASE_SLUGS)
    cases = [
        {
            'slug': 'nelehalni-pidaktsyzni-tovary',
            'cat': 'Бізнес-аналітика',
            'img': 'blog/magn.jpg',
            'demo': False,
            'title': 'Дослідження торгівлі нелегальними підакцизними товарами в Україні',
            'excerpt': 'Замовник хотів зрозуміти, де і як продають підроблені та контрабандні товари визначеного сегменту.',
            'seo_title': 'Нелегальні товари: де їх продають і як це рахують — Vartis',
            'seo_description': (
                'Замовник хотів зрозуміти, де і як продають підроблені та контрабандні товари '
                'визначеного сегменту, які марки трапляються частіше і звідки товар іде в магазини.'
            ),
            'client': 'Знеособлено за NDA',
            'service': 'Глибока бізнес-аналітика',
            'scope': '21 область',
            'stats': [
                ('2 293', 'торговельні точки з нелегальним товаром'),
                ('21', 'область охоплення'),
                ('75,1%', 'точок продають товар за заниженою ціною'),
                ('64,4%', 'усіх точок зосереджено у пʼяти областях'),
            ],
            'blocks': [
                {
                    'h': 'Стислий огляд — головне в цифрах',
                    'list': 'Майже чверть усіх точок — в одній області.\nУ кожній третій точці продають товар без акцизної марки.',
                },
                {
                    'h': 'Факти окремо від припущень',
                    'p': 'Щоб зʼясувати, звідки товар надходить у магазини, ми дослідили продаж у месенджерах.',
                    'facts': 'Усі посилки з одного міста і відділення.\nЗамовлення відправляють в один і той самий час.\nВідправники — нещодавно зареєстровані підприємці.',
                    'assumption': 'Три канали, найімовірніше, мають спільних організаторів.',
                    'why': 'Прямого підтвердження спільного власника немає — висновок позначений як припущення.',
                },
            ],
        },
        {
            'slug': 'ekspres-perevirka-postachalnyka',
            'cat': 'Перевірка контрагентів',
            'img': 'blog/laptop.jpg',
            'demo': True,
            'title': 'Експрес-перевірка нового постачальника через VI Analysis',
            'excerpt': 'Компанія отримала вигідну пропозицію з вимогою передоплати.',
            'seo_title': 'Експрес-перевірка постачальника до передоплати — Vartis',
            'seo_description': (
                'Компанія отримала вигідну пропозицію з вимогою передоплати. '
                'Перевірка до договору охоплює правові, фінансові, репутаційні та успадковані ризики.'
            ),
            'client': 'Демонстраційний приклад',
            'service': 'Перевірка контрагентів',
            'scope': 'Назва та код ЄДРПОУ',
            'stats': [('3', 'кроки: збір, оцінка, рекомендація'), ('3', 'рівні ризику')],
            'blocks': [
                {'h': 'Задача', 'p': 'Перевірити контрагента до підписання договору.'},
                {'h': 'Що перевіряє сервіс', 'list': 'Правові ризики\nФінансові ризики\nРепутаційні ризики\nУспадковані ризики'},
            ],
        },
        {
            'slug': 'rozsliduvannia-zbytkiv',
            'cat': 'Розслідування збитків',
            'img': 'blog/fin.jpg',
            'demo': True,
            'title': 'Продажі ростуть, а прибуток падає: пошук причин збитків',
            'excerpt': 'Витрати зростали, а за звітами все виглядало нормально.',
            'seo_title': 'Продажі ростуть, а прибуток падає: пошук причин збитків',
            'seo_description': (
                'Витрати зростали, а за звітами все виглядало нормально. '
                'Розбір типових причин: завищення цін закупівель, нестачі, списання і межі внутрішньої перевірки.'
            ),
            'client': 'Демонстраційний приклад',
            'service': 'Розслідування причин збитків',
            'scope': 'Процеси закупівель',
            'stats': [],
            'blocks': [
                {'h': 'Типова ситуація', 'list': 'Завищення цін закупівель\nНестачі та списання\nВнутрішня перевірка нічого не дала'},
                {'h': 'Конфіденційність', 'p': 'Висновки отримує лише особа, визначена в договорі.'},
            ],
        },
        {
            'slug': 'zakhyst-vid-vytoku',
            'cat': 'Захист інформації',
            'img': 'blog/lock.jpg',
            'demo': True,
            'title': 'Клієнти йдуть до конкурентів: побудова захисту від витоку',
            'excerpt': 'Компанія втрачала замовлення, а конкуренти знали більше, ніж мали б.',
            'seo_title': 'Клієнти йдуть до конкурентів: захист інформації від витоку',
            'seo_description': (
                'Компанія втрачала замовлення, а конкуренти знали більше, ніж мали б. '
                'У роботу входить система захисту, документальне оформлення і подальша актуалізація.'
            ),
            'client': 'Демонстраційний приклад',
            'service': 'Захист конфіденційної інформації',
            'scope': 'Офіс і транспорт',
            'stats': [],
            'blocks': [
                {'h': 'Що входить', 'list': 'Система захисту від витоку\nДокументальне оформлення\nПідтримка та актуалізація'},
            ],
        },
        {
            'slug': 'kryminalne-provadzhennia',
            'cat': 'Кримінальні провадження',
            'img': 'blog/law.jpg',
            'demo': True,
            'title': 'Інформаційна підтримка сторони захисту',
            'excerpt': 'Адвокатське обʼєднання потребувало перевірки достовірності даних обвинувачення.',
            'seo_title': 'Інформаційна підтримка адвоката у кримінальній справі',
            'seo_description': (
                'Адвокатське обʼєднання потребувало перевірки даних обвинувачення. '
                'Допомагаємо звірити дані, зібрати альтернативні версії та оцінити їх допустимість.'
            ),
            'client': 'Демонстраційний приклад',
            'service': 'Інформаційна підтримка у кримінальних провадженнях',
            'scope': 'Для адвокатів',
            'stats': [],
            'blocks': [
                {'h': 'Чим допомагаємо', 'list': 'Перевірка достовірності даних\nАльтернативні версії\nОцінка допустимості інформації'},
            ],
        },
    ]

    for data in cases:
        case, created = CaseStudy.objects.update_or_create(
            slug=data['slug'],
            defaults={
                'title': data['title'],
                'category': data['cat'],
                'excerpt': data['excerpt'],
                'client': data['client'],
                'service': data['service'],
                'scope': data['scope'],
                'is_demo': data['demo'],
                'is_published': True,
                'seo_title': data.get('seo_title', data['title']),
                'seo_description': data.get('seo_description', data['excerpt']),
                'h1': data['title'],
            },
        )
        assign_image(case.image, data['img'])
        case.save()
        if created or not case.blocks.exists():
            case.stats.all().delete()
            case.blocks.all().delete()
            for i, (v, l) in enumerate(data['stats']):
                CaseStat.objects.create(case=case, value=v, label=l, order=i)
            for i, block in enumerate(data['blocks']):
                CaseBlock.objects.create(
                    case=case,
                    heading=block.get('h', ''),
                    text=block.get('p', ''),
                    list_items=block.get('list', ''),
                    facts=block.get('facts', ''),
                    assumption=block.get('assumption', ''),
                    why=block.get('why', ''),
                    order=i,
                )
