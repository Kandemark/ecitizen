from rest_framework import viewsets, permissions
from core.mixins import OwnerFilterMixin
from ..models import TenderNotice, Bid, Contract
from ..serializers import TenderNoticeSerializer, BidSerializer, ContractSerializer


class TenderNoticeViewSet(viewsets.ModelViewSet):
    serializer_class = TenderNoticeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = TenderNotice.objects.all()
        published = self.request.query_params.get('published')
        if published and published.lower() == 'true':
            qs = qs.filter(is_published=True)
        return qs


class BidViewSet(OwnerFilterMixin, viewsets.ModelViewSet):
    serializer_class = BidSerializer
    permission_classes = [permissions.IsAuthenticated]


class ContractViewSet(viewsets.ModelViewSet):
    serializer_class = ContractSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Contract.objects.all()
