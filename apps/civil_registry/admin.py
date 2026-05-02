from django.contrib import admin
from .models import BirthCertificate, DeathCertificate, MarriageCertificate


@admin.register(BirthCertificate)
class BirthCertificateAdmin(admin.ModelAdmin):
    list_display = ['reference', 'user', 'child_name', 'date_of_birth', 'place_of_birth', 'gender', 'status', 'created_at']
    list_filter = ['status', 'gender', 'county_of_birth', 'created_at']
    search_fields = ['reference', 'child_name', 'father_name', 'mother_name', 'user__username']
    readonly_fields = ['reference']


@admin.register(DeathCertificate)
class DeathCertificateAdmin(admin.ModelAdmin):
    list_display = ['reference', 'user', 'deceased_name', 'date_of_death', 'place_of_death', 'status', 'created_at']
    list_filter = ['status', 'gender', 'created_at']
    search_fields = ['reference', 'deceased_name', 'informant_name', 'user__username']
    readonly_fields = ['reference']


@admin.register(MarriageCertificate)
class MarriageCertificateAdmin(admin.ModelAdmin):
    list_display = ['reference', 'user', 'spouse1_name', 'spouse2_name', 'marriage_date', 'marriage_type', 'status', 'created_at']
    list_filter = ['status', 'marriage_type', 'created_at']
    search_fields = ['reference', 'spouse1_name', 'spouse2_name', 'officiant_name', 'user__username']
    readonly_fields = ['reference']
