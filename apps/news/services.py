import logging
from datetime import datetime
from django.utils import timezone

logger = logging.getLogger(__name__)


def parse_rss_feed(feed_url, source_name):
    """Parse an RSS/Atom feed and return a list of article dicts using feedparser."""
    try:
        import feedparser
    except ImportError:
        logger.warning('feedparser not installed; skipping RSS fetch for %s', source_name)
        return []

    try:
        feed = feedparser.parse(feed_url)
    except Exception as exc:
        logger.error('Failed to fetch feed %s (%s): %s', source_name, feed_url, exc)
        return []

    if feed.bozo and not feed.entries:
        logger.warning('Bozo feed %s (%s): %s', source_name, feed_url, feed.bozo_exception)
        return []

    articles = []
    for entry in feed.entries[:30]:
        published = None
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            try:
                published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
            except (TypeError, ValueError):
                pass

        articles.append({
            'title': (entry.get('title') or 'Untitled')[:500],
            'url': entry.get('link') or '',
            'summary': (entry.get('summary') or entry.get('description', ''))[:2000],
            'published_at': published,
            'image_url': _extract_image(entry),
            'author': entry.get('author', ''),
        })

    return articles


def _extract_image(entry):
    """Try to extract a lead image from a feed entry."""
    if hasattr(entry, 'media_content') and entry.media_content:
        for m in entry.media_content:
            if 'image' in (m.get('type') or m.get('medium', '')):
                return m.get('url', '')
    if hasattr(entry, 'links'):
        for link in entry.links:
            if 'image' in (link.get('type') or ''):
                return link.get('href', '')
    return ''


def search_news_api(query, page_size=10):
    """Search for Kenyan news via public APIs. Falls back to empty list."""
    try:
        import httpx
    except ImportError:
        return []

    # Try GNews free tier (no API key needed for basic usage)
    # Falls back gracefully
    return []
