from django.db import migrations, models


def forwards(apps, schema_editor):
    from src.pages.home_directions_seed import seed_home_directions

    seed_home_directions()


class Migration(migrations.Migration):
    dependencies = [
        ('pages', '0010_canon_copy'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeDirection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Заголовок')),
                ('text', models.TextField(blank=True, verbose_name='Текст')),
                ('image', models.ImageField(blank=True, upload_to='pages/home/directions/', verbose_name='Зображення')),
                ('href', models.CharField(blank=True, max_length=200, verbose_name='Посилання')),
                ('is_visible', models.BooleanField(default=True, verbose_name='Показувати на головній')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок')),
                (
                    'page',
                    models.ForeignKey(
                        on_delete=models.CASCADE,
                        related_name='directions',
                        to='pages.homepage',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Напрям на головній',
                'verbose_name_plural': 'Напрями на головній',
                'ordering': ['order', 'id'],
            },
        ),
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
