from django.db import models
from django.contrib.auth.models import User
from core.models import TimestampMixin
from core.constants import APPLICATION_STATUSES


class TitleDeed(TimestampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='title_deeds')
    reference = models.CharField(max_length=30, unique=True, db_index=True)
    title_number = models.CharField(max_length=100)
    property_location = models.CharField(max_length=500)
    county = models.ForeignKey(
        'counties.County', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='title_deeds'
    )
    land_size_hectares = models.DecimalField(max_digits=12, decimal_places=4, default=0.0)
    tenure_type = models.CharField(max_length=50, default='freehold')
    registered_owner_name = models.CharField(max_length=255, blank=True)
    registration_date = models.DateField(null=True, blank=True)
    encumbrances = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUSES, default='draft')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Title Deed'

    def __str__(self):
        return f'Title Deed {self.title_number} — {self.property_location}'


class LandSearch(TimestampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='land_searches')
    reference = models.CharField(max_length=30, unique=True, db_index=True)
    title_number = models.CharField(max_length=100)
    search_purpose = models.CharField(max_length=500)
    search_date = models.DateTimeField(null=True, blank=True)
    search_result = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUSES, default='draft')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Land Search'

    def __str__(self):
        return f'Land Search {self.reference} — {self.title_number}'


class Transfer(TimestampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='land_transfers')
    reference = models.CharField(max_length=30, unique=True, db_index=True)
    title_deed = models.ForeignKey(
        TitleDeed, on_delete=models.CASCADE, related_name='transfers'
    )
    from_owner = models.CharField(max_length=255)
    to_owner = models.CharField(max_length=255)
    consideration_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    transfer_date = models.DateField(null=True, blank=True)
    transfer_type = models.CharField(max_length=50, default='sale')
    status = models.CharField(max_length=20, choices=APPLICATION_STATUSES, default='draft')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Transfer {self.reference}: {self.from_owner} -> {self.to_owner}'
