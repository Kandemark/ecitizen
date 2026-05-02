from rest_framework import serializers
from .models import OfficeLocation, TimeSlot, Appointment


class OfficeLocationSerializer(serializers.ModelSerializer):
    county_name = serializers.CharField(source='county.name', read_only=True)

    class Meta:
        model = OfficeLocation
        fields = ['id', 'name', 'county', 'county_name', 'address', 'phone', 'opening_time', 'closing_time']


class TimeSlotSerializer(serializers.ModelSerializer):
    office_name = serializers.CharField(source='office.name', read_only=True)

    class Meta:
        model = TimeSlot
        fields = ['id', 'office', 'office_name', 'date', 'start_time', 'end_time', 'max_capacity', 'is_available']


class AppointmentSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source='service.name', read_only=True)
    time_slot_detail = TimeSlotSerializer(source='time_slot', read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'time_slot', 'time_slot_detail', 'service', 'service_name', 'reference', 'status', 'notes', 'created_at']
        read_only_fields = ['reference', 'status']

    def create(self, validated_data):
        from core.utils import generate_tracking_id
        validated_data['user'] = self.context['request'].user
        validated_data['reference'] = generate_tracking_id('APT')
        appointment = super().create(validated_data)
        slot = appointment.time_slot
        slot.current_bookings += 1
        if slot.current_bookings >= slot.max_capacity:
            slot.is_available = False
        slot.save()
        return appointment
