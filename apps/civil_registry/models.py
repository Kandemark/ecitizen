from django.db import models
from django.contrib.auth.models import User
from core.models import TimestampMixin
from core.constants import APPLICATION_STATUSES, GENDER_CHOICES, COUNTIES


class BirthCertificate(TimestampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='birth_certificates')
    reference = models.CharField(max_length=30, unique=True, db_index=True)
    child_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    place_of_birth = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='male')
    father_name = models.CharField(max_length=255, blank=True)
    mother_name = models.CharField(max_length=255, blank=True)
    county_of_birth = models.CharField(max_length=3, choices=COUNTIES, blank=True)
    registration_number = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUSES, default='draft')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Birth Certificate {self.reference} — {self.child_name}'


class DeathCertificate(TimestampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='death_certificates')
    reference = models.CharField(max_length=30, unique=True, db_index=True)
    deceased_name = models.CharField(max_length=255)
    date_of_death = models.DateField()
    place_of_death = models.CharField(max_length=255)
    cause_of_death = models.CharField(max_length=500, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='male')
    age_at_death = models.PositiveSmallIntegerField(null=True, blank=True)
    next_of_kin = models.CharField(max_length=255, blank=True)
    informant_name = models.CharField(max_length=255, blank=True)
    registration_number = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUSES, default='draft')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Death Certificate {self.reference} — {self.deceased_name}'


class MarriageCertificate(TimestampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='marriage_certificates')
    reference = models.CharField(max_length=30, unique=True, db_index=True)
    spouse1_name = models.CharField(max_length=255)
    spouse2_name = models.CharField(max_length=255)
    marriage_date = models.DateField()
    marriage_place = models.CharField(max_length=255, blank=True)
    marriage_type = models.CharField(max_length=50, default='civil')
    officiant_name = models.CharField(max_length=255, blank=True)
    registration_number = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUSES, default='draft')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Marriage Certificate {self.reference} — {self.spouse1_name} & {self.spouse2_name}'
