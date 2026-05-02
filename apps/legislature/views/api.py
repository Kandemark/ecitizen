from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import Bill, Hansard, CommitteeReport, ParliamentarySitting
from .serializers import (
    BillSerializer, BillListSerializer,
    HansardSerializer, HansardListSerializer,
    CommitteeReportSerializer, CommitteeReportListSerializer,
    ParliamentarySittingSerializer,
)


class BillViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bill.objects.order_by('-date_introduced')
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'number', 'sponsor', 'summary']
    ordering_fields = ['date_introduced', 'date_passed', 'last_updated']

    def get_serializer_class(self):
        if self.action == 'list':
            return BillListSerializer
        return BillSerializer

    @action(detail=False)
    def active(self, request):
        active = Bill.objects.exclude(
            status__in=['assented', 'rejected', 'withdrawn']
        ).order_by('-date_introduced')[:20]
        serializer = BillListSerializer(active, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def recently_passed(self, request):
        passed = Bill.objects.filter(
            status__in=['passed', 'assented']
        ).order_by('-date_passed')[:20]
        serializer = BillListSerializer(passed, many=True)
        return Response(serializer.data)


class HansardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Hansard.objects.order_by('-date')
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['date']

    def get_serializer_class(self):
        if self.action == 'list':
            return HansardListSerializer
        return HansardSerializer


class CommitteeReportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CommitteeReport.objects.order_by('-date_published')
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'committee_name', 'summary']
    ordering_fields = ['date_published']

    def get_serializer_class(self):
        if self.action == 'list':
            return CommitteeReportListSerializer
        return CommitteeReportSerializer


class ParliamentarySittingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ParliamentarySitting.objects.order_by('-date')
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['session', 'agenda']
    ordering_fields = ['date']
    serializer_class = ParliamentarySittingSerializer
