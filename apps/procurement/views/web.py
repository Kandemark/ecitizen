from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..models import TenderNotice, Bid
from core.utils import generate_tracking_id


@login_required
def procurement_list(request):
    tenders = TenderNotice.objects.filter(is_published=True, status='published').order_by('-closing_date')
    my_bids = Bid.objects.filter(user=request.user).select_related('tender').order_by('-created_at')
    return render(request, 'procurement/list.html', {
        'tenders': tenders, 'my_bids': my_bids,
    })


@login_required
def tender_detail(request, ref):
    tender = get_object_or_404(
        TenderNotice.objects.filter(is_published=True).select_related('ministry'),
        reference=ref,
    )
    existing_bid = Bid.objects.filter(user=request.user, tender=tender).first()
    return render(request, 'procurement/tender_detail.html', {
        'tender': tender, 'existing_bid': existing_bid,
    })


@login_required
def bid_submit(request, tender_ref):
    tender = get_object_or_404(TenderNotice.objects.filter(is_published=True), reference=tender_ref)

    if Bid.objects.filter(user=request.user, tender=tender).exists():
        messages.error(request, 'You have already submitted a bid for this tender.')
        return redirect('procurement_tender_detail', ref=tender_ref)

    if request.method == 'POST':
        bid = Bid(
            user=request.user,
            reference=generate_tracking_id('BID'),
            tender=tender,
            bid_amount=request.POST.get('bid_amount', 0),
            company_name=request.POST.get('company_name', ''),
            registration_number=request.POST.get('registration_number', ''),
            bid_bond_reference=request.POST.get('bid_bond_reference', ''),
            status='submitted',
        )
        bid.save()
        from apps.applications.helpers import create_workflow_application
        create_workflow_application(bid, request.user)
        messages.success(request, f'Bid {bid.reference} submitted successfully.')
        return redirect('procurement_detail', app_type='bid', ref=bid.reference)

    return render(request, 'procurement/bid_apply.html', {'tender': tender})


@login_required
def procurement_detail(request, app_type, ref):
    if app_type == 'bid':
        instance = get_object_or_404(Bid.objects.select_related('tender'), user=request.user, reference=ref)
        return render(request, 'procurement/detail.html', {
            'record': instance, 'app_type': app_type, 'title': 'Bid',
        })

    messages.error(request, 'Invalid record type.')
    return redirect('procurement_list')
