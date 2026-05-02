from rest_framework.routers import DefaultRouter
from ..views.api import NotificationViewSet, NotificationPreferenceViewSet, DeviceTokenViewSet

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'preferences', NotificationPreferenceViewSet, basename='notificationpreference')
router.register(r'device-tokens', DeviceTokenViewSet, basename='devicetoken')

urlpatterns = router.urls
