from rest_framework import viewsets, permissions
from core.mixins import OwnerFilterMixin
from ..models import PassportApplication, VisaApplication, WorkPermit
from ..serializers import PassportApplicationSerializer, VisaApplicationSerializer, WorkPermitSerializer


class PassportApplicationViewSet(OwnerFilterMixin, viewsets.ModelViewSet):
    serializer_class = PassportApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]


class VisaApplicationViewSet(OwnerFilterMixin, viewsets.ModelViewSet):
    serializer_class = VisaApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]


class WorkPermitViewSet(OwnerFilterMixin, viewsets.ModelViewSet):
    serializer_class = WorkPermitSerializer
    permission_classes = [permissions.IsAuthenticated]
