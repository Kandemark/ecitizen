from django.urls import path
from ..views import web

urlpatterns = [
    path('apply/<slug:slug>/', web.apply_service, name='apply_service'),
    path('<str:ref>/', web.application_detail, name='application_detail'),
]
