from django.contrib import admin
from .models import APIKey, Webhook


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'is_active', 'expires_at', 'last_used_at', 'rate_limit']
    list_filter = ['is_active']
    search_fields = ['name', 'user__username']


@admin.register(Webhook)
class WebhookAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'event', 'url', 'is_active']
    list_filter = ['is_active', 'event']
    search_fields = ['name', 'user__username']
