from django.contrib import admin
from .models import TaxReturn, TaxAssessment, ComplianceCertificate


@admin.register(TaxReturn)
class TaxReturnAdmin(admin.ModelAdmin):
    list_display = ['reference', 'user', 'tax_type', 'tax_period', 'amount', 'amount_paid', 'status', 'created_at']
    list_filter = ['tax_type', 'status', 'filing_date', 'created_at']
    search_fields = ['reference', 'kra_pin', 'user__username']
    readonly_fields = ['reference']


@admin.register(TaxAssessment)
class TaxAssessmentAdmin(admin.ModelAdmin):
    list_display = ['reference', 'user', 'tax_type', 'assessment_year', 'total_assessed', 'balance_due', 'status', 'created_at']
    list_filter = ['tax_type', 'status', 'assessment_year', 'created_at']
    search_fields = ['reference', 'kra_pin', 'user__username']
    readonly_fields = ['reference']


@admin.register(ComplianceCertificate)
class ComplianceCertificateAdmin(admin.ModelAdmin):
    list_display = ['reference', 'user', 'certificate_type', 'is_valid', 'expiry_date', 'status', 'created_at']
    list_filter = ['certificate_type', 'is_valid', 'status', 'created_at']
    search_fields = ['reference', 'kra_pin', 'user__username']
    readonly_fields = ['reference']
