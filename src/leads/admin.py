from django.contrib import admin
from unfold.admin import ModelAdmin

from src.core.admin_mixins import TopDropdownFiltersMixin

from .models import Lead, LeadModal


@admin.register(Lead)
class LeadAdmin(TopDropdownFiltersMixin, ModelAdmin):
    list_display = ('name', 'phone', 'email', 'status', 'source_page', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'phone', 'email')
    readonly_fields = ('name', 'phone', 'email', 'message', 'consent', 'source_page', 'created_at')
    fields = ('status', 'name', 'phone', 'email', 'message', 'consent', 'source_page', 'created_at')

    def has_add_permission(self, request):
        return False


@admin.register(LeadModal)
class LeadModalAdmin(ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        from django.shortcuts import redirect
        from django.urls import reverse

        LeadModal.load()
        return redirect(reverse("admin:leads_leadmodal_change", args=[1]))
