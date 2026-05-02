from django.urls import path
from ..views import web

app_name = 'health'

urlpatterns = [
    path('', web.health_list, name='list'),
    path('record/apply/', web.health_record_apply, name='record_apply'),
    path('nhif/register/', web.nhif_register, name='nhif_register'),
    path('certificate/apply/', web.medical_cert_apply, name='cert_apply'),
    path('<str:app_type>/<str:ref>/', web.health_detail, name='detail'),
]
