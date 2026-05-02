from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..models import CourtCase, Filing, Fine
from core.utils import generate_tracking_id


@login_required
def judiciary_list(request):
    cases = CourtCase.objects.filter(user=request.user).order_by('-created_at')
    fines = Fine.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'judiciary/list.html', {'cases': cases, 'fines': fines})


@login_required
def case_file(request):
    if request.method == 'POST':
        c = CourtCase(
            user=request.user,
            reference=generate_tracking_id('CASE'),
            case_number=request.POST.get('case_number', ''),
            court_name=request.POST.get('court_name', ''),
            case_type=request.POST.get('case_type', 'civil'),
            title=request.POST.get('title', ''),
            description=request.POST.get('description', ''),
            status='submitted',
        )
        c.save()
        from apps.applications.helpers import create_workflow_application
        create_workflow_application(c, request.user)
        messages.success(request, f'Court case {c.reference} filed.')
        return redirect('judiciary_detail', app_type='case', ref=c.reference)

    return render(request, 'judiciary/case_apply.html', {
        'case_types': CourtCase._meta.get_field('case_type').choices,
    })


@login_required
def filing_submit(request, case_ref=None):
    court_case = None
    if case_ref:
        court_case = get_object_or_404(CourtCase, user=request.user, reference=case_ref)

    if request.method == 'POST':
        case_id = request.POST.get('case')
        if case_id:
            court_case = get_object_or_404(CourtCase, id=case_id, user=request.user)

        f = Filing(
            user=request.user,
            reference=generate_tracking_id('FILE'),
            case=court_case,
            filing_type=request.POST.get('filing_type', 'plaint'),
            title=request.POST.get('title', ''),
            description=request.POST.get('description', ''),
            status='submitted',
        )
        f.save()
        from apps.applications.helpers import create_workflow_application
        create_workflow_application(f, request.user)
        messages.success(request, f'Filing {f.reference} submitted.')
        return redirect('judiciary_detail', app_type='filing', ref=f.reference)

    cases = CourtCase.objects.filter(user=request.user)
    return render(request, 'judiciary/filing_apply.html', {
        'cases': cases,
        'filing_types': Filing._meta.get_field('filing_type').choices,
        'pre_selected_case': court_case,
    })


@login_required
def fine_pay(request):
    if request.method == 'POST':
        fine = Fine(
            user=request.user,
            reference=generate_tracking_id('FINE'),
            offense=request.POST.get('offense', ''),
            amount=request.POST.get('amount', 0),
            due_date=request.POST.get('due_date') or None,
            status='submitted',
        )
        fine.save()
        from apps.applications.helpers import create_workflow_application
        create_workflow_application(fine, request.user)
        messages.success(request, f'Fine {fine.reference} registered for payment.')
        return redirect('judiciary_detail', app_type='fine', ref=fine.reference)

    return render(request, 'judiciary/fine_apply.html')


@login_required
def judiciary_detail(request, app_type, ref):
    models_map = {
        'case': (CourtCase, 'Court Case'),
        'filing': (Filing, 'Filing'),
        'fine': (Fine, 'Fine'),
    }
    info = models_map.get(app_type)
    if not info:
        messages.error(request, 'Invalid record type.')
        return redirect('judiciary_list')

    model, title = info
    instance = get_object_or_404(model, user=request.user, reference=ref)
    return render(request, 'judiciary/detail.html', {
        'record': instance, 'app_type': app_type, 'title': title,
    })
