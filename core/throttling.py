"""
Custom DRF throttle classes for e-Citizen.

Scopes are configured in settings.REST_FRAMEWORK.DEFAULT_THROTTLE_RATES.
"""
from rest_framework.throttling import SimpleRateThrottle


class LoginRateThrottle(SimpleRateThrottle):
    """Throttle login attempts: 5/minute by default."""
    scope = 'login'

    def get_cache_key(self, request, view):
        if request.user and request.user.is_authenticated:
            return None  # Don't throttle authenticated users on login
        return self.cache_format % {'scope': self.scope, 'ident': self.get_ident(request)}


class RegistrationRateThrottle(SimpleRateThrottle):
    """Throttle new account registrations: 3/hour by default."""
    scope = 'registration'

    def get_cache_key(self, request, view):
        return self.cache_format % {'scope': self.scope, 'ident': self.get_ident(request)}


class SearchRateThrottle(SimpleRateThrottle):
    """Throttle search API calls: 30/minute by default."""
    scope = 'search'

    def get_cache_key(self, request, view):
        return self.cache_format % {'scope': self.scope, 'ident': self.get_ident(request)}


class BurstRateThrottle(SimpleRateThrottle):
    """Very restrictive throttle for suspicious activity: 10/minute."""
    scope = 'burst'

    def get_cache_key(self, request, view):
        return self.cache_format % {'scope': self.scope, 'ident': self.get_ident(request)}
