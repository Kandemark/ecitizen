from rest_framework.routers import DefaultRouter
from ..views.api import NewsArticleViewSet, NewsSourceViewSet

router = DefaultRouter()
router.register(r'sources', NewsSourceViewSet, basename='news-source')
router.register(r'articles', NewsArticleViewSet, basename='news-article')

urlpatterns = router.urls
