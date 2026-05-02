from django.contrib import admin
from .models import Profile, AuditEntry


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'id_number', 'phone', 'county', 'is_verified', 'role', 'created_at']
    list_filter = ['is_verified', 'role', 'county', 'gender']
    search_fields = ['user__username', 'user__email', 'id_number', 'phone']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(AuditEntry)
class AuditEntryAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'ip_address', 'created_at']
    list_filter = ['action', 'created_at']
    search_fields = ['user__username', 'action', 'details']
    readonly_fields = ['created_at']
