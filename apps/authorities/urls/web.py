from django.urls import path
from ..views import web

app_name = 'authorities'

urlpatterns = [
    path('', web.staff_dashboard, name='staff_dashboard'),
    path('review-queue/', web.review_queue, name='review_queue'),
    path('review/<int:application_id>/', web.review_application, name='review_application'),
    path('all-applications/', web.all_applications, name='all_applications'),
]
