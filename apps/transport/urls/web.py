from django.urls import path
from ..views import web

app_name = 'transport'

urlpatterns = [
    path('', web.transport_list, name='list'),
    path('license/apply/', web.driving_license_apply, name='license_apply'),
    path('vehicle/register/', web.vehicle_register, name='vehicle_register'),
    path('psv/apply/', web.psv_license_apply, name='psv_apply'),
    path('inspection/book/', web.inspection_book, name='inspection_book'),
    path('<str:app_type>/<str:ref>/', web.transport_detail, name='detail'),
]
