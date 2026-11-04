"""Dropdown-фільтри Unfold без префікса «За»."""

from collections.abc import Iterator

from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.core.validators import EMPTY_VALUES
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from unfold.contrib.filters.admin.mixins import DropdownMixin, ValueMixin
from unfold.contrib.filters.forms import DropdownForm


def _filter_label(title) -> str:
    return str(title).strip()


class VartisChoicesDropdownFilter(ValueMixin, DropdownMixin, admin.ChoicesFieldListFilter):
    def queryset(self, request: HttpRequest, queryset: QuerySet) -> QuerySet | None:
        if self.value() not in EMPTY_VALUES:
            return super().queryset(request, queryset)
        return queryset

    def choices(self, changelist: ChangeList) -> Iterator:
        choices = [self.all_option] if self.all_option else []
        choices.extend(self.field.flatchoices)
        yield {
            'form': self.form_class(
                label=_filter_label(self.title),
                name=self.lookup_kwarg,
                choices=choices,
                data={self.lookup_kwarg: self.value()},
            ),
        }


class VartisRelatedDropdownFilter(ValueMixin, DropdownMixin, admin.RelatedFieldListFilter):
    def queryset(self, request: HttpRequest, queryset: QuerySet) -> QuerySet | None:
        if self.value() not in EMPTY_VALUES:
            return super().queryset(request, queryset)
        return queryset

    def choices(self, changelist: ChangeList) -> Iterator:
        choices = [self.all_option, *self.lookup_choices] if self.all_option else list(self.lookup_choices)
        yield {
            'form': self.form_class(
                label=_filter_label(self.title),
                name=self.lookup_kwarg,
                choices=choices,
                data={self.lookup_kwarg: self.value()},
            ),
        }


class VartisAllValuesDropdownFilter(ValueMixin, DropdownMixin, admin.AllValuesFieldListFilter):
    def choices(self, changelist: ChangeList) -> Iterator:
        choices = [self.all_option] if self.all_option else []
        for val in self.lookup_choices:
            if val is None:
                continue
            choices.append((str(val), str(val)))
        yield {
            'form': self.form_class(
                label=_filter_label(self.title),
                name=self.lookup_kwarg,
                choices=choices,
                data={self.lookup_kwarg: self.value()},
            ),
        }


class VartisBooleanDropdownFilter(ValueMixin, DropdownMixin, admin.BooleanFieldListFilter):
    def queryset(self, request: HttpRequest, queryset: QuerySet) -> QuerySet | None:
        if self.value() not in EMPTY_VALUES:
            return super().queryset(request, queryset)
        return queryset

    def choices(self, changelist: ChangeList) -> Iterator:
        choices = [
            self.all_option,
            ('1', _('Yes')),
            ('0', _('No')),
        ]
        yield {
            'form': DropdownForm(
                label=_filter_label(self.title),
                name=self.lookup_kwarg,
                choices=choices,
                data={self.lookup_kwarg: self.value()},
            ),
        }
