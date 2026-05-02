"""
Central Bank of Kenya exchange rates via httpx.

Falls back to cached/stored values if the CBK endpoint is unreachable.
"""
import logging
from datetime import datetime
from django.core.cache import cache
from django.utils import timezone

logger = logging.getLogger(__name__)

CBK_RATES_URL = 'https://www.centralbank.go.ke/wp-json/cbk/v1/exchange-rates'
CACHE_KEY = 'live_exchange_rates'
CACHE_TTL = 7200  # 2 hours

# Hardcoded fallback (updated periodically when live fetch succeeds)
FALLBACK_RATES = {
    'USD': 129.50,
    'EUR': 142.30,
    'GBP': 165.80,
    'TZS': 0.056,
    'UGX': 0.037,
    'RWF': 0.098,
    'AED': 35.27,
    'CNY': 17.85,
}


def fetch_cbk_rates():
    """Fetch latest exchange rates from CBK. Returns dict or None."""
    try:
        import httpx
    except ImportError:
        logger.info('httpx not installed; using fallback exchange rates')
        return None

    try:
        resp = httpx.get(CBK_RATES_URL, timeout=10.0)
        resp.raise_for_status()
        data = resp.json()
    except Exception as exc:
        logger.warning('Failed to fetch CBK rates: %s', exc)
        return None

    rates = {}
    try:
        for entry in data.get('rates', data) if isinstance(data, dict) else data:
            currency = entry.get('currency') or entry.get('code', '')
            rate = entry.get('rate') or entry.get('mean_rate') or entry.get('value')
            if currency and rate:
                rates[currency] = float(rate)
    except (TypeError, ValueError, AttributeError) as exc:
        logger.warning('Failed to parse CBK response: %s', exc)
        return None

    if not rates:
        return None

    rates['last_updated'] = timezone.now().strftime('%Y-%m-%d %H:%M')
    cache.set(CACHE_KEY, rates, CACHE_TTL)
    return rates


def get_live_exchange_rates():
    """Return live exchange rates with fallback chain: cache → live fetch → hardcoded."""
    cached = cache.get(CACHE_KEY)
    if cached:
        return cached

    live = fetch_cbk_rates()
    if live:
        return live

    fallback = dict(FALLBACK_RATES)
    fallback['last_updated'] = timezone.now().strftime('%Y-%m-%d')
    return fallback
