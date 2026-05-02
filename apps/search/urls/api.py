from rest_framework.routers import DefaultRouter
from ..views.api import SearchIndexViewSet, SearchQueryViewSet

router = DefaultRouter()
router.register(r'indexes', SearchIndexViewSet, basename='searchindex')
router.register(r'queries', SearchQueryViewSet, basename='searchquery')

urlpatterns = router.urls
