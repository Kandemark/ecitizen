from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db import transaction

from apps.services.models import Service
from ..models import Application, ApplicationDocument
from core.utils import generate_tracking_id


@login_required
def apply_service(request, slug):
    service = get_object_or_404(
        Service.objects.filter(is_active=True).prefetch_related(
            'required_documents', 'eligibility_rules', 'counties'
        ),
        slug=slug,
    )

    # Check for existing draft
    existing = Application.objects.filter(
        user=request.user, service=service, status='draft'
    ).first()

    if request.method == 'POST':
        application = existing or Application(
            user=request.user,
            service=service,
            reference=generate_tracking_id('APP'),
        )

        # Handle optional county selection
        county_id = request.POST.get('county')
        if county_id:
            try:
                from apps.counties.models import County
                application.county = County.objects.get(id=county_id)
            except Exception:
                pass

        application.status = 'submitted'
        application.submitted_at = timezone.now()
        application.save()

        # Handle uploaded documents
        for doc_req in service.required_documents.filter(is_mandatory=True):
            file_key = f'doc_{doc_req.id}'
            if file_key in request.FILES:
                uploaded = request.FILES[file_key]
                ApplicationDocument.objects.create(
                    application=application,
                    document_type=doc_req,
                    file=uploaded,
                    original_filename=uploaded.name,
                )

        messages.success(request, f'Application {application.reference} submitted successfully.')
        return redirect('application_detail', ref=application.reference)

    return render(request, 'applications/apply.html', {
        'service': service,
        'existing_draft': existing,
    })


@login_required
def application_detail(request, ref):
    application = get_object_or_404(
        Application.objects.filter(user=request.user)
        .select_related('service', 'county')
        .prefetch_related('documents', 'status_history'),
        reference=ref,
    )
    return render(request, 'applications/detail.html', {
        'application': application,
    })
