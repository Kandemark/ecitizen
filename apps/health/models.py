from django.db import models
from django.contrib.auth.models import User
from core.models import TimestampMixin
from core.constants import APPLICATION_STATUSES


HEALTH_RECORD_TYPES = [
    ('outpatient', 'Outpatient'),
    ('inpatient', 'Inpatient'),
    ('maternal', 'Maternal'),
    ('child_health', 'Child Health'),
    ('immunization', 'Immunization'),
    ('chronic_disease', 'Chronic Disease'),
    ('laboratory', 'Laboratory'),
    ('pharmacy', 'Pharmacy'),
    ('referral', 'Referral'),
    ('other', 'Other'),
]

CERTIFICATE_TYPES = [
    ('medical_examination', 'Medical Examination'),
    ('fitness', 'Fitness Certificate'),
    ('disability', 'Disability Certificate'),
    ('death', 'Death Certificate (Medical)'),
    ('vaccination', 'Vaccination Certificate'),
    ('travel', 'Travel Health Certificate'),
    ('food_handler', 'Food Handler Certificate'),
    ('occupational', 'Occupational Health'),
]


class HealthRecord(TimestampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='health_records')
    reference = models.CharField(max_length=30, unique=True, db_index=True)
    facility_name = models.CharField(max_length=255)
    record_type = models.CharField(max_length=30, choices=HEALTH_RECORD_TYPES)
    visit_date = models.DateField(null=True, blank=True)
    diagnosis = models.TextField(blank=True)
    prescription = models.TextField(blank=True)
    attending_practitioner = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUSES, default='draft')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Health Record {self.reference} — {self.facility_name}'


class NHIFRegistration(TimestampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='nhif_registrations')
    reference = models.CharField(max_length=30, unique=True, db_index=True)
    nhif_number = models.CharField(max_length=20, blank=True)
    employer_name = models.CharField(max_length=255, blank=True)
    monthly_contribution = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    dependants = models.PositiveSmallIntegerField(default=0)
    registration_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUSES, default='draft')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'NHIF Registration'

    def __str__(self):
        return f'NHIF {self.nhif_number or self.reference}'


class MedicalCertificate(TimestampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medical_certificates')
    reference = models.CharField(max_length=30, unique=True, db_index=True)
    certificate_type = models.CharField(max_length=30, choices=CERTIFICATE_TYPES)
    issuing_facility = models.CharField(max_length=255)
    issuing_practitioner = models.CharField(max_length=255, blank=True)
    issued_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    findings = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUSES, default='draft')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Medical Certificate {self.reference} — {self.certificate_type}'
