from rest_framework import viewsets, permissions
from core.mixins import OwnerFilterMixin
from ..models import BusinessLicense, ProfessionalCertification
from ..serializers import BusinessLicenseSerializer, ProfessionalCertificationSerializer


class BusinessLicenseViewSet(OwnerFilterMixin, viewsets.ModelViewSet):
    serializer_class = BusinessLicenseSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProfessionalCertificationViewSet(OwnerFilterMixin, viewsets.ModelViewSet):
    serializer_class = ProfessionalCertificationSerializer
    permission_classes = [permissions.IsAuthenticated]
