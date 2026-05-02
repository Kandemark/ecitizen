from django.contrib import admin
from .models import HealthRecord, NHIFRegistration, MedicalCertificate


@admin.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):
    list_display = ['reference', 'user', 'facility_name', 'record_type', 'visit_date', 'status', 'created_at']
    list_filter = ['record_type', 'status', 'created_at']
    search_fields = ['reference', 'facility_name', 'attending_practitioner', 'user__username']
    readonly_fields = ['reference']


@admin.register(NHIFRegistration)
class NHIFRegistrationAdmin(admin.ModelAdmin):
    list_display = ['reference', 'user', 'nhif_number', 'employer_name', 'status', 'created_at']
    list_filter = ['status', 'registration_date', 'created_at']
    search_fields = ['reference', 'nhif_number', 'employer_name', 'user__username']
    readonly_fields = ['reference']


@admin.register(MedicalCertificate)
class MedicalCertificateAdmin(admin.ModelAdmin):
    list_display = ['reference', 'user', 'certificate_type', 'issuing_facility', 'issued_date', 'status', 'created_at']
    list_filter = ['certificate_type', 'status', 'created_at']
    search_fields = ['reference', 'issuing_facility', 'issuing_practitioner', 'user__username']
    readonly_fields = ['reference']
