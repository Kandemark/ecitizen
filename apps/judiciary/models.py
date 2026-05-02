from django.db import models
from django.contrib.auth.models import User
from core.models import TimestampMixin
from core.constants import APPLICATION_STATUSES


CASE_TYPES = [
    ('civil', 'Civil'),
    ('criminal', 'Criminal'),
    ('constitutional', 'Constitutional'),
    ('commercial', 'Commercial'),
    ('family', 'Family'),
    ('land', 'Land'),
    ('employment', 'Employment'),
    ('tax', 'Tax'),
    ('judicial_review', 'Judicial Review'),
    ('appeal', 'Appeal'),
]

FILING_TYPES = [
    ('plaint', 'Plaint'),
    ('defence', 'Defence'),
    ('application', 'Application'),
    ('affidavit', 'Affidavit'),
    ('submission', 'Submission'),
    ('notice', 'Notice'),
    ('petition', 'Petition'),
    ('other', 'Other'),
]


class CourtCase(TimestampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='court_cases')
    reference = models.CharField(max_length=30, unique=True, db_index=True)
    case_number = models.CharField(max_length=100)
    court_name = models.CharField(max_length=255)
    case_type = models.CharField(max_length=30, choices=CASE_TYPES)
    title = models.CharField(max_length=500, blank=True)
    description = models.TextField(blank=True)
    filing_date = models.DateField(null=True, blank=True)
    presiding_judge = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUSES, default='draft')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Case {self.case_number} — {self.court_name}'


class Filing(TimestampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='court_filings')
    reference = models.CharField(max_length=30, unique=True, db_index=True)
    case = models.ForeignKey(CourtCase, on_delete=models.CASCADE, related_name='filings')
    filing_type = models.CharField(max_length=30, choices=FILING_TYPES)
    title = models.CharField(max_length=500, blank=True)
    description = models.TextField(blank=True)
    filing_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUSES, default='draft')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Filing {self.reference} — {self.case.case_number}'


class HearingSchedule(TimestampMixin):
    case = models.ForeignKey(CourtCase, on_delete=models.CASCADE, related_name='hearings')
    hearing_date = models.DateField()
    hearing_time = models.TimeField()
    courtroom = models.CharField(max_length=100)
    judge_name = models.CharField(max_length=255, blank=True)
    hearing_type = models.CharField(max_length=100, blank=True)
    outcome = models.TextField(blank=True)
    next_hearing_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-hearing_date', 'hearing_time']

    def __str__(self):
        return f'Hearing {self.case.case_number} — {self.hearing_date} {self.hearing_time}'


class Fine(TimestampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fines')
    reference = models.CharField(max_length=30, unique=True, db_index=True)
    offense = models.CharField(max_length=500)
    offense_date = models.DateField(null=True, blank=True)
    court_case = models.ForeignKey(
        CourtCase, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='fines'
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    due_date = models.DateField(null=True, blank=True)
    payment_reference = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUSES, default='draft')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Fine {self.reference} — KES {self.amount:,.2f} ({self.offense[:50]})'
