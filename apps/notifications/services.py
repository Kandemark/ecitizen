import logging
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail
from .models import Notification, NotificationPreference, DeviceToken

logger = logging.getLogger(__name__)


class NotificationService:
    """Delivers notifications across email, SMS, and push channels."""

    @staticmethod
    def send(user, title, message, channel='in_app', related_object=None):
        """Send a notification through the specified channel."""
        pref = NotificationService._get_preferences(user)

        # Always create in-app notification
        notification = Notification.objects.create(
            user=user,
            title=title,
            message=message,
            channel=channel,
            content_type=None,
            object_id=None,
        )

        if channel == 'email' and pref and pref.email_enabled:
            NotificationService._send_email(user, title, message)

        if channel == 'sms' and pref and pref.sms_enabled:
            NotificationService._send_sms(user, message)

        if channel == 'push' and pref and pref.push_enabled:
            NotificationService._send_push(user, title, message)

        return notification

    @staticmethod
    def notify_application_update(application, status_change):
        """Notify user when their application status changes."""
        user = application.user
        title = f'Application {application.reference} — {status_change}'
        message = (
            f'Your application for {application.service.name} '
            f'(ref: {application.reference}) has been {status_change}.'
        )
        NotificationService.send(user, title, message, channel='email')

    @staticmethod
    def notify_payment_received(payment):
        """Notify user when payment is received."""
        user = payment.user
        title = f'Payment Received — {payment.reference}'
        message = (
            f'Your payment of KES {payment.amount:,.2f} has been received. '
            f'Receipt: {payment.mpesa_receipt or payment.reference}'
        )
        NotificationService.send(user, title, message, channel='email')

    @staticmethod
    def notify_review_assignment(assignment):
        """Notify staff when they are assigned a review."""
        if not assignment.assigned_to:
            return

        user = assignment.assigned_to
        title = f'New Review — {assignment.application.reference}'
        message = (
            f'You have been assigned to review {assignment.application.reference} '
            f'({assignment.application.service.name}). Step: {assignment.step.name}'
        )
        NotificationService.send(user, title, message, channel='email')

    @staticmethod
    def _send_email(user, title, message):
        """Send email via Django's SMTP."""
        if not user.email:
            return

        try:
            send_mail(
                subject=title,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
                html_message=f'<p>{message}</p>',
            )
        except Exception as e:
            logger.error(f'Failed to send email to {user.email}: {e}')

    @staticmethod
    def _send_sms(user, message):
        """Send SMS via Africa's Talking SDK."""
        if not hasattr(user, 'profile'):
            return

        phone = getattr(user.profile, 'phone_number', None)
        if not phone:
            return

        try:
            # Import only when used to avoid hard dependency
            import africastalking
            africastalking.initialize(
                settings.AFRICAS_TALKING_USERNAME,
                settings.AFRICAS_TALKING_API_KEY,
            )
            sms = africastalking.SMS
            sms.send(message, [str(phone)])
        except ImportError:
            logger.info(f'SMS module not installed; would send to {phone}: {message[:50]}...')
        except Exception as e:
            logger.error(f'Failed to send SMS to {phone}: {e}')

    @staticmethod
    def _send_push(user, title, message):
        """Send push notification via Firebase FCM."""
        tokens = DeviceToken.objects.filter(user=user, is_active=True)

        if not tokens:
            return

        try:
            import firebase_admin
            from firebase_admin import messaging

            if not firebase_admin._apps:
                cred_path = getattr(settings, 'FIREBASE_CREDENTIALS_PATH', None)
                if cred_path:
                    cred = firebase_admin.credentials.Certificate(cred_path)
                    firebase_admin.initialize_app(cred)

            for device in tokens:
                try:
                    msg = messaging.Message(
                        notification=messaging.Notification(title=title, body=message),
                        token=device.token,
                    )
                    messaging.send(msg)
                except messaging.UnregisteredError:
                    device.is_active = False
                    device.save(update_fields=['is_active'])
                except Exception as e:
                    logger.error(f'Push to {user.username}: {e}')
        except ImportError:
            logger.info('Firebase Admin SDK not installed; push notification skipped.')
        except Exception as e:
            logger.error(f'Push notification error: {e}')

    @staticmethod
    def _get_preferences(user):
        """Get user notification preferences, creating defaults if needed."""
        pref, _ = NotificationPreference.objects.get_or_create(user=user)
        return pref
