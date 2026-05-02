from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from ..models import Service, ServiceCategory


def service_browse(request):
    categories = ServiceCategory.objects.filter(is_active=True)
    services = Service.objects.filter(is_active=True).select_related('ministry', 'category')

    # ── Server-side filtering ──
    query = request.GET.get('q', '').strip()
    ministry_id = request.GET.get('ministry', '')
    category_id = request.GET.get('category', '')
    is_free = request.GET.get('is_free', '')

    if query:
        services = services.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(short_description__icontains=query)
            | Q(category__name__icontains=query)
            | Q(ministry__name__icontains=query)
        ).distinct()

    if ministry_id:
        services = services.filter(ministry_id=ministry_id)

    if category_id:
        services = services.filter(category_id=category_id)

    if is_free == '1':
        services = services.filter(fee_kes=0)

    # Ministry grouping for filter dropdown (always from full set)
    ministries = {}
    all_services = Service.objects.filter(is_active=True).select_related('ministry')
    for svc in all_services:
        if svc.ministry:
            m_name = svc.ministry.name
            if m_name not in ministries:
                ministries[m_name] = {
                    'ministry': svc.ministry,
                    'services': [],
                    'count': 0,
                }
            ministries[m_name]['count'] += 1

    has_filters = bool(query or ministry_id or category_id or is_free)

    popular = []
    if not has_filters:
        popular = services.filter(is_popular=True)[:12]

    context = {
        'categories': categories,
        'services': services,
        'ministries': ministries,
        'popular_services': popular,
        'total_services': services.count(),
        'has_filters': has_filters,
    }

    # HTMX: return only the grid partial
    if request.headers.get('HX-Request'):
        return render(request, 'services/includes/service_grid.html', context)

    return render(request, 'services/browse.html', context)


def service_detail(request, slug):
    service = get_object_or_404(
        Service.objects.filter(is_active=True)
        .select_related('ministry', 'category')
        .prefetch_related('eligibility_rules', 'required_documents', 'counties'),
        slug=slug,
    )
    related = Service.objects.filter(
        category=service.category, is_active=True
    ).exclude(pk=service.pk)[:6]

    return render(request, 'services/detail.html', {
        'service': service,
        'related_services': related,
    })
