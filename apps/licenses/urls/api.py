from rest_framework.routers import DefaultRouter
from ..views.api import BusinessLicenseViewSet, ProfessionalCertificationViewSet

router = DefaultRouter()
router.register(r'business-licenses', BusinessLicenseViewSet, basename='businesslicense')
router.register(r'professional-certifications', ProfessionalCertificationViewSet, basename='professionalcertification')

urlpatterns = router.urls
