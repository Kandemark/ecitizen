from django.db import models
from django.contrib.auth.models import User
from core.models import TimestampMixin
from core.constants import APPLICATION_STATUSES


TENDER_STATUSES = [
    ('draft', 'Draft'),
    ('published', 'Published'),
    ('under_review', 'Under Review'),
    ('awarded', 'Awarded'),
    ('cancelled', 'Cancelled'),
    ('closed', 'Closed'),
]


class TenderNotice(TimestampMixin):
    reference = models.CharField(max_length=30, unique=True, db_index=True)
    title = models.CharField(max_length=500)
    ministry = models.ForeignKey(
        'ministries.Ministry', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='tenders'
    )
    tender_number = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    procurement_method = models.CharField(max_length=100, default='open_tender')
    closing_date = models.DateTimeField()
    bid_bond_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    estimated_value = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    is_published = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=TENDER_STATUSES, default='draft')

    class Meta:
        ordering = ['-closing_date']

    def __str__(self):
        return f'Tender {self.reference} — {self.title[:80]}'


class Bid(TimestampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    reference = models.CharField(max_length=30, unique=True, db_index=True)
    tender = models.ForeignKey(TenderNotice, on_delete=models.CASCADE, related_name='bids')
    bid_amount = models.DecimalField(max_digits=14, decimal_places=2)
    company_name = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=100, blank=True)
    bid_bond_reference = models.CharField(max_length=100, blank=True)
    technical_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    financial_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    submission_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUSES, default='draft')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Bid {self.reference} — {self.tender.title[:50]}' if self.tender else f'Bid {self.reference}'


class Contract(TimestampMixin):
    reference = models.CharField(max_length=30, unique=True, db_index=True)
    tender = models.ForeignKey(
        TenderNotice, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='contracts'
    )
    contract_number = models.CharField(max_length=100, blank=True)
    awarded_to = models.CharField(max_length=255)
    contract_value = models.DecimalField(max_digits=14, decimal_places=2)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    contract_type = models.CharField(max_length=100, default='supply')
    signing_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUSES, default='draft')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Contract {self.reference} — {self.awarded_to}'
