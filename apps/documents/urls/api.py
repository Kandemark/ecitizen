from rest_framework.routers import DefaultRouter
from ..views.api import DocumentViewSet

router = DefaultRouter()
router.register(r'', DocumentViewSet, basename='document')

urlpatterns = router.urls
