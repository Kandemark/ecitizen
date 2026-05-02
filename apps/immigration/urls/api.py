from rest_framework.routers import DefaultRouter
from ..views.api import PassportApplicationViewSet, VisaApplicationViewSet, WorkPermitViewSet

router = DefaultRouter()
router.register(r'passports', PassportApplicationViewSet, basename='passport')
router.register(r'visas', VisaApplicationViewSet, basename='visa')
router.register(r'work-permits', WorkPermitViewSet, basename='workpermit')

urlpatterns = router.urls
