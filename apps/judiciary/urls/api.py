from rest_framework.routers import DefaultRouter
from ..views.api import CourtCaseViewSet, FilingViewSet, HearingScheduleViewSet, FineViewSet

router = DefaultRouter()
router.register(r'cases', CourtCaseViewSet, basename='courtcase')
router.register(r'filings', FilingViewSet, basename='filing')
router.register(r'hearings', HearingScheduleViewSet, basename='hearingschedule')
router.register(r'fines', FineViewSet, basename='fine')

urlpatterns = router.urls
