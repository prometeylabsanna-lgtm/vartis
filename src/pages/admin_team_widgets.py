"""Віджети списків команди: адмін бачить рядки, JSON збирається сам."""

from __future__ import annotations

import json

from django.forms.widgets import Widget
from unfold.widgets import INPUT_CLASSES


def _parse_list(value):
    if value in (None, '', [], ()):
        return []
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except json.JSONDecodeError:
            lines = [line.strip() for line in value.splitlines() if line.strip()]
            return lines
    if isinstance(value, list):
        return value
    return []


def _input_class(*extra: str) -> str:
    classes = list(INPUT_CLASSES) + ['cms-list__input', *extra]
    return ' '.join(dict.fromkeys(classes))


class ExpertiseListWidget(Widget):
    template_name = 'admin/widgets/cms_string_list.html'

    def format_value(self, value):
        items = []
        for item in _parse_list(value):
            text = str(item).strip()
            if text:
                items.append(text)
        return items or ['']

    def value_from_datadict(self, data, files, name):
        return [item.strip() for item in data.getlist(f'{name}_item') if item.strip()]

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['items'] = self.format_value(value)
        context['widget']['input_class'] = _input_class()
        return context

    class Media:
        js = ('js/admin/cms_json_list.js',)
        css = {'all': ('css/admin/cms_json_list.css',)}


class CareerPathWidget(Widget):
    template_name = 'admin/widgets/cms_career_path.html'

    def format_value(self, value):
        rows = []
        for item in _parse_list(value):
            if isinstance(item, dict):
                title = str(item.get('t') or item.get('title') or '').strip()
                year = str(item.get('y') or item.get('year') or '').strip()
            else:
                title = str(item).strip()
                year = ''
            if title:
                rows.append({'t': title, 'y': year})
        return rows or [{'t': '', 'y': ''}]

    def value_from_datadict(self, data, files, name):
        titles = data.getlist(f'{name}_t')
        years = data.getlist(f'{name}_y')
        rows = []
        for index, title in enumerate(titles):
            text = title.strip()
            if not text:
                continue
            year = years[index].strip() if index < len(years) else ''
            rows.append({'t': text, 'y': year})
        return rows

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['items'] = self.format_value(value)
        context['widget']['title_class'] = _input_class('cms-list__title')
        context['widget']['year_class'] = _input_class('cms-list__year')
        return context

    class Media:
        js = ('js/admin/cms_json_list.js',)
        css = {'all': ('css/admin/cms_json_list.css',)}
