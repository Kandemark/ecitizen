from rest_framework.routers import DefaultRouter
from ..views.api import CountyViewSet, SubCountyViewSet, WardViewSet, VillageViewSet, ConstituencyViewSet

router = DefaultRouter()
# Specific routes MUST be registered before the generic r'' county route
# to avoid 'sub-counties' being captured by CountyViewSet's lookup_field='code'
router.register(r'sub-counties', SubCountyViewSet, basename='subcounty')
router.register(r'wards', WardViewSet, basename='ward')
router.register(r'villages', VillageViewSet, basename='village')
router.register(r'constituencies', ConstituencyViewSet, basename='constituency')
router.register(r'', CountyViewSet, basename='county')

urlpatterns = router.urls
