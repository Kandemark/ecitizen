from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..models import LoanApplication, SchoolRegistration, ExamResult
from core.utils import generate_tracking_id


@login_required
def education_list(request):
    loans = LoanApplication.objects.filter(user=request.user).order_by('-created_at')
    schools = SchoolRegistration.objects.filter(user=request.user).select_related('county').order_by('-created_at')
    exams = ExamResult.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'education/list.html', {
        'loans': loans, 'schools': schools, 'exams': exams,
    })


@login_required
def loan_apply(request):
    if request.method == 'POST':
        loan = LoanApplication(
            user=request.user,
            reference=generate_tracking_id('LOAN'),
            loan_type=request.POST.get('loan_type', 'undergraduate'),
            institution=request.POST.get('institution', ''),
            campus=request.POST.get('campus', ''),
            course_of_study=request.POST.get('course_of_study', ''),
            year_of_study=request.POST.get('year_of_study', 1),
            amount=request.POST.get('amount', 0),
            status='submitted',
        )
        loan.save()
        from apps.applications.helpers import create_workflow_application
        create_workflow_application(loan, request.user)
        messages.success(request, f'Loan application {loan.reference} submitted.')
        return redirect('education_detail', app_type='loan', ref=loan.reference)

    return render(request, 'education/loan_apply.html', {
        'loan_types': LoanApplication._meta.get_field('loan_type').choices,
    })


@login_required
def school_register(request):
    if request.method == 'POST':
        s = SchoolRegistration(
            user=request.user,
            reference=generate_tracking_id('SCH'),
            school_name=request.POST.get('school_name', ''),
            registration_type=request.POST.get('registration_type', 'primary'),
            physical_address=request.POST.get('physical_address', ''),
            postal_address=request.POST.get('postal_address', ''),
            proprietor_name=request.POST.get('proprietor_name', ''),
            status='submitted',
        )
        county_id = request.POST.get('county')
        if county_id:
            try:
                from apps.counties.models import County
                s.county = County.objects.get(id=county_id)
            except Exception:
                pass
        s.save()
        from apps.applications.helpers import create_workflow_application
        create_workflow_application(s, request.user)
        messages.success(request, f'School registration {s.reference} submitted.')
        return redirect('education_detail', app_type='school', ref=s.reference)

    from apps.counties.models import County
    return render(request, 'education/school_apply.html', {
        'reg_types': SchoolRegistration._meta.get_field('registration_type').choices,
        'counties': County.objects.all(),
    })


@login_required
def exam_result_request(request):
    if request.method == 'POST':
        e = ExamResult(
            user=request.user,
            reference=generate_tracking_id('EXAM'),
            exam_type=request.POST.get('exam_type', 'kcpe'),
            index_number=request.POST.get('index_number', ''),
            examination_year=request.POST.get('examination_year') or None,
            school_name=request.POST.get('school_name', ''),
            status='submitted',
        )
        e.save()
        from apps.applications.helpers import create_workflow_application
        create_workflow_application(e, request.user)
        messages.success(request, f'Exam result request {e.reference} submitted.')
        return redirect('education_detail', app_type='exam', ref=e.reference)

    return render(request, 'education/exam_apply.html', {
        'exam_types': ExamResult._meta.get_field('exam_type').choices,
    })


@login_required
def education_detail(request, app_type, ref):
    models_map = {
        'loan': (LoanApplication, 'Loan Application'),
        'school': (SchoolRegistration, 'School Registration'),
        'exam': (ExamResult, 'Exam Result'),
    }
    info = models_map.get(app_type)
    if not info:
        messages.error(request, 'Invalid record type.')
        return redirect('education_list')

    model, title = info
    instance = get_object_or_404(model, user=request.user, reference=ref)
    return render(request, 'education/detail.html', {
        'record': instance, 'app_type': app_type, 'title': title,
    })
