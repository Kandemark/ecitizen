from django.db import models
from django.contrib.auth.models import User
from core.models import TimestampMixin, UUIDMixin
from core.constants import GENDER_CHOICES, USER_ROLES, ID_TYPES


class Profile(TimestampMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    id_number = models.CharField(max_length=20, blank=True, db_index=True)
    id_type = models.CharField(max_length=20, choices=ID_TYPES, default='national_id')
    phone = models.CharField(max_length=15, blank=True, db_index=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    county = models.ForeignKey(
        'counties.County', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='residents'
    )
    sub_county = models.ForeignKey(
        'counties.SubCounty', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='residents'
    )
    ward = models.ForeignKey(
        'counties.Ward', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='residents'
    )
    village = models.ForeignKey(
        'counties.Village', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='residents'
    )
    postal_address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    is_verified = models.BooleanField(default=False)
    role = models.CharField(max_length=20, choices=USER_ROLES, default='citizen')
    transaction_pin = models.CharField(max_length=128, blank=True)
    preferences = models.JSONField(default=dict, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['id_number']),
            models.Index(fields=['phone']),
        ]

    def __str__(self):
        return f"{self.user.username} — {self.get_id_type_display()}"


class AuditEntry(TimestampMixin):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    details = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    content_type = models.ForeignKey(
        'contenttypes.ContentType', on_delete=models.SET_NULL, null=True, blank=True
    )
    object_id = models.CharField(max_length=255, blank=True)
    data = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name_plural = 'Audit Entries'
        ordering = ['-created_at']
        indexes = [models.Index(fields=['-created_at'])]

    def __str__(self):
        username = self.user.username if self.user else 'system'
        return f'{username} — {self.action}'
