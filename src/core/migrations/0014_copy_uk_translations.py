from django.db import migrations


def copy_default_language(apps, schema_editor):
    from django.core.management import call_command

    call_command('update_translation_fields', verbosity=0)


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0013_en_locale'),
        ('pages', '0013_en_locale'),
        ('blog', '0005_en_locale'),
        ('leads', '0003_en_locale'),
    ]

    operations = [
        migrations.RunPython(copy_default_language, migrations.RunPython.noop),
    ]
