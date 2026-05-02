from django.db import models
from django.contrib.auth.models import User
from core.models import TimestampMixin


class Dashboard(TimestampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dashboards')
    name = models.CharField(max_length=255)
    layout = models.JSONField(default=dict, blank=True)
    is_default = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'name'],
                name='unique_user_dashboard_name'
            ),
        ]

    def __str__(self):
        return f'{self.name} — {self.user.username}'


class Widget(TimestampMixin):
    WIDGET_TYPE_CHOICES = [
        ('chart_bar', 'Bar Chart'),
        ('chart_line', 'Line Chart'),
        ('chart_pie', 'Pie Chart'),
        ('table', 'Data Table'),
        ('metric', 'Single Metric'),
        ('map', 'Map'),
        ('list', 'List'),
        ('custom', 'Custom'),
    ]
    dashboard = models.ForeignKey(
        Dashboard, on_delete=models.CASCADE, related_name='widgets'
    )
    title = models.CharField(max_length=255)
    widget_type = models.CharField(max_length=20, choices=WIDGET_TYPE_CHOICES, default='metric')
    config = models.JSONField(default=dict, blank=True)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['dashboard', 'position']

    def __str__(self):
        return f'{self.title} ({self.widget_type}) on {self.dashboard.name}'


class Metric(TimestampMixin):
    name = models.CharField(max_length=255)
    value = models.FloatField(default=0.0)
    source = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}: {self.value}'
