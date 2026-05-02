"""
Weather data via Open-Meteo free API (no API key required).

Covers 47 Kenyan county capitals.
"""
import logging
from django.core.cache import cache

logger = logging.getLogger(__name__)

CACHE_TTL = 1800  # 30 minutes

# County capitals with coordinates
COUNTY_COORDS = {
    '001': {'name': 'Mombasa', 'lat': -4.0435, 'lon': 39.6682},
    '002': {'name': 'Kwale', 'lat': -4.1737, 'lon': 39.4521},
    '003': {'name': 'Kilifi', 'lat': -3.6305, 'lon': 39.8499},
    '004': {'name': 'Tana River', 'lat': -1.5000, 'lon': 39.5000},
    '005': {'name': 'Lamu', 'lat': -2.2717, 'lon': 40.9020},
    '006': {'name': 'Taita Taveta', 'lat': -3.4000, 'lon': 38.3667},
    '007': {'name': 'Garissa', 'lat': -0.4536, 'lon': 39.6408},
    '008': {'name': 'Wajir', 'lat': 1.7471, 'lon': 40.0573},
    '009': {'name': 'Mandera', 'lat': 3.9371, 'lon': 41.8569},
    '010': {'name': 'Marsabit', 'lat': 2.3280, 'lon': 37.9899},
    '011': {'name': 'Isiolo', 'lat': 0.3546, 'lon': 37.5822},
    '012': {'name': 'Meru', 'lat': 0.0464, 'lon': 37.6559},
    '013': {'name': 'Tharaka Nithi', 'lat': -0.3000, 'lon': 37.9333},
    '014': {'name': 'Embu', 'lat': -0.5317, 'lon': 37.4500},
    '015': {'name': 'Kitui', 'lat': -1.3670, 'lon': 38.0106},
    '016': {'name': 'Machakos', 'lat': -1.5177, 'lon': 37.2634},
    '017': {'name': 'Makueni', 'lat': -1.8000, 'lon': 37.6167},
    '020': {'name': 'Kirinyaga', 'lat': -0.5000, 'lon': 37.2833},
    '021': {'name': 'Muranga', 'lat': -0.7167, 'lon': 37.1500},
    '022': {'name': 'Kiambu', 'lat': -1.1667, 'lon': 36.8333},
    '023': {'name': 'Turkana', 'lat': 3.1167, 'lon': 35.6000},
    '024': {'name': 'West Pokot', 'lat': 1.2333, 'lon': 35.0000},
    '025': {'name': 'Samburu', 'lat': 1.1667, 'lon': 36.6833},
    '026': {'name': 'Trans Nzoia', 'lat': 1.0833, 'lon': 34.9833},
    '027': {'name': 'Uasin Gishu', 'lat': 0.5167, 'lon': 35.2833},
    '028': {'name': 'Elgeyo Marakwet', 'lat': 0.5000, 'lon': 35.6000},
    '029': {'name': 'Nandi', 'lat': 0.1667, 'lon': 35.1500},
    '030': {'name': 'Baringo', 'lat': 0.4667, 'lon': 35.9667},
    '031': {'name': 'Laikipia', 'lat': 0.0000, 'lon': 36.6667},
    '032': {'name': 'Nakuru', 'lat': -0.2833, 'lon': 36.0667},
    '033': {'name': 'Narok', 'lat': -1.0833, 'lon': 35.8667},
    '034': {'name': 'Kajiado', 'lat': -1.8500, 'lon': 36.7833},
    '035': {'name': 'Kericho', 'lat': -0.3667, 'lon': 35.2833},
    '036': {'name': 'Bomet', 'lat': -0.7833, 'lon': 35.3500},
    '037': {'name': 'Kakamega', 'lat': 0.2833, 'lon': 34.7500},
    '038': {'name': 'Vihiga', 'lat': 0.0500, 'lon': 34.7333},
    '039': {'name': 'Bungoma', 'lat': 0.5667, 'lon': 34.5667},
    '040': {'name': 'Busia', 'lat': 0.4600, 'lon': 34.1117},
    '041': {'name': 'Siaya', 'lat': 0.0617, 'lon': 34.2881},
    '042': {'name': 'Kisumu', 'lat': -0.0917, 'lon': 34.7680},
    '043': {'name': 'Homa Bay', 'lat': -0.5167, 'lon': 34.4500},
    '044': {'name': 'Migori', 'lat': -1.0667, 'lon': 34.4667},
    '045': {'name': 'Kisii', 'lat': -0.6833, 'lon': 34.7667},
    '046': {'name': 'Nyamira', 'lat': -0.5833, 'lon': 34.9833},
    '047': {'name': 'Nairobi', 'lat': -1.2921, 'lon': 36.8219},
}


def fetch_county_weather(county_code):
    """Fetch current weather for a county capital from Open-Meteo."""
    coords = COUNTY_COORDS.get(county_code)
    if not coords:
        return None

    cache_key = f'weather_{county_code}'
    cached = cache.get(cache_key)
    if cached:
        return cached

    try:
        import httpx
    except ImportError:
        return None

    url = (
        f'https://api.open-meteo.com/v1/forecast'
        f'?latitude={coords["lat"]}&longitude={coords["lon"]}'
        f'&current=temperature_2m,weather_code,wind_speed_10m&timezone=Africa/Nairobi'
    )
    try:
        resp = httpx.get(url, timeout=10.0)
        resp.raise_for_status()
        data = resp.json()
        current = data.get('current', {})
        weather = {
            'name': coords['name'],
            'temperature': current.get('temperature_2m'),
            'weather_code': current.get('weather_code'),
            'wind_speed': current.get('wind_speed_10m'),
            'condition': _weather_desc(current.get('weather_code', 0)),
        }
        cache.set(cache_key, weather, CACHE_TTL)
        return weather
    except Exception as exc:
        logger.warning('Failed to fetch weather for %s: %s', coords['name'], exc)
        return None


def _weather_desc(code):
    """Map WMO weather codes to simple descriptions."""
    mapping = {
        0: 'Clear', 1: 'Mostly Clear', 2: 'Partly Cloudy', 3: 'Overcast',
        45: 'Fog', 48: 'Frost Fog',
        51: 'Light Drizzle', 53: 'Drizzle', 55: 'Heavy Drizzle',
        61: 'Light Rain', 63: 'Rain', 65: 'Heavy Rain',
        71: 'Light Snow', 73: 'Snow', 75: 'Heavy Snow',
        80: 'Light Showers', 81: 'Showers', 82: 'Heavy Showers',
        95: 'Thunderstorm', 96: 'Hail Thunderstorm', 99: 'Severe Thunderstorm',
    }
    return mapping.get(code, 'Unknown')
