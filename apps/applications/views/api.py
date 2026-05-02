from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from core.mixins import OwnerFilterMixin
from ..models import Application, FormField, StatusHistory
from ..serializers import (
    ApplicationSerializer, FormFieldSerializer,
    StatusHistorySerializer,
)


class ApplicationViewSet(OwnerFilterMixin, viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        application = self.get_object()
        if application.status != 'draft':
            return Response({'detail': 'Only draft applications can be submitted.'}, status=400)
        application.status = 'submitted'
        from django.utils import timezone
        application.submitted_at = timezone.now()
        application.save()
        StatusHistory.objects.create(
            application=application, status='submitted',
            changed_by=request.user, comment='Application submitted.'
        )
        return Response({'status': 'submitted'})

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        application = self.get_object()
        application.status = 'cancelled'
        application.save()
        StatusHistory.objects.create(
            application=application, status='cancelled',
            changed_by=request.user, comment='Cancelled by applicant.'
        )
        return Response({'status': 'cancelled'})


class FormFieldViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FormFieldSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        service_slug = self.request.query_params.get('service')
        qs = FormField.objects.all()
        if service_slug:
            qs = qs.filter(service__slug=service_slug)
        return qs
