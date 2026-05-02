from rest_framework.routers import DefaultRouter
from ..views.api import (
    ServiceViewSet, ServiceCategoryViewSet,
    EligibilityRuleViewSet, RequiredDocumentViewSet,
)

router = DefaultRouter()
router.register(r'categories', ServiceCategoryViewSet, basename='category')
router.register(r'', ServiceViewSet, basename='service')
router.register(r'rules', EligibilityRuleViewSet, basename='eligibilityrule')
router.register(r'documents', RequiredDocumentViewSet, basename='requireddocument')

urlpatterns = router.urls
