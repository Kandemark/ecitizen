from django.contrib import admin
from .models import Feedback, Complaint, SatisfactionSurvey


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'service', 'rating', 'is_public', 'created_at']
    list_filter = ['rating', 'is_public', 'created_at']
    search_fields = ['title', 'comment', 'user__username', 'service__name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['reference', 'subject', 'user', 'category', 'status', 'created_at']
    list_filter = ['category', 'status', 'created_at']
    search_fields = ['reference', 'subject', 'description', 'user__username']
    readonly_fields = ['reference', 'created_at', 'updated_at']


@admin.register(SatisfactionSurvey)
class SatisfactionSurveyAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
