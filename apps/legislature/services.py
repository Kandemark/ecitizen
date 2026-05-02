import logging
from datetime import date, timedelta, datetime
from typing import Optional

import httpx

logger = logging.getLogger(__name__)

PARLIAMENT_BASE = 'https://api.parliament.go.ke/v1'
BILLS_URL = f'{PARLIAMENT_BASE}/bills'
HANSARDS_URL = f'{PARLIAMENT_BASE}/hansards'
COMMITTEES_URL = f'{PARLIAMENT_BASE}/committees'
SITTINGS_URL = f'{PARLIAMENT_BASE}/sittings'

TIMEOUT = 30.0


def _client() -> httpx.Client:
    return httpx.Client(timeout=TIMEOUT, headers={
        'Accept': 'application/json',
        'User-Agent': 'eCitizen-Kenya/1.0',
    })


def _parse_date(d: Optional[str]) -> Optional[date]:
    if not d:
        return None
    for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%B %d, %Y'):
        try:
            return date.fromisoformat(d) if fmt == '%Y-%m-%d' else \
                   datetime.strptime(d, fmt).date()
        except (ValueError, TypeError):
            continue
    return None


def fetch_bills(house: str = 'national_assembly', status: Optional[str] = None,
                since: Optional[date] = None) -> list[dict]:
    """
    Fetch bills from the Kenya Parliament API.

    Returns list of dicts with keys matching the Bill model fields.
    Falls back to an empty list if the API is unreachable.
    """
    params = {'house': house}
    if status:
        params['status'] = status
    if since:
        params['since'] = since.isoformat()

    try:
        with _client() as client:
            resp = client.get(BILLS_URL, params=params)
            resp.raise_for_status()
            data = resp.json()
            results = data.get('results') or data.get('data') or []
            return [_normalise_bill(b) for b in results]
    except Exception as exc:
        logger.warning('Failed to fetch bills from Parliament API: %s', exc)
        return []


def fetch_hansards(house: str = 'national_assembly',
                   since: Optional[date] = None) -> list[dict]:
    params = {'house': house}
    if since:
        params['since'] = since.isoformat()
    try:
        with _client() as client:
            resp = client.get(HANSARDS_URL, params=params)
            resp.raise_for_status()
            data = resp.json()
            results = data.get('results') or data.get('data') or []
            return [_normalise_hansard(h) for h in results]
    except Exception as exc:
        logger.warning('Failed to fetch hansards from Parliament API: %s', exc)
        return []


def fetch_committee_reports(since: Optional[date] = None) -> list[dict]:
    params = {}
    if since:
        params['since'] = since.isoformat()
    try:
        with _client() as client:
            resp = client.get(COMMITTEES_URL, params=params)
            resp.raise_for_status()
            data = resp.json()
            results = data.get('results') or data.get('data') or []
            return [_normalise_report(r) for r in results]
    except Exception as exc:
        logger.warning('Failed to fetch committee reports from Parliament API: %s', exc)
        return []


def fetch_sittings(house: str = 'national_assembly',
                   since: Optional[date] = None) -> list[dict]:
    params = {'house': house}
    if since:
        params['since'] = since.isoformat()
    try:
        with _client() as client:
            resp = client.get(SITTINGS_URL, params=params)
            resp.raise_for_status()
            data = resp.json()
            results = data.get('results') or data.get('data') or []
            return [_normalise_sitting(s) for s in results]
    except Exception as exc:
        logger.warning('Failed to fetch sittings from Parliament API: %s', exc)
        return []


# --- Normalisers ---

def _normalise_bill(b: dict) -> dict:
    return {
        'source_id': str(b.get('id') or b.get('bill_id', '')),
        'title': b.get('title', ''),
        'number': str(b.get('number') or b.get('bill_no', '')),
        'house': b.get('house', 'national_assembly').lower().replace(' ', '_'),
        'sponsor': b.get('sponsor', ''),
        'status': _map_bill_status(b.get('status', '')),
        'summary': b.get('summary') or b.get('description', ''),
        'date_introduced': _parse_date(b.get('date_introduced') or b.get('introduced_date')),
        'date_passed': _parse_date(b.get('date_passed') or b.get('passed_date')),
        'date_assented': _parse_date(b.get('date_assented') or b.get('assented_date')),
        'full_text_url': b.get('full_text_url') or b.get('document_url', ''),
    }


def _normalise_hansard(h: dict) -> dict:
    return {
        'source_id': str(h.get('id') or h.get('hansard_id', '')),
        'title': h.get('title', ''),
        'date': _parse_date(h.get('date')) or date.today(),
        'house': h.get('house', 'national_assembly').lower().replace(' ', '_'),
        'sitting_number': str(h.get('sitting_number') or h.get('sitting_no', '')),
        'content': h.get('content') or h.get('text', ''),
        'summary': h.get('summary', ''),
        'source_url': h.get('url') or h.get('source_url', ''),
    }


def _normalise_report(r: dict) -> dict:
    return {
        'source_id': str(r.get('id') or r.get('report_id', '')),
        'committee_name': r.get('committee') or r.get('committee_name', ''),
        'title': r.get('title', ''),
        'date_published': _parse_date(r.get('date_published') or r.get('date')),
        'summary': r.get('summary') or r.get('description', ''),
        'recommendations': r.get('recommendations', ''),
        'full_text_url': r.get('full_text_url') or r.get('document_url', ''),
    }


def _normalise_sitting(s: dict) -> dict:
    return {
        'source_id': str(s.get('id') or s.get('sitting_id', '')),
        'date': _parse_date(s.get('date')) or date.today(),
        'house': s.get('house', 'national_assembly').lower().replace(' ', '_'),
        'session': s.get('session', ''),
        'agenda': s.get('agenda') or s.get('order_business', ''),
        'minutes_url': s.get('minutes_url', ''),
        'order_paper_url': s.get('order_paper_url') or s.get('order_paper', ''),
    }


def _map_bill_status(raw: str) -> str:
    mapping = {
        'draft': 'draft',
        'first reading': 'first_reading',
        'first_reading': 'first_reading',
        'second reading': 'second_reading',
        'second_reading': 'second_reading',
        'committee': 'committee',
        'committee stage': 'committee',
        'report': 'report',
        'report stage': 'report',
        'third reading': 'third_reading',
        'third_reading': 'third_reading',
        'passed': 'passed',
        'assented': 'assented',
        'assented to': 'assented',
        'rejected': 'rejected',
        'withdrawn': 'withdrawn',
    }
    return mapping.get(raw.lower().strip(), 'draft')
