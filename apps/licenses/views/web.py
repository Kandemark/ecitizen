from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..models import BusinessLicense, ProfessionalCertification
from core.utils import generate_tracking_id


@login_required
def licenses_list(request):
    business = BusinessLicense.objects.filter(user=request.user).order_by('-created_at')
    certifications = ProfessionalCertification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'licenses/list.html', {
        'business_licenses': business, 'certifications': certifications,
    })


@login_required
def business_license_apply(request):
    if request.method == 'POST':
        l = BusinessLicense(
            user=request.user,
            reference=generate_tracking_id('BL'),
            business_name=request.POST.get('business_name', ''),
            license_type=request.POST.get('license_type', 'single_business'),
            registration_number=request.POST.get('registration_number', ''),
            physical_address=request.POST.get('physical_address', ''),
            postal_address=request.POST.get('postal_address', ''),
            business_email=request.POST.get('business_email', ''),
            business_phone=request.POST.get('business_phone', ''),
            number_of_employees=request.POST.get('number_of_employees', 0),
            status='submitted',
        )
        county_id = request.POST.get('county')
        if county_id:
            try:
                from apps.counties.models import County
                l.county = County.objects.get(id=county_id)
            except Exception:
                pass
        l.save()
        from apps.applications.helpers import create_workflow_application
        create_workflow_application(l, request.user)
        messages.success(request, f'Business license application {l.reference} submitted.')
        return redirect('licenses_detail', app_type='business', ref=l.reference)

    from apps.counties.models import County
    return render(request, 'licenses/business_apply.html', {
        'license_types': BusinessLicense._meta.get_field('license_type').choices,
        'counties': County.objects.all(),
    })


@login_required
def professional_cert_apply(request):
    if request.method == 'POST':
        c = ProfessionalCertification(
            user=request.user,
            reference=generate_tracking_id('PROF'),
            certification_name=request.POST.get('certification_name', ''),
            certification_type=request.POST.get('certification_type', 'other'),
            issuing_body=request.POST.get('issuing_body', ''),
            registration_number=request.POST.get('registration_number', ''),
            status='submitted',
        )
        c.save()
        from apps.applications.helpers import create_workflow_application
        create_workflow_application(c, request.user)
        messages.success(request, f'Professional certification application {c.reference} submitted.')
        return redirect('licenses_detail', app_type='certification', ref=c.reference)

    return render(request, 'licenses/certification_apply.html', {
        'cert_types': ProfessionalCertification._meta.get_field('certification_type').choices,
    })


@login_required
def licenses_detail(request, app_type, ref):
    models_map = {
        'business': (BusinessLicense, 'Business License'),
        'certification': (ProfessionalCertification, 'Professional Certification'),
    }
    info = models_map.get(app_type)
    if not info:
        messages.error(request, 'Invalid record type.')
        return redirect('licenses_list')

    model, title = info
    instance = get_object_or_404(model, user=request.user, reference=ref)
    return render(request, 'licenses/detail.html', {
        'record': instance, 'app_type': app_type, 'title': title,
    })
