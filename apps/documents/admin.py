from django.contrib import admin
from .models import Document, DocumentShare


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'file_size', 'mime_type', 'is_verified', 'created_at']
    list_filter = ['is_verified']
    search_fields = ['name', 'user__username']


@admin.register(DocumentShare)
class DocumentShareAdmin(admin.ModelAdmin):
    list_display = ['document', 'shared_with', 'can_view', 'can_download', 'expires_at']
