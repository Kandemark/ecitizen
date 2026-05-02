from rest_framework.routers import DefaultRouter
from ..views.api import OfficeLocationViewSet, TimeSlotViewSet, AppointmentViewSet

router = DefaultRouter()
router.register(r'offices', OfficeLocationViewSet, basename='office')
router.register(r'slots', TimeSlotViewSet, basename='timeslot')
router.register(r'', AppointmentViewSet, basename='appointment')

urlpatterns = router.urls
