from rest_framework.routers import DefaultRouter
from ..views.api import ExternalSystemViewSet, DataExchangeViewSet, SyncLogViewSet

router = DefaultRouter()
router.register(r'systems', ExternalSystemViewSet, basename='externalsystem')
router.register(r'exchanges', DataExchangeViewSet, basename='dataexchange')
router.register(r'sync-logs', SyncLogViewSet, basename='synclog')

urlpatterns = router.urls
