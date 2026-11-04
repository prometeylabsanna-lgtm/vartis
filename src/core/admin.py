from django.contrib import admin
from unfold.admin import ModelAdmin

from .admin_site_content_proxies import register_site_content_section_admins
from .models import SiteSettings

register_site_content_section_admins()


@admin.register(SiteSettings)
class SiteSettingsAdmin(ModelAdmin):
    fieldsets = (
        ('Компанія', {
            'fields': ('company_name', 'tagline'),
        }),
        ('Контакти', {
            'fields': ('phone', 'email', 'address', 'map_embed_url', 'facebook_url'),
        }),
        ('SEO за замовчуванням', {
            'fields': ('default_seo_title', 'default_seo_description'),
        }),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        SiteSettings.load()
        return super().changelist_view(request, extra_context)
