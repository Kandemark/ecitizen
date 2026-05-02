from rest_framework import viewsets, permissions, filters
from ..models import Dashboard, Widget, Metric
from ..serializers import (
    DashboardSerializer, DashboardListSerializer,
    WidgetSerializer, MetricSerializer,
)


class DashboardViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name', 'created_at']

    def get_queryset(self):
        return Dashboard.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return DashboardListSerializer
        return DashboardSerializer

    def perform_create(self, serializer):
        if serializer.validated_data.get('is_default', False):
            Dashboard.objects.filter(
                user=self.request.user, is_default=True
            ).update(is_default=False)
        serializer.save(user=self.request.user)


class WidgetViewSet(viewsets.ModelViewSet):
    serializer_class = WidgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Widget.objects.filter(dashboard__user=self.request.user)


class MetricViewSet(viewsets.ModelViewSet):
    queryset = Metric.objects.all()
    serializer_class = MetricSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'source']
    ordering_fields = ['name', 'value']
