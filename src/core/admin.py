from django import forms
from django.contrib import admin
from django.contrib.admin import ModelAdmin as DjangoModelAdmin
from unfold.admin import ModelAdmin
from unfold.forms import ActionForm

from .admin_i18n import BilingualAdminMixin
from .admin_recent_actions import patch_admin_urls
from .admin_site_content_proxies import register_site_content_section_admins
from .admin_site_content_widgets import CmsImageFieldWidget
from .models import SiteSettings
from .models_interface import InterfaceCopy

register_site_content_section_admins()
patch_admin_urls()


@admin.register(SiteSettings)
class SiteSettingsAdmin(BilingualAdminMixin, ModelAdmin):
    fieldsets = (
        ('Компанія', {
            'classes': ('tab',),
            'fields': ('company_name', 'tagline', 'logo'),
        }),
        ('Контакти', {
            'classes': ('tab',),
            'fields': ('phone', 'email', 'address', 'map_embed_url', 'facebook_url', 'telegram_chat_url', 'telegram_url'),
        }),
        ('SEO', {
            'classes': ('tab',),
            'fields': ('default_seo_title', 'default_seo_description'),
        }),
    )

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj=obj, change=change, **kwargs)
        if 'logo' in form.base_fields:
            preview = ''
            if obj and obj.logo:
                try:
                    preview = obj.logo.url
                except (ValueError, OSError):
                    preview = ''
            form.base_fields['logo'].widget = CmsImageFieldWidget(
                hint='Рекомендовано: PNG з прозорістю, ~180×100 px, до 500 КБ. Показується в шапці та футері.',
                preview_url=preview,
            )
        return form

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        SiteSettings.load()
        return super().changelist_view(request, extra_context)


class VartisActionForm(ActionForm):
    action = forms.ChoiceField(
        label='',
        widget=forms.Select(attrs={
            'class': 'vartis-action-select',
            'aria-label': 'Виберіть дію',
            'x-model': 'action',
        }),
    )


def _ukrainian_action_choices(self, request, default_choices=None):
    return DjangoModelAdmin.get_action_choices(self, request, [('', 'Виберіть дію')])


ModelAdmin.action_form = VartisActionForm
ModelAdmin.get_action_choices = _ukrainian_action_choices


@admin.register(InterfaceCopy)
class InterfaceCopyAdmin(BilingualAdminMixin, ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        from django.shortcuts import redirect
        from django.urls import reverse

        InterfaceCopy.load()
        return redirect(reverse('admin:core_interfacecopy_change', args=[1]))
