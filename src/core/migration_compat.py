"""Сумісність старих data-міграцій, які викликають код на «живих» моделях.

core 0007/0008 запускають content_sync.sync_editorial() з реальними моделями.
На чистій БД (тести, нове середовище) у цей момент ще немає колонок, доданих
пізнішими міграціями (напр. SiteSettings.telegram_chat_url з core 0009),
і SELECT падає. Тут ми тимчасово відкладаємо (defer) такі поля на час виклику.
На проді 0007/0008 вже застосовані — поведінка там не змінюється.
"""

from contextlib import contextmanager


@contextmanager
def defer_missing_columns(schema_editor, *models):
    connection = schema_editor.connection
    patched = []
    with connection.cursor() as cursor:
        for model in models:
            table = model._meta.db_table
            existing = {col.name for col in connection.introspection.get_table_description(cursor, table)}
            missing = [f.attname for f in model._meta.concrete_fields if f.column not in existing]
            if missing:
                original = model.__dict__['objects']
                model.objects = model._default_manager.defer(*missing)
                patched.append((model, original))
    try:
        yield
    finally:
        for model, original in patched:
            setattr(model, 'objects', original)
