from django.contrib import admin
from .models import SearchIndex, SearchQuery


@admin.register(SearchIndex)
class SearchIndexAdmin(admin.ModelAdmin):
    list_display = ['title', 'content_type', 'object_id', 'last_indexed']
    list_filter = ['content_type', 'last_indexed']
    search_fields = ['title', 'description']
    readonly_fields = ['last_indexed', 'created_at', 'updated_at']


@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ['query', 'user', 'results_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['query', 'user__username']
    readonly_fields = ['created_at']
