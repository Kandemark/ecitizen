from django.contrib import admin
from .models import Bill, Hansard, CommitteeReport, ParliamentarySitting


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('number', 'title', 'house', 'status', 'sponsor', 'date_introduced', 'last_updated')
    list_filter = ('status', 'house')
    search_fields = ('title', 'number', 'sponsor', 'summary')


@admin.register(Hansard)
class HansardAdmin(admin.ModelAdmin):
    list_display = ('title', 'house', 'date', 'sitting_number')
    list_filter = ('house', 'date')
    search_fields = ('title', 'content')


@admin.register(CommitteeReport)
class CommitteeReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'committee_name', 'date_published')
    search_fields = ('title', 'committee_name', 'summary')


@admin.register(ParliamentarySitting)
class ParliamentarySittingAdmin(admin.ModelAdmin):
    list_display = ('date', 'house', 'session')
    list_filter = ('house', 'date')
    search_fields = ('session', 'agenda')
