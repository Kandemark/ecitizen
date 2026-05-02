from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views.api import AuthViewSet, ProfileViewSet

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', AuthViewSet.as_view({'post': 'login'}), name='api-login'),
    path('register/', AuthViewSet.as_view({'post': 'register'}), name='api-register'),
    path('logout/', AuthViewSet.as_view({'post': 'logout'}), name='api-logout'),
]
