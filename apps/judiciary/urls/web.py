from django.urls import path
from ..views import web

app_name = 'judiciary'

urlpatterns = [
    path('', web.judiciary_list, name='list'),
    path('case/file/', web.case_file, name='case_file'),
    path('filing/submit/', web.filing_submit, name='filing_submit'),
    path('filing/submit/<str:case_ref>/', web.filing_submit, name='filing_submit_for_case'),
    path('fine/pay/', web.fine_pay, name='fine_pay'),
    path('<str:app_type>/<str:ref>/', web.judiciary_detail, name='detail'),
]
