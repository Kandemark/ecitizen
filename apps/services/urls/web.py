from django.urls import path
from ..views import web

urlpatterns = [
    path('browse/', web.service_browse, name='service_browse'),
    path('<slug:slug>/', web.service_detail, name='service_detail'),
]
