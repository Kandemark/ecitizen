from rest_framework import serializers
from .models import WorkflowDefinition, ApprovalStep, ReviewAssignment, EscalationRule


class ApprovalStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalStep
        fields = ['id', 'name', 'order', 'role_required', 'can_reject', 'can_request_revision']


class EscalationRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EscalationRule
        fields = ['id', 'step', 'auto_escalate_after_hours']


class WorkflowDefinitionSerializer(serializers.ModelSerializer):
    steps = ApprovalStepSerializer(many=True, read_only=True)
    escalation_rules = EscalationRuleSerializer(many=True, read_only=True)

    class Meta:
        model = WorkflowDefinition
        fields = ['id', 'name', 'description', 'service', 'max_days_per_step', 'steps', 'escalation_rules']


class ReviewAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewAssignment
        fields = ['id', 'application', 'step', 'assigned_to', 'is_completed', 'decision', 'comment', 'completed_at']
