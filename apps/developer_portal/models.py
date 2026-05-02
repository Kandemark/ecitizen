from django.db import models
from django.contrib.auth.models import User
from core.models import TimestampMixin


class DeveloperRegistration(TimestampMixin):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='developer_registrations')
    organization = models.CharField(max_length=255)
    website = models.URLField(blank=True)
    use_case = models.TextField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f'{self.organization} — {self.user.username} ({self.status})'


class SandboxEnvironment(TimestampMixin):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sandbox_environments'
    )
    name = models.CharField(max_length=255)
    base_url = models.URLField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Sandbox: {self.name} ({self.user.username})'
