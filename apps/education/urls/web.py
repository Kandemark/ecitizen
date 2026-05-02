from django.urls import path
from ..views import web

app_name = 'education'

urlpatterns = [
    path('', web.education_list, name='list'),
    path('loan/apply/', web.loan_apply, name='loan_apply'),
    path('school/register/', web.school_register, name='school_register'),
    path('exam/request/', web.exam_result_request, name='exam_request'),
    path('<str:app_type>/<str:ref>/', web.education_detail, name='detail'),
]
