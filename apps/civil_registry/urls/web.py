from django.urls import path
from ..views import web

app_name = 'civil_registry'

urlpatterns = [
    path('', web.certificate_list, name='list'),
    path('apply/<str:cert_type>/', web.certificate_apply, name='apply'),
    path('<str:cert_type>/<str:ref>/', web.certificate_detail, name='detail'),
]
