from django.contrib import admin
from .models import BusinessLicense, ProfessionalCertification


@admin.register(BusinessLicense)
class BusinessLicenseAdmin(admin.ModelAdmin):
    list_display = ['reference', 'user', 'business_name', 'license_type', 'county', 'status', 'created_at']
    list_filter = ['license_type', 'status', 'county', 'created_at']
    search_fields = ['reference', 'business_name', 'registration_number', 'user__username']
    readonly_fields = ['reference']


@admin.register(ProfessionalCertification)
class ProfessionalCertificationAdmin(admin.ModelAdmin):
    list_display = ['reference', 'user', 'certification_name', 'issuing_body', 'status', 'created_at']
    list_filter = ['certification_type', 'status', 'created_at']
    search_fields = ['reference', 'certification_name', 'issuing_body', 'registration_number', 'user__username']
    readonly_fields = ['reference']
