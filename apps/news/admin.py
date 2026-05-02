from django.contrib import admin
from .models import NewsSource, NewsArticle


@admin.register(NewsSource)
class NewsSourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'feed_url', 'is_active', 'last_fetched']
    list_filter = ['is_active']
    search_fields = ['name', 'feed_url']


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'source', 'published_at', 'is_kenya_related']
    list_filter = ['is_kenya_related', 'source']
    search_fields = ['title', 'summary']
    date_hierarchy = 'published_at'
