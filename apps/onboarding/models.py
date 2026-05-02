from django.db import models
from django.contrib.auth.models import User
from core.models import TimestampMixin


class OnboardingStep(TimestampMixin):
    STEP_CHOICES = [
        ('welcome', 'Welcome'),
        ('id_type', 'ID Type'),
        ('personal_info', 'Personal Info'),
        ('contact_info', 'Contact Info'),
        ('location', 'Location'),
        ('id_verification', 'ID Verification'),
        ('biometric', 'Biometric Capture'),
        ('account_setup', 'Account Setup'),
        ('preferences', 'Preferences'),
        ('complete', 'Complete'),
    ]
    name = models.CharField(max_length=50, choices=STEP_CHOICES, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.IntegerField(unique=True)
    is_required = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.order}. {self.name}'


class OnboardingProgress(TimestampMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='onboarding')
    current_step = models.IntegerField(default=1)
    is_complete = models.BooleanField(default=False)
    completed_steps = models.JSONField(default=list, blank=True)
    data = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name_plural = 'Onboarding Progress'

    def __str__(self):
        return f'{self.user.username} — Step {self.current_step}'

    def advance_step(self):
        self.completed_steps.append(self.current_step)
        self.current_step += 1
        if self.current_step > 10:
            self.is_complete = True
        self.save()

    def go_to_step(self, step):
        if 1 <= step <= 10:
            self.current_step = step
            self.save()
