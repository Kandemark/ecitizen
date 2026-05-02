from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import Q
from core.throttling import SearchRateThrottle
from ..models import SearchIndex, SearchQuery
from ..serializers import SearchIndexSerializer, SearchQuerySerializer
from ..services import search_all

SEARCH_VECTOR = SearchVector('title', weight='A') + SearchVector('description', weight='B')


class SearchIndexViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SearchIndex.objects.all()
    serializer_class = SearchIndexSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['last_indexed', 'title']


class SearchQueryViewSet(viewsets.ModelViewSet):
    serializer_class = SearchQuerySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']

    def get_queryset(self):
        return SearchQuery.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'], throttle_classes=[SearchRateThrottle])
    def search(self, request):
        query_str = request.data.get('query', '').strip()
        if not query_str or len(query_str) < 2:
            return Response({'results': [], 'count': 0})

        # Use PostgreSQL full-text search
        query = SearchQuery(query_str, config='english')
        rank = SearchRank(SEARCH_VECTOR, query)

        results = SearchIndex.objects.annotate(rank=rank).filter(
            Q(rank__gt=0) | Q(title__icontains=query_str) | Q(description__icontains=query_str)
        ).order_by('-rank')[:50]

        count = results.count()
        if request.user.is_authenticated:
            SearchQuery.objects.create(
                user=request.user,
                query=query_str,
                results_count=count,
            )

        results_data = []
        for r in results:
            results_data.append({
                'id': r.id,
                'title': r.title,
                'description': r.description,
                'content_type': r.content_type.model,
                'object_id': r.object_id,
                'last_indexed': r.last_indexed,
                'rank': round(r.rank, 4) if r.rank else 0,
            })

        return Response({'results': results_data, 'count': count})

    @action(detail=False, methods=['get'], throttle_classes=[SearchRateThrottle])
    def global_search(self, request):
        """Cross-model search across services, news, and indexed content."""
        query_str = request.GET.get('q', '').strip()
        if not query_str or len(query_str) < 2:
            return Response({'results': [], 'count': 0})

        results = search_all(query_str, limit=30)
        return Response({'results': results, 'count': len(results)})
