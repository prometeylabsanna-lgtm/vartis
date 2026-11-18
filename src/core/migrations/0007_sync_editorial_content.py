from django.db import migrations


def sync_saved_content(apps, schema_editor):
    from src.core.content_sync import sync_editorial
    from src.core.migration_compat import defer_missing_columns
    from src.core.models import SiteSettings

    # Колонки з пізніших міграцій (напр. telegram_chat_url, core 0009) тут ще не існують.
    with defer_missing_columns(schema_editor, SiteSettings):
        sync_editorial()


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
        ('cases', '0001_initial'),
        ('core', '0006_official_contacts_and_translit'),
        ('pages', '0008_official_contacts_and_translit'),
    ]

    operations = [
        migrations.RunPython(sync_saved_content, migrations.RunPython.noop),
    ]
