from django.core.validators import MinValueValidator
from django.db import migrations, models


def copy_estimated_minutes(apps, schema_editor):
    Article = apps.get_model('blog', 'Article')
    ArticleBlock = apps.get_model('blog', 'ArticleBlock')
    for article in Article.objects.all():
        words = len((article.excerpt or '').split())
        for block in ArticleBlock.objects.filter(article_id=article.pk):
            words += len((block.heading or '').split())
            words += len((block.text or '').split())
            words += len((block.list_items or '').split())
        article.read_minutes = max(1, round(words / 180)) if words else 6
        article.save(update_fields=['read_minutes'])


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_canon_page_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='read_minutes',
            field=models.PositiveIntegerField(
                default=6,
                help_text='Скільки хвилин показувати біля статті.',
                validators=[MinValueValidator(1)],
                verbose_name='Хвилин читання',
            ),
        ),
        migrations.RunPython(copy_estimated_minutes, migrations.RunPython.noop),
    ]
