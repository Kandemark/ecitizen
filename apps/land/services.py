"""
Land services — title deeds, land searches, and transfers.

Constitutional mandate: Chapter 5 (Land and Environment, Art. 60-68) — principles
of land policy, classification of land, and land rights administration.
"""
from decimal import Decimal
from core.utils import generate_application_reference
from .models import TitleDeed, LandSearch, Transfer


def submit_title_deed(*, user, title_number, property_location, county_id=None,
                       land_size_hectares=Decimal('0'), tenure_type='freehold',
                       registered_owner_name='', **kwargs):
    ref = generate_application_reference('TTL')
    deed = TitleDeed.objects.create(
        user=user, reference=ref,
        title_number=title_number, property_location=property_location,
        county_id=county_id, land_size_hectares=land_size_hectares,
        tenure_type=tenure_type, registered_owner_name=registered_owner_name,
        status='draft',
    )
    deed.status = 'submitted'
    deed.save(update_fields=['status'])
    return deed


def submit_land_search(*, user, title_number, search_purpose, **kwargs):
    ref = generate_application_reference('LSR')
    search = LandSearch.objects.create(
        user=user, reference=ref,
        title_number=title_number, search_purpose=search_purpose,
        status='draft',
    )
    search.status = 'submitted'
    search.save(update_fields=['status'])
    return search


def submit_transfer(*, user, title_deed_id, from_owner, to_owner,
                     consideration_amount=Decimal('0'), transfer_type='sale', **kwargs):
    ref = generate_application_reference('TRF')
    transfer = Transfer.objects.create(
        user=user, reference=ref,
        title_deed_id=title_deed_id, from_owner=from_owner,
        to_owner=to_owner, consideration_amount=consideration_amount,
        transfer_type=transfer_type,
        status='draft',
    )
    transfer.status = 'submitted'
    transfer.save(update_fields=['status'])
    return transfer


def get_user_land_records(user):
    return {
        'title_deeds': TitleDeed.objects.filter(user=user).order_by('-created_at'),
        'land_searches': LandSearch.objects.filter(user=user).order_by('-created_at'),
        'transfers': Transfer.objects.filter(user=user).order_by('-created_at'),
    }
