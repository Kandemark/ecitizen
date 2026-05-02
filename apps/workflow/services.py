from django.utils import timezone
from django.db.models import Q
from .models import WorkflowDefinition, ApprovalStep, ReviewAssignment, EscalationRule


class WorkflowEngine:
    """Orchestrates review assignments and escalations when applications are submitted."""

    @staticmethod
    def on_application_submitted(application):
        """Create review assignments for all workflow steps when app is submitted."""
        service = application.service
        try:
            wf_def = WorkflowDefinition.objects.select_related('service').prefetch_related(
                'steps'
            ).get(service=service)
        except WorkflowDefinition.DoesNotExist:
            return

        steps = wf_def.steps.order_by('order')
        for step in steps:
            ReviewAssignment.objects.get_or_create(
                application=application,
                step=step,
                defaults={'assigned_to': WorkflowEngine._find_reviewer(step)},
            )

        application.status = 'in_review'
        application.save(update_fields=['status'])

    @staticmethod
    def on_step_completed(assignment, decision):
        """Progress application when a review step is completed."""
        assignment.decision = decision
        assignment.is_completed = True
        assignment.completed_at = timezone.now()
        assignment.save()

        application = assignment.application

        if decision == 'rejected':
            application.status = 'rejected'
            application.save(update_fields=['status'])
            return

        if decision == 'revision':
            application.status = 'pending_documents'
            application.save(update_fields=['status'])
            return

        # Check if all steps are done
        pending = ReviewAssignment.objects.filter(
            application=application, is_completed=False
        ).exists()

        if not pending:
            application.status = 'approved'
            application.save(update_fields=['status'])

    @staticmethod
    def check_escalations():
        """Find overdue review assignments and escalate them."""
        now = timezone.now()
        overdue = ReviewAssignment.objects.filter(
            is_completed=False,
            created_at__lt=now - timezone.timedelta(hours=72),
        ).select_related('step', 'application')

        for assignment in overdue:
            try:
                rule = EscalationRule.objects.get(
                    workflow=assignment.step.workflow,
                    step=assignment.step,
                )
                if rule.escalate_to:
                    assignment.assigned_to = rule.escalate_to
                    assignment.save(update_fields=['assigned_to'])
            except EscalationRule.DoesNotExist:
                continue

    @staticmethod
    def _find_reviewer(step):
        """Find an appropriate reviewer based on role. Returns User or None."""
        from django.contrib.auth.models import User as DjangoUser
        role_map = {
            'agency_staff': 'agency_staff',
            'supervisor': 'supervisor',
            'director': 'director',
            'administrator': 'administrator',
        }
        role = role_map.get(step.role_required, 'agency_staff')

        user = DjangoUser.objects.filter(
            profile__role=role, is_active=True
        ).order_by('?').first()

        if not user:
            user = DjangoUser.objects.filter(
                is_staff=True, is_active=True
            ).order_by('?').first()

        return user
