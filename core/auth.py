"""Custom auth for API: session auth without CSRF so frontend can POST with session cookie."""
from rest_framework.authentication import SessionAuthentication


class SessionAuthenticationNoCSRF(SessionAuthentication):
    """Session auth that does not enforce CSRF (for API called from same-host frontend)."""

    def enforce_csrf(self, request):
        pass  # Skip CSRF so session cookie is enough for POST from frontend
