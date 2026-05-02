from django.contrib import admin
from .models import PollingStation, VoterRecord, Candidate


@admin.register(PollingStation)
class PollingStationAdmin(admin.ModelAdmin):
    list_display = ['name', 'county', 'constituency_name', 'ward_name', 'registered_voters', 'is_active']
    list_filter = ['is_active', 'county', 'constituency_name']
    search_fields = ['name', 'constituency_name', 'ward_name', 'station_code']


@admin.register(VoterRecord)
class VoterRecordAdmin(admin.ModelAdmin):
    list_display = ['reference', 'user', 'voter_number', 'id_number', 'polling_station', 'is_verified', 'status', 'created_at']
    list_filter = ['is_verified', 'status', 'registration_date', 'created_at']
    search_fields = ['reference', 'voter_number', 'id_number', 'user__username']
    readonly_fields = ['reference']


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'political_party', 'election_type', 'county', 'is_cleared']
    list_filter = ['election_type', 'is_cleared', 'political_party', 'county']
    search_fields = ['name', 'position', 'political_party', 'constituency_name', 'ward_name']
