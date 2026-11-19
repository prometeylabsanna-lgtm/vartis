from django.db import migrations


def forwards(apps, schema_editor):
    from src.pages.canon_seed import sync_all

    sync_all()


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0009_canon_page_fields"),
        ("core", "0011_canon_page_fields"),
        ("leads", "0002_canon_page_fields"),
        ("blog", "0002_canon_page_fields"),
        ("cases", "0002_canon_page_fields"),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
