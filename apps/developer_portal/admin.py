from django.contrib import admin
from .models import DeveloperRegistration, SandboxEnvironment


@admin.register(DeveloperRegistration)
class DeveloperRegistrationAdmin(admin.ModelAdmin):
    list_display = ['user', 'organization', 'website', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'organization', 'use_case']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(SandboxEnvironment)
class SandboxEnvironmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'base_url', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'user__username', 'base_url']
    readonly_fields = ['created_at', 'updated_at']
