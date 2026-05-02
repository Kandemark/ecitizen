from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from core.models import TimestampMixin


class AuditEntry(TimestampMixin):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='audit_entries'
    )
    action = models.CharField(max_length=255)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, blank=True,
        related_name='audit_entries'
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_object = GenericForeignKey('content_type', 'object_id')
    data = models.JSONField(
        default=dict, blank=True,
        help_text='JSON containing before/after snapshots of the changed data'
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Audit Entries'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['action']),
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f'{self.action} by {self.user.username if self.user else "System"}'


class ComplianceCheck(TimestampMixin):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    check_function = models.CharField(
        max_length=255,
        help_text='Dotted path to the compliance check function'
    )
    is_passing = models.BooleanField(default=True)
    last_checked = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        status = 'PASS' if self.is_passing else 'FAIL'
        return f'{self.name} [{status}]'


class DataAccessLog(TimestampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='data_access_logs')
    data_type = models.CharField(max_length=100)
    record_id = models.PositiveIntegerField()
    access_reason = models.TextField(blank=True)
    accessed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-accessed_at']
        indexes = [
            models.Index(fields=['user', 'accessed_at']),
            models.Index(fields=['data_type', 'record_id']),
        ]

    def __str__(self):
        return f'{self.user.username} accessed {self.data_type}#{self.record_id}'
