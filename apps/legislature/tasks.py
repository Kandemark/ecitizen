import logging
from datetime import date, timedelta

from celery import shared_task
from django.utils import timezone

from .services import fetch_bills, fetch_hansards, fetch_committee_reports, fetch_sittings
from .models import Bill, Hansard, CommitteeReport, ParliamentarySitting

logger = logging.getLogger(__name__)


def _upsert(model, lookup_field: str, defaults: dict, source_id: str | None):
    """Insert or update a record keyed by source_id."""
    if not source_id:
        return None
    obj, created = model.objects.update_or_create(
        **{lookup_field: source_id},
        defaults=defaults,
    )
    return obj


@shared_task(name='legislature.sync_bills')
def sync_bills():
    since = date.today() - timedelta(days=90)
    count = 0
    for house in ('national_assembly', 'senate'):
        bills = fetch_bills(house=house, since=since)
        for b in bills:
            if not b.get('source_id'):
                continue
            _upsert(Bill, 'source_id', b, b['source_id'])
            count += 1
    logger.info('Synced %d bills from Parliament API', count)
    return count


@shared_task(name='legislature.sync_hansards')
def sync_hansards():
    since = date.today() - timedelta(days=30)
    count = 0
    for house in ('national_assembly', 'senate'):
        records = fetch_hansards(house=house, since=since)
        for h in records:
            if not h.get('source_id'):
                continue
            _upsert(Hansard, 'source_id', h, h['source_id'])
            count += 1
    logger.info('Synced %d hansard records from Parliament API', count)
    return count


@shared_task(name='legislature.sync_committee_reports')
def sync_committee_reports():
    since = date.today() - timedelta(days=180)
    reports = fetch_committee_reports(since=since)
    count = 0
    for r in reports:
        if not r.get('source_id'):
            continue
        _upsert(CommitteeReport, 'source_id', r, r['source_id'])
        count += 1
    logger.info('Synced %d committee reports from Parliament API', count)
    return count


@shared_task(name='legislature.sync_sittings')
def sync_sittings():
    since = date.today() - timedelta(days=14)
    count = 0
    for house in ('national_assembly', 'senate'):
        sittings = fetch_sittings(house=house, since=since)
        for s in sittings:
            if not s.get('source_id'):
                continue
            _upsert(ParliamentarySitting, 'source_id', s, s['source_id'])
            count += 1
    logger.info('Synced %d parliamentary sittings from Parliament API', count)
    return count


@shared_task(name='legislature.sync_all_parliament_data')
def sync_all_parliament_data():
    """Master task that triggers all parliament data syncs."""
    bills = sync_bills()
    hansards = sync_hansards()
    reports = sync_committee_reports()
    sittings = sync_sittings()
    total = bills + hansards + reports + sittings
    logger.info('Full parliament sync complete: %d total records (bills=%d, hansards=%d, reports=%d, sittings=%d)',
                total, bills, hansards, reports, sittings)
    return total
