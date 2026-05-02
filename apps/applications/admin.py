from django.contrib import admin
from .models import Application, FormField, ApplicationDocument, StatusHistory


class StatusHistoryInline(admin.TabularInline):
    model = StatusHistory
    extra = 0
    readonly_fields = ['status', 'comment', 'changed_by', 'created_at']


class ApplicationDocumentInline(admin.TabularInline):
    model = ApplicationDocument
    extra = 0


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['reference', 'user', 'service', 'status', 'submitted_at']
    list_filter = ['status', 'service__category', 'county', 'created_at']
    search_fields = ['reference', 'user__username', 'service__name']
    inlines = [StatusHistoryInline, ApplicationDocumentInline]
    readonly_fields = ['reference']


@admin.register(FormField)
class FormFieldAdmin(admin.ModelAdmin):
    list_display = ['label', 'field_type', 'service', 'is_required', 'order']
    list_filter = ['field_type', 'service']
    search_fields = ['label']


@admin.register(ApplicationDocument)
class ApplicationDocumentAdmin(admin.ModelAdmin):
    list_display = ['original_filename', 'application', 'is_verified']
    list_filter = ['is_verified']
    search_fields = ['original_filename', 'application__reference']


@admin.register(StatusHistory)
class StatusHistoryAdmin(admin.ModelAdmin):
    list_display = ['application', 'status', 'changed_by', 'created_at']
    list_filter = ['status']
    search_fields = ['application__reference']
