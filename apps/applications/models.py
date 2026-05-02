from django.db import models
from django.contrib.auth.models import User
from core.models import TimestampMixin, UUIDMixin
from core.constants import APPLICATION_STATUSES


class FormField(TimestampMixin):
    FIELD_TYPES = [
        ('text', 'Text'),
        ('textarea', 'Text Area'),
        ('number', 'Number'),
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('date', 'Date'),
        ('select', 'Select'),
        ('file', 'File Upload'),
        ('checkbox', 'Checkbox'),
    ]
    service = models.ForeignKey(
        'services.Service', on_delete=models.CASCADE, related_name='form_fields'
    )
    label = models.CharField(max_length=255)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES, default='text')
    is_required = models.BooleanField(default=False)
    options = models.JSONField(default=list, blank=True)
    placeholder = models.CharField(max_length=255, blank=True)
    help_text = models.CharField(max_length=500, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.label} ({self.service.name})'


class Application(TimestampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    service = models.ForeignKey(
        'services.Service', on_delete=models.CASCADE, related_name='applications'
    )
    reference = models.CharField(max_length=30, unique=True, db_index=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUSES, default='draft')
    form_data = models.JSONField(default=dict, blank=True)
    county = models.ForeignKey(
        'counties.County', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='applications'
    )
    submitted_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['reference']), models.Index(fields=['status'])]

    def __str__(self):
        return f'{self.reference} — {self.service.name} ({self.status})'


class ApplicationDocument(TimestampMixin):
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, related_name='documents'
    )
    document_type = models.ForeignKey(
        'services.RequiredDocument', on_delete=models.SET_NULL,
        null=True, related_name='application_documents'
    )
    file = models.FileField(upload_to='application_docs/')
    original_filename = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.original_filename} — {self.application.reference}'


class StatusHistory(TimestampMixin):
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, related_name='status_history'
    )
    status = models.CharField(max_length=20, choices=APPLICATION_STATUSES)
    comment = models.TextField(blank=True)
    changed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        verbose_name_plural = 'Status Histories'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.application.reference}: {self.status}'
