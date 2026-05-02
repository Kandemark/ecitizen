from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..models import ReportTemplate, GeneratedReport


@login_required
def reports_list(request):
    templates = ReportTemplate.objects.all().order_by('name')
    generated = GeneratedReport.objects.filter(user=request.user).select_related('template').order_by('-created_at')
    return render(request, 'reports/list.html', {
        'templates': templates, 'generated': generated,
    })


@login_required
def report_generate(request, template_id):
    template = get_object_or_404(ReportTemplate, id=template_id)

    if request.method == 'POST':
        fmt = request.POST.get('format', 'pdf')
        report = GeneratedReport(
            user=request.user,
            template=template,
            parameters=request.POST.get('parameters', '{}'),
            format=fmt,
            status='pending',
        )
        report.save()
        messages.success(request, f'Report "{template.name}" is being generated. You will be notified when ready.')
        return redirect('reports_list')

    return render(request, 'reports/generate.html', {
        'template': template,
        'formats': GeneratedReport._meta.get_field('format').choices,
    })
