from django.db import models
from django.contrib.auth.models import User
from core.models import TimestampMixin, UUIDMixin


class WorkflowDefinition(TimestampMixin):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    service = models.OneToOneField(
        'services.Service', on_delete=models.CASCADE, related_name='workflow'
    )
    max_days_per_step = models.PositiveIntegerField(default=7)

    def __str__(self):
        return f'Workflow: {self.service.name}'


class ApprovalStep(TimestampMixin):
    workflow = models.ForeignKey(
        WorkflowDefinition, on_delete=models.CASCADE, related_name='steps'
    )
    name = models.CharField(max_length=255)
    order = models.IntegerField()
    role_required = models.CharField(
        max_length=30, default='agency_staff',
        choices=[
            ('agency_staff', 'Agency Staff'),
            ('supervisor', 'Supervisor'),
            ('director', 'Director'),
            ('administrator', 'Administrator'),
        ]
    )
    can_reject = models.BooleanField(default=True)
    can_request_revision = models.BooleanField(default=True)

    class Meta:
        ordering = ['workflow', 'order']

    def __str__(self):
        return f'{self.workflow.name} — Step {self.order}: {self.name}'


class ReviewAssignment(TimestampMixin):
    application = models.ForeignKey(
        'applications.Application', on_delete=models.CASCADE,
        related_name='review_assignments'
    )
    step = models.ForeignKey(ApprovalStep, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    is_completed = models.BooleanField(default=False)
    decision = models.CharField(
        max_length=20, blank=True,
        choices=[('approved', 'Approved'), ('rejected', 'Rejected'), ('revision', 'Revision')]
    )
    comment = models.TextField(blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Review: {self.application.reference} — {self.step.name}'


class EscalationRule(TimestampMixin):
    workflow = models.ForeignKey(
        WorkflowDefinition, on_delete=models.CASCADE, related_name='escalation_rules'
    )
    step = models.ForeignKey(ApprovalStep, on_delete=models.CASCADE)
    auto_escalate_after_hours = models.IntegerField(default=72)
    escalate_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='escalations'
    )

    def __str__(self):
        return f'Escalation: {self.step.name} after {self.auto_escalate_after_hours}h'
