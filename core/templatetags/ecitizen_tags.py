import json as json_lib
from django import template
from django.utils import timezone
from django.urls import reverse

register = template.Library()


@register.filter
def range_filter(value):
    """Return range(0, value) for template use."""
    try:
        return range(int(value))
    except (ValueError, TypeError):
        return range(0)


@register.filter
def json(data):
    """Convert Python dict/list to JSON string."""
    return json_lib.dumps(data)


@register.filter
def status_color(status):
    """Return Tailwind CSS color for a status."""
    colors = {
        # Application statuses
        'draft': 'bg-gray-100 text-gray-700',
        'submitted': 'bg-blue-100 text-blue-700',
        'in_review': 'bg-yellow-100 text-yellow-700',
        'under_review': 'bg-yellow-100 text-yellow-700',
        'pending_documents': 'bg-orange-100 text-orange-700',
        'approved': 'bg-green-100 text-green-700',
        'completed': 'bg-green-100 text-green-800',
        'rejected': 'bg-red-100 text-red-700',
        'appealed': 'bg-purple-100 text-purple-700',
        # Payment statuses
        'pending': 'bg-yellow-100 text-yellow-700',
        'processing': 'bg-blue-100 text-blue-700',
        'failed': 'bg-red-100 text-red-700',
        'refunded': 'bg-purple-100 text-purple-700',
        'cancelled': 'bg-gray-100 text-gray-500',
        # Appointment statuses
        'scheduled': 'bg-blue-100 text-blue-700',
        'confirmed': 'bg-green-100 text-green-700',
        'in_progress': 'bg-indigo-100 text-indigo-700',
        'no_show': 'bg-red-100 text-red-700',
    }
    return colors.get(status, 'bg-gray-100 text-gray-700')


@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''


@register.simple_tag
def absolute_url(view_name, *args, **kwargs):
    return reverse(view_name, args=args, kwargs=kwargs)
