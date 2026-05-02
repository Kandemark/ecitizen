from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q
from ..models import County


def county_list(request):
    counties = County.objects.filter(is_active=True).annotate(
        service_count=Count('services', filter=Q(services__is_active=True))
    ).order_by('code')

    return render(request, 'counties/list.html', {
        'counties': counties,
    })


def county_detail(request, code):
    county = get_object_or_404(
        County.objects.filter(is_active=True),
        code=code,
    )
    services = county.services.filter(is_active=True).select_related(
        'category', 'ministry'
    ).order_by('category__name', 'name')

    # Group services by category
    by_category = {}
    for svc in services:
        cat_name = svc.category.name if svc.category else 'General'
        if cat_name not in by_category:
            by_category[cat_name] = []
        by_category[cat_name].append(svc)

    return render(request, 'counties/detail.html', {
        'county': county,
        'services': services,
        'services_by_category': by_category,
    })
