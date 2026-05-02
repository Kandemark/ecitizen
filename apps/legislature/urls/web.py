from django.urls import path
from ..views import web

app_name = 'legislature'

urlpatterns = [
    path('', web.legislature_dashboard, name='dashboard'),
    path('bills/', web.bills_list, name='bills_list'),
    path('bills/<int:bill_id>/', web.bill_detail, name='bill_detail'),
    path('hansards/', web.hansards_list, name='hansards_list'),
    path('hansards/<int:hansard_id>/', web.hansard_detail, name='hansard_detail'),
    path('committee-reports/', web.committee_reports_list, name='committee_reports_list'),
    path('committee-reports/<int:report_id>/', web.committee_report_detail, name='committee_report_detail'),
    path('sittings/', web.sittings_list, name='sittings_list'),
]
