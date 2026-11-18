"""Українські назви полів адмінки замість «Hero»/«Eyebrow» у вже створених SiteBlock.

Міняє лише точні старі назви (ідемпотентно); власні назви, змінені вручну, не чіпає.
Контент (text_html) не змінюється.
"""

from django.db import migrations

RENAMES = {
    'Hero заголовок': 'Заголовок першого екрана',
    'Hero текст': 'Текст першого екрана',
    'Hero зображення': 'Зображення першого екрана',
    'Показувати Hero': 'Показувати перший екран',
    'Eyebrow науки': 'Надзаголовок науки',
    'Eyebrow партнерів': 'Надзаголовок партнерів',
}


def forwards(apps, schema_editor):
    SiteBlock = apps.get_model('core', 'SiteBlock')
    for old, new in RENAMES.items():
        SiteBlock.objects.filter(label=old).update(label=new)


def backwards(apps, schema_editor):
    SiteBlock = apps.get_model('core', 'SiteBlock')
    for old, new in RENAMES.items():
        SiteBlock.objects.filter(label=new).update(label=old)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_telegram_chat_url_and_ua_labels'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
