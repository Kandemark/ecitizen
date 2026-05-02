from django.contrib import admin
from .models import TenderNotice, Bid, Contract


class BidInline(admin.TabularInline):
    model = Bid
    extra = 0
    readonly_fields = ['reference']
    fields = ['reference', 'company_name', 'bid_amount', 'status', 'created_at']


@admin.register(TenderNotice)
class TenderNoticeAdmin(admin.ModelAdmin):
    list_display = ['reference', 'title', 'ministry', 'closing_date', 'estimated_value', 'is_published', 'status']
    list_filter = ['status', 'is_published', 'ministry', 'procurement_method', 'closing_date']
    search_fields = ['reference', 'title', 'tender_number', 'description']
    readonly_fields = ['reference']
    inlines = [BidInline]


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ['reference', 'user', 'tender', 'company_name', 'bid_amount', 'technical_score', 'financial_score', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['reference', 'company_name', 'registration_number', 'user__username']
    readonly_fields = ['reference']


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ['reference', 'tender', 'awarded_to', 'contract_value', 'start_date', 'end_date', 'status', 'created_at']
    list_filter = ['status', 'contract_type', 'created_at']
    search_fields = ['reference', 'awarded_to', 'contract_number']
    readonly_fields = ['reference']
