from rest_framework.routers import DefaultRouter
from ..views.api import VerificationRequestViewSet

router = DefaultRouter()
router.register(r'', VerificationRequestViewSet, basename='verification')

urlpatterns = router.urls
