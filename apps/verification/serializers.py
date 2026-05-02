from rest_framework import serializers
from .models import VerificationRequest, VerificationResult


class VerificationResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationResult
        fields = ['is_match', 'confidence_score', 'details']


class VerificationRequestSerializer(serializers.ModelSerializer):
    result = VerificationResultSerializer(read_only=True)

    class Meta:
        model = VerificationRequest
        fields = ['id', 'id_number', 'id_type', 'status', 'result', 'verified_at', 'created_at']
        read_only_fields = ['status', 'verified_at', 'verified_by']
