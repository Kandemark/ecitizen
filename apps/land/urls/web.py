from django.urls import path
from ..views import web

app_name = 'land'

urlpatterns = [
    path('', web.land_list, name='list'),
    path('title-deed/apply/', web.title_deed_apply, name='title_deed_apply'),
    path('search/apply/', web.land_search_apply, name='search_apply'),
    path('transfer/apply/', web.transfer_apply, name='transfer_apply'),
    path('<str:app_type>/<str:ref>/', web.land_detail, name='detail'),
]
