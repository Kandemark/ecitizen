from rest_framework.routers import DefaultRouter
from ..views.api import ConsultationViewSet, PublicCommentViewSet, PetitionViewSet

router = DefaultRouter()
router.register(r'consultations', ConsultationViewSet, basename='consultation')
router.register(r'comments', PublicCommentViewSet, basename='publiccomment')
router.register(r'petitions', PetitionViewSet, basename='petition')

urlpatterns = router.urls
