from django.db import models
from core.models import TimestampMixin


class ExternalSystem(TimestampMixin):
    AUTH_TYPE_CHOICES = [
        ('api_key', 'API Key'),
        ('oauth', 'OAuth 2.0'),
        ('basic', 'Basic Auth'),
    ]
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    base_url = models.URLField()
    auth_type = models.CharField(max_length=20, choices=AUTH_TYPE_CHOICES, default='api_key')
    credentials = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f'{self.name} ({self.code})'


class DataExchange(TimestampMixin):
    DIRECTION_CHOICES = [
        ('inbound', 'Inbound'),
        ('outbound', 'Outbound'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    system = models.ForeignKey(
        ExternalSystem, on_delete=models.CASCADE, related_name='data_exchanges'
    )
    direction = models.CharField(max_length=10, choices=DIRECTION_CHOICES, default='outbound')
    data_type = models.CharField(max_length=100)
    payload = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['system', 'status']),
            models.Index(fields=['direction']),
        ]

    def __str__(self):
        return f'{self.direction} exchange: {self.data_type} ({self.status})'


class SyncLog(TimestampMixin):
    STATUS_CHOICES = [
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    exchange = models.ForeignKey(
        DataExchange, on_delete=models.CASCADE, related_name='sync_logs'
    )
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='running')
    records_processed = models.PositiveIntegerField(default=0)
    errors = models.JSONField(default=dict, blank=True)
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-started_at']
        indexes = [
            models.Index(fields=['exchange', 'status']),
        ]

    def __str__(self):
        return f'SyncLog for {self.exchange} — {self.status} ({self.records_processed} records)'
