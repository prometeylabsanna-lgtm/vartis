"""Вкладки Українська / English у формах адмінки, як у Gestia."""

from __future__ import annotations

UK_TAB = 'Українська'
EN_TAB = 'English'


def _field_names(model) -> set[str]:
    names = set()
    for field in model._meta.get_fields():
        name = getattr(field, 'name', None)
        if name:
            names.add(name)
    return names


def _en_pair(name, existing):
    if name == 'slug' and 'slug_en' in existing:
        return 'slug_en'
    extra = f'{name}_en'
    if not str(name).endswith('_en') and extra in existing:
        return extra
    return None


def _flatten(fields):
    for item in fields or ():
        if isinstance(item, (list, tuple)):
            yield from item
        else:
            yield item


def collect_uk_en(fields, model):
    existing = _field_names(model)
    uk, en = [], []
    seen_uk, seen_en = set(), set()
    for name in _flatten(fields):
        if str(name).endswith('_en'):
            if name not in seen_en:
                seen_en.add(name)
                en.append(name)
            continue
        if name not in seen_uk:
            seen_uk.add(name)
            uk.append(name)
        extra = _en_pair(name, existing)
        if extra and extra not in seen_en:
            seen_en.add(extra)
            en.append(extra)
    return uk, en


def expand_names(names, model):
    """Спочатку українські й спільні поля, потім англійські — для інлайнів."""
    uk, en = collect_uk_en(names, model)
    out = uk + en
    return type(names)(out) if not isinstance(names, list) else out


def expand_field_spec(spec, model):
    if not isinstance(spec, (list, tuple)):
        return spec
    uk, en = collect_uk_en(spec, model)
    return type(spec)(uk + en)


def language_fieldsets(fieldsets, model):
    """Дві вкладки мови + вкладки без перекладу (баннер, оформлення)."""
    if not fieldsets:
        return fieldsets
    first_title = fieldsets[0][0]
    if first_title in (UK_TAB, EN_TAB):
        return fieldsets

    uk_fields = []
    en_fields = []
    extra = []
    seen_uk, seen_en = set(), set()
    for title, opts in fieldsets:
        opts = dict(opts)
        fields = opts.get('fields') or ()
        uk, en = collect_uk_en(fields, model)
        if en:
            for name in uk:
                if name not in seen_uk:
                    seen_uk.add(name)
                    uk_fields.append(name)
            for name in en:
                if name not in seen_en:
                    seen_en.add(name)
                    en_fields.append(name)
        else:
            extra.append((title, opts))

    if not en_fields:
        return tuple(fieldsets)

    result = [
        (UK_TAB, {'classes': ['tab'], 'fields': tuple(uk_fields)}),
        (EN_TAB, {'classes': ['tab'], 'fields': tuple(en_fields)}),
    ]
    result.extend(extra)
    return tuple(result)


def expand_fieldsets(fieldsets, model):
    return language_fieldsets(fieldsets, model)


class BilingualAdminMixin:
    def get_fieldsets(self, request, obj=None):
        return language_fieldsets(super().get_fieldsets(request, obj), self.model)

    def get_fields(self, request, obj=None):
        return expand_field_spec(super().get_fields(request, obj), self.model)
