from django.urls import path
from ..views import web

app_name = 'reports'

urlpatterns = [
    path('', web.reports_list, name='list'),
    path('generate/<int:template_id>/', web.report_generate, name='generate'),
]
