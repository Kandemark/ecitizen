from django.db import models
from django.contrib.auth.models import User
from core.models import TimestampMixin
from core.utils import generate_tracking_id


class EmergencyContact(TimestampMixin):
    SERVICE_TYPE_CHOICES = [
        ('police', 'Police'),
        ('fire', 'Fire'),
        ('ambulance', 'Ambulance'),
        ('other', 'Other'),
    ]
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPE_CHOICES, default='police')
    county = models.ForeignKey(
        'counties.County', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='emergency_contacts'
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['service_type', 'name']
        indexes = [
            models.Index(fields=['service_type', 'is_active']),
        ]

    def __str__(self):
        return f'{self.name} — {self.get_service_type_display()} ({self.phone})'


class EmergencyReport(TimestampMixin):
    EMERGENCY_TYPE_CHOICES = [
        ('police', 'Police'),
        ('fire', 'Fire'),
        ('ambulance', 'Ambulance'),
        ('disaster', 'Disaster'),
        ('accident', 'Accident'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('reported', 'Reported'),
        ('dispatched', 'Dispatched'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emergency_reports')
    reference = models.CharField(max_length=30, unique=True, db_index=True)
    emergency_type = models.CharField(
        max_length=20, choices=EMERGENCY_TYPE_CHOICES, default='other'
    )
    location = models.CharField(max_length=500)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reported')
    reported_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-reported_at']
        indexes = [
            models.Index(fields=['reference']),
            models.Index(fields=['status']),
            models.Index(fields=['emergency_type']),
        ]

    def __str__(self):
        return f'{self.reference} — {self.get_emergency_type_display()} ({self.status})'

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = generate_tracking_id(prefix='EMG')
        super().save(*args, **kwargs)
