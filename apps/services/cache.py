"""Service catalog caching and signal-based invalidation."""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from core.cache import invalidate_service_cache
from .models import Service, ServiceCategory
from core.cache import cache_get_or_set, TTL_MEDIUM


@receiver(post_save, sender=Service)
@receiver(post_delete, sender=Service)
def invalidate_on_service_change(sender, instance, **kwargs):
    invalidate_service_cache()


@receiver(post_save, sender=ServiceCategory)
@receiver(post_delete, sender=ServiceCategory)
def invalidate_on_category_change(sender, instance, **kwargs):
    invalidate_service_cache()


def get_popular_services(limit=12):
    """Get popular services, cached 30 minutes."""
    def _build():
        from .models import Service
        return list(
            Service.objects.filter(is_popular=True, is_active=True)
            .select_related('ministry', 'category')
            .values('name', 'slug', 'icon', 'short_description', 'fee_kes')[:limit]
        )
    return cache_get_or_set('service_popular', _build, TTL_MEDIUM)
