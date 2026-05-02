from rest_framework import viewsets, permissions
from core.mixins import OwnerFilterMixin
from ..models import TitleDeed, LandSearch, Transfer
from ..serializers import TitleDeedSerializer, LandSearchSerializer, TransferSerializer


class TitleDeedViewSet(OwnerFilterMixin, viewsets.ModelViewSet):
    serializer_class = TitleDeedSerializer
    permission_classes = [permissions.IsAuthenticated]


class LandSearchViewSet(OwnerFilterMixin, viewsets.ModelViewSet):
    serializer_class = LandSearchSerializer
    permission_classes = [permissions.IsAuthenticated]


class TransferViewSet(OwnerFilterMixin, viewsets.ModelViewSet):
    serializer_class = TransferSerializer
    permission_classes = [permissions.IsAuthenticated]
