from django.db import models
from django.contrib.auth.models import User
from core.models import TimestampMixin
from core.constants import APPLICATION_STATUSES


LOAN_TYPES = [
    ('undergraduate', 'Undergraduate Loan'),
    ('postgraduate', 'Postgraduate Loan'),
    ('tvet', 'TVET Loan'),
    ('bursary', 'Bursary'),
]

REGISTRATION_TYPES = [
    ('primary', 'Primary School'),
    ('secondary', 'Secondary School'),
    ('tvet', 'TVET Institution'),
    ('university', 'University'),
    ('tertiary', 'Tertiary College'),
    ('other', 'Other'),
]

EXAM_TYPES = [
    ('kcpe', 'KCPE'),
    ('kcse', 'KCSE'),
    ('diploma', 'Diploma'),
    ('certificate', 'Certificate'),
    ('degree', 'Degree'),
    ('professional', 'Professional'),
]


class LoanApplication(TimestampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loan_applications')
    reference = models.CharField(max_length=30, unique=True, db_index=True)
    loan_type = models.CharField(max_length=30, choices=LOAN_TYPES, default='undergraduate')
    institution = models.CharField(max_length=255)
    campus = models.CharField(max_length=255, blank=True)
    course_of_study = models.CharField(max_length=255, blank=True)
    year_of_study = models.PositiveSmallIntegerField(default=1)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    amount_approved = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    disbursement_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUSES, default='draft')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Loan {self.reference} — {self.institution} (KES {self.amount:,.2f})'


class SchoolRegistration(TimestampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='school_registrations')
    reference = models.CharField(max_length=30, unique=True, db_index=True)
    school_name = models.CharField(max_length=255)
    registration_type = models.CharField(max_length=30, choices=REGISTRATION_TYPES)
    registration_number = models.CharField(max_length=100, blank=True)
    county = models.ForeignKey(
        'counties.County', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='school_registrations'
    )
    physical_address = models.TextField(blank=True)
    postal_address = models.CharField(max_length=100, blank=True)
    proprietor_name = models.CharField(max_length=255, blank=True)
    registration_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUSES, default='draft')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'School {self.reference} — {self.school_name}'


class ExamResult(TimestampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exam_results')
    reference = models.CharField(max_length=30, unique=True, db_index=True)
    exam_type = models.CharField(max_length=30, choices=EXAM_TYPES)
    index_number = models.CharField(max_length=50)
    examination_year = models.PositiveSmallIntegerField(null=True, blank=True)
    school_name = models.CharField(max_length=255, blank=True)
    mean_grade = models.CharField(max_length=10, blank=True)
    total_points = models.PositiveSmallIntegerField(default=0)
    certificate_number = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUSES, default='draft')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Exam Result {self.reference} — {self.exam_type} ({self.index_number})'
