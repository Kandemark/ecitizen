from rest_framework.routers import DefaultRouter
from ..views.api import WorkflowDefinitionViewSet, ReviewAssignmentViewSet

router = DefaultRouter()
router.register(r'definitions', WorkflowDefinitionViewSet, basename='workflow-definition')
router.register(r'reviews', ReviewAssignmentViewSet, basename='review')

urlpatterns = router.urls
