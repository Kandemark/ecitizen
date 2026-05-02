from rest_framework import serializers
from .models import ExternalSystem, DataExchange, SyncLog


class ExternalSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalSystem
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class SyncLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SyncLog
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class DataExchangeSerializer(serializers.ModelSerializer):
    system_name = serializers.CharField(source='system.name', read_only=True)
    sync_logs = SyncLogSerializer(many=True, read_only=True)

    class Meta:
        model = DataExchange
        fields = '__all__'
        read_only_fields = ['status', 'completed_at', 'created_at', 'updated_at']
