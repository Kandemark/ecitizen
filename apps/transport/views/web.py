from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..models import DrivingLicense, VehicleRegistration, PSVLicense, VehicleInspection
from core.utils import generate_tracking_id


@login_required
def transport_list(request):
    licenses = DrivingLicense.objects.filter(user=request.user).order_by('-created_at')
    vehicles = VehicleRegistration.objects.filter(user=request.user).order_by('-created_at')
    psv = PSVLicense.objects.filter(user=request.user).select_related('vehicle').order_by('-created_at')
    inspections = VehicleInspection.objects.filter(user=request.user).select_related('vehicle').order_by('-created_at')
    return render(request, 'transport/list.html', {
        'licenses': licenses,
        'vehicles': vehicles,
        'psv_licenses': psv,
        'inspections': inspections,
    })


@login_required
def driving_license_apply(request):
    if request.method == 'POST':
        dl = DrivingLicense(
            user=request.user,
            reference=generate_tracking_id('DL'),
            license_class=request.POST.get('license_class', 'B'),
            blood_group=request.POST.get('blood_group', ''),
            status='submitted',
        )
        dl.save()
        from apps.applications.helpers import create_workflow_application
        create_workflow_application(dl, request.user)
        messages.success(request, f'Driving license application {dl.reference} submitted.')
        return redirect('transport_detail', app_type='license', ref=dl.reference)

    return render(request, 'transport/license_apply.html', {
        'classes': DrivingLicense._meta.get_field('license_class').choices,
    })


@login_required
def vehicle_register(request):
    if request.method == 'POST':
        v = VehicleRegistration(
            user=request.user,
            reference=generate_tracking_id('VREG'),
            plate_number=request.POST.get('plate_number', ''),
            vehicle_make=request.POST.get('vehicle_make', ''),
            vehicle_model=request.POST.get('vehicle_model', ''),
            year_of_manufacture=request.POST.get('year_of_manufacture') or None,
            color=request.POST.get('color', ''),
            vin=request.POST.get('vin', ''),
            engine_number=request.POST.get('engine_number', ''),
            status='submitted',
        )
        v.save()
        from apps.applications.helpers import create_workflow_application
        create_workflow_application(v, request.user)
        messages.success(request, f'Vehicle registration {v.reference} submitted.')
        return redirect('transport_detail', app_type='vehicle', ref=v.reference)

    return render(request, 'transport/vehicle_apply.html')


@login_required
def psv_license_apply(request):
    if request.method == 'POST':
        vehicle_id = request.POST.get('vehicle')
        vehicle = None
        if vehicle_id:
            vehicle = get_object_or_404(VehicleRegistration, id=vehicle_id, user=request.user)

        p = PSVLicense(
            user=request.user,
            reference=generate_tracking_id('PSV'),
            vehicle=vehicle,
            route=request.POST.get('route', ''),
            operator_name=request.POST.get('operator_name', ''),
            sacco_name=request.POST.get('sacco_name', ''),
            capacity=request.POST.get('capacity', 0),
            status='submitted',
        )
        p.save()
        from apps.applications.helpers import create_workflow_application
        create_workflow_application(p, request.user)
        messages.success(request, f'PSV license application {p.reference} submitted.')
        return redirect('transport_detail', app_type='psv', ref=p.reference)

    vehicles = VehicleRegistration.objects.filter(user=request.user, status='approved')
    return render(request, 'transport/psv_apply.html', {'vehicles': vehicles})


@login_required
def inspection_book(request):
    if request.method == 'POST':
        vehicle_id = request.POST.get('vehicle')
        vehicle = None
        if vehicle_id:
            vehicle = get_object_or_404(VehicleRegistration, id=vehicle_id, user=request.user)

        insp = VehicleInspection(
            user=request.user,
            reference=generate_tracking_id('INSP'),
            vehicle=vehicle,
            inspection_center=request.POST.get('inspection_center', ''),
            status='submitted',
        )
        insp.save()
        from apps.applications.helpers import create_workflow_application
        create_workflow_application(insp, request.user)
        messages.success(request, f'Inspection booking {insp.reference} submitted.')
        return redirect('transport_detail', app_type='inspection', ref=insp.reference)

    vehicles = VehicleRegistration.objects.filter(user=request.user)
    return render(request, 'transport/inspection_apply.html', {'vehicles': vehicles})


@login_required
def transport_detail(request, app_type, ref):
    models_map = {
        'license': (DrivingLicense, 'Driving License'),
        'vehicle': (VehicleRegistration, 'Vehicle Registration'),
        'psv': (PSVLicense, 'PSV License'),
        'inspection': (VehicleInspection, 'Vehicle Inspection'),
    }
    info = models_map.get(app_type)
    if not info:
        messages.error(request, 'Invalid record type.')
        return redirect('transport_list')

    model, title = info
    instance = get_object_or_404(model, user=request.user, reference=ref)
    return render(request, 'transport/detail.html', {
        'record': instance, 'app_type': app_type, 'title': title,
    })
