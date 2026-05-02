from django.contrib import admin
from .models import Chapter, Article, Schedule


class ArticleInline(admin.TabularInline):
    model = Article
    extra = 0
    fields = ('number', 'title', 'order')


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('number', 'title', 'article_count', 'order')
    search_fields = ('title', 'subtitle')
    inlines = [ArticleInline]


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('number', 'title', 'chapter', 'order')
    list_filter = ('chapter',)
    search_fields = ('title', 'content', 'number')


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('number', 'title', 'order')
    search_fields = ('title', 'content')
