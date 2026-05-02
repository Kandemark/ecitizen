from rest_framework import serializers
from .models import Consultation, PublicComment, Petition


class ConsultationSerializer(serializers.ModelSerializer):
    ministry_name = serializers.CharField(source='ministry.name', read_only=True)
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Consultation
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def get_comment_count(self, obj):
        return obj.comments.filter(is_approved=True).count()


class PublicCommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    consultation_title = serializers.CharField(source='consultation.title', read_only=True)

    class Meta:
        model = PublicComment
        fields = '__all__'
        read_only_fields = ['user', 'is_approved', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class PetitionSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    ministry_name = serializers.CharField(source='target_ministry.name', read_only=True)
    progress = serializers.SerializerMethodField()

    class Meta:
        model = Petition
        fields = '__all__'
        read_only_fields = [
            'user', 'reference', 'signature_count', 'status',
            'created_at', 'updated_at'
        ]

    def get_progress(self, obj):
        if obj.threshold > 0:
            return round((obj.signature_count / obj.threshold) * 100, 1)
        return 0.0

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
