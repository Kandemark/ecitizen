from rest_framework import viewsets, permissions, filters
from ..models import AuditEntry, ComplianceCheck, DataAccessLog
from ..serializers import AuditEntrySerializer, ComplianceCheckSerializer, DataAccessLogSerializer


class AuditEntryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditEntry.objects.all()
    serializer_class = AuditEntrySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['action', 'user__username']
    ordering_fields = ['timestamp']


class ComplianceCheckViewSet(viewsets.ModelViewSet):
    queryset = ComplianceCheck.objects.all()
    serializer_class = ComplianceCheckSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'last_checked', 'is_passing']


class DataAccessLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DataAccessLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['data_type', 'access_reason', 'user__username']
    ordering_fields = ['accessed_at']

    def get_queryset(self):
        return DataAccessLog.objects.filter(user=self.request.user)
