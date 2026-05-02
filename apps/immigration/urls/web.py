from django.urls import path
from ..views import web

app_name = 'immigration'

urlpatterns = [
    path('', web.application_list, name='list'),
    path('passport/apply/', web.passport_apply, name='passport_apply'),
    path('visa/apply/', web.visa_apply, name='visa_apply'),
    path('permit/apply/', web.work_permit_apply, name='permit_apply'),
    path('<str:app_type>/<str:ref>/', web.application_detail, name='detail'),
]
