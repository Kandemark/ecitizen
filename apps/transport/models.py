from django.db import models
from django.contrib.auth.models import User
from core.models import TimestampMixin
from core.constants import APPLICATION_STATUSES


LICENSE_CLASSES = [
    ('A1', 'Motorcycle (A1)'),
    ('A2', 'Motorcycle >250cc (A2)'),
    ('B', 'Light Motor Vehicle (B)'),
    ('C', 'Light Truck (C)'),
    ('D', 'PSV Matatu/Bus (D)'),
    ('E', 'Heavy Truck (E)'),
    ('F', 'Special (F)'),
    ('G', 'Industrial/Agricultural (G)'),
]


class DrivingLicense(TimestampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='driving_licenses')
    reference = models.CharField(max_length=30, unique=True, db_index=True)
    license_class = models.CharField(max_length=3, choices=LICENSE_CLASSES)
    blood_group = models.CharField(max_length=5, blank=True)
    issued_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUSES, default='draft')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Driving License {self.reference} ({self.license_class})'


class VehicleRegistration(TimestampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicle_registrations')
    reference = models.CharField(max_length=30, unique=True, db_index=True)
    plate_number = models.CharField(max_length=20)
    vehicle_make = models.CharField(max_length=100)
    vehicle_model = models.CharField(max_length=100, blank=True)
    year_of_manufacture = models.PositiveSmallIntegerField(null=True, blank=True)
    color = models.CharField(max_length=50, blank=True)
    vin = models.CharField('VIN/Chassis Number', max_length=50, blank=True)
    engine_number = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUSES, default='draft')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Vehicle {self.plate_number} ({self.reference})'


class PSVLicense(TimestampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='psv_licenses')
    reference = models.CharField(max_length=30, unique=True, db_index=True)
    vehicle = models.ForeignKey(
        VehicleRegistration, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='psv_licenses'
    )
    route = models.CharField(max_length=255)
    operator_name = models.CharField(max_length=255, blank=True)
    sacco_name = models.CharField(max_length=255, blank=True)
    capacity = models.PositiveSmallIntegerField(default=0)
    issued_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUSES, default='draft')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'PSV License'

    def __str__(self):
        return f'PSV License {self.reference} — {self.route}'


class VehicleInspection(TimestampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicle_inspections')
    reference = models.CharField(max_length=30, unique=True, db_index=True)
    vehicle = models.ForeignKey(
        VehicleRegistration, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='inspections'
    )
    inspection_date = models.DateField(null=True, blank=True)
    inspection_center = models.CharField(max_length=255, blank=True)
    result = models.CharField(max_length=30, default='pending')
    expiry_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUSES, default='draft')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Inspection {self.reference} — {self.result}'
