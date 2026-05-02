from rest_framework.routers import DefaultRouter
from ..views.api import EmergencyContactViewSet, EmergencyReportViewSet

router = DefaultRouter()
router.register(r'contacts', EmergencyContactViewSet, basename='emergencycontact')
router.register(r'reports', EmergencyReportViewSet, basename='emergencyreport')

urlpatterns = router.urls
