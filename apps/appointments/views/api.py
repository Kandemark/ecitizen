from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from core.mixins import OwnerFilterMixin
from ..models import OfficeLocation, TimeSlot, Appointment
from ..serializers import OfficeLocationSerializer, TimeSlotSerializer, AppointmentSerializer


class OfficeLocationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OfficeLocation.objects.filter(is_active=True)
    serializer_class = OfficeLocationSerializer
    permission_classes = [permissions.AllowAny]


class TimeSlotViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TimeSlotSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = TimeSlot.objects.filter(is_available=True, date__gte=timezone.now().date())
        office = self.request.query_params.get('office')
        if office:
            qs = qs.filter(office_id=office)
        return qs


class AppointmentViewSet(OwnerFilterMixin, viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        appointment = self.get_object()
        appointment.status = 'cancelled'
        appointment.save()
        slot = appointment.time_slot
        slot.current_bookings = max(0, slot.current_bookings - 1)
        slot.is_available = True
        slot.save()
        return Response({'status': 'cancelled'})
