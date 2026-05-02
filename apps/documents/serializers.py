from rest_framework import serializers
from .models import Document, DocumentShare


class DocumentShareSerializer(serializers.ModelSerializer):
    shared_with_username = serializers.CharField(source='shared_with.username', read_only=True)

    class Meta:
        model = DocumentShare
        fields = ['id', 'shared_with', 'shared_with_username', 'can_view', 'can_download', 'expires_at']


class DocumentSerializer(serializers.ModelSerializer):
    shares = DocumentShareSerializer(many=True, read_only=True)

    class Meta:
        model = Document
        fields = ['id', 'name', 'file', 'file_size', 'mime_type', 'is_verified', 'tags', 'shares', 'created_at']
        read_only_fields = ['id', 'file_size', 'mime_type', 'is_verified']
