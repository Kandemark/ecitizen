from django.contrib import admin
from .models import AuditEntry, ComplianceCheck, DataAccessLog


@admin.register(AuditEntry)
class AuditEntryAdmin(admin.ModelAdmin):
    list_display = ['action', 'user', 'content_type', 'object_id', 'ip_address', 'timestamp']
    list_filter = ['action', 'timestamp']
    search_fields = ['action', 'user__username', 'ip_address']
    readonly_fields = ['timestamp']


@admin.register(ComplianceCheck)
class ComplianceCheckAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_passing', 'last_checked', 'created_at']
    list_filter = ['is_passing']
    search_fields = ['name', 'description', 'check_function']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(DataAccessLog)
class DataAccessLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'data_type', 'record_id', 'accessed_at']
    list_filter = ['data_type', 'accessed_at']
    search_fields = ['user__username', 'data_type', 'access_reason']
    readonly_fields = ['accessed_at']
