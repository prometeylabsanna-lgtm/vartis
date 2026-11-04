from django.contrib import admin
from unfold.admin import ModelAdmin

from .admin_recent_actions import patch_admin_urls
from .admin_site_content_proxies import register_site_content_section_admins
from .admin_site_content_widgets import CmsImageFieldWidget
from .models import SiteSettings

register_site_content_section_admins()
patch_admin_urls()


@admin.register(SiteSettings)
class SiteSettingsAdmin(ModelAdmin):
    fieldsets = (
        ('Компанія', {
            'classes': ('tab',),
            'fields': ('company_name', 'tagline', 'logo'),
        }),
        ('Контакти', {
            'classes': ('tab',),
            'fields': ('phone', 'email', 'address', 'map_embed_url', 'facebook_url'),
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
