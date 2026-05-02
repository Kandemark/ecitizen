from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from core.models import TimestampMixin


class SearchIndex(TimestampMixin):
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name='search_indexes'
    )
    object_id = models.PositiveIntegerField()
    related_object = GenericForeignKey('content_type', 'object_id')
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    indexed_data = models.JSONField(default=dict, blank=True)
    last_indexed = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Search Indexes'
        ordering = ['-last_indexed']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['last_indexed']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['content_type', 'object_id'],
                name='unique_search_index_entry'
            ),
        ]

    def __str__(self):
        return f'SearchIndex: {self.title}'


class SearchQuery(TimestampMixin):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='search_queries'
    )
    query = models.TextField()
    results_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Search Queries'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        user_display = self.user.username if self.user else 'Anonymous'
        return f'"{self.query}" by {user_display} ({self.results_count} results)'
