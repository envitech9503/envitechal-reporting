"""Office-network rule for every signed-in user (owner decision 20-10-2026).

All users - administrators included - may use the LIMS only from the office networks in
settings.OFFICE_ALLOWED_IPS (Karachi 110.93.247.168, Lahore 124.29.208.36). Only the usernames in
settings.OFFICE_IP_EXEMPT_USERS (the CEO, ImranKazmi) may work from anywhere.

The client address is the X-Real-IP header set by our nginx proxy (never X-Forwarded-For, which a
client can forge). The rule is applied at sign-in (views.misc.userlogin) and on every request, so it
also covers the Django admin sign-in and sessions that were opened before the rule existed.
"""
from django.conf import settings
from django.contrib.auth import logout
from django.http import HttpResponseForbidden

_DEFAULT_IPS = ['110.93.247.168', '124.29.208.36']


def client_ip(request):
    return (request.META.get('HTTP_X_REAL_IP') or request.META.get('REMOTE_ADDR') or '').strip()


def is_exempt(user):
    names = {u.lower() for u in getattr(settings, 'OFFICE_IP_EXEMPT_USERS', [])}
    return bool(user is not None and getattr(user, 'username', '') and user.username.lower() in names)


def office_ip(request):
    return client_ip(request) in getattr(settings, 'OFFICE_ALLOWED_IPS', _DEFAULT_IPS)


def denied_response():
    return HttpResponseForbidden(
        '<h2 style="font-family:sans-serif">Access from this network is not permitted</h2>'
        '<p style="font-family:sans-serif">The Envi Tech AL reporting software can be used only from the Karachi or Lahore '
        'office network. Please connect from the office, or contact the administrator. (Your IP is not allowed.)</p>')


class OfficeIPMiddleware:
    """Sign out any authenticated, non-exempt user whose request does not come from an office network."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        u = getattr(request, 'user', None)
        if u is not None and u.is_authenticated and not is_exempt(u) and not office_ip(request):
            logout(request)
            return denied_response()
        return self.get_response(request)
