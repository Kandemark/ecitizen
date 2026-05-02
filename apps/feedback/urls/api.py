from rest_framework.routers import DefaultRouter
from ..views.api import FeedbackViewSet, ComplaintViewSet, SatisfactionSurveyViewSet

router = DefaultRouter()
router.register(r'feedback', FeedbackViewSet, basename='feedback')
router.register(r'complaints', ComplaintViewSet, basename='complaint')
router.register(r'surveys', SatisfactionSurveyViewSet, basename='satisfactionsurvey')

urlpatterns = router.urls
