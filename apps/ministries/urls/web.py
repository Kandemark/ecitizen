from django.urls import path
from ..views import web

urlpatterns = [
    path('', web.ministry_list, name='ministry_list'),
    path('<str:code>/', web.ministry_detail, name='ministry_detail'),
]
