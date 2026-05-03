from django.urls import path
from ..views import web

urlpatterns = [
    path('', web.county_list, name='county_list'),
    path('api/nearest/', web.nearest_county, name='nearest_county'),
    path('api/session-county/', web.get_session_county, name='session_county'),
    path('<str:code>/', web.county_detail, name='county_detail'),
]
