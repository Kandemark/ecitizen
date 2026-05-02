from datetime import timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import F

from apps.services.models import Service
from ..models import Appointment, TimeSlot
from core.utils import generate_tracking_id


@login_required
def book_appointment(request):
    service_slug = request.GET.get('service', '')
    service = None
    if service_slug:
        try:
            service = Service.objects.get(slug=service_slug, is_active=True)
        except Service.DoesNotExist:
            pass

    # Show available time slots for next 30 days
    today = timezone.now().date()
    end_date = today + timedelta(days=30)
    available_slots = TimeSlot.objects.filter(
        date__gte=today,
        date__lte=end_date,
        is_available=True,
        current_bookings__lt=F('max_capacity'),
    ).select_related('office').order_by('date', 'start_time')

    if request.method == 'POST':
        slot_id = request.POST.get('time_slot')
        service_id = request.POST.get('service')
        notes = request.POST.get('notes', '')

        slot = get_object_or_404(TimeSlot, id=slot_id, is_available=True)
        svc = get_object_or_404(Service, id=service_id, is_active=True) if service_id else None

        appointment = Appointment.objects.create(
            user=request.user,
            time_slot=slot,
            service=svc,
            reference=generate_tracking_id('APT'),
            status='scheduled',
            notes=notes,
        )
        # Update slot capacity
        slot.current_bookings += 1
        if slot.current_bookings >= slot.max_capacity:
            slot.is_available = False
        slot.save()

        messages.success(request, f'Appointment {appointment.reference} booked.')
        return redirect('my_appointments')

    return render(request, 'appointments/book.html', {
        'service': service,
        'available_slots': available_slots,
        'services': Service.objects.filter(is_active=True),
    })


@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(
        user=request.user
    ).select_related('service', 'time_slot__office').order_by(
        '-time_slot__date', '-time_slot__start_time'
    )
    return render(request, 'appointments/my_list.html', {
        'appointments': appointments,
    })


@login_required
def cancel_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, user=request.user)
    if appointment.status in ('scheduled', 'confirmed'):
        appointment.status = 'cancelled'
        appointment.save()
        # Release slot
        slot = appointment.time_slot
        slot.current_bookings = max(0, slot.current_bookings - 1)
        slot.is_available = True
        slot.save()
        messages.success(request, 'Appointment cancelled.')
    return redirect('my_appointments')
