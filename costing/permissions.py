"""Role-based authorisation for the Costing module.

Visibility policy (decided by Imran, 17-07-2026): costs, margins and the
catalogue are VISIBLE to every logged-in staff member; management functions
are restricted as below. Management functions (add / edit / clone / delete) are restricted to
administrators (Django superusers) and management-grade roles. The allowed
role set is configurable via settings.COSTING_MANAGE_ROLES (a list of
case-insensitive substrings matched against the user's role name); it
defaults to any role containing 'manager' (Lab / Deputy / Assistant Manager)
plus 'ceo'. Read-only viewing remains open to any logged-in user.
"""
from functools import wraps
from django.apps import apps
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect

DEFAULT_MANAGE_ROLES = ['manager', 'ceo']


def user_role_name(user):
    """Return the user's role name string, or '' if none / not resolvable."""
    if not getattr(user, 'is_authenticated', False):
        return ''
    try:
        Signatures = apps.get_model('EnviTechAlApp', 'Signatures')
    except Exception:
        return ''
    try:
        s = Signatures.objects.select_related('role').filter(user=user).first()
        return ((getattr(getattr(s, 'role', None), 'role', '') or '')).strip()
    except Exception:
        return ''


def can_manage_costing(user):
    """True if the user may add/edit/clone/delete costing parameters."""
    if not getattr(user, 'is_authenticated', False):
        return False
    if getattr(user, 'is_superuser', False):
        return True
    role = user_role_name(user).lower()
    if not role:
        return False
    keys = [str(k).lower() for k in getattr(settings, 'COSTING_MANAGE_ROLES', DEFAULT_MANAGE_ROLES)]
    return any(k in role for k in keys)


def manage_required(view):
    """Decorator: enforce can_manage_costing, else redirect to the list with a message."""
    @wraps(view)
    def _wrapped(request, *args, **kwargs):
        if not can_manage_costing(request.user):
            messages.error(
                request,
                'You are not authorised to manage costing. This is limited to '
                'admin, manager and assistant manager roles.')
            return redirect('costing:list')
        return view(request, *args, **kwargs)
    return _wrapped
