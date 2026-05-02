from rest_framework import serializers
from .models import EmergencyContact, EmergencyReport


class EmergencyContactSerializer(serializers.ModelSerializer):
    service_type_display = serializers.CharField(
        source='get_service_type_display', read_only=True
    )

    class Meta:
        model = EmergencyContact
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class EmergencyReportSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    emergency_type_display = serializers.CharField(
        source='get_emergency_type_display', read_only=True
    )

    class Meta:
        model = EmergencyReport
        fields = '__all__'
        read_only_fields = ['user', 'reference', 'status', 'reported_at', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
