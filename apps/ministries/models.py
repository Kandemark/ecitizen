from django.db import models
from core.models import TimestampMixin


class Ministry(TimestampMixin):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Ministries'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Department(TimestampMixin):
    ministry = models.ForeignKey(Ministry, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    director = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['ministry', 'name']

    def __str__(self):
        return f'{self.name} — {self.ministry.name}'


class Division(TimestampMixin):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='divisions')
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20, unique=True)

    class Meta:
        ordering = ['department', 'name']

    def __str__(self):
        return f'{self.name} — {self.department.name}'
