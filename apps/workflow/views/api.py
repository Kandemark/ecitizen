from rest_framework import viewsets, permissions
from ..models import WorkflowDefinition, ApprovalStep, ReviewAssignment
from ..serializers import WorkflowDefinitionSerializer, ReviewAssignmentSerializer


class WorkflowDefinitionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WorkflowDefinition.objects.all()
    serializer_class = WorkflowDefinitionSerializer
    permission_classes = [permissions.IsAuthenticated]


class ReviewAssignmentViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewAssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = ReviewAssignment.objects.all()
        if not self.request.user.is_staff:
            qs = qs.filter(assigned_to=self.request.user)
        return qs
