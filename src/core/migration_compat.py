"""Сумісність старих data-міграцій, які викликають код на «живих» моделях.

core 0007/0008 запускають content_sync.sync_editorial() з реальними моделями.
На чистій БД (тести, нове середовище) у цей момент ще немає колонок, доданих
пізнішими міграціями (напр. SiteSettings.telegram_chat_url з core 0009),
і SELECT падає. Тут ми тимчасово відкладаємо (defer) такі поля на час виклику.
На проді 0007/0008 вже застосовані — поведінка там не змінюється.
"""

from contextlib import contextmanager

from django.apps import apps


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


@contextmanager
def hide_unmigrated_fields(schema_editor):
    """Прибирає з моделей колонки, яких ще немає в таблиці.

    Потрібно для data-міграцій, що викликають живі моделі після появи
    полів перекладу: інакше SELECT/INSERT шукає seo_title_uk занадто рано.
    """
    from django.db.models.base import Model
    from django.db.models.query import QuerySet
    from modeltranslation.fields import TranslationFieldDescriptor
    from modeltranslation.manager import MultilingualQuerySet

    connection = schema_editor.connection
    hidden = []
    tables = set(connection.introspection.table_names())
    with connection.cursor() as cursor:
        for model in apps.get_models():
            if model._meta.proxy or not model._meta.managed:
                continue
            table = model._meta.db_table
            if table not in tables:
                continue
            columns = {
                col.name for col in connection.introspection.get_table_description(cursor, table)
            }
            removed = False
            for field in list(model._meta.local_fields):
                if field.column not in columns:
                    model._meta.local_fields.remove(field)
                    hidden.append((model, field))
                    removed = True
            if removed:
                model._meta._expire_cache()

    original_get = TranslationFieldDescriptor.__get__
    original_set = TranslationFieldDescriptor.__set__

    def _get(self, instance, owner):
        if instance is None:
            return self
        if self.field.name in instance.__dict__:
            return instance.__dict__[self.field.name]
        return original_get(self, instance, owner)

    def _set(self, instance, value):
        instance.__dict__[self.field.name] = value

    original_update = MultilingualQuerySet._update

    def _update(self, values, *args, **kwargs):
        return QuerySet._update(self, values)

    saved_inits = []
    for model in {item[0] for item in hidden}:
        saved_inits.append((model, model.__init__))

        def _init(self, *args, __model=model, **kwargs):
            self._mt_init = True
            valid = {field.name for field in __model._meta.concrete_fields}
            kwargs = {key: value for key, value in kwargs.items() if key in valid}
            return Model.__init__(self, *args, **kwargs)

        model.__init__ = _init

    TranslationFieldDescriptor.__get__ = _get
    TranslationFieldDescriptor.__set__ = _set
    MultilingualQuerySet._update = _update
    try:
        yield
    finally:
        TranslationFieldDescriptor.__get__ = original_get
        TranslationFieldDescriptor.__set__ = original_set
        MultilingualQuerySet._update = original_update
        for model, init in saved_inits:
            model.__init__ = init
        seen = set()
        for model, field in hidden:
            model._meta.local_fields.append(field)
            seen.add(model)
        for model in seen:
            model._meta._expire_cache()
