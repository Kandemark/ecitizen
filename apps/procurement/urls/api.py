from rest_framework.routers import DefaultRouter
from ..views.api import TenderNoticeViewSet, BidViewSet, ContractViewSet

router = DefaultRouter()
router.register(r'tenders', TenderNoticeViewSet, basename='tendernotice')
router.register(r'bids', BidViewSet, basename='bid')
router.register(r'contracts', ContractViewSet, basename='contract')

urlpatterns = router.urls
