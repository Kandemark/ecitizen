from django.contrib import admin
from .models import WorkflowDefinition, ApprovalStep, ReviewAssignment, EscalationRule


class ApprovalStepInline(admin.TabularInline):
    model = ApprovalStep
    extra = 1


@admin.register(WorkflowDefinition)
class WorkflowDefinitionAdmin(admin.ModelAdmin):
    list_display = ['name', 'service', 'max_days_per_step']
    search_fields = ['name', 'service__name']
    inlines = [ApprovalStepInline]


@admin.register(ApprovalStep)
class ApprovalStepAdmin(admin.ModelAdmin):
    list_display = ['name', 'workflow', 'order', 'role_required']
    list_filter = ['workflow', 'role_required']


@admin.register(ReviewAssignment)
class ReviewAssignmentAdmin(admin.ModelAdmin):
    list_display = ['application', 'step', 'assigned_to', 'is_completed', 'decision', 'completed_at']
    list_filter = ['is_completed', 'decision']
    search_fields = ['application__reference']


@admin.register(EscalationRule)
class EscalationRuleAdmin(admin.ModelAdmin):
    list_display = ['workflow', 'step', 'auto_escalate_after_hours']
