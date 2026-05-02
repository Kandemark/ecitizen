from rest_framework import viewsets, permissions
from core.mixins import OwnerFilterMixin
from ..models import HealthRecord, NHIFRegistration, MedicalCertificate
from ..serializers import HealthRecordSerializer, NHIFRegistrationSerializer, MedicalCertificateSerializer


class HealthRecordViewSet(OwnerFilterMixin, viewsets.ModelViewSet):
    serializer_class = HealthRecordSerializer
    permission_classes = [permissions.IsAuthenticated]


class NHIFRegistrationViewSet(OwnerFilterMixin, viewsets.ModelViewSet):
    serializer_class = NHIFRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]


class MedicalCertificateViewSet(OwnerFilterMixin, viewsets.ModelViewSet):
    serializer_class = MedicalCertificateSerializer
    permission_classes = [permissions.IsAuthenticated]
