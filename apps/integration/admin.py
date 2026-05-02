from django.contrib import admin
from .models import ExternalSystem, DataExchange, SyncLog


class SyncLogInline(admin.TabularInline):
    model = SyncLog
    extra = 0
    readonly_fields = ['started_at', 'finished_at']


@admin.register(ExternalSystem)
class ExternalSystemAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'auth_type', 'is_active', 'created_at']
    list_filter = ['auth_type', 'is_active']
    search_fields = ['name', 'code']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(DataExchange)
class DataExchangeAdmin(admin.ModelAdmin):
    list_display = ['system', 'direction', 'data_type', 'status', 'completed_at', 'created_at']
    list_filter = ['direction', 'status', 'system']
    search_fields = ['data_type', 'system__name']
    inlines = [SyncLogInline]
    readonly_fields = ['created_at', 'updated_at']


@admin.register(SyncLog)
class SyncLogAdmin(admin.ModelAdmin):
    list_display = ['exchange', 'status', 'records_processed', 'started_at', 'finished_at']
    list_filter = ['status']
    search_fields = ['exchange__data_type', 'exchange__system__name']
    readonly_fields = ['started_at', 'finished_at', 'created_at', 'updated_at']
