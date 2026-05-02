from django.contrib import admin
from .models import ReportTemplate, GeneratedReport


@admin.register(ReportTemplate)
class ReportTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'report_type', 'created_at']
    list_filter = ['report_type']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(GeneratedReport)
class GeneratedReportAdmin(admin.ModelAdmin):
    list_display = ['template', 'user', 'format', 'status', 'created_at']
    list_filter = ['format', 'status', 'created_at']
    search_fields = ['template__name', 'user__username']
    readonly_fields = ['created_at', 'updated_at', 'file']
