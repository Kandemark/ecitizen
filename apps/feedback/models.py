from django.db import models
from django.contrib.auth.models import User
from core.models import TimestampMixin
from core.utils import generate_tracking_id


class Feedback(TimestampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedback_entries')
    service = models.ForeignKey(
        'services.Service', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='feedback_entries'
    )
    rating = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        help_text='Rating from 1 (worst) to 5 (best)'
    )
    title = models.CharField(max_length=255)
    comment = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['rating']),
            models.Index(fields=['service', 'is_public']),
        ]

    def __str__(self):
        return f'{self.title} ({self.rating}/5) by {self.user.username}'


class Complaint(TimestampMixin):
    CATEGORY_CHOICES = [
        ('service_delivery', 'Service Delivery'),
        ('staff_conduct', 'Staff Conduct'),
        ('corruption', 'Corruption'),
        ('delay', 'Delay in Service'),
        ('discrimination', 'Discrimination'),
        ('billing', 'Billing / Fees'),
        ('accessibility', 'Accessibility'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('investigating', 'Investigating'),
        ('resolved', 'Resolved'),
        ('escalated', 'Escalated'),
        ('dismissed', 'Dismissed'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints')
    reference = models.CharField(max_length=30, unique=True, db_index=True)
    subject = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='other')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    resolution = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['reference']),
            models.Index(fields=['status']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return f'{self.reference} — {self.subject} ({self.status})'

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = generate_tracking_id(prefix='CMP')
        super().save(*args, **kwargs)


class SatisfactionSurvey(TimestampMixin):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
