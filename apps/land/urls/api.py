from rest_framework.routers import DefaultRouter
from ..views.api import TitleDeedViewSet, LandSearchViewSet, TransferViewSet

router = DefaultRouter()
router.register(r'title-deeds', TitleDeedViewSet, basename='titledeed')
router.register(r'land-searches', LandSearchViewSet, basename='landsearch')
router.register(r'transfers', TransferViewSet, basename='transfer')

urlpatterns = router.urls
