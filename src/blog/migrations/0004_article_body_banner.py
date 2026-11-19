from django.db import migrations, models


def copy_blocks_into_body(apps, schema_editor):
    from src.blog.body_html import article_blocks_to_html

    Article = apps.get_model('blog', 'Article')
    ArticleBlock = apps.get_model('blog', 'ArticleBlock')
    for article in Article.objects.all():
        if (article.body or '').strip():
            continue
        blocks = ArticleBlock.objects.filter(article_id=article.pk).order_by('order', 'id')
        html = article_blocks_to_html(blocks)
        if html:
            article.body = html
            article.save(update_fields=['body'])


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_article_read_minutes'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='body',
            field=models.TextField(blank=True, verbose_name='Текст'),
        ),
        migrations.CreateModel(
            name='BlogArticleBanner',
            fields=[],
            options={
                'verbose_name': 'Банер у статті',
                'verbose_name_plural': 'Банер у статті',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('blog.blogpage',),
        ),
        migrations.RunPython(copy_blocks_into_body, migrations.RunPython.noop),
    ]
