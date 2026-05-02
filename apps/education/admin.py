from django.contrib import admin
from .models import LoanApplication, SchoolRegistration, ExamResult


@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = ['reference', 'user', 'loan_type', 'institution', 'amount', 'amount_approved', 'status', 'created_at']
    list_filter = ['loan_type', 'status', 'created_at']
    search_fields = ['reference', 'institution', 'campus', 'course_of_study', 'user__username']
    readonly_fields = ['reference']


@admin.register(SchoolRegistration)
class SchoolRegistrationAdmin(admin.ModelAdmin):
    list_display = ['reference', 'user', 'school_name', 'registration_type', 'county', 'status', 'created_at']
    list_filter = ['registration_type', 'status', 'county', 'created_at']
    search_fields = ['reference', 'school_name', 'registration_number', 'proprietor_name', 'user__username']
    readonly_fields = ['reference']


@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ['reference', 'user', 'exam_type', 'index_number', 'mean_grade', 'status', 'created_at']
    list_filter = ['exam_type', 'status', 'examination_year', 'created_at']
    search_fields = ['reference', 'index_number', 'school_name', 'certificate_number', 'user__username']
    readonly_fields = ['reference']
