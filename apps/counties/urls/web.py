from django.urls import path
from ..views import web

urlpatterns = [
    path('', web.county_list, name='county_list'),
    path('<str:code>/', web.county_detail, name='county_detail'),
]
