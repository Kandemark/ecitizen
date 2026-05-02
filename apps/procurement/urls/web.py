from django.urls import path
from ..views import web

app_name = 'procurement'

urlpatterns = [
    path('', web.procurement_list, name='list'),
    path('tender/<str:ref>/', web.tender_detail, name='tender_detail'),
    path('tender/<str:tender_ref>/bid/', web.bid_submit, name='bid_submit'),
    path('<str:app_type>/<str:ref>/', web.procurement_detail, name='detail'),
]
