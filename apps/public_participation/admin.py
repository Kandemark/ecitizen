from django.contrib import admin
from .models import Consultation, PublicComment, Petition


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ['title', 'ministry', 'start_date', 'end_date', 'is_active', 'status']
    list_filter = ['is_active', 'status', 'ministry']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(PublicComment)
class PublicCommentAdmin(admin.ModelAdmin):
    list_display = ['consultation', 'user', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['comment', 'user__username', 'consultation__title']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Petition)
class PetitionAdmin(admin.ModelAdmin):
    list_display = ['reference', 'title', 'user', 'target_ministry', 'signature_count', 'threshold', 'status']
    list_filter = ['status', 'target_ministry']
    search_fields = ['reference', 'title', 'description', 'user__username']
    readonly_fields = ['reference', 'created_at', 'updated_at']
