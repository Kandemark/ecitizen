from rest_framework.routers import DefaultRouter
from ..views.api import (
    DrivingLicenseViewSet, VehicleRegistrationViewSet,
    PSVLicenseViewSet, VehicleInspectionViewSet,
)

router = DefaultRouter()
router.register(r'driving-licenses', DrivingLicenseViewSet, basename='drivinglicense')
router.register(r'vehicle-registrations', VehicleRegistrationViewSet, basename='vehicleregistration')
router.register(r'psv-licenses', PSVLicenseViewSet, basename='psvlicense')
router.register(r'vehicle-inspections', VehicleInspectionViewSet, basename='vehicleinspection')

urlpatterns = router.urls
