from rest_framework.routers import DefaultRouter
from ..views.api import MinistryViewSet, DepartmentViewSet, DivisionViewSet

router = DefaultRouter()
router.register(r'', MinistryViewSet, basename='ministry')
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'divisions', DivisionViewSet, basename='division')

urlpatterns = router.urls
