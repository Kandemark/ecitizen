from django.urls import path
from ..views import web

urlpatterns = [
    path('', web.onboarding_wizard, name='onboarding'),
]
