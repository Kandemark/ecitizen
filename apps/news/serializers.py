from rest_framework import serializers
from .models import NewsArticle, NewsSource


class NewsSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsSource
        fields = ['id', 'name', 'url', 'is_active', 'last_fetched']


class NewsArticleSerializer(serializers.ModelSerializer):
    source_name = serializers.CharField(source='source.name', read_only=True)

    class Meta:
        model = NewsArticle
        fields = [
            'id', 'source', 'source_name', 'title', 'url',
            'summary', 'published_at', 'image_url', 'author',
            'created_at',
        ]
