from django.urls import path
from ..views import web

app_name = 'licenses'

urlpatterns = [
    path('', web.licenses_list, name='list'),
    path('business/apply/', web.business_license_apply, name='business_apply'),
    path('certification/apply/', web.professional_cert_apply, name='certification_apply'),
    path('<str:app_type>/<str:ref>/', web.licenses_detail, name='detail'),
]
