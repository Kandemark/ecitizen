import json
import math

from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie

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
    # County government services only — those with a constitutional function
    county_services = county.services.filter(
        is_active=True, constitutional_function__isnull=False
    ).select_related('category', 'ministry', 'constitutional_function').order_by(
        'constitutional_function__order', 'name'
    )

    # Group by constitutional function
    by_function = {}
    for svc in county_services:
        cf = svc.constitutional_function
        key = (cf.name, cf.mandate_ref)
        if key not in by_function:
            by_function[key] = []
        by_function[key].append(svc)

    services_grouped = [
        {'name': label, 'mandate_ref': ref, 'services': svcs}
        for (label, ref), svcs in by_function.items()
    ]

    # DB-backed constitutional mandates
    from apps.services.models import ConstitutionalFunction
    county_mandates = ConstitutionalFunction.objects.filter(is_active=True).order_by('order')

    return render(request, 'counties/detail.html', {
        'county': county,
        'county_services': county_services,
        'services_grouped': services_grouped,
        'county_mandates': county_mandates,
    })


def _haversine(lat1, lon1, lat2, lon2):
    """Distance in km between two coordinates using the Haversine formula."""
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


@require_POST
def nearest_county(request):
    """Accept lat/lon, return the nearest Kenyan county. Stores choice in session."""
    try:
        body = json.loads(request.body)
        lat = float(body.get('latitude', 0))
        lon = float(body.get('longitude', 0))
    except (json.JSONDecodeError, ValueError, TypeError):
        return JsonResponse({'error': 'Invalid coordinates'}, status=400)

    from apps.integration.services.weather import COUNTY_COORDS

    best_code = None
    best_dist = float('inf')

    for code, coords in COUNTY_COORDS.items():
        dist = _haversine(lat, lon, coords['lat'], coords['lon'])
        if dist < best_dist:
            best_dist = dist
            best_code = code

    if best_code is None:
        return JsonResponse({'error': 'No county found'}, status=500)

    # Store in session
    request.session['detected_county'] = best_code

    # Look up county details
    try:
        county = County.objects.get(code=best_code, is_active=True)
        county_data = {
            'code': county.code,
            'name': county.name,
            'capital': county.capital,
            'distance_km': round(best_dist, 1),
        }
    except County.DoesNotExist:
        county_data = {'code': best_code, 'distance_km': round(best_dist, 1)}

    return JsonResponse({
        'county': county_data,
        'detected': True,
    })


@ensure_csrf_cookie
def get_session_county(request):
    """Return the county stored in session, if any."""
    code = request.session.get('detected_county')
    if not code:
        return JsonResponse({'county': None})

    try:
        county = County.objects.get(code=code, is_active=True)
        return JsonResponse({
            'county': {
                'code': county.code,
                'name': county.name,
                'capital': county.capital,
            }
        })
    except County.DoesNotExist:
        return JsonResponse({'county': None})
