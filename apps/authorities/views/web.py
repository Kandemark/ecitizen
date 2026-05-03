from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone

from apps.applications.models import Application, StatusHistory
from apps.workflow.models import ReviewAssignment, ApprovalStep
from apps.services.models import Service, ConstitutionalFunction


@staff_member_required(login_url='login')
def staff_dashboard(request):
    """Government staff dashboard — workload overview and quick actions."""
    pending_assignments = ReviewAssignment.objects.filter(
        assigned_to=request.user,
        is_completed=False,
    ).select_related('application', 'application__service', 'step')
    pending_count = pending_assignments.count()

    recent_applications = Application.objects.filter(
        status__in=['submitted', 'in_review', 'pending_documents']
    ).select_related('user', 'service').order_by('-submitted_at')[:20]

    total_pending = Application.objects.filter(
        status__in=['submitted', 'in_review']
    ).count()

    # Stats by status
    status_counts = Application.objects.values('status').annotate(
        count=Count('id')
    ).order_by('status')

    # County-mandated services — DB-backed with service counts
    county_mandates = ConstitutionalFunction.objects.filter(
        is_active=True
    ).prefetch_related('services').order_by('order')

    return render(request, 'authorities/dashboard.html', {
        'pending_assignments': pending_assignments,
        'pending_count': pending_count,
        'recent_applications': recent_applications,
        'total_pending': total_pending,
        'status_counts': status_counts,
        'county_mandates': county_mandates,
    })


@staff_member_required(login_url='login')
def review_queue(request):
    """Queue of applications awaiting review by this staff member."""
    status_filter = request.GET.get('status', '')
    service_filter = request.GET.get('service', '')

    assignments = ReviewAssignment.objects.filter(
        assigned_to=request.user,
    ).select_related('application', 'application__user', 'application__service', 'step')

    if status_filter == 'pending':
        assignments = assignments.filter(is_completed=False)
    elif status_filter == 'completed':
        assignments = assignments.filter(is_completed=True)

    if service_filter:
        assignments = assignments.filter(application__service_id=service_filter)

    assignments = assignments.order_by('-application__submitted_at')

    services = Service.objects.filter(is_active=True)

    return render(request, 'authorities/review_queue.html', {
        'assignments': assignments,
        'current_status': status_filter,
        'current_service': service_filter,
        'services': services,
    })


@staff_member_required(login_url='login')
def review_application(request, application_id):
    """Review a single application — view details, make decision."""
    application = get_object_or_404(
        Application.objects.select_related('user', 'service'),
        id=application_id,
    )

    # Get or create review assignment for this staff member
    assignment = ReviewAssignment.objects.filter(
        application=application,
        assigned_to=request.user,
        is_completed=False,
    ).first()

    if request.method == 'POST':
        decision = request.POST.get('decision', '')
        comment = request.POST.get('comment', '')

        if decision == 'approved':
            application.status = 'approved'
            application.completed_at = timezone.now()
            application.save()
            if assignment:
                assignment.decision = 'approved'
                assignment.comment = comment
                assignment.is_completed = True
                assignment.completed_at = timezone.now()
                assignment.save()
            messages.success(request, f'Application {application.reference} approved.')
        elif decision == 'rejected':
            application.status = 'rejected'
            application.save()
            if assignment:
                assignment.decision = 'rejected'
                assignment.comment = comment
                assignment.is_completed = True
                assignment.completed_at = timezone.now()
                assignment.save()
            messages.success(request, f'Application {application.reference} rejected.')
        elif decision == 'revision':
            application.status = 'pending_documents'
            application.save()
            if assignment:
                assignment.decision = 'revision'
                assignment.comment = comment
                assignment.is_completed = True
                assignment.completed_at = timezone.now()
                assignment.save()
            messages.success(request, f'Revision requested for {application.reference}.')

        # Record in status history
        StatusHistory.objects.create(
            application=application,
            status=application.status,
            comment=comment,
            changed_by=request.user,
        )

        return redirect('authorities:review_queue')

    history = application.status_history.select_related('changed_by').order_by('-created_at')
    service_docs = application.service.required_documents.all() if application.service else []

    return render(request, 'authorities/review_application.html', {
        'application': application,
        'assignment': assignment,
        'history': history,
        'service_docs': service_docs,
    })


@staff_member_required(login_url='login')
def all_applications(request):
    """Browse all applications across all services — admin view."""
    status_filter = request.GET.get('status', '')
    service_filter = request.GET.get('service', '')
    q = request.GET.get('q', '')

    apps = Application.objects.select_related('user', 'service').order_by('-submitted_at')

    if status_filter:
        apps = apps.filter(status=status_filter)
    if service_filter:
        apps = apps.filter(service_id=service_filter)
    if q:
        apps = apps.filter(
            Q(reference__icontains=q) |
            Q(user__username__icontains=q) |
            Q(service__name__icontains=q)
        )

    services = Service.objects.filter(is_active=True)

    return render(request, 'authorities/all_applications.html', {
        'applications': apps[:100],
        'current_status': status_filter,
        'current_service': service_filter,
        'query': q,
        'services': services,
        'status_choices': Application._meta.get_field('status').choices,
    })
