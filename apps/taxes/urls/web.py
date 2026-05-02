from django.urls import path
from ..views import web

app_name = 'taxes'

urlpatterns = [
    path('', web.taxes_list, name='list'),
    path('return/file/', web.tax_return_file, name='return_file'),
    path('assessment/request/', web.assessment_request, name='assessment_request'),
    path('compliance/apply/', web.compliance_apply, name='compliance_apply'),
    path('<str:app_type>/<str:ref>/', web.taxes_detail, name='detail'),
]
