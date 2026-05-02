import logging
from datetime import timedelta
from django.utils import timezone
from celery import shared_task

from .models import NewsSource, NewsArticle
from .services import parse_rss_feed

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=2, default_retry_delay=300)
def fetch_news_source(self, source_id):
    """Fetch articles from a single news source."""
    try:
        source = NewsSource.objects.get(id=source_id, is_active=True)
    except NewsSource.DoesNotExist:
        return

    articles = parse_rss_feed(source.feed_url, source.name)

    if not articles:
        source.last_fetched = timezone.now()
        source.save(update_fields=['last_fetched'])
        return f'{source.name}: no articles found'

    created = 0
    for article_data in articles:
        if not article_data['url']:
            continue
        _, is_new = NewsArticle.objects.get_or_create(
            url=article_data['url'],
            defaults={
                'source': source,
                'title': article_data['title'],
                'summary': article_data['summary'],
                'published_at': article_data['published_at'] or timezone.now(),
                'image_url': article_data['image_url'],
                'author': article_data['author'],
            },
        )
        if is_new:
            created += 1

    source.last_fetched = timezone.now()
    source.fetch_error = ''
    source.save(update_fields=['last_fetched', 'fetch_error'])

    logger.info('Fetched %s: %d new articles (total %d entries)', source.name, created, len(articles))
    return f'{source.name}: {created} new articles'


@shared_task
def fetch_all_news_sources():
    """Fetch articles from all active news sources."""
    source_ids = NewsSource.objects.filter(is_active=True).values_list('id', flat=True)
    if not source_ids:
        return 'No active news sources'

    for sid in source_ids:
        fetch_news_source.delay(sid)

    return f'Enqueued {len(source_ids)} news source fetches'


@shared_task
def cleanup_old_articles(days=90):
    """Remove articles older than the given number of days."""
    cutoff = timezone.now() - timedelta(days=days)
    deleted, _ = NewsArticle.objects.filter(published_at__lt=cutoff).delete()
    logger.info('Cleaned up %d old news articles (older than %d days)', deleted, days)
    return f'Deleted {deleted} articles'
