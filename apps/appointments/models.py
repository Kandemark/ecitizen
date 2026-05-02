from django.db import models
from django.contrib.auth.models import User
from core.models import TimestampMixin, UUIDMixin


class OfficeLocation(TimestampMixin):
    name = models.CharField(max_length=255)
    county = models.ForeignKey('counties.County', on_delete=models.CASCADE, related_name='offices')
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    opening_time = models.TimeField(default='08:00')
    closing_time = models.TimeField(default='17:00')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} — {self.county.name}'


class TimeSlot(TimestampMixin):
    office = models.ForeignKey(OfficeLocation, on_delete=models.CASCADE, related_name='time_slots')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    max_capacity = models.PositiveIntegerField(default=1)
    current_bookings = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ['date', 'start_time']

    def __str__(self):
        return f'{self.office.name}: {self.date} {self.start_time}-{self.end_time}'


class Appointment(TimestampMixin):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, related_name='appointments')
    service = models.ForeignKey('services.Service', on_delete=models.SET_NULL, null=True, blank=True)
    reference = models.CharField(max_length=30, unique=True, db_index=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['time_slot__date', 'time_slot__start_time']

    def __str__(self):
        return f'{self.reference} — {self.user.username} ({self.status})'
