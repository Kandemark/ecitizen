from django.db import models
from django.contrib.auth.models import User
from core.models import TimestampMixin

class PassportApplication(TimestampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='passport_applications')
    reference = models.CharField(max_length=30, unique=True)
    passport_type = models.CharField(max_length=30, default='ordinary')
    status = models.CharField(max_length=20, default='draft')

class VisaApplication(TimestampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='visa_applications')
    reference = models.CharField(max_length=30, unique=True)
    visa_type = models.CharField(max_length=30)
    status = models.CharField(max_length=20, default='draft')

class WorkPermit(TimestampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='work_permits')
    reference = models.CharField(max_length=30, unique=True)
    permit_class = models.CharField(max_length=5)
    employer = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, default='draft')
