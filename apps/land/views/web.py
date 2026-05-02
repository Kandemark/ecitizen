from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..models import TitleDeed, LandSearch, Transfer
from core.utils import generate_tracking_id


@login_required
def land_list(request):
    title_deeds = TitleDeed.objects.filter(user=request.user).order_by('-created_at')
    searches = LandSearch.objects.filter(user=request.user).order_by('-created_at')
    transfers = Transfer.objects.filter(user=request.user).select_related('title_deed').order_by('-created_at')
    return render(request, 'land/list.html', {
        'title_deeds': title_deeds,
        'searches': searches,
        'transfers': transfers,
    })


@login_required
def title_deed_apply(request):
    if request.method == 'POST':
        deed = TitleDeed(
            user=request.user,
            reference=generate_tracking_id('DEED'),
            title_number=request.POST.get('title_number', ''),
            property_location=request.POST.get('property_location', ''),
            land_size_hectares=request.POST.get('land_size_hectares', 0),
            tenure_type=request.POST.get('tenure_type', 'freehold'),
            registered_owner_name=request.POST.get('registered_owner_name', ''),
            encumbrances=request.POST.get('encumbrances', ''),
            status='submitted',
        )
        county_id = request.POST.get('county')
        if county_id:
            try:
                from apps.counties.models import County
                deed.county = County.objects.get(id=county_id)
            except Exception:
                pass
        deed.save()
        from apps.applications.helpers import create_workflow_application
        create_workflow_application(deed, request.user)
        messages.success(request, f'Title deed application {deed.reference} submitted.')
        return redirect('land_detail', app_type='title_deed', ref=deed.reference)

    from apps.counties.models import County
    return render(request, 'land/title_deed_apply.html', {
        'counties': County.objects.all(),
        'tenure_types': ['freehold', 'leasehold', 'customary', 'sectional'],
    })


@login_required
def land_search_apply(request):
    if request.method == 'POST':
        search = LandSearch(
            user=request.user,
            reference=generate_tracking_id('LSRC'),
            title_number=request.POST.get('title_number', ''),
            search_purpose=request.POST.get('search_purpose', ''),
            status='submitted',
        )
        search.save()
        from apps.applications.helpers import create_workflow_application
        create_workflow_application(search, request.user)
        messages.success(request, f'Land search {search.reference} submitted.')
        return redirect('land_detail', app_type='land_search', ref=search.reference)

    return render(request, 'land/search_apply.html')


@login_required
def transfer_apply(request):
    if request.method == 'POST':
        title_deed_id = request.POST.get('title_deed')
        title_deed = None
        if title_deed_id:
            title_deed = get_object_or_404(TitleDeed, id=title_deed_id, user=request.user)

        transfer = Transfer(
            user=request.user,
            reference=generate_tracking_id('TRNF'),
            title_deed=title_deed,
            from_owner=request.POST.get('from_owner', ''),
            to_owner=request.POST.get('to_owner', ''),
            consideration_amount=request.POST.get('consideration_amount', 0),
            transfer_type=request.POST.get('transfer_type', 'sale'),
            status='submitted',
        )
        transfer.save()
        from apps.applications.helpers import create_workflow_application
        create_workflow_application(transfer, request.user)
        messages.success(request, f'Transfer application {transfer.reference} submitted.')
        return redirect('land_detail', app_type='transfer', ref=transfer.reference)

    title_deeds = TitleDeed.objects.filter(user=request.user, status__in=['approved', 'completed'])
    return render(request, 'land/transfer_apply.html', {
        'title_deeds': title_deeds,
        'transfer_types': ['sale', 'gift', 'inheritance', 'subdivision', 'amalgamation'],
    })


@login_required
def land_detail(request, app_type, ref):
    models_map = {
        'title_deed': (TitleDeed, 'Title Deed'),
        'land_search': (LandSearch, 'Land Search'),
        'transfer': (Transfer, 'Transfer'),
    }
    model_info = models_map.get(app_type)
    if not model_info:
        messages.error(request, 'Invalid record type.')
        return redirect('land_list')

    model, title = model_info
    instance = get_object_or_404(model, user=request.user, reference=ref)
    return render(request, 'land/detail.html', {
        'record': instance,
        'app_type': app_type,
        'title': title,
    })
