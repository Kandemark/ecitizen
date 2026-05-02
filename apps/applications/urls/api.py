from rest_framework.routers import DefaultRouter
from ..views.api import ApplicationViewSet, FormFieldViewSet

router = DefaultRouter()
router.register(r'', ApplicationViewSet, basename='application')
router.register(r'form-fields', FormFieldViewSet, basename='formfield')

urlpatterns = router.urls
