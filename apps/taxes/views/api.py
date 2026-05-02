from rest_framework import viewsets, permissions
from core.mixins import OwnerFilterMixin
from ..models import TaxReturn, TaxAssessment, ComplianceCertificate
from ..serializers import TaxReturnSerializer, TaxAssessmentSerializer, ComplianceCertificateSerializer


class TaxReturnViewSet(OwnerFilterMixin, viewsets.ModelViewSet):
    serializer_class = TaxReturnSerializer
    permission_classes = [permissions.IsAuthenticated]


class TaxAssessmentViewSet(OwnerFilterMixin, viewsets.ModelViewSet):
    serializer_class = TaxAssessmentSerializer
    permission_classes = [permissions.IsAuthenticated]


class ComplianceCertificateViewSet(OwnerFilterMixin, viewsets.ModelViewSet):
    serializer_class = ComplianceCertificateSerializer
    permission_classes = [permissions.IsAuthenticated]
