from rest_framework.routers import DefaultRouter
from ..views.api import DeveloperRegistrationViewSet, SandboxEnvironmentViewSet

router = DefaultRouter()
router.register(r'registrations', DeveloperRegistrationViewSet, basename='developerregistration')
router.register(r'sandboxes', SandboxEnvironmentViewSet, basename='sandboxenvironment')

urlpatterns = router.urls
