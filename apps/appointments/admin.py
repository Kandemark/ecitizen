from django.contrib import admin
from .models import OfficeLocation, TimeSlot, Appointment


@admin.register(OfficeLocation)
class OfficeLocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'county', 'is_active']
    list_filter = ['county', 'is_active']
    search_fields = ['name']


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['office', 'date', 'start_time', 'end_time', 'max_capacity', 'is_available']
    list_filter = ['office', 'date', 'is_available']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['reference', 'user', 'time_slot', 'service', 'status']
    list_filter = ['status']
    search_fields = ['reference', 'user__username']
