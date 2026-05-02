from django.contrib import admin
from .models import EmergencyContact, EmergencyReport


@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'service_type', 'county', 'is_active', 'created_at']
    list_filter = ['service_type', 'is_active', 'county']
    search_fields = ['name', 'phone']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(EmergencyReport)
class EmergencyReportAdmin(admin.ModelAdmin):
    list_display = ['reference', 'user', 'emergency_type', 'location', 'status', 'reported_at']
    list_filter = ['emergency_type', 'status', 'reported_at']
    search_fields = ['reference', 'location', 'description', 'user__username']
    readonly_fields = ['reference', 'reported_at', 'created_at', 'updated_at']
