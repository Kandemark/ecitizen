from rest_framework import viewsets, permissions, filters
from ..models import ExternalSystem, DataExchange, SyncLog
from ..serializers import ExternalSystemSerializer, DataExchangeSerializer, SyncLogSerializer


class ExternalSystemViewSet(viewsets.ModelViewSet):
    queryset = ExternalSystem.objects.all()
    serializer_class = ExternalSystemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'is_active']


class DataExchangeViewSet(viewsets.ModelViewSet):
    queryset = DataExchange.objects.all()
    serializer_class = DataExchangeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'status']


class SyncLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SyncLog.objects.all()
    serializer_class = SyncLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['started_at', 'status']
