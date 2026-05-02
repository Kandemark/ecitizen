from rest_framework import viewsets, permissions, filters
from ..models import Consultation, PublicComment, Petition
from ..serializers import ConsultationSerializer, PublicCommentSerializer, PetitionSerializer


class ConsultationViewSet(viewsets.ModelViewSet):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['start_date', 'end_date', 'status']


class PublicCommentViewSet(viewsets.ModelViewSet):
    serializer_class = PublicCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']

    def get_queryset(self):
        return PublicComment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PetitionViewSet(viewsets.ModelViewSet):
    serializer_class = PetitionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['reference', 'title', 'description']
    ordering_fields = ['created_at', 'signature_count', 'status']

    def get_queryset(self):
        return Petition.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
