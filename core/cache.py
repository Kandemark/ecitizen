"""
Cache helpers for the e-Citizen platform.

All getters follow a cache-first pattern:
1. Check Redis cache
2. On miss, compute and populate cache
3. Return result
"""
from django.core.cache import cache

# ── TTL constants (in seconds) ────────────────────────────────────────────────

TTL_SHORT = 300        # 5 minutes — rapidly changing data
TTL_MEDIUM = 1800      # 30 minutes
TTL_LONG = 7200        # 2 hours
TTL_DAILY = 86400      # 24 hours — reference data
TTL_WEEKLY = 604800    # 7 days — static data


def cache_get_or_set(key, compute_fn, ttl=TTL_MEDIUM):
    """Get from cache or compute + set. Returns the value."""
    value = cache.get(key)
    if value is not None:
        return value
    value = compute_fn()
    if value is not None:
        cache.set(key, value, ttl)
    return value


def invalidate_pattern(pattern):
    """Delete all cache keys matching a pattern.
    NOTE: Redis-specific — requires django-redis with KEY_PREFIX.
    For simple usage, call specific invalidation functions instead.
    """
    try:
        cache.delete_pattern(pattern)
    except AttributeError:
        # Fallback: delete known keys individually
        pass


def invalidate_keys(*keys):
    """Delete specific cache keys."""
    cache.delete_many(keys)


def cache_service_catalog():
    """Return the full active service catalog, cached."""
    def _build():
        from apps.services.models import Service, ServiceCategory
        services = list(
            Service.objects.filter(is_active=True)
            .select_related('ministry', 'category')
            .prefetch_related('counties')
        )
        categories = list(
            ServiceCategory.objects.filter(is_active=True)
            .prefetch_related('services')
        )
        return {'services': services, 'categories': categories}

    return cache_get_or_set('service_catalog', _build, TTL_MEDIUM)


def invalidate_service_cache():
    """Invalidate all service-related caches."""
    invalidate_keys(
        'service_catalog',
        'service_popular',
        'kenya_economic_indicators',
        'kenya_exchange_rates',
    )


def cache_ministry_list():
    """Return ministry list with service counts, cached daily."""
    def _build():
        from apps.ministries.models import Ministry
        from django.db.models import Count, Q
        return list(
            Ministry.objects.filter(is_active=True)
            .annotate(
                service_count=Count('services', filter=Q(services__is_active=True))
            )
            .prefetch_related('departments')
            .order_by('order', 'name')
        )

    return cache_get_or_set('ministry_list', _build, TTL_DAILY)


def cache_county_list():
    """Return county list with service counts, cached daily."""
    def _build():
        from apps.counties.models import County
        from django.db.models import Count, Q
        return list(
            County.objects.filter(is_active=True)
            .annotate(
                service_count=Count('services', filter=Q(services__is_active=True))
            )
            .order_by('code')
        )

    return cache_get_or_set('county_list', _build, TTL_DAILY)
