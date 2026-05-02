import secrets
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from core.models import TimestampMixin, UUIDMixin


class APIKey(TimestampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='api_keys')
    name = models.CharField(max_length=100)
    key = models.CharField(max_length=64, unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    last_used_at = models.DateTimeField(null=True, blank=True)
    rate_limit = models.IntegerField(default=1000)

    class Meta:
        verbose_name = 'API Key'

    def __str__(self):
        return f'{self.name} — {self.user.username}'

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = secrets.token_hex(32)
        super().save(*args, **kwargs)

    def is_valid(self):
        if not self.is_active:
            return False
        if self.expires_at and self.expires_at < timezone.now():
            return False
        return True


class Webhook(TimestampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='webhooks')
    name = models.CharField(max_length=100)
    url = models.URLField()
    event = models.CharField(max_length=100)
    secret = models.CharField(max_length=64, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} — {self.event}'

    def save(self, *args, **kwargs):
        if not self.secret:
            self.secret = secrets.token_hex(16)
        super().save(*args, **kwargs)
