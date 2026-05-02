from django.db import models
from django.contrib.auth.models import User
from core.models import TimestampMixin
from core.constants import APPLICATION_STATUSES


BUSINESS_LICENSE_TYPES = [
    ('single_business', 'Single Business Permit'),
    ('general_trade', 'General Trade License'),
    ('manufacturing', 'Manufacturing License'),
    ('hospitality', 'Hospitality & Entertainment'),
    ('health_facility', 'Health Facility License'),
    ('transport', 'Transport Business License'),
    ('professional', 'Professional Services License'),
    ('financial', 'Financial Services License'),
    ('import_export', 'Import/Export License'),
    ('other', 'Other'),
]

CERTIFICATION_TYPES = [
    ('medical', 'Medical'),
    ('legal', 'Legal'),
    ('engineering', 'Engineering'),
    ('accounting', 'Accounting'),
    ('architecture', 'Architecture'),
    ('teaching', 'Teaching'),
    ('real_estate', 'Real Estate'),
    ('surveying', 'Surveying'),
    ('other', 'Other'),
]


class BusinessLicense(TimestampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='business_licenses')
    reference = models.CharField(max_length=30, unique=True, db_index=True)
    business_name = models.CharField(max_length=255)
    license_type = models.CharField(max_length=30, choices=BUSINESS_LICENSE_TYPES)
    registration_number = models.CharField(max_length=100, blank=True)
    county = models.ForeignKey(
        'counties.County', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='business_licenses'
    )
    physical_address = models.TextField(blank=True)
    postal_address = models.CharField(max_length=100, blank=True)
    business_email = models.EmailField(blank=True)
    business_phone = models.CharField(max_length=15, blank=True)
    number_of_employees = models.PositiveIntegerField(default=0)
    issued_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUSES, default='draft')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Business License {self.reference} — {self.business_name}'


class ProfessionalCertification(TimestampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='professional_certifications')
    reference = models.CharField(max_length=30, unique=True, db_index=True)
    certification_name = models.CharField(max_length=255)
    certification_type = models.CharField(max_length=30, choices=CERTIFICATION_TYPES, default='other')
    issuing_body = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=100, blank=True)
    issued_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUSES, default='draft')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Certification {self.reference} — {self.certification_name}'
