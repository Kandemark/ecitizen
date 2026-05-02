from django.db import models
from core.models import TimestampMixin


class County(TimestampMixin):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=100)
    capital = models.CharField(max_length=100, blank=True)
    governor = models.CharField(max_length=100, blank=True)
    population = models.PositiveBigIntegerField(default=0)
    area_sqkm = models.FloatField(default=0.0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Counties'
        ordering = ['code']

    def __str__(self):
        return f'{self.name} ({self.code})'


class SubCounty(TimestampMixin):
    county = models.ForeignKey(County, on_delete=models.CASCADE, related_name='sub_counties')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)

    class Meta:
        verbose_name_plural = 'Sub Counties'
        ordering = ['county', 'name']

    def __str__(self):
        return f'{self.name} — {self.county.name}'


class Ward(TimestampMixin):
    sub_county = models.ForeignKey(SubCounty, on_delete=models.CASCADE, related_name='wards')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=15, unique=True)

    class Meta:
        ordering = ['sub_county', 'name']

    def __str__(self):
        return f'{self.name} — {self.sub_county.name}'


class Constituency(TimestampMixin):
    county = models.ForeignKey(County, on_delete=models.CASCADE, related_name='constituencies')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    mp_name = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name_plural = 'Constituencies'
        ordering = ['county', 'name']

    def __str__(self):
        return f'{self.name} — {self.county.name}'


class Village(TimestampMixin):
    """Sub-location / Village — the smallest administrative unit in Kenya."""
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name='villages')
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=20, unique=True)

    class Meta:
        ordering = ['ward', 'name']

    def __str__(self):
        return f'{self.name} — {self.ward.name}'
