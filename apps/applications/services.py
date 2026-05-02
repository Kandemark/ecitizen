"""
Application submission engine — unified entry point for all service applications.

Each ministry app registers its handler here. When a citizen submits an application
form, the engine validates, persists, assigns a reviewer, and triggers notifications.
"""
import logging
from typing import Any, Optional

from django.db import transaction
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

# Registry of app-specific submission handlers.
# Keyed by app_label, each handler receives: user, data: dict
# Must return the created model instance.
_HANDLERS: dict[str, callable] = {}


def register_handler(app_label: str, fn: callable):
    _HANDLERS[app_label] = fn


def submit_application(user: User, service_type: str, data: dict[str, Any]):
    """
    Create a new application record.

    service_type is the app_label (e.g. 'civil_registry', 'immigration').
    Returns the created object.
    """
    handler = _HANDLERS.get(service_type)
    if not handler:
        raise ValueError(f'No handler registered for service type: {service_type}')

    with transaction.atomic():
        instance = handler(user, data)

        # Trigger workflow if available
        _maybe_trigger_workflow(instance, user)

        logger.info('Application submitted: type=%s ref=%s user=%s',
                     service_type, getattr(instance, 'reference', 'N/A'), user.pk)
        return instance


def _maybe_trigger_workflow(instance, user):
    """Notify workflow engine of new submission so review assignments fire."""
    try:
        from apps.workflow.services import WorkflowEngine
        WorkflowEngine.on_application_submitted(instance)
    except Exception as exc:
        logger.warning('Workflow trigger skipped: %s', exc)


def get_application_status(reference: str):
    """Return a status-timeline dict for a given reference."""
    from .models import Application
    try:
        app = Application.objects.prefetch_related(
            'status_history'
        ).get(reference=reference)
    except Application.DoesNotExist:
        return None

    return {
        'reference': app.reference,
        'status': app.status,
        'status_display': app.get_status_display(),
        'submitted_at': app.submitted_at,
        'completed_at': app.completed_at,
        'history': [
            {'status': h.get_status_display(), 'comment': h.comment, 'timestamp': h.created_at}
            for h in app.status_history.all()
        ],
    }
