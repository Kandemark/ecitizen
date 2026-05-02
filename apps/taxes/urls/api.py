from rest_framework.routers import DefaultRouter
from ..views.api import TaxReturnViewSet, TaxAssessmentViewSet, ComplianceCertificateViewSet

router = DefaultRouter()
router.register(r'returns', TaxReturnViewSet, basename='taxreturn')
router.register(r'assessments', TaxAssessmentViewSet, basename='taxassessment')
router.register(r'compliance-certificates', ComplianceCertificateViewSet, basename='compliancecertificate')

urlpatterns = router.urls
