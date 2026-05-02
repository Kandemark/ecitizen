from rest_framework.routers import DefaultRouter
from ..views.api import BirthCertificateViewSet, DeathCertificateViewSet, MarriageCertificateViewSet

router = DefaultRouter()
router.register(r'birth-certificates', BirthCertificateViewSet, basename='birthcertificate')
router.register(r'death-certificates', DeathCertificateViewSet, basename='deathcertificate')
router.register(r'marriage-certificates', MarriageCertificateViewSet, basename='marriagecertificate')

urlpatterns = router.urls
