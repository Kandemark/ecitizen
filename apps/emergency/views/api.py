from rest_framework import viewsets, permissions, filters
from ..models import EmergencyContact, EmergencyReport
from ..serializers import EmergencyContactSerializer, EmergencyReportSerializer


class EmergencyContactViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EmergencyContact.objects.filter(is_active=True)
    serializer_class = EmergencyContactSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'phone']
    ordering_fields = ['service_type', 'name']


class EmergencyReportViewSet(viewsets.ModelViewSet):
    serializer_class = EmergencyReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['reported_at', 'status']

    def get_queryset(self):
        return EmergencyReport.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
