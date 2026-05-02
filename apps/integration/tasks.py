import logging
from celery import shared_task
from .services.exchange_rates import fetch_cbk_rates
from .services.world_bank import fetch_world_bank_indicators
from .services.weather import fetch_county_weather, COUNTY_COORDS

logger = logging.getLogger(__name__)


@shared_task
def refresh_economic_data():
    """Refresh exchange rates and World Bank indicators."""
    rates = fetch_cbk_rates()
    indicators = fetch_world_bank_indicators()
    return {
        'rates_updated': rates is not None,
        'indicators_updated': indicators is not None,
    }


@shared_task
def fetch_cbk_exchange_rates():
    """Fetch latest CBK exchange rates."""
    result = fetch_cbk_rates()
    return 'updated' if result else 'fallback'


@shared_task
def refresh_all_weather():
    """Fetch weather for all 47 Kenyan county capitals."""
    updated = 0
    for code in COUNTY_COORDS:
        weather = fetch_county_weather(code)
        if weather:
            updated += 1
    logger.info('Weather refreshed for %d counties', updated)
    return f'{updated}/47 counties updated'


@shared_task
def refresh_county_weather(county_code):
    """Fetch weather for a single county."""
    weather = fetch_county_weather(county_code)
    return weather['name'] if weather else 'failed'
