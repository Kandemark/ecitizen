from rest_framework.routers import DefaultRouter
from ..views.api import DashboardViewSet, WidgetViewSet, MetricViewSet

router = DefaultRouter()
router.register(r'dashboards', DashboardViewSet, basename='dashboard')
router.register(r'widgets', WidgetViewSet, basename='widget')
router.register(r'metrics', MetricViewSet, basename='metric')

urlpatterns = router.urls
