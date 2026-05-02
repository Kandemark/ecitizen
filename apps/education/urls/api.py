from rest_framework.routers import DefaultRouter
from ..views.api import LoanApplicationViewSet, SchoolRegistrationViewSet, ExamResultViewSet

router = DefaultRouter()
router.register(r'loans', LoanApplicationViewSet, basename='loanapplication')
router.register(r'schools', SchoolRegistrationViewSet, basename='schoolregistration')
router.register(r'exam-results', ExamResultViewSet, basename='examresult')

urlpatterns = router.urls
