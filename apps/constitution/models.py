from django.db import models


class Chapter(models.Model):
    """A chapter of the Constitution of Kenya, 2010."""
    number = models.PositiveSmallIntegerField(unique=True, db_index=True)
    title = models.CharField(max_length=300)
    subtitle = models.CharField(max_length=500, blank=True)
    overview = models.TextField(blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order', 'number']

    def __str__(self):
        return f'Chapter {self.number} — {self.title}'

    @property
    def article_count(self):
        return self.articles.count()


class Article(models.Model):
    """A constitutional article within a chapter."""
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='articles')
    number = models.CharField(max_length=20, db_index=True)
    title = models.CharField(max_length=500)
    content = models.TextField()
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['chapter', 'order']
        indexes = [
            models.Index(fields=['chapter', 'order']),
        ]

    def __str__(self):
        return f'Article {self.number} — {self.title}'


class Schedule(models.Model):
    """A schedule appended to the Constitution."""
    number = models.PositiveSmallIntegerField(unique=True, db_index=True)
    title = models.CharField(max_length=300)
    content = models.TextField()
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order', 'number']

    def __str__(self):
        return f'Schedule {self.number} — {self.title}'
