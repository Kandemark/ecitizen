from django.urls import path
from ..views import web

app_name = 'participation'

urlpatterns = [
    path('', web.participation_list, name='list'),
    path('consultation/<int:pk>/', web.consultation_detail, name='consultation_detail'),
    path('petition/create/', web.petition_create, name='petition_create'),
    path('petition/<str:ref>/', web.petition_detail, name='petition_detail'),
]
