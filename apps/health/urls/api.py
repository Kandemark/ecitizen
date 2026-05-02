from rest_framework.routers import DefaultRouter
from ..views.api import HealthRecordViewSet, NHIFRegistrationViewSet, MedicalCertificateViewSet

router = DefaultRouter()
router.register(r'health-records', HealthRecordViewSet, basename='healthrecord')
router.register(r'nhif-registrations', NHIFRegistrationViewSet, basename='nhifregistration')
router.register(r'medical-certificates', MedicalCertificateViewSet, basename='medicalcertificate')

urlpatterns = router.urls
