from celery import shared_task
from .services import WorkflowEngine


@shared_task(name='workflow.check_escalations')
def check_escalations():
    """Periodic task: check for overdue review assignments and escalate."""
    WorkflowEngine.check_escalations()
