from django.contrib import admin
from .models import Notification, NotificationPreference


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'channel', 'is_read', 'created_at']
    list_filter = ['channel', 'is_read', 'created_at']
    search_fields = ['title', 'message', 'user__username']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_enabled', 'sms_enabled', 'push_enabled', 'quiet_hours_start', 'quiet_hours_end']
    list_filter = ['email_enabled', 'sms_enabled', 'push_enabled']
    search_fields = ['user__username']
    readonly_fields = ['created_at', 'updated_at']
