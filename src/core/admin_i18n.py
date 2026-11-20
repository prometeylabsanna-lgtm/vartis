"""Пари українське поле / поле (EN) у формах адмінки."""

from __future__ import annotations


def _field_names(model) -> set[str]:
    names = set()
    for field in model._meta.get_fields():
        name = getattr(field, 'name', None)
        if name:
            names.add(name)
    return names


def expand_names(names, model):
    existing = _field_names(model)
    out = []
    seen = set()
    for name in names:
        if name in seen:
            continue
        seen.add(name)
        out.append(name)
        extra = None
        if name == 'slug' and 'slug_en' in existing:
            extra = 'slug_en'
        elif not str(name).endswith('_en') and f'{name}_en' in existing:
            extra = f'{name}_en'
        if extra and extra not in seen:
            seen.add(extra)
            out.append(extra)
    return type(names)(out) if not isinstance(names, list) else out


def expand_field_spec(spec, model):
    if not isinstance(spec, (list, tuple)):
        return spec
    expanded = []
    for item in spec:
        if isinstance(item, (list, tuple)):
            expanded.append(expand_names(item, model))
        else:
            expanded.extend(expand_names((item,), model))
    return type(spec)(expanded)


def expand_fieldsets(fieldsets, model):
    result = []
    for title, opts in fieldsets:
        opts = dict(opts)
        if 'fields' in opts:
            opts['fields'] = expand_field_spec(tuple(opts['fields']), model)
        result.append((title, opts))
    return result


class BilingualAdminMixin:
    def get_fieldsets(self, request, obj=None):
        return expand_fieldsets(super().get_fieldsets(request, obj), self.model)

    def get_fields(self, request, obj=None):
        return expand_field_spec(super().get_fields(request, obj), self.model)
