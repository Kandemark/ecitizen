from rest_framework.routers import DefaultRouter
from ..views.api import APIKeyViewSet, WebhookViewSet

router = DefaultRouter()
router.register(r'keys', APIKeyViewSet, basename='apikey')
router.register(r'webhooks', WebhookViewSet, basename='webhook')

urlpatterns = router.urls
