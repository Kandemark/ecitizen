from rest_framework.routers import DefaultRouter
from ..views.api import ConversationViewSet, MessageViewSet, SupportTicketViewSet

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'tickets', SupportTicketViewSet, basename='supportticket')

urlpatterns = router.urls
