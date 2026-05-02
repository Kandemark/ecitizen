from django.contrib import admin
from .models import TitleDeed, LandSearch, Transfer


class TransferInline(admin.TabularInline):
    model = Transfer
    extra = 0
    readonly_fields = ['reference']
    fields = ['reference', 'from_owner', 'to_owner', 'status', 'created_at']


@admin.register(TitleDeed)
class TitleDeedAdmin(admin.ModelAdmin):
    list_display = ['reference', 'user', 'title_number', 'property_location', 'county', 'status', 'created_at']
    list_filter = ['status', 'county', 'tenure_type', 'created_at']
    search_fields = ['reference', 'title_number', 'property_location', 'user__username']
    readonly_fields = ['reference']
    inlines = [TransferInline]


@admin.register(LandSearch)
class LandSearchAdmin(admin.ModelAdmin):
    list_display = ['reference', 'user', 'title_number', 'search_purpose', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['reference', 'title_number', 'user__username']
    readonly_fields = ['reference']


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ['reference', 'user', 'title_deed', 'from_owner', 'to_owner', 'status', 'created_at']
    list_filter = ['status', 'transfer_type', 'created_at']
    search_fields = ['reference', 'from_owner', 'to_owner', 'user__username']
    readonly_fields = ['reference']
