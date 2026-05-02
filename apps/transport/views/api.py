from rest_framework import viewsets, permissions
from core.mixins import OwnerFilterMixin
from ..models import DrivingLicense, VehicleRegistration, PSVLicense, VehicleInspection
from ..serializers import (
    DrivingLicenseSerializer, VehicleRegistrationSerializer,
    PSVLicenseSerializer, VehicleInspectionSerializer,
)


class DrivingLicenseViewSet(OwnerFilterMixin, viewsets.ModelViewSet):
    serializer_class = DrivingLicenseSerializer
    permission_classes = [permissions.IsAuthenticated]


class VehicleRegistrationViewSet(OwnerFilterMixin, viewsets.ModelViewSet):
    serializer_class = VehicleRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]


class PSVLicenseViewSet(OwnerFilterMixin, viewsets.ModelViewSet):
    serializer_class = PSVLicenseSerializer
    permission_classes = [permissions.IsAuthenticated]


class VehicleInspectionViewSet(OwnerFilterMixin, viewsets.ModelViewSet):
    serializer_class = VehicleInspectionSerializer
    permission_classes = [permissions.IsAuthenticated]
