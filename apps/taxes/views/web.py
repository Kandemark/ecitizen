from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..models import TaxReturn, TaxAssessment, ComplianceCertificate
from core.utils import generate_tracking_id


@login_required
def taxes_list(request):
    returns = TaxReturn.objects.filter(user=request.user).order_by('-created_at')
    assessments = TaxAssessment.objects.filter(user=request.user).order_by('-created_at')
    certificates = ComplianceCertificate.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'taxes/list.html', {
        'returns': returns, 'assessments': assessments, 'certificates': certificates,
    })


@login_required
def tax_return_file(request):
    if request.method == 'POST':
        t = TaxReturn(
            user=request.user,
            reference=generate_tracking_id('TAX'),
            tax_type=request.POST.get('tax_type', 'income_tax'),
            tax_period=request.POST.get('tax_period', ''),
            period_start=request.POST.get('period_start') or None,
            period_end=request.POST.get('period_end') or None,
            amount=request.POST.get('amount', 0),
            kra_pin=request.POST.get('kra_pin', ''),
            status='submitted',
        )
        t.save()
        from apps.applications.helpers import create_workflow_application
        create_workflow_application(t, request.user)
        messages.success(request, f'Tax return {t.reference} filed.')
        return redirect('taxes_detail', app_type='return', ref=t.reference)

    return render(request, 'taxes/return_apply.html', {
        'tax_types': TaxReturn._meta.get_field('tax_type').choices,
    })


@login_required
def assessment_request(request):
    if request.method == 'POST':
        a = TaxAssessment(
            user=request.user,
            reference=generate_tracking_id('ASMT'),
            assessment_year=request.POST.get('assessment_year', 2026),
            tax_type=request.POST.get('tax_type', 'income_tax'),
            total_income=request.POST.get('total_income', 0),
            kra_pin=request.POST.get('kra_pin', ''),
            status='submitted',
        )
        a.save()
        from apps.applications.helpers import create_workflow_application
        create_workflow_application(a, request.user)
        messages.success(request, f'Tax assessment {a.reference} submitted.')
        return redirect('taxes_detail', app_type='assessment', ref=a.reference)

    return render(request, 'taxes/assessment_apply.html', {
        'tax_types': TaxAssessment._meta.get_field('tax_type').choices,
    })


@login_required
def compliance_apply(request):
    if request.method == 'POST':
        c = ComplianceCertificate(
            user=request.user,
            reference=generate_tracking_id('CERT'),
            certificate_type=request.POST.get('certificate_type', 'Tax Compliance Certificate'),
            kra_pin=request.POST.get('kra_pin', ''),
            status='submitted',
        )
        c.save()
        from apps.applications.helpers import create_workflow_application
        create_workflow_application(c, request.user)
        messages.success(request, f'Compliance certificate request {c.reference} submitted.')
        return redirect('taxes_detail', app_type='compliance', ref=c.reference)

    return render(request, 'taxes/compliance_apply.html')


@login_required
def taxes_detail(request, app_type, ref):
    models_map = {
        'return': (TaxReturn, 'Tax Return'),
        'assessment': (TaxAssessment, 'Tax Assessment'),
        'compliance': (ComplianceCertificate, 'Compliance Certificate'),
    }
    info = models_map.get(app_type)
    if not info:
        messages.error(request, 'Invalid record type.')
        return redirect('taxes_list')

    model, title = info
    instance = get_object_or_404(model, user=request.user, reference=ref)
    return render(request, 'taxes/detail.html', {
        'record': instance, 'app_type': app_type, 'title': title,
    })
