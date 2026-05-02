from rest_framework import viewsets, permissions
from core.mixins import OwnerFilterMixin
from ..models import LoanApplication, SchoolRegistration, ExamResult
from ..serializers import LoanApplicationSerializer, SchoolRegistrationSerializer, ExamResultSerializer


class LoanApplicationViewSet(OwnerFilterMixin, viewsets.ModelViewSet):
    serializer_class = LoanApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]


class SchoolRegistrationViewSet(OwnerFilterMixin, viewsets.ModelViewSet):
    serializer_class = SchoolRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]


class ExamResultViewSet(OwnerFilterMixin, viewsets.ModelViewSet):
    serializer_class = ExamResultSerializer
    permission_classes = [permissions.IsAuthenticated]
