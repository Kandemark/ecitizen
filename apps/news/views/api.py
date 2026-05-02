from rest_framework import viewsets, permissions, filters
from ..models import NewsArticle, NewsSource
from ..serializers import NewsArticleSerializer, NewsSourceSerializer


class NewsSourceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NewsSource.objects.filter(is_active=True)
    serializer_class = NewsSourceSerializer
    permission_classes = [permissions.AllowAny]


class NewsArticleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NewsArticle.objects.select_related('source').order_by('-published_at')
    serializer_class = NewsArticleSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['published_at', 'title']
    search_fields = ['title', 'summary']
