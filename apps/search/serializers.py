from rest_framework import serializers
from .models import SearchIndex, SearchQuery


class SearchIndexSerializer(serializers.ModelSerializer):
    content_type_name = serializers.CharField(source='content_type.model', read_only=True)

    class Meta:
        model = SearchIndex
        fields = '__all__'
        read_only_fields = ['last_indexed', 'created_at', 'updated_at']


class SearchQuerySerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = SearchQuery
        fields = '__all__'
        read_only_fields = ['user', 'results_count', 'created_at', 'updated_at']
