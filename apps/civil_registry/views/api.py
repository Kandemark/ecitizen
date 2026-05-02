from rest_framework import viewsets, permissions
from core.mixins import OwnerFilterMixin
from ..models import BirthCertificate, DeathCertificate, MarriageCertificate
from ..serializers import (
    BirthCertificateSerializer, DeathCertificateSerializer, MarriageCertificateSerializer,
)


class BirthCertificateViewSet(OwnerFilterMixin, viewsets.ModelViewSet):
    serializer_class = BirthCertificateSerializer
    permission_classes = [permissions.IsAuthenticated]


class DeathCertificateViewSet(OwnerFilterMixin, viewsets.ModelViewSet):
    serializer_class = DeathCertificateSerializer
    permission_classes = [permissions.IsAuthenticated]


class MarriageCertificateViewSet(OwnerFilterMixin, viewsets.ModelViewSet):
    serializer_class = MarriageCertificateSerializer
    permission_classes = [permissions.IsAuthenticated]
