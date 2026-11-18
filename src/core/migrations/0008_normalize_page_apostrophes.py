from django.db import migrations


def sync_saved_content(apps, schema_editor):
    from src.core.content_sync import sync_editorial

    sync_editorial()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_sync_editorial_content'),
    ]

    operations = [
        migrations.RunPython(sync_saved_content, migrations.RunPython.noop),
    ]
