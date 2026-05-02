from django.db import models
from django.contrib.auth.models import User
from core.models import TimestampMixin
from core.utils import generate_tracking_id


class Consultation(TimestampMixin):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('under_review', 'Under Review'),
        ('completed', 'Completed'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    ministry = models.ForeignKey(
        'ministries.Ministry', on_delete=models.CASCADE, related_name='consultations'
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')

    class Meta:
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['ministry', 'is_active']),
        ]

    def __str__(self):
        return self.title


class PublicComment(TimestampMixin):
    consultation = models.ForeignKey(
        Consultation, on_delete=models.CASCADE, related_name='comments'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='public_comments')
    comment = models.TextField()
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['consultation', 'is_approved']),
        ]

    def __str__(self):
        return f'Comment by {self.user.username} on {self.consultation.title}'


class Petition(TimestampMixin):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('collecting_signatures', 'Collecting Signatures'),
        ('under_review', 'Under Review'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('closed', 'Closed'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='petitions')
    reference = models.CharField(max_length=30, unique=True, db_index=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    target_ministry = models.ForeignKey(
        'ministries.Ministry', on_delete=models.CASCADE, related_name='petitions'
    )
    signature_count = models.PositiveIntegerField(default=0)
    threshold = models.PositiveIntegerField(default=1000)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='draft')

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['reference']),
            models.Index(fields=['status']),
            models.Index(fields=['target_ministry']),
        ]

    def __str__(self):
        return f'{self.reference} — {self.title} ({self.signature_count}/{self.threshold})'

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = generate_tracking_id(prefix='PET')
        super().save(*args, **kwargs)
