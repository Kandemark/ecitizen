from rest_framework import viewsets, permissions
from ..models import APIKey, Webhook
from ..serializers import APIKeySerializer, WebhookSerializer


class APIKeyViewSet(viewsets.ModelViewSet):
    serializer_class = APIKeySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return APIKey.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        return {'request': self.request}


class WebhookViewSet(viewsets.ModelViewSet):
    serializer_class = WebhookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Webhook.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        return {'request': self.request}
