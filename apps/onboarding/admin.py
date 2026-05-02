from django.contrib import admin
from .models import OnboardingStep, OnboardingProgress


@admin.register(OnboardingStep)
class OnboardingStepAdmin(admin.ModelAdmin):
    list_display = ['order', 'name', 'title', 'is_required']
    ordering = ['order']


@admin.register(OnboardingProgress)
class OnboardingProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'current_step', 'is_complete', 'created_at']
    list_filter = ['is_complete', 'current_step']
    search_fields = ['user__username']
