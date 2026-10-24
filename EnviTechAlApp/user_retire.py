"""Retiring a user who has left the company (owner decision 24-10-2026).

A user account is never deleted: deleting a Django user removes the e-signature row (Signatures, CASCADE) - which
empties the signature of every report that person signed - blanks 139 "created / updated / approved by" links
(SET_NULL) and leaves the audit history pointing at a number with no name. Retiring keeps the account record, so
every report, signature, log and trace keeps the person's name, and makes the account unusable:

  * cannot sign in (inactive, unusable password; an open session ends at the next request),
  * no rights (not staff, not administrator, no groups, no permissions),
  * removed from the signature drop-downs (they list active users only) and from the default user list,
  * the e-signature image stays on file so documents already signed keep printing it.

Used by the Django admin action "Retire selected users" (EnviTechAlApp/admin.py) and by
`manage.py retire_users <username> ... --reason "..." [--apply]`.
"""
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone


def protected(user):
    """Accounts that may not be retired from the screens: the exempt CEO account(s)."""
    names = {u.lower() for u in getattr(settings, 'OFFICE_IP_EXEMPT_USERS', [])}
    return (user.username or '').lower() in names


def retire(user, by=None, reason=''):
    """Retire one account in place. Returns a list of the changes made (empty if it was already retired)."""
    changes = []
    if user.is_active:
        user.is_active = False; changes.append('deactivated')
    if user.is_staff:
        user.is_staff = False; changes.append('staff access removed')
    if user.is_superuser:
        user.is_superuser = False; changes.append('administrator rights removed')
    if user.has_usable_password():
        user.set_unusable_password(); changes.append('password disabled')
    user.save()
    if user.groups.exists():
        user.groups.clear(); changes.append('groups cleared')
    if user.user_permissions.exists():
        user.user_permissions.clear(); changes.append('permissions cleared')
    if changes:
        try:
            from EnviTechAlApp.models import AuditLog
            who = (by.get_full_name() or by.username) if by else 'System'
            AuditLog.objects.create(user=by, created_by=by, timestamp=timezone.localtime().strftime('%d-%m-%Y %H:%M'),
                                    action='Retired user %s (%s) - %s; records, signatures and logs kept. Reason: %s. By %s.'
                                           % (user.username, user.get_full_name() or '-', ', '.join(changes), reason or '-', who))
        except Exception:
            pass
    return changes


def linked_counts(user):
    """{model label: rows linked to this user} - every record that keeps the user's name after retirement."""
    from django.apps import apps
    from EnviTechAlApp.models import Signatures
    User = get_user_model()
    sig_ids = list(Signatures.objects.filter(user=user).values_list('id', flat=True))
    out = {}
    for m in apps.get_models():
        for f in m._meta.get_fields():
            if not ((getattr(f, 'many_to_one', False) or getattr(f, 'one_to_one', False)) and f.concrete):
                continue
            try:
                if f.related_model is User:
                    n = m._default_manager.filter(**{f.attname: user.pk}).count()
                elif f.related_model is Signatures and sig_ids:
                    n = m._default_manager.filter(**{f.attname + '__in': sig_ids}).count()
                else:
                    continue
            except Exception:
                continue
            if n:
                out[m._meta.label] = out.get(m._meta.label, 0) + n
    return out
