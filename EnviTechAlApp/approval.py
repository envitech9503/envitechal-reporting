"""Phase 1 approval workflow: approved records are locked (12-07-2026).
Roles v1: superusers approve/unapprove and may still edit; all other
users are analysts and cannot change or delete an approved record."""
from django.core.exceptions import PermissionDenied
from django.db.models.signals import pre_save, pre_delete

MODEL_KEYS = {}


def _acting_user():
    try:
        from simple_history.models import HistoricalRecords
        req = getattr(HistoricalRecords.context, 'request', None)
        return getattr(req, 'user', None)
    except Exception:
        return None


def _is_locked(key, pk):
    from EnviTechAlApp.models import ApprovalStatus
    return ApprovalStatus.objects.filter(model_key=key, record_id=pk).exists()


def _guard(sender, instance, **kwargs):
    key = MODEL_KEYS.get(sender)
    if not key or instance.pk is None:
        return
    if _is_locked(key, instance.pk):
        u = _acting_user()
        if u is not None and getattr(u, 'is_superuser', False):
            return
        raise PermissionDenied(
            'This record has been approved and is locked. '
            'Ask an administrator to unapprove it before making changes.')


def wire_guards(mapping):
    for model, key in mapping.items():
        MODEL_KEYS[model] = key
        pre_save.connect(_guard, sender=model, dispatch_uid='etal_guard_save_%s' % key)
        pre_delete.connect(_guard, sender=model, dispatch_uid='etal_guard_del_%s' % key)
