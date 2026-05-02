from django.db import models
from django.contrib.auth.models import User
from core.models import TimestampMixin, UUIDMixin


class VerificationRequest(TimestampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='verification_requests')
    id_number = models.CharField(max_length=20)
    id_type = models.CharField(max_length=30, default='national_id')
    status = models.CharField(max_length=20, default='pending',
        choices=[('pending', 'Pending'), ('in_progress', 'In Progress'),
                 ('verified', 'Verified'), ('rejected', 'Rejected')])
    verified_at = models.DateTimeField(null=True, blank=True)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='verifications_done')

    def __str__(self):
        return f'{self.user.username} — {self.id_number} ({self.status})'


class VerificationResult(TimestampMixin):
    request = models.OneToOneField(VerificationRequest, on_delete=models.CASCADE, related_name='result')
    is_match = models.BooleanField(default=False)
    confidence_score = models.FloatField(default=0.0)
    details = models.JSONField(default=dict, blank=True)
