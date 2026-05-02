import logging
import base64
import json
from datetime import datetime
from decimal import Decimal
from django.conf import settings
from django.utils import timezone
from django.db import transaction as db_transaction

logger = logging.getLogger(__name__)


class MpesaGateway:
    """Safaricom M-Pesa Daraja API integration for STK Push and B2C."""

    CONSUMER_KEY = getattr(settings, 'MPESA_CONSUMER_KEY', '')
    CONSUMER_SECRET = getattr(settings, 'MPESA_CONSUMER_SECRET', '')
    PASSKEY = getattr(settings, 'MPESA_PASSKEY', '')
    SHORTCODE = getattr(settings, 'MPESA_SHORTCODE', '174379')
    CALLBACK_BASE = getattr(settings, 'MPESA_CALLBACK_BASE', '')
    ENVIRONMENT = getattr(settings, 'MPESA_ENVIRONMENT', 'sandbox')

    @classmethod
    def _base_url(cls):
        if cls.ENVIRONMENT == 'production':
            return 'https://api.safaricom.co.ke'
        return 'https://sandbox.safaricom.co.ke'

    @classmethod
    def _auth_token(cls):
        """Get OAuth access token from Safaricom."""
        try:
            import httpx
        except ImportError:
            logger.error('httpx required for M-Pesa integration')
            return None

        auth = base64.b64encode(
            f'{cls.CONSUMER_KEY}:{cls.CONSUMER_SECRET}'.encode()
        ).decode()

        try:
            resp = httpx.get(
                f'{cls._base_url()}/oauth/v1/generate?grant_type=client_credentials',
                headers={'Authorization': f'Basic {auth}'},
                timeout=30,
            )
            if resp.status_code == 200:
                return resp.json().get('access_token')
            logger.error(f'M-Pesa auth failed: {resp.status_code} {resp.text}')
        except Exception as e:
            logger.error(f'M-Pesa auth error: {e}')

        return None

    @classmethod
    def stk_push(cls, phone_number, amount, account_reference, description=''):
        """
        Initiate M-Pesa STK Push (Lipa Na M-Pesa Online).

        Args:
            phone_number: Format 2547XXXXXXXX
            amount: Decimal or float
            account_reference: Your internal transaction reference
            description: Short description of payment

        Returns:
            dict with CheckoutRequestID, MerchantRequestID, ResponseCode, etc.
        """
        try:
            import httpx
        except ImportError:
            return {'error': 'httpx required', 'ResponseCode': '1'}

        token = cls._auth_token()
        if not token:
            return {'error': 'Auth failed', 'ResponseCode': '1'}

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode(
            f'{cls.SHORTCODE}{cls.PASSKEY}{timestamp}'.encode()
        ).decode()

        payload = {
            'BusinessShortCode': cls.SHORTCODE,
            'Password': password,
            'Timestamp': timestamp,
            'TransactionType': 'CustomerPayBillOnline',
            'Amount': int(float(amount)),
            'PartyA': str(phone_number),
            'PartyB': cls.SHORTCODE,
            'PhoneNumber': str(phone_number),
            'CallBackURL': f'{cls.CALLBACK_BASE}/api/v1/payments/mpesa/callback/',
            'AccountReference': str(account_reference)[:12],
            'TransactionDesc': (description or 'e-Citizen Payment')[:13],
        }

        try:
            resp = httpx.post(
                f'{cls._base_url()}/mpesa/stkpush/v1/processrequest',
                json=payload,
                headers={
                    'Authorization': f'Bearer {token}',
                    'Content-Type': 'application/json',
                },
                timeout=30,
            )
            return resp.json()
        except Exception as e:
            logger.error(f'STK Push error: {e}')
            return {'error': str(e), 'ResponseCode': '1'}

    @classmethod
    def stk_query(cls, checkout_request_id):
        """Query the status of an STK Push transaction."""
        try:
            import httpx
        except ImportError:
            return {'error': 'httpx required'}

        token = cls._auth_token()
        if not token:
            return {'error': 'Auth failed'}

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode(
            f'{cls.SHORTCODE}{cls.PASSKEY}{timestamp}'.encode()
        ).decode()

        payload = {
            'BusinessShortCode': cls.SHORTCODE,
            'Password': password,
            'Timestamp': timestamp,
            'CheckoutRequestID': checkout_request_id,
        }

        try:
            resp = httpx.post(
                f'{cls._base_url()}/mpesa/stkpushquery/v1/query',
                json=payload,
                headers={
                    'Authorization': f'Bearer {token}',
                    'Content-Type': 'application/json',
                },
                timeout=30,
            )
            return resp.json()
        except Exception as e:
            logger.error(f'STK Query error: {e}')
            return {'error': str(e)}

    @classmethod
    def b2c_payment(cls, phone_number, amount, reference, description='Refund'):
        """
        Send money from business to customer (B2C) — used for refunds.

        Args:
            phone_number: Format 2547XXXXXXXX
            amount: Decimal
            reference: Internal transaction reference
            description: Payment description
        """
        try:
            import httpx
        except ImportError:
            return {'error': 'httpx required'}

        token = cls._auth_token()
        if not token:
            return {'error': 'Auth failed'}

        payload = {
            'OriginatorConversationID': reference,
            'InitiatorName': getattr(settings, 'MPESA_INITIATOR_NAME', ''),
            'SecurityCredential': getattr(settings, 'MPESA_SECURITY_CREDENTIAL', ''),
            'CommandID': 'BusinessPayment',
            'Amount': int(float(amount)),
            'PartyA': cls.SHORTCODE,
            'PartyB': str(phone_number),
            'Remarks': description[:100],
            'QueueTimeOutURL': f'{cls.CALLBACK_BASE}/api/v1/payments/mpesa/b2c-timeout/',
            'ResultURL': f'{cls.CALLBACK_BASE}/api/v1/payments/mpesa/b2c-result/',
            'Occasion': description[:100],
        }

        try:
            resp = httpx.post(
                f'{cls._base_url()}/mpesa/b2c/v1/paymentrequest',
                json=payload,
                headers={
                    'Authorization': f'Bearer {token}',
                    'Content-Type': 'application/json',
                },
                timeout=30,
            )
            return resp.json()
        except Exception as e:
            logger.error(f'B2C error: {e}')
            return {'error': str(e)}

    @classmethod
    def process_callback(cls, callback_data):
        """
        Process M-Pesa STK callback and update payment transaction.

        Expected callback_data structure:
        {
            "Body": {
                "stkCallback": {
                    "MerchantRequestID": "...",
                    "CheckoutRequestID": "...",
                    "ResultCode": 0,
                    "ResultDesc": "...",
                    "CallbackMetadata": {
                        "Item": [
                            {"Name": "Amount", "Value": 100},
                            {"Name": "MpesaReceiptNumber", "Value": "ABC123"},
                            {"Name": "PhoneNumber", "Value": 254712345678},
                        ]
                    }
                }
            }
        }
        """
        from apps.payments.models import PaymentTransaction, Invoice, Receipt
        from core.utils import generate_tracking_id

        try:
            callback = callback_data.get('Body', {}).get('stkCallback', {})
            result_code = callback.get('ResultCode', 1)

            # Parse metadata
            items = {}
            metadata = callback.get('CallbackMetadata', {}).get('Item', [])
            for item in metadata:
                items[item.get('Name', '')] = item.get('Value', '')

            amount = items.get('Amount', 0)
            mpesa_receipt = items.get('MpesaReceiptNumber', '')
            phone = items.get('PhoneNumber', '')

            if result_code != 0:
                logger.warning(f'M-Pesa callback failure: {callback.get("ResultDesc")}')
                return False

            # Match by phone number (most recent pending payment for that phone)
            payment = PaymentTransaction.objects.filter(
                mpesa_phone__endswith=str(phone)[-9:],
                status='pending',
            ).order_by('-created_at').first()

            if not payment:
                logger.warning(f'No pending payment found for phone {phone}')
                return False

            payment.mpesa_receipt = mpesa_receipt
            payment.status = 'completed'
            payment.save()

            # Create receipt
            Receipt.objects.create(
                payment=payment,
                receipt_number=generate_tracking_id('RCPT'),
            )

            # Mark associated invoice as paid
            Invoice.objects.filter(
                user=payment.user,
                is_paid=False,
            ).update(is_paid=True, paid_at=timezone.now())

            return True

        except Exception as e:
            logger.error(f'Callback processing error: {e}')
            return False
