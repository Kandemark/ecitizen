from django.contrib import admin
from .models import CourtCase, Filing, HearingSchedule, Fine


class FilingInline(admin.TabularInline):
    model = Filing
    extra = 0
    readonly_fields = ['reference']
    fields = ['reference', 'filing_type', 'status', 'created_at']


class HearingScheduleInline(admin.TabularInline):
    model = HearingSchedule
    extra = 0
    fields = ['hearing_date', 'hearing_time', 'courtroom', 'outcome']


@admin.register(CourtCase)
class CourtCaseAdmin(admin.ModelAdmin):
    list_display = ['reference', 'user', 'case_number', 'court_name', 'case_type', 'status', 'created_at']
    list_filter = ['case_type', 'status', 'court_name', 'created_at']
    search_fields = ['reference', 'case_number', 'title', 'user__username']
    readonly_fields = ['reference']
    inlines = [FilingInline, HearingScheduleInline]


@admin.register(Filing)
class FilingAdmin(admin.ModelAdmin):
    list_display = ['reference', 'user', 'case', 'filing_type', 'status', 'created_at']
    list_filter = ['filing_type', 'status', 'created_at']
    search_fields = ['reference', 'case__case_number', 'user__username']
    readonly_fields = ['reference']


@admin.register(HearingSchedule)
class HearingScheduleAdmin(admin.ModelAdmin):
    list_display = ['case', 'hearing_date', 'hearing_time', 'courtroom', 'judge_name']
    list_filter = ['hearing_date', 'courtroom']
    search_fields = ['case__case_number', 'courtroom', 'judge_name']


@admin.register(Fine)
class FineAdmin(admin.ModelAdmin):
    list_display = ['reference', 'user', 'offense', 'amount', 'amount_paid', 'due_date', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['reference', 'offense', 'user__username']
    readonly_fields = ['reference']
