from rest_framework import viewsets, permissions, parsers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from core.mixins import OwnerFilterMixin
from ..models import Document, DocumentShare
from ..serializers import DocumentSerializer, DocumentShareSerializer


class DocumentViewSet(OwnerFilterMixin, viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def share(self, request, pk=None):
        document = self.get_object()
        serializer = DocumentShareSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(document=document)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
