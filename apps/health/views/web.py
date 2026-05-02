from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..models import HealthRecord, NHIFRegistration, MedicalCertificate
from core.utils import generate_tracking_id


@login_required
def health_list(request):
    records = HealthRecord.objects.filter(user=request.user).order_by('-created_at')
    nhif = NHIFRegistration.objects.filter(user=request.user).order_by('-created_at')
    certificates = MedicalCertificate.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'health/list.html', {
        'records': records, 'nhif': nhif, 'certificates': certificates,
    })


@login_required
def health_record_apply(request):
    if request.method == 'POST':
        r = HealthRecord(
            user=request.user,
            reference=generate_tracking_id('HLTH'),
            facility_name=request.POST.get('facility_name', ''),
            record_type=request.POST.get('record_type', 'outpatient'),
            visit_date=request.POST.get('visit_date') or None,
            diagnosis=request.POST.get('diagnosis', ''),
            prescription=request.POST.get('prescription', ''),
            attending_practitioner=request.POST.get('attending_practitioner', ''),
            notes=request.POST.get('notes', ''),
            status='submitted',
        )
        r.save()
        from apps.applications.helpers import create_workflow_application
        create_workflow_application(r, request.user)
        messages.success(request, f'Health record {r.reference} submitted.')
        return redirect('health_detail', app_type='record', ref=r.reference)

    return render(request, 'health/record_apply.html', {
        'record_types': HealthRecord._meta.get_field('record_type').choices,
    })


@login_required
def nhif_register(request):
    if request.method == 'POST':
        n = NHIFRegistration(
            user=request.user,
            reference=generate_tracking_id('NHIF'),
            employer_name=request.POST.get('employer_name', ''),
            monthly_contribution=request.POST.get('monthly_contribution', 0),
            dependants=request.POST.get('dependants', 0),
            status='submitted',
        )
        n.save()
        from apps.applications.helpers import create_workflow_application
        create_workflow_application(n, request.user)
        messages.success(request, f'NHIF registration {n.reference} submitted.')
        return redirect('health_detail', app_type='nhif', ref=n.reference)

    return render(request, 'health/nhif_apply.html')


@login_required
def medical_cert_apply(request):
    if request.method == 'POST':
        c = MedicalCertificate(
            user=request.user,
            reference=generate_tracking_id('MED'),
            certificate_type=request.POST.get('certificate_type', 'medical_examination'),
            issuing_facility=request.POST.get('issuing_facility', ''),
            issuing_practitioner=request.POST.get('issuing_practitioner', ''),
            findings=request.POST.get('findings', ''),
            status='submitted',
        )
        c.save()
        from apps.applications.helpers import create_workflow_application
        create_workflow_application(c, request.user)
        messages.success(request, f'Medical certificate application {c.reference} submitted.')
        return redirect('health_detail', app_type='certificate', ref=c.reference)

    return render(request, 'health/cert_apply.html', {
        'cert_types': MedicalCertificate._meta.get_field('certificate_type').choices,
    })


@login_required
def health_detail(request, app_type, ref):
    models_map = {
        'record': (HealthRecord, 'Health Record'),
        'nhif': (NHIFRegistration, 'NHIF Registration'),
        'certificate': (MedicalCertificate, 'Medical Certificate'),
    }
    info = models_map.get(app_type)
    if not info:
        messages.error(request, 'Invalid record type.')
        return redirect('health_list')

    model, title = info
    instance = get_object_or_404(model, user=request.user, reference=ref)
    return render(request, 'health/detail.html', {
        'record': instance, 'app_type': app_type, 'title': title,
    })
