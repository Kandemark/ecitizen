from rest_framework.routers import DefaultRouter
from ..views.api import AuditEntryViewSet, ComplianceCheckViewSet, DataAccessLogViewSet

router = DefaultRouter()
router.register(r'entries', AuditEntryViewSet, basename='auditentry')
router.register(r'compliance', ComplianceCheckViewSet, basename='compliancecheck')
router.register(r'data-access', DataAccessLogViewSet, basename='dataaccesslog')

urlpatterns = router.urls
