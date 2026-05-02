from django.contrib import admin
from .models import Dashboard, Widget, Metric


class WidgetInline(admin.TabularInline):
    model = Widget
    extra = 0


@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'is_default', 'created_at']
    list_filter = ['is_default', 'created_at']
    search_fields = ['name', 'user__username']
    inlines = [WidgetInline]
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Widget)
class WidgetAdmin(admin.ModelAdmin):
    list_display = ['title', 'dashboard', 'widget_type', 'position', 'created_at']
    list_filter = ['widget_type']
    search_fields = ['title', 'dashboard__name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = ['name', 'value', 'source', 'updated_at']
    search_fields = ['name', 'source']
    readonly_fields = ['updated_at']
