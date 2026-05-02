from .constants import COUNTIES


def global_context(request):
    """Context variables available to all templates."""
    return {
        'KENYAN_COUNTIES': COUNTIES,
        'current_year': 2026,
    }
