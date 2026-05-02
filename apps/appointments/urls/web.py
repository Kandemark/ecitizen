from django.urls import path
from ..views import web

urlpatterns = [
    path('book/', web.book_appointment, name='book_appointment'),
    path('', web.my_appointments, name='my_appointments'),
    path('<int:pk>/cancel/', web.cancel_appointment, name='cancel_appointment'),
]
