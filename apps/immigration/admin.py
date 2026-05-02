from django.contrib import admin
from .models import PassportApplication, VisaApplication, WorkPermit


@admin.register(PassportApplication)
class PassportApplicationAdmin(admin.ModelAdmin):
    list_display = ['reference', 'user', 'passport_type', 'status', 'created_at']
    list_filter = ['status', 'passport_type']
    search_fields = ['reference', 'user__username']
    readonly_fields = ['reference']


@admin.register(VisaApplication)
class VisaApplicationAdmin(admin.ModelAdmin):
    list_display = ['reference', 'user', 'visa_type', 'status', 'created_at']
    list_filter = ['status', 'visa_type']
    search_fields = ['reference', 'user__username']
    readonly_fields = ['reference']


@admin.register(WorkPermit)
class WorkPermitAdmin(admin.ModelAdmin):
    list_display = ['reference', 'user', 'permit_class', 'employer', 'status', 'created_at']
    list_filter = ['status', 'permit_class']
    search_fields = ['reference', 'user__username']
    readonly_fields = ['reference']
