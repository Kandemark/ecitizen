from django.contrib import admin
from .models import Conversation, Message, SupportTicket


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ['created_at']


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['subject', 'created_at']
    search_fields = ['subject']
    filter_horizontal = ['participants']
    inlines = [MessageInline]
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'sender', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['body', 'sender__username', 'conversation__subject']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ['reference', 'subject', 'user', 'priority', 'status', 'assigned_to', 'created_at']
    list_filter = ['priority', 'status', 'created_at']
    search_fields = ['reference', 'subject', 'description', 'user__username']
    readonly_fields = ['reference', 'created_at', 'updated_at']
