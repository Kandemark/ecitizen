from rest_framework.routers import DefaultRouter
from ..views.api import PollingStationViewSet, VoterRecordViewSet, CandidateViewSet

router = DefaultRouter()
router.register(r'polling-stations', PollingStationViewSet, basename='pollingstation')
router.register(r'voter-records', VoterRecordViewSet, basename='voterrecord')
router.register(r'candidates', CandidateViewSet, basename='candidate')

urlpatterns = router.urls
