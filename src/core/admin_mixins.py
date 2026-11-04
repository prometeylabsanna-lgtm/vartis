"""Спільні міксини адмінки Unfold."""

from __future__ import annotations

from django.db import models

from .admin_filters import (
    VartisAllValuesDropdownFilter,
    VartisBooleanDropdownFilter,
    VartisChoicesDropdownFilter,
    VartisRangeDateFilter,
    VartisRelatedDropdownFilter,
)


class TopDropdownFiltersMixin:
    """
    Усі list_filter — випадаючі меню зверху сторінки (не сайдбар справа).
    Підписи без префікса «За».
    """

    list_filter_sheet = False

    def get_list_filter(self, request):
        raw = list(super().get_list_filter(request))
        converted = []
        options: dict = {}

        for item in raw:
            if isinstance(item, (tuple, list)):
                field_path, filter_cls = item[0], item[1]
                converted.append((field_path, filter_cls))
                options[field_path] = {
                    'horizontal': True,
                    'label': self._filter_label_for_path(field_path),
                }
                continue

            if isinstance(item, str):
                field_path = item
                field = self._resolve_field(field_path)
                filter_cls = self._dropdown_class_for_field(field)
                converted.append((field_path, filter_cls))
                options[field_path] = {
                    'horizontal': True,
                    'label': self._filter_label_for_path(field_path),
                }
                continue

            # SimpleListFilter (клас)
            converted.append(item)
            param = getattr(item, 'parameter_name', None)
            title = getattr(item, 'title', param)
            if param:
                options[param] = {
                    'horizontal': True,
                    'label': str(title).strip() if title else param,
                }

        self._vartis_list_filter_options = options
        return converted

    @property
    def list_filter_options(self):
        if hasattr(self, '_vartis_list_filter_options'):
            return self._vartis_list_filter_options
        return {}

    def _resolve_field(self, field_path: str):
        bits = field_path.split('__')
        field = None
        model = self.model
        for bit in bits:
            field = model._meta.get_field(bit)
            model = getattr(getattr(field, 'remote_field', None), 'model', model)
        return field

    def _filter_label_for_path(self, field_path: str) -> str:
        try:
            return str(self._resolve_field(field_path).verbose_name).strip()
        except Exception:
            return field_path

    @staticmethod
    def _dropdown_class_for_field(field):
        if getattr(field, 'remote_field', None) is not None:
            return VartisRelatedDropdownFilter
        if isinstance(field, models.BooleanField):
            return VartisBooleanDropdownFilter
        if isinstance(field, (models.DateTimeField, models.DateField)):
            return VartisRangeDateFilter
        if getattr(field, 'choices', None):
            return VartisChoicesDropdownFilter
        return VartisAllValuesDropdownFilter
