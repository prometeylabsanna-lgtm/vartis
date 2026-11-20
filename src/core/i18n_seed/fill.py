"""Заповнює порожні англійські поля, не затираючи окремий переклад редактора."""

from __future__ import annotations

from contextlib import contextmanager

_CYRILLIC_START = '\u0400'
_CYRILLIC_END = '\u04FF'


def _default(obj, name):
    try:
        field = obj._meta.get_field(name)
    except Exception:
        return None
    default = field.default
    if default is None or getattr(field, 'empty_strings_allowed', False) and default is None:
        return default
    return default() if callable(default) else default


def _blank(value) -> bool:
    return value is None or value == '' or value == [] or value == {}


def looks_ukrainian(value) -> bool:
    if not isinstance(value, str):
        return False
    return any(_CYRILLIC_START <= ch <= _CYRILLIC_END for ch in value)


def open_for_english(current, ukrainian, default) -> bool:
    if _blank(current):
        return True
    # Якщо в EN уже лежить український текст (seed при активній 'en'), це не переклад.
    if looks_ukrainian(current):
        return True
    if default not in (None, '') and current == default:
        return True
    if not _blank(ukrainian) and current == ukrainian:
        return True
    return False


@contextmanager
def under_ukrainian():
    from django.utils import translation

    with translation.override('uk'):
        yield


def fill_en(obj, **values) -> bool:
    dirty = False
    for name, english in values.items():
        if english is None:
            continue
        if name.endswith('_en'):
            field_name = name
            base = name[:-3]
        else:
            field_name = f'{name}_en'
            base = name
        if not hasattr(obj, field_name):
            continue
        current = getattr(obj, field_name)
        ukrainian = getattr(obj, f'{base}_uk', None)
        if ukrainian is None:
            ukrainian = getattr(obj, base, None)
        if not open_for_english(current, ukrainian, _default(obj, base)):
            continue
        if current == english:
            continue
        setattr(obj, field_name, english)
        dirty = True
    if dirty:
        obj.save()
    return dirty


def fill_ordered(queryset, rows):
    items = list(queryset.order_by('order', 'id'))
    for item, row in zip(items, rows):
        fill_en(item, **row)
