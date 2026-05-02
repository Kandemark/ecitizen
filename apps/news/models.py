from django.db import models
from core.models import TimestampMixin


class NewsSource(TimestampMixin):
    name = models.CharField(max_length=200)
    url = models.URLField()
    feed_url = models.URLField(unique=True)
    is_active = models.BooleanField(default=True)
    last_fetched = models.DateTimeField(null=True, blank=True)
    fetch_error = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class NewsArticle(TimestampMixin):
    source = models.ForeignKey(NewsSource, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=500)
    url = models.URLField(unique=True)
    summary = models.TextField(blank=True)
    published_at = models.DateTimeField(null=True, blank=True, db_index=True)
    image_url = models.URLField(blank=True)
    author = models.CharField(max_length=200, blank=True)
    is_kenya_related = models.BooleanField(default=True)

    class Meta:
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title
