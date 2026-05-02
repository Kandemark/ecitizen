from datetime import date

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Bill, Hansard, CommitteeReport, ParliamentarySitting


def legislature_dashboard(request):
    """Parliament activity overview: recent bills, latest hansards, upcoming sittings."""
    bills = Bill.objects.order_by('-last_updated')[:10]
    recent_hansards = Hansard.objects.order_by('-date')[:5]
    recent_reports = CommitteeReport.objects.order_by('-date_published')[:5]
    upcoming_sittings = ParliamentarySitting.objects.filter(
        date__gte=date.today()
    ).order_by('date')[:10]
    return render(request, 'legislature/dashboard.html', {
        'bills': bills,
        'recent_hansards': recent_hansards,
        'recent_reports': recent_reports,
        'upcoming_sittings': upcoming_sittings,
    })


def bills_list(request):
    status = request.GET.get('status', '')
    house = request.GET.get('house', '')
    bills = Bill.objects.select_related().order_by('-date_introduced')
    if status:
        bills = bills.filter(status=status)
    if house:
        bills = bills.filter(house=house)
    return render(request, 'legislature/bills_list.html', {
        'bills': bills,
        'current_status': status,
        'current_house': house,
        'statuses': Bill.Status.choices,
        'houses': Bill.House.choices,
    })


def bill_detail(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    return render(request, 'legislature/bill_detail.html', {'bill': bill})


def hansards_list(request):
    house = request.GET.get('house', '')
    hansards = Hansard.objects.order_by('-date')
    if house:
        hansards = hansards.filter(house=house)
    return render(request, 'legislature/hansards_list.html', {
        'hansards': hansards,
        'current_house': house,
    })


def hansard_detail(request, hansard_id):
    hansard = get_object_or_404(Hansard, id=hansard_id)
    return render(request, 'legislature/hansard_detail.html', {'hansard': hansard})


def committee_reports_list(request):
    reports = CommitteeReport.objects.order_by('-date_published')
    return render(request, 'legislature/committee_reports_list.html', {
        'reports': reports,
    })


def committee_report_detail(request, report_id):
    report = get_object_or_404(CommitteeReport, id=report_id)
    return render(request, 'legislature/committee_report_detail.html', {'report': report})


def sittings_list(request):
    house = request.GET.get('house', '')
    sittings = ParliamentarySitting.objects.order_by('-date')
    if house:
        sittings = sittings.filter(house=house)
    return render(request, 'legislature/sittings_list.html', {
        'sittings': sittings,
        'current_house': house,
    })
