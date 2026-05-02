"""
Tests for the WorkflowEngine — application submission, step progression, escalation.
"""
from datetime import timedelta

import pytest
from django.utils import timezone

from apps.services.models import Service, ServiceCategory
from apps.applications.models import Application
from apps.workflow.models import (
    WorkflowDefinition, ApprovalStep, ReviewAssignment, EscalationRule,
)
from apps.workflow.services import WorkflowEngine


@pytest.mark.django_db
class TestWorkflowEngine:
    def test_submit_triggers_review_assignments(self, user, staff_user):
        cat = ServiceCategory.objects.create(name='Test')
        service = Service.objects.create(name='Test Svc', slug='test-svc', category=cat)

        wf = WorkflowDefinition.objects.create(service=service, name='Test WF')
        step = ApprovalStep.objects.create(
            workflow=wf, name='Initial Review', order=1,
            role_required='agency_staff',
        )

        app = Application.objects.create(
            user=user, service=service, reference='REF-001',
            status='submitted',
        )

        WorkflowEngine.on_application_submitted(app)

        app.refresh_from_db()
        assert app.status == 'in_review'

        assignments = ReviewAssignment.objects.filter(application=app)
        assert assignments.count() == 1
        assert assignments.first().step == step

    def test_step_approval_progresses(self, user):
        cat = ServiceCategory.objects.create(name='T')
        service = Service.objects.create(name='S', slug='s', category=cat)

        wf = WorkflowDefinition.objects.create(service=service, name='WF')
        step = ApprovalStep.objects.create(
            workflow=wf, name='Review', order=1, role_required='agency_staff',
        )

        app = Application.objects.create(
            user=user, service=service, reference='REF-002',
            status='submitted',
        )
        assignment = ReviewAssignment.objects.create(
            application=app, step=step,
        )

        WorkflowEngine.on_step_completed(assignment, 'approved')

        app.refresh_from_db()
        assert app.status == 'approved'

    def test_step_rejection_stops_workflow(self, user):
        cat = ServiceCategory.objects.create(name='T2')
        service = Service.objects.create(name='S2', slug='s2', category=cat)

        wf = WorkflowDefinition.objects.create(service=service, name='WF2')
        step = ApprovalStep.objects.create(
            workflow=wf, name='Review', order=1, role_required='agency_staff',
        )

        app = Application.objects.create(
            user=user, service=service, reference='REF-003',
            status='submitted',
        )
        assignment = ReviewAssignment.objects.create(
            application=app, step=step,
        )

        WorkflowEngine.on_step_completed(assignment, 'rejected')

        app.refresh_from_db()
        assert app.status == 'rejected'

    def test_escalation_finds_overdue(self, user, staff_user):
        cat = ServiceCategory.objects.create(name='T3')
        service = Service.objects.create(name='S3', slug='s3', category=cat)

        wf = WorkflowDefinition.objects.create(service=service, name='WF3')
        step = ApprovalStep.objects.create(
            workflow=wf, name='Review', order=1, role_required='agency_staff',
        )

        app = Application.objects.create(
            user=user, service=service, reference='REF-004',
            status='in_review',
        )

        # Create an assignment that's 100 hours old
        assignment = ReviewAssignment.objects.create(
            application=app, step=step,
        )
        assignment.created_at = timezone.now() - timedelta(hours=100)
        assignment.save(update_fields=['created_at'])

        EscalationRule.objects.create(
            workflow=wf, step=step,
            auto_escalate_after_hours=72,
            escalate_to=staff_user,
        )

        WorkflowEngine.check_escalations()

        assignment.refresh_from_db()
        assert assignment.assigned_to == staff_user
