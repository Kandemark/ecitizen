from rest_framework import viewsets, permissions, filters
from ..models import DeveloperRegistration, SandboxEnvironment
from ..serializers import DeveloperRegistrationSerializer, SandboxEnvironmentSerializer


class DeveloperRegistrationViewSet(viewsets.ModelViewSet):
    serializer_class = DeveloperRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'status']

    def get_queryset(self):
        return DeveloperRegistration.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SandboxEnvironmentViewSet(viewsets.ModelViewSet):
    serializer_class = SandboxEnvironmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SandboxEnvironment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
