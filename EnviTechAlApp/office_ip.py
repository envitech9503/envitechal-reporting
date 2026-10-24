"""Office-network rule for every signed-in user (owner decision 20-10-2026; per-office switch 24-10-2026).

Users may use the LIMS only from an office network: Karachi 110.93.247.168 or Lahore 124.29.208.36 (table
OfficeNetwork, editable by administrators on /office-network/; settings.OFFICE_ALLOWED_IPS is the fallback when the
table cannot be read). Only the usernames in settings.OFFICE_IP_EXEMPT_USERS (the CEO, ImranKazmi) may always work
from anywhere.

Per-office switch (24-10-2026): when an administrator turns the protection OFF for an office (e.g. its internet is
down), the staff of that office may work from any network; the other office stays protected. A user's office is the
office of their e-signature profile (Signatures.office), else their QC laboratory assignment (ControlChartReviewer).
A user with no office is free only when the protection is OFF for every office.

The client address is the X-Real-IP header set by our nginx proxy (never X-Forwarded-For, which a client can forge).
The rule is applied at sign-in (views.misc.userlogin) and on every request, so it also covers the Django admin sign-in
and sessions that were opened before the rule existed.
"""
import time

from django.conf import settings
from django.contrib.auth import logout
from django.http import HttpResponseForbidden

_DEFAULT_IPS = ['110.93.247.168', '124.29.208.36']
_TTL = 10.0                       # seconds a worker keeps the rules; a change reaches every worker within this time
_cache = {'at': 0.0, 'rules': None}


def client_ip(request):
    return (request.META.get('HTTP_X_REAL_IP') or request.META.get('REMOTE_ADDR') or '').strip()


def is_exempt(user):
    names = {u.lower() for u in getattr(settings, 'OFFICE_IP_EXEMPT_USERS', [])}
    return bool(user is not None and getattr(user, 'username', '') and user.username.lower() in names)


def can_switch(user):
    """May this user turn the office-network protection ON / OFF? Only the usernames in settings.OFFICE_SWITCH_USERS
    (owner decision 24-10-2026: the CEO, Sana and Hina), and only while the account is active."""
    names = {u.lower() for u in getattr(settings, 'OFFICE_SWITCH_USERS', ['ImranKazmi'])}
    return bool(user is not None and getattr(user, 'is_authenticated', False) and user.is_active
                and (user.username or '').lower() in names)


def invalidate():
    _cache['at'] = 0.0


def rules():
    """{location: {'ip': str, 'enforced': bool}}. Falls back to settings (every office protected) if the table is
    empty or cannot be read - the rule never fails open."""
    now = time.monotonic()
    if _cache['rules'] is not None and now - _cache['at'] < _TTL:
        return _cache['rules']
    r = {}
    try:
        from EnviTechAlApp.models import OfficeNetwork
        r = {o.location: {'ip': o.ip_address.strip(), 'enforced': bool(o.enforced)} for o in OfficeNetwork.objects.all()}
    except Exception:
        r = {}
    if not r:
        ips = list(getattr(settings, 'OFFICE_ALLOWED_IPS', _DEFAULT_IPS))
        r = {'Karachi': {'ip': ips[0] if ips else '', 'enforced': True}, 'Lahore': {'ip': ips[1] if len(ips) > 1 else '', 'enforced': True}}
        for extra in ips[2:]:
            r['Office %s' % extra] = {'ip': extra, 'enforced': True}
    _cache['rules'], _cache['at'] = r, now
    return r


def office_ip(request):
    """True when the request comes from one of the office networks."""
    ip = client_ip(request)
    return bool(ip) and (any(v['ip'] == ip for v in rules().values()) or ip in getattr(settings, 'OFFICE_EXTRA_IPS', ()))


def user_offices(user):
    """Offices the user belongs to: the e-signature profile's office, else the QC laboratory assignment."""
    out = set()
    try:
        from EnviTechAlApp.models import Signatures
        off = (Signatures.objects.filter(user=user).values_list('office', flat=True).first() or '').strip().title()
        if off:
            out.add(off)
    except Exception:
        pass
    if not out:
        try:
            from QC.models import ControlChartReviewer
            out |= set(ControlChartReviewer.objects.filter(user=user).values_list('location', flat=True))
        except Exception:
            pass
    return out


def allowed(user, request):
    """May this (authenticated) user work from the network of this request?"""
    if is_exempt(user) or office_ip(request):
        return True
    r = rules()
    offices = user_offices(user)
    known = [o for o in offices if o in r]
    if known:
        return any(not r[o]['enforced'] for o in known)
    return bool(r) and all(not v['enforced'] for v in r.values())


def denied_response():
    return HttpResponseForbidden(
        '<h2 style="font-family:sans-serif">Access from this network is not permitted</h2>'
        '<p style="font-family:sans-serif">The Envi Tech AL reporting software can be used only from the Karachi or Lahore '
        'office network. Please connect from the office, or contact the administrator. (Your IP is not allowed.)</p>')


class OfficeIPMiddleware:
    """Sign out any authenticated user who may not work from the network of the request."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        u = getattr(request, 'user', None)
        if u is not None and u.is_authenticated and not allowed(u, request):
            logout(request)
            return denied_response()
        return self.get_response(request)
