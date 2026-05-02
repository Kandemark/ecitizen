from rest_framework import viewsets, permissions
from core.mixins import OwnerFilterMixin
from ..models import PollingStation, VoterRecord, Candidate
from ..serializers import PollingStationSerializer, VoterRecordSerializer, CandidateSerializer


class PollingStationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PollingStationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PollingStation.objects.filter(is_active=True)


class VoterRecordViewSet(OwnerFilterMixin, viewsets.ModelViewSet):
    serializer_class = VoterRecordSerializer
    permission_classes = [permissions.IsAuthenticated]


class CandidateViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CandidateSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Candidate.objects.all()
