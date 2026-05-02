import uuid
import time
import logging

logger = logging.getLogger(__name__)


class RequestIDMiddleware:
    """Attach a unique request ID to every request for tracing."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.id = str(uuid.uuid4())[:8]
        response = self.get_response(request)
        response['X-Request-ID'] = request.id
        return response


class SecurityHeadersMiddleware:
    """Add security-related HTTP headers to every response."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Content Security Policy
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com "
            "https://unpkg.com https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com "
            "https://cdn.tailwindcss.com https://cdn.jsdelivr.net; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data: https:; "
            "connect-src 'self' https:; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "form-action 'self'; "
        )
        response['Content-Security-Policy'] = csp
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = (
            'camera=(), microphone=(), geolocation=(self), '
            'payment=(self), usb=()'
        )

        # Cache control for sensitive pages
        if request.path.startswith('/dashboard') or request.path.startswith('/profile'):
            response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'

        return response


class AuditLogMiddleware:
    """Log basic request info for audit trail."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.time()
        response = self.get_response(request)
        duration = time.time() - start

        if request.user.is_authenticated:
            logger.info(
                'request_id=%s user=%s method=%s path=%s status=%s duration=%.3f',
                getattr(request, 'id', '-'),
                request.user.username,
                request.method,
                request.path,
                response.status_code,
                duration,
            )

        return response
