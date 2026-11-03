"""R14 (Lab Manager Karachi 03-11-2026, point 8): drafts of the Raw Data Sheet being entered.

The Add / manual RDS pages (DW, WW) send the form every few seconds and on leaving the page; the latest draft of a user
for a sample and page is kept (one row, replaced) for 7 days after its last save. Reopening the page lists the user's drafts; "Resume" rebuilds the
sheet from the draft. Saving the RDS removes its draft. A draft belongs to its user only and is never printed."""
import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST

from QC.models import RdsDraft

KINDS, PAGES, MAX_BYTES = ('dw', 'ww'), ('add', 'manual'), 2 * 1024 * 1024
KEEP_DAYS = 7          # owner 03-11-2026: a draft is not kept for long - removed 7 days after its last save


def _args(src):
    kind, page = str(src.get('kind') or '').lower(), str(src.get('page') or '').lower()
    sid = str(src.get('sample_id') or '').strip()
    if kind not in KINDS or page not in PAGES:
        return None
    return kind, page, sid


def _purge():
    from datetime import timedelta
    RdsDraft.objects.filter(updated_at__lt=timezone.now() - timedelta(days=KEEP_DAYS)).delete()


def _when(dt):
    return timezone.localtime(dt).strftime('%d-%m-%Y %H:%M:%S')


@login_required
@require_POST
def rds_draft_save(request):
    if len(request.body) > MAX_BYTES:
        return JsonResponse({'status': 'error', 'message': 'The draft is too large to save.'}, status=413)
    try:
        body = json.loads(request.body.decode('utf-8'))
    except (ValueError, UnicodeDecodeError):
        return JsonResponse({'status': 'error', 'message': 'Bad draft.'}, status=400)
    a = _args(body)
    if not a or not a[2] or not isinstance(body.get('payload'), dict):
        return JsonResponse({'status': 'error', 'message': 'Bad draft.'}, status=400)
    kind, page, sid = a
    _purge()
    from QC.rds_guard import sample_city, user_lab                  # a draft only for a sample of the user's laboratory
    lab, city = user_lab(request), sample_city(kind, sid)
    if lab and city and city.lower() != lab.lower():
        return JsonResponse({'status': 'error', 'message': 'This sample belongs to another laboratory.'}, status=403)
    d, _ = RdsDraft.objects.update_or_create(user=request.user, kind=kind, page=page, sample_id=sid,
                                             defaults={'payload': json.dumps(body['payload'])})
    return JsonResponse({'status': 'ok', 'saved_at': _when(d.updated_at)})


@login_required
def rds_draft_list(request):
    a = _args(request.GET)
    if not a:
        return JsonResponse({'status': 'error'}, status=400)
    kind, page, _ = a
    _purge()
    rows = RdsDraft.objects.filter(user=request.user, kind=kind, page=page).order_by('-updated_at')[:50]
    return JsonResponse({'status': 'ok', 'drafts': [{'sample_id': d.sample_id, 'saved_at': _when(d.updated_at)} for d in rows]})


@login_required
def rds_draft_get(request):
    a = _args(request.GET)
    if not a or not a[2]:
        return JsonResponse({'status': 'error'}, status=400)
    kind, page, sid = a
    d = RdsDraft.objects.filter(user=request.user, kind=kind, page=page, sample_id=sid).first()
    if d is None:
        return JsonResponse({'status': 'none'})
    return JsonResponse({'status': 'ok', 'saved_at': _when(d.updated_at), 'payload': json.loads(d.payload)})


@login_required
@require_POST
def rds_draft_delete(request):
    try:
        body = json.loads(request.body.decode('utf-8'))
    except (ValueError, UnicodeDecodeError):
        body = {}
    a = _args(body)
    if not a or not a[2]:
        return JsonResponse({'status': 'error'}, status=400)
    kind, page, sid = a
    RdsDraft.objects.filter(user=request.user, kind=kind, page=page, sample_id=sid).delete()
    return JsonResponse({'status': 'ok'})


def clear_drafts(request, kind, sample_id):
    """Called when the RDS of the sample is saved: the user's drafts of it (either page) are no longer needed."""
    try:
        if getattr(request, 'user', None) is not None and request.user.is_authenticated:
            RdsDraft.objects.filter(user=request.user, kind=kind, sample_id=str(sample_id or '').strip()).delete()
    except Exception:
        pass
