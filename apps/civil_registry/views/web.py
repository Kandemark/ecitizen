from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from ..models import BirthCertificate, DeathCertificate, MarriageCertificate
from core.utils import generate_tracking_id


CERTIFICATE_TYPES = {
    'birth': {
        'model': BirthCertificate,
        'title': 'Birth Certificate',
        'icon': 'baby',
        'description': 'Apply for a birth certificate for a child born in Kenya.',
        'fields': ['child_name', 'date_of_birth', 'place_of_birth', 'gender',
                   'father_name', 'mother_name', 'county_of_birth'],
    },
    'death': {
        'model': DeathCertificate,
        'title': 'Death Certificate',
        'icon': 'book',
        'description': 'Apply for a death certificate for a deceased person.',
        'fields': ['deceased_name', 'date_of_death', 'place_of_death', 'cause_of_death',
                   'gender', 'age_at_death', 'next_of_kin', 'informant_name'],
    },
    'marriage': {
        'model': MarriageCertificate,
        'title': 'Marriage Certificate',
        'icon': 'heart',
        'description': 'Apply for a marriage certificate.',
        'fields': ['spouse1_name', 'spouse2_name', 'marriage_date', 'marriage_place',
                   'marriage_type', 'officiant_name'],
    },
}


@login_required
def certificate_list(request):
    birth = BirthCertificate.objects.filter(user=request.user).order_by('-created_at')
    death = DeathCertificate.objects.filter(user=request.user).order_by('-created_at')
    marriage = MarriageCertificate.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'civil_registry/list.html', {
        'birth_certificates': birth,
        'death_certificates': death,
        'marriage_certificates': marriage,
    })


@login_required
def certificate_apply(request, cert_type):
    config = CERTIFICATE_TYPES.get(cert_type)
    if not config:
        messages.error(request, 'Invalid certificate type.')
        return redirect('civil_registry_list')

    model = config['model']

    if request.method == 'POST':
        instance = model(user=request.user, reference=generate_tracking_id('CERT'))

        for field in config['fields']:
            value = request.POST.get(field, '')
            if field == 'date_of_birth' and value:
                instance.date_of_birth = value
            elif field == 'date_of_death' and value:
                instance.date_of_death = value
            elif field == 'marriage_date' and value:
                instance.marriage_date = value
            elif field == 'age_at_death' and value:
                try:
                    instance.age_at_death = int(value)
                except ValueError:
                    pass
            elif field == 'county_of_birth' and value:
                instance.county_of_birth = value
            elif hasattr(instance, field):
                setattr(instance, field, value)

        instance.status = 'submitted'
        instance.save()
        from apps.applications.helpers import create_workflow_application
        create_workflow_application(instance, request.user)
        messages.success(request, f'{config["title"]} application {instance.reference} submitted successfully.')
        return redirect('civil_registry_detail', cert_type=cert_type, ref=instance.reference)

    return render(request, 'civil_registry/apply.html', {
        'config': config,
        'cert_type': cert_type,
    })


@login_required
def certificate_detail(request, cert_type, ref):
    config = CERTIFICATE_TYPES.get(cert_type)
    if not config:
        messages.error(request, 'Invalid certificate type.')
        return redirect('civil_registry_list')

    instance = get_object_or_404(config['model'], user=request.user, reference=ref)
    return render(request, 'civil_registry/detail.html', {
        'certificate': instance,
        'config': config,
        'cert_type': cert_type,
    })
