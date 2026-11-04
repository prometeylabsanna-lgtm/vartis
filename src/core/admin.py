from django.contrib import admin
from unfold.admin import ModelAdmin

from .admin_recent_actions import patch_admin_urls
from .admin_site_content_proxies import register_site_content_section_admins
from .models import SiteSettings

register_site_content_section_admins()
patch_admin_urls()


@admin.register(SiteSettings)
class SiteSettingsAdmin(ModelAdmin):
    fieldsets = (
        ('Компанія', {
            'classes': ('tab',),
            'fields': ('company_name', 'tagline'),
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

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        SiteSettings.load()
        return super().changelist_view(request, extra_context)
