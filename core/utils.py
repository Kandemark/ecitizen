import uuid
import random
import string
from datetime import datetime
from django.utils import timezone


def generate_tracking_id(prefix='ECZ'):
    """Generate a unique tracking ID like ECZ-20260501-ABCD1234."""
    date_part = timezone.now().strftime('%Y%m%d')
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return f'{prefix}-{date_part}-{random_part}'


def generate_receipt_number():
    """Generate a unique receipt number for payments."""
    return generate_tracking_id(prefix='RCP')


def generate_application_reference():
    """Generate a unique application reference number."""
    return generate_tracking_id(prefix='APP')


def kenyan_phone_validator(phone):
    """Validate Kenyan phone number format (Safaricom/Airtel/Telkom)."""
    phone = str(phone).strip().lstrip('+')
    if phone.startswith('254'):
        phone = phone[3:]
    if phone.startswith('0'):
        phone = phone[1:]
    if len(phone) != 9:
        return False
    prefixes = [
        '10', '11', '12',  # Safaricom
        '70', '71', '72', '74', '75', '76', '77', '78', '79',  # Mobile
        '20', '21', '22',  # Fixed
    ]
    return any(phone.startswith(p) for p in prefixes)


def format_currency(amount):
    """Format amount in KES."""
    return f'KES {amount:,.2f}'
