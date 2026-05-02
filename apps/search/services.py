"""
PostgreSQL full-text search across e-Citizen models.

Uses Django's SearchVector, SearchQuery, and SearchRank for
relevance-ranked search with proper stemming and weighting.
"""
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import Q, F
from django.db.models.expressions import RawSQL


# Weight configuration: A=highest priority, D=lowest
SERVICE_VECTOR = SearchVector('name', weight='A') + \
    SearchVector('short_description', weight='B') + \
    SearchVector('description', weight='C')

NEWS_VECTOR = SearchVector('title', weight='A') + \
    SearchVector('summary', weight='B')

SEARCH_INDEX_VECTOR = SearchVector('title', weight='A') + \
    SearchVector('description', weight='B')


def search_services(query_str, limit=50):
    """Full-text search across active services."""
    from apps.services.models import Service

    if not query_str or len(query_str.strip()) < 2:
        return Service.objects.none()

    query = SearchQuery(query_str, config='english')
    rank = SearchRank(SERVICE_VECTOR, query)

    return Service.objects.filter(is_active=True).annotate(
        rank=rank,
        search_headline=RawSQL(
            "ts_headline('english', name || ' ' || COALESCE(short_description, ''), "
            "plainto_tsquery('english', %s), 'StartSel=<mark>, StopSel=</mark>')",
            [query_str],
        ),
    ).filter(
        Q(rank__gt=0) | _build_simple_fallback(query_str)
    ).order_by('-rank')[:limit]


def search_news(query_str, limit=50):
    """Full-text search across news articles."""
    from apps.news.models import NewsArticle

    if not query_str or len(query_str.strip()) < 2:
        return NewsArticle.objects.none()

    query = SearchQuery(query_str, config='english')
    rank = SearchRank(NEWS_VECTOR, query)

    return NewsArticle.objects.annotate(rank=rank).filter(
        Q(rank__gt=0) | Q(title__icontains=query_str) | Q(summary__icontains=query_str)
    ).order_by('-rank', '-published_at')[:limit]


def search_all(query_str, limit=50):
    """Cross-model search returning a unified list of results."""
    results = []

    services = list(search_services(query_str, limit=20).values(
        'id', 'name', 'short_description', 'slug', 'rank'
    ))
    for s in services:
        s['_type'] = 'service'
        s['_title'] = s.pop('name')
        s['_description'] = s.pop('short_description')
        s['_url'] = f'/services/{s.pop("slug")}/'
        results.append(s)

    news = list(search_news(query_str, limit=20).select_related('source').values(
        'id', 'title', 'summary', 'url', 'published_at', 'rank', 'source__name'
    ))
    for n in news:
        n['_type'] = 'news'
        n['_title'] = n.pop('title')
        n['_description'] = n.pop('summary')
        n['_url'] = n.pop('url')
        n['source_name'] = n.pop('source__name')
        results.append(n)

    # Sort by rank descending
    results.sort(key=lambda r: r.get('rank', 0), reverse=True)
    return results[:limit]


def _build_simple_fallback(query_str):
    """Fallback to icontains for when tsquery returns no hits."""
    return (
        Q(name__icontains=query_str)
        | Q(short_description__icontains=query_str)
        | Q(description__icontains=query_str)
        | Q(category__name__icontains=query_str)
        | Q(ministry__name__icontains=query_str)
    )
