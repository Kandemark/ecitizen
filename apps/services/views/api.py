from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.db.models import Q, Count
from core.throttling import SearchRateThrottle
from ..models import Service, ServiceCategory, EligibilityRule, RequiredDocument
from ..serializers import (
    ServiceListSerializer, ServiceDetailSerializer,
    ServiceCategorySerializer, EligibilityRuleSerializer,
    RequiredDocumentSerializer,
)
from ..filters import ServiceFilter


class ServiceCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ServiceCategory.objects.filter(is_active=True)
    serializer_class = ServiceCategorySerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False)
    def with_services(self, request):
        """Return categories annotated with active service counts."""
        categories = self.get_queryset().annotate(
            service_count=Count('services', filter=Q(services__is_active=True))
        ).filter(service_count__gt=0)
        data = []
        for cat in categories:
            d = self.get_serializer(cat).data
            d['service_count'] = cat.service_count
            data.append(d)
        return Response(data)


class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Service.objects.filter(is_active=True).select_related(
        'category', 'ministry'
    ).prefetch_related('counties', 'eligibility_rules', 'required_documents')
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ServiceFilter
    ordering_fields = ['name', 'fee_kes', 'order', '-is_popular', 'processing_time']
    ordering = ['order', 'name']
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ServiceDetailSerializer
        return ServiceListSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action == 'retrieve':
            qs = qs.prefetch_related(
                'eligibility_rules', 'required_documents',
                'counties', 'category',
            )
        return qs

    @action(detail=False)
    def popular(self, request):
        """Return top popular services, limit 20."""
        qs = self.get_queryset().filter(is_popular=True)[:20]
        page = self.paginate_queryset(qs)
        if page is not None:
            return self.get_paginated_response(
                ServiceListSerializer(page, many=True).data
            )
        return Response(ServiceListSerializer(qs, many=True).data)

    @action(detail=False)
    def recommended(self, request):
        """Return services recommended for a given county."""
        county_code = request.query_params.get('county')
        qs = self.get_queryset()
        if county_code:
            qs = qs.filter(counties__code=county_code)
            if not qs.exists():
                qs = self.get_queryset().filter(is_popular=True)
        else:
            qs = qs.filter(is_popular=True)
        qs = qs[:12]
        page = self.paginate_queryset(qs)
        if page is not None:
            return self.get_paginated_response(
                ServiceListSerializer(page, many=True).data
            )
        return Response(ServiceListSerializer(qs, many=True).data)

    @action(detail=False, throttle_classes=[SearchRateThrottle])
    def search(self, request):
        """Full-text search across services by name, description, ministry, category."""
        query = request.query_params.get('q', '').strip()
        if not query:
            return Response([])
        qs = self.get_queryset().filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(short_description__icontains=query)
            | Q(category__name__icontains=query)
            | Q(ministry__name__icontains=query)
        ).distinct()[:50]
        page = self.paginate_queryset(qs)
        if page is not None:
            return self.get_paginated_response(
                ServiceListSerializer(page, many=True).data
            )
        return Response(ServiceListSerializer(qs, many=True).data)


class EligibilityRuleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EligibilityRule.objects.all()
    serializer_class = EligibilityRuleSerializer
    permission_classes = [permissions.AllowAny]


class RequiredDocumentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RequiredDocument.objects.all()
    serializer_class = RequiredDocumentSerializer
    permission_classes = [permissions.AllowAny]
