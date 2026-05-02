from django.db import models
from core.models import TimestampMixin, UUIDMixin


class ServiceCategory(TimestampMixin):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='Building')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    ministry = models.ForeignKey(
        'ministries.Ministry', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='service_categories'
    )

    class Meta:
        verbose_name_plural = 'Service Categories'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class EligibilityRule(TimestampMixin):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    min_age = models.PositiveSmallIntegerField(default=0)
    max_age = models.PositiveSmallIntegerField(default=100)
    required_id_types = models.JSONField(default=list, blank=True)
    kenyan_citizen_only = models.BooleanField(default=True)
    conditions = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.name


class RequiredDocument(TimestampMixin):
    DOCUMENT_TYPES = [
        ('national_id', 'National ID'),
        ('passport', 'Passport'),
        ('birth_certificate', 'Birth Certificate'),
        ('kra_pin', 'KRA PIN Certificate'),
        ('passport_photo', 'Passport Photo'),
        ('proof_residence', 'Proof of Residence'),
        ('marriage_cert', 'Marriage Certificate'),
        ('medical_report', 'Medical Report'),
        ('police_clearance', 'Police Clearance'),
        ('academic_cert', 'Academic Certificate'),
        ('business_reg', 'Business Registration'),
        ('tax_compliance', 'Tax Compliance Certificate'),
        ('other', 'Other'),
    ]
    name = models.CharField(max_length=200)
    document_type = models.CharField(max_length=30, choices=DOCUMENT_TYPES, default='other')
    description = models.TextField(blank=True)
    is_mandatory = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Service(TimestampMixin):
    category = models.ForeignKey(
        ServiceCategory, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='services'
    )
    ministry = models.ForeignKey(
        'ministries.Ministry', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='services'
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    short_description = models.CharField(max_length=500, blank=True)
    icon = models.CharField(max_length=50, default='IdentificationCard')
    processing_time = models.CharField(max_length=100, blank=True)
    fee_kes = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_popular = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_online = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    eligibility_rules = models.ManyToManyField(EligibilityRule, blank=True, related_name='services')
    required_documents = models.ManyToManyField(RequiredDocument, blank=True, related_name='services')
    counties = models.ManyToManyField('counties.County', blank=True, related_name='services')

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name
