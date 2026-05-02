from rest_framework import viewsets, permissions
from ..models import Ministry, Department, Division
from ..serializers import MinistrySerializer, DepartmentSerializer, DivisionSerializer


class MinistryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ministry.objects.filter(is_active=True)
    serializer_class = MinistrySerializer
    permission_classes = [permissions.AllowAny]


class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Department.objects.filter(is_active=True)
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.AllowAny]


class DivisionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer
    permission_classes = [permissions.AllowAny]
