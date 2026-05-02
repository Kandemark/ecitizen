from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..models import PassportApplication, VisaApplication, WorkPermit
from core.utils import generate_tracking_id


@login_required
def application_list(request):
    passports = PassportApplication.objects.filter(user=request.user).order_by('-created_at')
    visas = VisaApplication.objects.filter(user=request.user).order_by('-created_at')
    permits = WorkPermit.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'immigration/list.html', {
        'passports': passports,
        'visas': visas,
        'permits': permits,
    })


@login_required
def passport_apply(request):
    if request.method == 'POST':
        app = PassportApplication(
            user=request.user,
            reference=generate_tracking_id('PPT'),
            passport_type=request.POST.get('passport_type', 'ordinary'),
            status='submitted',
        )
        app.save()
        from apps.applications.helpers import create_workflow_application
        create_workflow_application(app, request.user)
        messages.success(request, f'Passport application {app.reference} submitted.')
        return redirect('immigration_detail', app_type='passport', ref=app.reference)

    return render(request, 'immigration/passport_apply.html', {
        'types': [
            ('ordinary', 'Ordinary (32 pages)'),
            ('diplomatic', 'Diplomatic'),
            ('east_african', 'East African Passport'),
            ('interim', 'Interim Certificate'),
        ],
    })


@login_required
def visa_apply(request):
    if request.method == 'POST':
        app = VisaApplication(
            user=request.user,
            reference=generate_tracking_id('VISA'),
            visa_type=request.POST.get('visa_type', 'single_entry'),
            status='submitted',
        )
        app.save()
        from apps.applications.helpers import create_workflow_application
        create_workflow_application(app, request.user)
        messages.success(request, f'Visa application {app.reference} submitted.')
        return redirect('immigration_detail', app_type='visa', ref=app.reference)

    return render(request, 'immigration/visa_apply.html', {
        'types': [
            ('single_entry', 'Single Entry'),
            ('multiple_entry', 'Multiple Entry'),
            ('transit', 'Transit Visa'),
            ('east_africa_tourist', 'East Africa Tourist Visa'),
            ('courtesy', 'Courtesy Visa'),
        ],
    })


@login_required
def work_permit_apply(request):
    if request.method == 'POST':
        app = WorkPermit(
            user=request.user,
            reference=generate_tracking_id('PERM'),
            permit_class=request.POST.get('permit_class', 'B'),
            employer=request.POST.get('employer', ''),
            status='submitted',
        )
        app.save()
        from apps.applications.helpers import create_workflow_application
        create_workflow_application(app, request.user)
        messages.success(request, f'Work permit application {app.reference} submitted.')
        return redirect('immigration_detail', app_type='permit', ref=app.reference)

    return render(request, 'immigration/permit_apply.html', {
        'classes': [
            ('A', 'Class A — Prospecting / Mining'),
            ('B', 'Class B — Agriculture / Animal Husbandry'),
            ('C', 'Class C — Prescribed Profession'),
            ('D', 'Class D — Employment'),
            ('F', 'Class F — Specific Manufacturing'),
            ('G', 'Class G — Trade / Business / Consultancy'),
            ('I', 'Class I — Approved Religious / Charitable'),
            ('K', 'Class K — Retired / Annuitant'),
            ('M', 'Class M — Refugee'),
        ],
    })


@login_required
def application_detail(request, app_type, ref):
    models_map = {
        'passport': (PassportApplication, 'Passport Application'),
        'visa': (VisaApplication, 'Visa Application'),
        'permit': (WorkPermit, 'Work Permit'),
    }
    model_info = models_map.get(app_type)
    if not model_info:
        messages.error(request, 'Invalid application type.')
        return redirect('immigration_list')

    model, title = model_info
    instance = get_object_or_404(model, user=request.user, reference=ref)
    return render(request, 'immigration/detail.html', {
        'application': instance,
        'app_type': app_type,
        'title': title,
    })
