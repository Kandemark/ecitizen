from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from core.models import TimestampMixin
from core.constants import NOTIFICATION_CHANNELS


class Notification(TimestampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    channel = models.CharField(max_length=20, choices=NOTIFICATION_CHANNELS, default='in_app')
    is_read = models.BooleanField(default=False)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, blank=True,
        related_name='notifications'
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['content_type', 'object_id']),
        ]

    def __str__(self):
        return f'{self.title} — {self.user.username} ({self.channel})'


class NotificationPreference(TimestampMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preference')
    email_enabled = models.BooleanField(default=True)
    sms_enabled = models.BooleanField(default=True)
    push_enabled = models.BooleanField(default=True)
    quiet_hours_start = models.TimeField(null=True, blank=True)
    quiet_hours_end = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f'Preferences for {self.user.username}'


class DeviceToken(TimestampMixin):
    PLATFORM_CHOICES = [
        ('ios', 'iOS'),
        ('android', 'Android'),
        ('web', 'Web'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='device_tokens')
    platform = models.CharField(max_length=10, choices=PLATFORM_CHOICES)
    token = models.CharField(max_length=500)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = [['user', 'token']]

    def __str__(self):
        return f'{self.user.username} — {self.platform}'
