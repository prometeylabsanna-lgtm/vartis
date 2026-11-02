from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Lead


@admin.register(Lead)
class LeadAdmin(ModelAdmin):
    list_display = ('name', 'phone', 'email', 'status', 'source_page', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'phone', 'email')
    readonly_fields = ('name', 'phone', 'email', 'message', 'consent', 'source_page', 'created_at')
    fields = ('status', 'name', 'phone', 'email', 'message', 'consent', 'source_page', 'created_at')

    def has_add_permission(self, request):
        return False
