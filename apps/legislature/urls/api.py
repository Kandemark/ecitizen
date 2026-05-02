from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views import api

router = DefaultRouter()
router.register(r'bills', api.BillViewSet, basename='api-bill')
router.register(r'hansards', api.HansardViewSet, basename='api-hansard')
router.register(r'committee-reports', api.CommitteeReportViewSet, basename='api-committee-report')
router.register(r'sittings', api.ParliamentarySittingViewSet, basename='api-sitting')

app_name = 'legislature_api'

urlpatterns = [
    path('', include(router.urls)),
]
