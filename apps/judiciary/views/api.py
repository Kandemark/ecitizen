from rest_framework import viewsets, permissions
from core.mixins import OwnerFilterMixin
from ..models import CourtCase, Filing, HearingSchedule, Fine
from ..serializers import CourtCaseSerializer, FilingSerializer, HearingScheduleSerializer, FineSerializer


class CourtCaseViewSet(OwnerFilterMixin, viewsets.ModelViewSet):
    serializer_class = CourtCaseSerializer
    permission_classes = [permissions.IsAuthenticated]


class FilingViewSet(OwnerFilterMixin, viewsets.ModelViewSet):
    serializer_class = FilingSerializer
    permission_classes = [permissions.IsAuthenticated]


class HearingScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = HearingScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return HearingSchedule.objects.filter(
            case__user=self.request.user
        )


class FineViewSet(OwnerFilterMixin, viewsets.ModelViewSet):
    serializer_class = FineSerializer
    permission_classes = [permissions.IsAuthenticated]
