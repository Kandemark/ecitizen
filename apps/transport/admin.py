from django.contrib import admin
from .models import DrivingLicense, VehicleRegistration, PSVLicense, VehicleInspection


@admin.register(DrivingLicense)
class DrivingLicenseAdmin(admin.ModelAdmin):
    list_display = ['reference', 'user', 'license_class', 'status', 'created_at']
    list_filter = ['license_class', 'status', 'created_at']
    search_fields = ['reference', 'user__username']
    readonly_fields = ['reference']


@admin.register(VehicleRegistration)
class VehicleRegistrationAdmin(admin.ModelAdmin):
    list_display = ['reference', 'user', 'plate_number', 'vehicle_make', 'status', 'created_at']
    list_filter = ['status', 'vehicle_make', 'created_at']
    search_fields = ['reference', 'plate_number', 'user__username', 'vin']
    readonly_fields = ['reference']


@admin.register(PSVLicense)
class PSVLicenseAdmin(admin.ModelAdmin):
    list_display = ['reference', 'user', 'route', 'vehicle', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['reference', 'route', 'operator_name', 'sacco_name', 'user__username']
    readonly_fields = ['reference']


@admin.register(VehicleInspection)
class VehicleInspectionAdmin(admin.ModelAdmin):
    list_display = ['reference', 'user', 'vehicle', 'inspection_date', 'result', 'status', 'created_at']
    list_filter = ['result', 'status', 'inspection_date', 'created_at']
    search_fields = ['reference', 'inspection_center', 'user__username']
    readonly_fields = ['reference']
