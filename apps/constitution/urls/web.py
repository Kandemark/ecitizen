from django.urls import path
from ..views import web

app_name = 'constitution'

urlpatterns = [
    path('', web.constitution_browse, name='browse'),
    path('chapter/<int:number>/', web.constitution_chapter, name='chapter'),
    path('article/<str:number>/', web.constitution_article, name='article'),
    path('schedules/', web.constitution_schedules, name='schedules'),
    path('search/', web.constitution_search, name='search'),
]
