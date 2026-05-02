from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q
from ..models import Ministry, Department


def ministry_list(request):
    ministries = Ministry.objects.filter(is_active=True).prefetch_related(
        'departments', 'services'
    ).annotate(
        service_count=Count('services', filter=Q(services__is_active=True))
    ).order_by('order', 'name')

    total_services = sum(m.service_count for m in ministries)

    return render(request, 'ministries/browse.html', {
        'ministries': ministries,
        'total_services': total_services,
    })


def ministry_detail(request, code):
    ministry = get_object_or_404(
        Ministry.objects.filter(is_active=True).prefetch_related(
            'departments',
            'departments__divisions',
            'services__category',
        ),
        code=code,
    )
    services = ministry.services.filter(is_active=True).select_related('category')
    departments = ministry.departments.filter(is_active=True)

    return render(request, 'ministries/detail.html', {
        'ministry': ministry,
        'services': services,
        'departments': departments,
    })
