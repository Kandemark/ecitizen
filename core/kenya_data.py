"""
Kenya public data accessors.

Each getter follows a cache → live-fetch → hardcoded-fallback chain.
Hardcoded values are the last-resort fallback for when external APIs are unreachable.
"""
from django.core.cache import cache

# ── Hardcoded fallbacks (used only when live services are down) ──────────

_FALLBACK_INDICATORS = {
    'inflation_rate': 5.1,
    'gdp_growth': 5.4,
    'population': 56000000,
    'unemployment_rate': 4.9,
    'public_debt_to_gdp': 68.4,
    'cbr_rate': 10.00,
    'foreign_exchange_reserves': 7.2,
}

_FALLBACK_RATES = {
    'USD': 129.50,
    'EUR': 142.30,
    'GBP': 165.80,
    'TZS': 0.056,
    'UGX': 0.037,
    'RWF': 0.098,
    'AED': 35.27,
    'CNY': 17.85,
}


def get_economic_indicators():
    """Return KNBS/CBK economic indicators via World Bank API, cached 24h."""
    indicators = cache.get('kenya_economic_indicators')
    if indicators:
        return indicators

    try:
        from apps.integration.services.world_bank import get_world_bank_indicators
        live = get_world_bank_indicators()
        if live:
            cache.set('kenya_economic_indicators', live, 86400)
            return live
    except Exception:
        pass

    fallback = dict(_FALLBACK_INDICATORS)
    fallback['last_updated'] = '2026-04-15'
    cache.set('kenya_economic_indicators', fallback, 3600)
    return fallback


def get_exchange_rates():
    """Return CBK indicative exchange rates, cached 6h."""
    rates = cache.get('kenya_exchange_rates')
    if rates:
        return rates

    try:
        from apps.integration.services.exchange_rates import get_live_exchange_rates
        live = get_live_exchange_rates()
        if live:
            cache.set('kenya_exchange_rates', live, 21600)
            return live
    except Exception:
        pass

    fallback = dict(_FALLBACK_RATES)
    fallback['last_updated'] = '2026-04-30'
    cache.set('kenya_exchange_rates', fallback, 3600)
    return fallback
