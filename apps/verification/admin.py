from django.contrib import admin
from .models import VerificationRequest, VerificationResult


@admin.register(VerificationRequest)
class VerificationRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'id_number', 'id_type', 'status', 'verified_at']
    list_filter = ['status', 'id_type']
    search_fields = ['user__username', 'id_number']


@admin.register(VerificationResult)
class VerificationResultAdmin(admin.ModelAdmin):
    list_display = ['request', 'is_match', 'confidence_score']
    list_filter = ['is_match']
