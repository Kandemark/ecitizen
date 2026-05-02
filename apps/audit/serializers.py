from rest_framework import serializers
from .models import AuditEntry, ComplianceCheck, DataAccessLog


class AuditEntrySerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    content_type_name = serializers.CharField(source='content_type.model', read_only=True)

    class Meta:
        model = AuditEntry
        fields = '__all__'
        read_only_fields = ['user', 'timestamp']


class ComplianceCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplianceCheck
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class DataAccessLogSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = DataAccessLog
        fields = '__all__'
        read_only_fields = ['user', 'accessed_at']
