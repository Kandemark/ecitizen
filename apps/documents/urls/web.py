from django.urls import path
from ..views import web

urlpatterns = [
    path('', web.document_list, name='document_list'),
    path('upload/', web.document_upload, name='document_upload'),
    path('<int:pk>/delete/', web.document_delete, name='document_delete'),
]
