"""
World Bank API client for Kenya economic indicators.

Free, no API key required. Rate-limited to ~1 req/sec.
"""
import logging
from django.core.cache import cache
from django.utils import timezone

logger = logging.getLogger(__name__)

WB_BASE = 'https://api.worldbank.org/v2'
CACHE_KEY = 'world_bank_indicators'
CACHE_TTL = 86400  # 24 hours

INDICATORS = {
    'NY.GDP.MKTP.KD.ZG': 'gdp_growth',
    'FP.CPI.TOTL.ZG': 'inflation_rate',
    'SP.POP.TOTL': 'population',
    'SL.UEM.TOTL.ZS': 'unemployment_rate',
    'GC.DOD.TOTL.GD.ZS': 'public_debt_to_gdp',
}

FALLBACK = {
    'inflation_rate': 5.1,
    'gdp_growth': 5.4,
    'population': 56000000,
    'unemployment_rate': 4.9,
    'public_debt_to_gdp': 68.4,
    'cbr_rate': 10.00,
    'foreign_exchange_reserves': 7.2,
}


def fetch_world_bank_indicators():
    """Fetch Kenya indicators from World Bank API."""
    try:
        import httpx
    except ImportError:
        logger.info('httpx not installed; using fallback indicators')
        return None

    indicators = {}
    for wb_code, our_key in INDICATORS.items():
        url = f'{WB_BASE}/country/KE/indicator/{wb_code}?format=json&per_page=1&MRV=1'
        try:
            resp = httpx.get(url, timeout=15.0)
            resp.raise_for_status()
            data = resp.json()
            if isinstance(data, list) and len(data) > 1 and data[1]:
                val = data[1][0].get('value')
                if val is not None:
                    indicators[our_key] = float(val)
        except Exception as exc:
            logger.warning('Failed to fetch %s from World Bank: %s', wb_code, exc)

    if not indicators:
        return None

    indicators['last_updated'] = timezone.now().strftime('%Y-%m-%d')
    cache.set(CACHE_KEY, indicators, CACHE_TTL)
    return indicators


def get_world_bank_indicators():
    """Return economic indicators: cache → live fetch → fallback."""
    cached = cache.get(CACHE_KEY)
    if cached:
        return cached

    live = fetch_world_bank_indicators()
    if live:
        # Merge with fallback for any missing indicators
        full = dict(FALLBACK)
        full.update(live)
        full['last_updated'] = live.get('last_updated', timezone.now().strftime('%Y-%m-%d'))
        return full

    fallback = dict(FALLBACK)
    fallback['last_updated'] = timezone.now().strftime('%Y-%m-%d')
    return fallback
