from django.db import models
from django.contrib.auth.models import User
from core.models import TimestampMixin


class ReportTemplate(TimestampMixin):
    REPORT_TYPE_CHOICES = [
        ('tabular', 'Tabular Report'),
        ('chart', 'Chart Report'),
        ('summary', 'Summary Report'),
        ('analytics', 'Analytics Report'),
        ('custom', 'Custom Report'),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    report_type = models.CharField(max_length=30, choices=REPORT_TYPE_CHOICES, default='tabular')
    template_content = models.TextField(blank=True)
    parameters = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class GeneratedReport(TimestampMixin):
    FORMAT_CHOICES = [
        ('pdf', 'PDF'),
        ('excel', 'Excel'),
        ('csv', 'CSV'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('generating', 'Generating'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='generated_reports')
    template = models.ForeignKey(
        ReportTemplate, on_delete=models.CASCADE, related_name='generated_reports'
    )
    parameters = models.JSONField(default=dict, blank=True)
    file = models.FileField(upload_to='generated_reports/', null=True, blank=True)
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default='pdf')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['user', 'created_at']),
        ]

    def __str__(self):
        return f'{self.template.name} — {self.user.username} ({self.status})'
