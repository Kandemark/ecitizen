from rest_framework import serializers
from .models import Application, FormField, ApplicationDocument, StatusHistory


class FormFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormField
        fields = ['id', 'label', 'field_type', 'is_required', 'options', 'placeholder', 'help_text', 'order']


class StatusHistorySerializer(serializers.ModelSerializer):
    changed_by_name = serializers.CharField(source='changed_by.username', read_only=True)

    class Meta:
        model = StatusHistory
        fields = ['id', 'status', 'comment', 'changed_by', 'changed_by_name', 'created_at']


class ApplicationDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationDocument
        fields = ['id', 'document_type', 'file', 'original_filename', 'is_verified', 'created_at']
        read_only_fields = ['is_verified']


class ApplicationSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source='service.name', read_only=True)
    status_history = StatusHistorySerializer(many=True, read_only=True)
    documents = ApplicationDocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Application
        fields = [
            'id', 'user', 'service', 'service_name', 'reference', 'status',
            'form_data', 'county', 'documents', 'status_history',
            'submitted_at', 'completed_at', 'created_at', 'updated_at',
        ]
        read_only_fields = ['reference', 'status', 'submitted_at', 'completed_at']

    def create(self, validated_data):
        from core.utils import generate_application_reference
        validated_data['user'] = self.context['request'].user
        validated_data['reference'] = generate_application_reference()
        application = super().create(validated_data)
        StatusHistory.objects.create(
            application=application, status='draft',
            changed_by=validated_data['user'],
            comment='Application created.'
        )
        return application
