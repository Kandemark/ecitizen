from django.db import models
from django.contrib.auth.models import User
from core.models import TimestampMixin
from core.constants import APPLICATION_STATUSES


TAX_TYPES = [
    ('income_tax', 'Income Tax (PAYE)'),
    ('corporate_tax', 'Corporate Tax'),
    ('vat', 'Value Added Tax'),
    ('excise_duty', 'Excise Duty'),
    ('customs_duty', 'Customs Duty'),
    ('capital_gains', 'Capital Gains Tax'),
    ('withholding', 'Withholding Tax'),
    ('turnover', 'Turnover Tax'),
    ('rental_income', 'Rental Income Tax'),
    ('other', 'Other'),
]


class TaxReturn(TimestampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tax_returns')
    reference = models.CharField(max_length=30, unique=True, db_index=True)
    tax_type = models.CharField(max_length=30, choices=TAX_TYPES)
    tax_period = models.CharField(max_length=50)
    period_start = models.DateField(null=True, blank=True)
    period_end = models.DateField(null=True, blank=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    amount_paid = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    filing_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    kra_pin = models.CharField('KRA PIN', max_length=20, blank=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUSES, default='draft')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Tax Return {self.reference} — {self.tax_type} ({self.tax_period})'


class TaxAssessment(TimestampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tax_assessments')
    reference = models.CharField(max_length=30, unique=True, db_index=True)
    assessment_year = models.PositiveSmallIntegerField()
    tax_type = models.CharField(max_length=30, choices=TAX_TYPES)
    total_income = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    taxable_income = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    total_assessed = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    tax_paid = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    balance_due = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    assessment_date = models.DateField(null=True, blank=True)
    kra_pin = models.CharField('KRA PIN', max_length=20, blank=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUSES, default='draft')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Tax Assessment {self.reference} — {self.assessment_year}'


class ComplianceCertificate(TimestampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='compliance_certificates')
    reference = models.CharField(max_length=30, unique=True, db_index=True)
    certificate_type = models.CharField(max_length=100)
    kra_pin = models.CharField('KRA PIN', max_length=20, blank=True)
    issued_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    is_valid = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUSES, default='draft')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Compliance Certificate {self.reference} — {self.certificate_type}'
