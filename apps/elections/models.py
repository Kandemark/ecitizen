from django.db import models
from django.contrib.auth.models import User
from core.models import TimestampMixin
from core.constants import APPLICATION_STATUSES


class PollingStation(TimestampMixin):
    name = models.CharField(max_length=255)
    county = models.ForeignKey(
        'counties.County', on_delete=models.CASCADE, related_name='polling_stations'
    )
    constituency_name = models.CharField(max_length=255)
    ward_name = models.CharField(max_length=255)
    registration_center = models.CharField(max_length=255, blank=True)
    station_code = models.CharField(max_length=20, unique=True, blank=True)
    registered_voters = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['county', 'constituency_name', 'ward_name', 'name']

    def __str__(self):
        return f'{self.name} — {self.ward_name}, {self.constituency_name}'


class VoterRecord(TimestampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='voter_records')
    reference = models.CharField(max_length=30, unique=True, db_index=True)
    polling_station = models.ForeignKey(
        PollingStation, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='voters'
    )
    voter_number = models.CharField(max_length=50)
    id_number = models.CharField(max_length=20, blank=True)
    registration_date = models.DateField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUSES, default='draft')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Voter {self.voter_number} — {self.reference}'


class Candidate(TimestampMixin):
    name = models.CharField(max_length=255)
    election_type = models.CharField(max_length=100)
    political_party = models.CharField(max_length=255, blank=True)
    position = models.CharField(max_length=255)
    county = models.ForeignKey(
        'counties.County', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='candidates'
    )
    constituency_name = models.CharField(max_length=255, blank=True)
    ward_name = models.CharField(max_length=255, blank=True)
    symbol = models.CharField(max_length=100, blank=True)
    is_cleared = models.BooleanField(default=False)

    class Meta:
        ordering = ['election_type', 'position', 'name']

    def __str__(self):
        return f'{self.name} — {self.position} ({self.political_party})'
