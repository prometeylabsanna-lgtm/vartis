from django.db import migrations, models


def reset_styles(apps, schema_editor):
    PageStyle = apps.get_model("core", "PageStyle")
    for row in PageStyle.objects.all():
        changed = False
        if row.glass_enabled:
            row.glass_enabled = False
            changed = True
        bg = (row.background_color or "").strip().lower()
        text = (row.text_color or "").strip().lower()
        if bg in {"#0b1626", "0b1626"}:
            row.background_color = ""
            changed = True
        if text in {"#f6f0e6", "f6f0e6", "#e8edf4", "e8edf4"}:
            row.text_color = ""
            changed = True
        if changed:
            row.save(update_fields=["glass_enabled", "background_color", "text_color"])


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_site_header_footer_uk_names"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pagestyle",
            name="glass_enabled",
            field=models.BooleanField(default=False, verbose_name="Скло (glass)"),
        ),
        migrations.RunPython(reset_styles, noop),
    ]
