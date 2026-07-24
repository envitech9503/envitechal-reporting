"""
Reagent & Standards Preparation — QC views (additive, 23-07-2026; QA-hardened).
Mirrors the QC form + list + controlled-PDF pattern (see dw.py). Registered by
QC/views/__init__.py via `from .reagent_prep import *` + _FAMILY_MODULES.
"""
from .shared import *  # noqa: F401,F403  (FPDF, models, render, JsonResponse, csrf_exempt, get_object_or_404, os, json, datetime...)

import os as _os
import re as _re
import json as _json
from datetime import datetime as _dt, date as _date, timedelta as _tdelta
from django.db.models import Q as _Q
from django.db import transaction as _tx
from django.utils import timezone as _tz
from django.utils.safestring import mark_safe as _mark_safe
from django.views.decorators.clickjacking import xframe_options_sameorigin as _xframe_sameorigin

try:  # new in round-2b: running standardisation-history log (optional until migrated)
    from EnviTechAlApp.models import ReagentStandardisationHistory as _RSHist
except Exception:
    _RSHist = None

_LOGO = "static/assets/EnviTechAL LOGO.png"
_CALIBRI = "static/fonts/calibri.ttf"
_CALIBRIB = "static/fonts/calibrib.ttf"
_LOCS = ['Karachi', 'Lahore']


def _safe_json(obj):
    """JSON for inline <script> injection — escape chars that could break out of
    the script element (prevents stored XSS from user-entered names/descriptions)."""
    s = _json.dumps(obj)
    s = (s.replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
          .replace(' ', '\\u2028').replace(' ', '\\u2029'))
    return _mark_safe(s)


def _parse_date(v):
    v = (v or '').strip()
    if not v:
        return None
    for fmt in ('%Y-%m-%d', '%d-%m-%Y'):
        try:
            return _dt.strptime(v, fmt).date()
        except Exception:
            pass
    return None


def _f(v):
    try:
        return float(str(v).replace(',', '').strip())
    except Exception:
        return None


def _docctrl(location):
    """Per-lab control document row for this module (office-editable in admin)."""
    obj, _created = InventoryDocControl.objects.get_or_create(
        module='reagent_prep', location=location,
        defaults={'doc_no': '', 'issue_no': '01', 'rev_no': '00'})
    return obj


def _split_cat_lot(raw):
    """Inventory has no dedicated CAT field — the lab records both in one lot_no
    string, e.g. 'CAT NO. C532.1000  LOT NO: E1078375'. Split into (cat, lot)."""
    raw = (raw or '').strip()
    if not raw:
        return '', ''
    up = raw.upper()
    ci, li = up.find('CAT'), up.find('LOT')

    def _clean(x):
        return _re.sub(r'^\s*(NO\.?|NUMBER)?\s*[:.\-]?\s*', '', x, flags=_re.I).strip()

    if ci != -1 and li != -1:
        if ci < li:
            return _clean(raw[ci + 3:li]), _clean(raw[li + 3:])
        return _clean(raw[ci + 3:]), _clean(raw[li + 3:ci])
    if li != -1:
        return '', _clean(raw[li + 3:])
    if ci != -1:
        return _clean(raw[ci + 3:]), ''
    return '', raw


def _inventory_for_autocomplete():
    rows = []
    try:
        for lot in (ChemicalLot.objects
                    .exclude(status='Discarded')
                    .select_related('item')
                    .order_by('item__name', 'id')[:800]):
            it = lot.item
            cat, lotno = _split_cat_lot(lot.lot_no)
            rows.append({
                'id': lot.id,
                'name': it.name if it else '',
                'cat': cat,
                'lot': lotno,
                'make': lot.supplier or '',
                'expiry': lot.expiry.strftime('%d-%m-%Y') if lot.expiry else '',
            })
    except Exception:
        rows = []
    return rows


def _docctrl_data(location):
    c = _docctrl(location)
    return {
        'doc_no': c.doc_no or '',
        'issue_date': getattr(c, 'issue_date', '') or '',
        'issue_no': c.issue_no or '01',
        'rev_no': c.rev_no or '00',
    }


def _user_name(user):
    try:
        if not user or not getattr(user, 'is_authenticated', False):
            return ''
        return (user.get_full_name() or user.get_username() or '').strip()
    except Exception:
        return ''


def _next_numbers(location):
    """Suggest the next reagent number per prefix seen in this lab, e.g. RG-13.
    Analyst-editable; purely advisory (Decision D3 auto-suggest)."""
    pat = _re.compile(r'^([A-Za-z]+)[-\s]?0*(\d+)$')
    best = {}
    try:
        for rn in (ReagentPrep.objects.filter(location=location)
                   .exclude(reagent_no='').values_list('reagent_no', flat=True)):
            m = pat.match((rn or '').strip())
            if not m:
                continue
            pref = m.group(1).upper()
            n = int(m.group(2))
            if n > best.get(pref, 0):
                best[pref] = n
    except Exception:
        return []
    return ['%s-%02d' % (p, n + 1) for p, n in sorted(best.items())]


def _is_verified(obj):
    return bool(getattr(obj, 'verified_at', None))


def _snapshot(obj):
    try:
        stdf = obj.standardisation.factor
    except Exception:
        stdf = None
    return {
        'location': obj.location, 'month': obj.month, 'reagent_name': obj.reagent_name,
        'reagent_no': obj.reagent_no, 'rtype': obj.rtype, 'description': obj.description,
        'final_volume': obj.final_volume, 'conc_value': obj.conc_value, 'conc_unit': obj.conc_unit,
        'prepared_by': obj.prepared_by, 'verified_by': obj.verified_by,
        'dop': obj.dop.isoformat() if obj.dop else '', 'doe': obj.doe.isoformat() if obj.doe else '',
        'remarks': obj.remarks, 'chem_count': obj.chemicals.count(), 'std_factor': stdf,
    }


_DIFF_LABELS = [
    ('reagent_name', 'Name'), ('reagent_no', 'No.'), ('rtype', 'Type'),
    ('location', 'Location'), ('month', 'Month'), ('conc_value', 'Conc value'),
    ('conc_unit', 'Conc unit'), ('final_volume', 'Final volume'), ('dop', 'D.O.P.'),
    ('doe', 'D.O.E.'), ('prepared_by', 'Prepared by'), ('verified_by', 'Verified by'),
    ('description', 'Description'), ('remarks', 'Remarks'), ('chem_count', 'Chemicals'),
    ('std_factor', 'Std factor'),
]


def _diff(old, new):
    def _s(v):
        return '-' if v in (None, '') else str(v)
    parts = []
    for k, lab in _DIFF_LABELS:
        if old.get(k) != new.get(k):
            parts.append('%s: %s → %s' % (lab, _s(old.get(k)), _s(new.get(k))))
    return '; '.join(parts) if parts else 'no field changes'


def _audit(prep, user, action, changed=''):
    try:
        ReagentPrepAudit.objects.create(
            prep=prep,
            user=(user if getattr(user, 'is_authenticated', False) else None),
            action=str(action)[:30], changed=(changed or '')[:2000])
    except Exception:
        pass


def _history(obj):
    rows = []
    try:
        for a in obj.audits.all()[:60]:
            rows.append({
                'action': a.action,
                'user': _user_name(a.user) or '-',
                'at': a.at.strftime('%d-%m-%Y %H:%M') if a.at else '',
                'changed': a.changed or '',
            })
    except Exception:
        rows = []
    return rows


def _std_sig(f, tn, sd, ps, tml, nn):
    """Comparable signature of a standardisation event (dedupe consecutive saves)."""
    def _r(x):
        return round(x, 6) if isinstance(x, (int, float)) else x
    return (_r(f), _r(tn), sd or '', (ps or '').strip(), _r(tml), _r(nn))


def _maybe_log_std(obj, s, user):
    """Append a standardisation-history entry when the values differ from the most
    recently recorded one (a genuine standardisation / re-standardisation event).
    Never raises into the save path."""
    if _RSHist is None:
        return
    try:
        newk = _std_sig(s.factor, s.true_N,
                        s.std_date.isoformat() if s.std_date else '',
                        s.primary_std, s.titrant_ml, s.nominal_N)
        last = obj.std_history.order_by('-recorded_at', '-id').first()
        if last is not None:
            lastk = _std_sig(last.factor, last.true_N,
                             last.std_date.isoformat() if last.std_date else '',
                             last.primary_std, last.titrant_ml, last.nominal_N)
            if lastk == newk:
                return  # unchanged since last log -> don't duplicate
        _RSHist.objects.create(
            prep=obj, location=s.location, primary_std=s.primary_std,
            ps_mass=s.ps_mass, ps_purity=s.ps_purity, ps_eqwt=s.ps_eqwt,
            titrant_ml=s.titrant_ml, nominal_N=s.nominal_N, true_N=s.true_N,
            factor=s.factor, unit=s.unit, std_date=s.std_date, next_due=s.next_due,
            recorded_by=(user if getattr(user, 'is_authenticated', False) else None))
    except Exception:
        pass


def _std_history(obj):
    rows = []
    if _RSHist is None:
        return rows
    try:
        for h in obj.std_history.all()[:60]:
            rows.append({
                'std_date': h.std_date.strftime('%d-%m-%Y') if h.std_date else '',
                'primary_std': h.primary_std or '',
                'factor': h.factor, 'true_N': h.true_N, 'unit': h.unit or 'N',
                'nominal_N': h.nominal_N, 'titrant_ml': h.titrant_ml,
                'next_due': h.next_due.strftime('%d-%m-%Y') if h.next_due else '',
                'by': _user_name(h.recorded_by) or '-',
                'at': h.recorded_at.strftime('%d-%m-%Y %H:%M') if h.recorded_at else '',
            })
    except Exception:
        rows = []
    return rows


def _record_json(obj):
    chems = [{
        's_no': c.s_no, 'chemical_name': c.chemical_name, 'cat_no': c.cat_no,
        'lot_no': c.lot_no, 'quantity': c.quantity, 'make': c.make, 'expiry': c.expiry,
        'chemical_lot': c.chemical_lot_id,
    } for c in obj.chemicals.all()]
    std = None
    try:
        s = obj.standardisation
        std = {
            'location': s.location, 'primary_std': s.primary_std, 'ps_mass': s.ps_mass,
            'ps_purity': s.ps_purity, 'ps_eqwt': s.ps_eqwt, 'titrant_ml': s.titrant_ml,
            'nominal_N': s.nominal_N, 'true_N': s.true_N, 'factor': s.factor, 'unit': s.unit,
            'std_date': s.std_date.strftime('%Y-%m-%d') if s.std_date else '',
            'next_due': s.next_due.strftime('%Y-%m-%d') if s.next_due else '',
        }
    except ReagentStandardisation.DoesNotExist:
        std = None
    vuser = getattr(obj, 'verified_by_user', None)
    vat = getattr(obj, 'verified_at', None)
    return {
        'id': obj.id, 'location': obj.location, 'month': obj.month,
        'reagent_name': obj.reagent_name, 'reagent_no': obj.reagent_no, 'rtype': obj.rtype,
        'description': obj.description, 'final_volume': obj.final_volume,
        'conc_value': obj.conc_value, 'conc_unit': obj.conc_unit,
        'prepared_by': obj.prepared_by, 'verified_by': obj.verified_by,
        'dop': obj.dop.strftime('%Y-%m-%d') if obj.dop else '',
        'doe': obj.doe.strftime('%Y-%m-%d') if obj.doe else '',
        'remarks': obj.remarks, 'chemicals': chems, 'standardisation': std,
        # round-2 additions
        'updated_at': obj.updated_at.strftime('%Y-%m-%dT%H:%M:%S') if getattr(obj, 'updated_at', None) else '',
        'updated_by': _user_name(getattr(obj, 'updated_by', None)),
        'verified': bool(vat),
        'verified_by_name': _user_name(vuser),
        'verified_at': vat.strftime('%d-%m-%Y %H:%M') if vat else '',
        'created_by_name': _user_name(getattr(obj, 'created_by', None)),
        'history': _history(obj),
        'std_history': _std_history(obj),
    }


def reagent_prep(request):
    """Create / edit / clone / view form page."""
    edit_id = request.GET.get('id')
    clone_id = request.GET.get('clone')
    view_id = request.GET.get('view')
    record = None
    view_only = False
    if view_id:
        obj = get_object_or_404(ReagentPrep, id=view_id)
        record = _record_json(obj)
        view_only = True
    elif edit_id:
        obj = get_object_or_404(ReagentPrep, id=edit_id)
        record = _record_json(obj)
    elif clone_id:
        obj = get_object_or_404(ReagentPrep, id=clone_id)
        record = _record_json(obj)
        record['id'] = None
        record['reagent_no'] = ''
        record['verified'] = False
        record['verified_by_name'] = ''
        record['verified_at'] = ''
        record['history'] = []
        record['updated_at'] = ''
    docctrl = {loc: _docctrl_data(loc) for loc in _LOCS}
    # Full access for all users: control-number editing is open to everyone.
    context = {
        'record_json': _safe_json(record),
        'inventory_json': _safe_json(_inventory_for_autocomplete()),
        'docctrl_json': _safe_json(docctrl),
        'is_admin_json': _safe_json(True),
        'locations': _safe_json(_LOCS),
        'nextno_json': _safe_json({loc: _next_numbers(loc) for loc in _LOCS}),
        'view_only_json': _safe_json(view_only),
        'me_json': _safe_json(_user_name(getattr(request, 'user', None))),
    }
    return render(request, 'reagent_prep_form.html', context)


@csrf_exempt
def reagent_prep_doc_save(request):
    """Save the per-lab control document number. Open to all logged-in users
    (full-access policy for this module)."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    g = request.POST
    location = g.get('location') if g.get('location') in _LOCS else 'Karachi'
    c = _docctrl(location)
    c.doc_no = (g.get('doc_no') or '').strip()[:60]
    c.issue_date = (g.get('issue_date') or '').strip()[:30]
    c.issue_no = (g.get('issue_no') or '').strip()[:10] or '01'
    c.rev_no = (g.get('rev_no') or '').strip()[:10] or '00'
    if getattr(request, 'user', None) and request.user.is_authenticated:
        try:
            c.updated_by = request.user
        except Exception:
            pass
    c.save()
    return JsonResponse({'ok': True, 'location': location, 'doc': _docctrl_data(location)})


@csrf_exempt
def reagent_prep_save(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    try:
        data = _json.loads(request.body.decode('utf-8') or '{}')
    except Exception:
        return JsonResponse({'error': 'Invalid JSON payload'}, status=400)

    name = (data.get('reagent_name') or '').strip()
    if not name:
        return JsonResponse({'error': 'Reagent name is required'}, status=400)
    location = data.get('location') if data.get('location') in _LOCS else 'Karachi'
    user = getattr(request, 'user', None)

    # date sanity (G3): expiry cannot precede preparation
    dop = _parse_date(data.get('dop'))
    doe = _parse_date(data.get('doe'))
    if dop and doe and doe < dop:
        return JsonResponse({'error': 'D.O.E. (expiry) cannot be earlier than D.O.P. (prepared).'}, status=400)

    rtype = (data.get('rtype') or 'Reagent').strip()[:30]
    reagent_no = (data.get('reagent_no') or '').strip()[:40]

    rid = data.get('id')
    old = None
    was_verified = False
    if rid:
        try:
            obj = ReagentPrep.objects.get(id=int(rid))
        except Exception:
            return JsonResponse({'error': 'Record not found'}, status=404)
        # optimistic lock (G5): reject if the DB row moved on since the form loaded
        client_ts = (data.get('client_updated_at') or '').strip()
        if client_ts and getattr(obj, 'updated_at', None):
            if obj.updated_at.strftime('%Y-%m-%dT%H:%M:%S') > client_ts:
                who = _user_name(getattr(obj, 'updated_by', None)) or 'another user'
                return JsonResponse({'stale': True, 'message':
                    'This record was changed by %s while you were editing. Reload to get the latest version before saving.' % who},
                    status=409)
        old = _snapshot(obj)
        was_verified = _is_verified(obj)
    else:
        obj = ReagentPrep()
        if user and user.is_authenticated:
            obj.created_by = user

    # duplicate reagent number warning (G4): warn (don't block) on a same-lab clash
    if reagent_no and not data.get('force'):
        dup = ReagentPrep.objects.filter(location=location, reagent_no__iexact=reagent_no)
        if rid:
            dup = dup.exclude(id=int(rid))
        if dup.exists():
            return JsonResponse({'warning': True, 'field': 'reagent_no', 'message':
                'Reagent No. "%s" already exists for %s. Save anyway?' % (reagent_no, location)})

    prepared = (data.get('prepared_by') or '').strip() or _user_name(user)

    # All mutations atomic — an edit never leaves the record with its old child
    # rows deleted but new ones un-written.
    with _tx.atomic():
        obj.location = location
        obj.month = (data.get('month') or '').strip()[:30]
        obj.reagent_name = name[:200]
        obj.reagent_no = reagent_no
        obj.rtype = rtype
        obj.description = (data.get('description') or '').strip()
        obj.final_volume = (data.get('final_volume') or '').strip()[:40]
        obj.conc_value = (data.get('conc_value') or '').strip()[:40]
        obj.conc_unit = (data.get('conc_unit') or '').strip()[:20]
        obj.prepared_by = prepared[:120]
        obj.verified_by = (data.get('verified_by') or '').strip()[:120]
        obj.dop = dop
        obj.doe = doe
        obj.remarks = (data.get('remarks') or '').strip()[:300]
        if user and user.is_authenticated:
            try:
                obj.updated_by = user
            except Exception:
                pass
        # editing content invalidates a prior verification (four-eyes guard)
        if was_verified:
            try:
                obj.verified_by_user = None
                obj.verified_at = None
            except Exception:
                pass
        obj.save()

        # replace child chemical rows
        obj.chemicals.all().delete()
        for i, row in enumerate(data.get('chemicals') or [], start=1):
            cname = (row.get('chemical_name') or '').strip()
            if not cname:
                continue
            lot_id = row.get('chemical_lot')
            lot_obj = None
            if lot_id:
                try:
                    lot_obj = ChemicalLot.objects.get(id=int(lot_id))
                except Exception:
                    lot_obj = None
            _cat = (row.get('cat_no') or '').strip()
            _lot = (row.get('lot_no') or '').strip()
            # if CAT was left blank but the combined string landed in LOT, split it
            # so the two columns are stored (and later printed) correctly.
            if (not _cat) and _lot and 'CAT' in _lot.upper():
                _sc, _sl = _split_cat_lot(_lot)
                _cat = _sc or _cat
                _lot = _sl
            ReagentPrepChemical.objects.create(
                prep=obj, s_no=row.get('s_no') or i, chemical_name=cname[:200],
                cat_no=_cat[:80],
                lot_no=_lot[:80],
                quantity=(row.get('quantity') or '').strip()[:60],
                make=(row.get('make') or '').strip()[:120],
                expiry=(row.get('expiry') or '').strip()[:40],
                chemical_lot=lot_obj)

        # standardisation. F3 fix: an empty payload on a *titrant* must NEVER wipe a
        # stored factor. Delete only when the record is no longer a titrant (the form
        # confirms this with the user before sending an empty payload for a non-titrant).
        std = data.get('standardisation')
        has_payload = bool(std and (std.get('factor') not in (None, '') or std.get('true_N') not in (None, '')))
        if has_payload:
            s, _c = ReagentStandardisation.objects.get_or_create(prep=obj)
            s.location = location
            s.primary_std = (std.get('primary_std') or '').strip()[:120]
            s.ps_mass = _f(std.get('ps_mass'))
            s.ps_purity = _f(std.get('ps_purity'))
            s.ps_eqwt = _f(std.get('ps_eqwt'))
            s.titrant_ml = _f(std.get('titrant_ml'))
            s.nominal_N = _f(std.get('nominal_N'))
            s.true_N = _f(std.get('true_N'))
            s.factor = _f(std.get('factor'))
            s.unit = (std.get('unit') or 'N').strip()[:10]
            s.std_date = _parse_date(std.get('std_date'))
            s.next_due = _parse_date(std.get('next_due'))
            s.save()
            # running standardisation-history log (round-2b): record genuine events
            _maybe_log_std(obj, s, user)
        elif rtype != 'Standardised titrant':
            ReagentStandardisation.objects.filter(prep=obj).delete()
        # else: titrant with no fresh payload -> keep the stored factor untouched (F3)

    # audit trail (G2). type change is called out separately for auditors.
    if old is None:
        _audit(obj, user, 'created', 'record created')
    else:
        action = 'type-changed' if old.get('rtype') != obj.rtype else 'updated'
        _audit(obj, user, action, _diff(old, _snapshot(obj)))
    if was_verified:
        _audit(obj, user, 'unverified', 'verification cleared by edit')

    obj.refresh_from_db(fields=['updated_at'])
    return JsonResponse({'ok': True, 'id': obj.id,
                         'updated_at': obj.updated_at.strftime('%Y-%m-%dT%H:%M:%S') if obj.updated_at else '',
                         'history': _history(obj),
                         'std_history': _std_history(obj)})


@csrf_exempt
def reagent_prep_verify(request):
    """Verify / unverify a record. Open to any logged-in user (full-access policy);
    verifier identity and time are recorded for traceability, and any later content
    edit clears the verification (see reagent_prep_save)."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    try:
        data = _json.loads(request.body.decode('utf-8') or '{}')
    except Exception:
        data = request.POST
    try:
        obj = ReagentPrep.objects.get(id=int(data.get('id')))
    except Exception:
        return JsonResponse({'error': 'Record not found'}, status=404)
    user = getattr(request, 'user', None)
    action = (data.get('action') or 'verify').strip()
    if action == 'unverify':
        obj.verified_by_user = None
        obj.verified_at = None
        obj.save(update_fields=['verified_by_user', 'verified_at', 'updated_at'])
        _audit(obj, user, 'unverified', 'verification removed')
        return JsonResponse({'ok': True, 'verified': False})
    obj.verified_by_user = user if (user and user.is_authenticated) else None
    obj.verified_at = _tz.now()
    obj.save(update_fields=['verified_by_user', 'verified_at', 'updated_at'])
    _audit(obj, user, 'verified', 'verified by %s' % (_user_name(user) or '-'))
    return JsonResponse({'ok': True, 'verified': True,
                         'verified_by_name': _user_name(user),
                         'verified_at': obj.verified_at.strftime('%d-%m-%Y %H:%M')})


def reagent_prep_list(request):
    loc = request.GET.get('location') or 'All'
    q = (request.GET.get('q') or '').strip()
    month = (request.GET.get('month') or '').strip()
    status = (request.GET.get('status') or 'all').strip().lower()
    sort = (request.GET.get('sort') or '').strip()
    try:
        page = max(1, int(request.GET.get('page') or 1))
    except Exception:
        page = 1
    per_page = 50
    today = _date.today()
    soon = today + _tdelta(days=14)

    qs = ReagentPrep.objects.all()
    if loc in _LOCS:
        qs = qs.filter(location=loc)
    if month:
        qs = qs.filter(month__icontains=month)
    if q:
        qs = qs.filter(
            _Q(reagent_name__icontains=q) |
            _Q(reagent_no__icontains=q) |
            _Q(chemicals__chemical_name__icontains=q)).distinct()
    if status == 'active':
        qs = qs.filter(_Q(doe__isnull=True) | _Q(doe__gte=today))
    elif status == 'expiring':
        qs = qs.filter(doe__gte=today, doe__lte=soon)
    elif status == 'expired':
        qs = qs.filter(doe__lt=today)

    order = {'doe': 'doe', '-doe': '-doe', 'no': 'reagent_no', '-no': '-reagent_no'}.get(sort, '-created_at')
    qs = qs.order_by(order)

    total = qs.count()
    pages = max(1, (total + per_page - 1) // per_page)
    page = min(page, pages)
    start = (page - 1) * per_page
    rows = []
    for o in qs[start:start + per_page]:
        expired = bool(o.doe and o.doe < today)
        expiring = bool(o.doe and today <= o.doe <= soon)
        rows.append({'o': o, 'expired': expired, 'expiring': expiring,
                     'verified': _is_verified(o)})
    return render(request, 'reagent_prep_list.html', {
        'list': rows, 'location': loc, 'q': q, 'month': month, 'status': status,
        'sort': sort, 'locations': _LOCS, 'total': total, 'page': page,
        'pages': pages, 'has_prev': page > 1, 'has_next': page < pages,
        'prev_page': page - 1, 'next_page': page + 1,
    })


@_xframe_sameorigin
def reagent_prep_calculator(request):
    """Standalone fully-loaded calculator, embedded in the form via iframe.
    Served raw (not through the template engine) so the calculator's own JS
    braces are never parsed as Django template tags. xframe_sameorigin lets the
    same-origin iframe render it (site default is X-Frame-Options: DENY)."""
    for p in ('templates/reagent_calc_tool.html',
              _os.path.join(_os.path.dirname(__file__), '..', '..', 'templates', 'reagent_calc_tool.html')):
        try:
            with open(p, encoding='utf-8') as fh:
                return HttpResponse(fh.read())
        except Exception:
            continue
    return HttpResponse('<p>Calculator asset not found.</p>', status=404)


def reagent_prep_manual(request):
    """Serve the module user manual (self-contained searchable HTML) raw, so its
    own CSS/JS braces are never parsed as Django template tags. Linked from the
    form and list headers as 'User Manual'."""
    for p in ('templates/reagent_prep_manual.html',
              _os.path.join(_os.path.dirname(__file__), '..', '..', 'templates', 'reagent_prep_manual.html')):
        try:
            with open(p, encoding='utf-8') as fh:
                return HttpResponse(fh.read())
        except Exception:
            continue
    return HttpResponse('<p>User manual asset not found.</p>', status=404)


# ---------------------------------------------------------------- controlled PDF
def _make_reagent_pdf(location, records, draft=False):
    """Build one controlled PDF for `records`, all belonging to `location`.
    Single source of truth for both the per-record PDF and the monthly/batch PDF
    (entries stack 2-3 per page like the original paper log). `draft` overlays a
    subtle diagonal DRAFT watermark (unverified single-record PDFs, Decision D1)."""
    ctrl = _docctrl(location)
    today = _date.today()

    class CustomPDF(FPDF):
        def __init__(self, *a, **k):
            super().__init__(*a, **k)
            # House brand font is Calibri (unicode TTF) — supports subscripts (H2SO4),
            # micro sign, etc. Fall back to Helvetica (+ latin-1 sanitising) only if
            # the TTF is unavailable, so the report can never crash on chemistry text.
            self.fam = 'Helvetica'
            try:
                if _os.path.exists(_CALIBRI):
                    self.add_font('Calibri', '', _CALIBRI, uni=True)
                    self.add_font('Calibri', 'B',
                                  _CALIBRIB if _os.path.exists(_CALIBRIB) else _CALIBRI, uni=True)
                    self.fam = 'Calibri'
            except Exception:
                self.fam = 'Helvetica'

        def t(self, s):
            s = '' if s is None else str(s)
            if self.fam == 'Calibri':
                return s
            return s.encode('latin-1', 'replace').decode('latin-1')

        def header(self):
            # DRAFT watermark (unverified records) — drawn first so content overlays it
            if draft:
                self.set_font(self.fam, 'B', 64)
                self.set_text_color(232, 232, 232)
                try:
                    with self.rotation(45, self.w / 2.0, self.h / 2.0):
                        self.text(self.w / 2.0 - 48, self.h / 2.0 + 12, 'DRAFT')
                except Exception:
                    self.set_xy(0, self.h / 2.0 - 12)
                    self.cell(0, 24, 'DRAFT', align='C')
                self.set_text_color(0, 0, 0)
            if _os.path.exists(_LOGO):
                try:
                    self.image(_LOGO, 10, 8, 20, 22)
                except Exception:
                    pass
            # Centred title block (matches the original controlled record). The logo
            # sits far left and the control box far right (x>=150); the centred text
            # (centre ~105) clears both. Sub-line retained as a brand line (Decision D2).
            self.set_xy(10, 10)
            self.set_font(self.fam, 'B', 15)
            self.cell(0, 7, 'ENVI TECH AL', align='C', ln=1)
            self.set_x(10)
            self.set_font(self.fam, '', 8)
            self.cell(0, 5, self.t('Analytical Laboratory - Environmental & Water Testing'), align='C', ln=1)
            self.set_x(10)
            self.set_font(self.fam, 'B', 11)
            self.cell(0, 6, 'REAGENT PREPARATION RECORD', align='C', ln=1)
            # control box (top-right) — Decision D1: retained on the digital record
            bx, by, bw = 150, 8, 52
            self.set_font(self.fam, '', 7)
            self.set_xy(bx, by)
            rows = [
                ('Doc No.', ctrl.doc_no or '-'),
                ('Issue Date', getattr(ctrl, 'issue_date', '') or '-'),
                ('Issue No.', ctrl.issue_no or '-'),
                ('Rev No.', ctrl.rev_no or '-'),
                ('Location', location),
            ]
            y = by
            for k, v in rows:
                self.set_xy(bx, y)
                self.set_font(self.fam, 'B', 7)
                self.cell(22, 5, k, border=1)
                self.set_font(self.fam, '', 7)
                self.cell(bw - 22, 5, self.t(' ' + str(v)), border=1, ln=1)
                y += 5
            self.set_draw_color(0, 0, 0)
            self.line(10, 33, 202, 33)
            self.set_y(37)

        def footer(self):
            # Controlled-document line, then the branded contact band (matches the
            # original controlled record: phone left, head office centre, email/web right).
            self.set_y(-20)
            self.set_font(self.fam, 'I' if self.fam == 'Helvetica' else '', 6.5)
            self.set_text_color(90, 90, 90)
            self.cell(0, 4,
                      'ENVI TECH AL  -  Controlled document.  Uncontrolled when printed.',
                      align='C', ln=1)
            self.set_text_color(0, 0, 0)
            self.set_draw_color(15, 81, 50)
            self.set_line_width(0.4)
            yb = self.get_y() + 0.6
            self.line(10, yb, 200, yb)
            self.set_line_width(0.2)
            self.set_draw_color(0, 0, 0)
            y0 = yb + 1.2
            self.set_font(self.fam, '', 6.5)
            self.set_xy(10, y0)
            self.cell(90, 3.6, self.t('Tel: +92 310 2288801'), align='L')
            self.set_xy(110, y0)
            self.cell(90, 3.6, self.t('info@envitechal.com   -   www.envitechal.com'), align='R')
            self.set_xy(10, y0 + 3.6)
            self.cell(0, 3.6, self.t(
                'Head Office: 345, First Floor, Street-15, Block-3, Bahadurabad, Karachi. 75900, Pakistan.'),
                align='C', ln=1)
            self.set_xy(10, y0 + 7.2)
            self.cell(0, 3.6, 'Page %s of {nb}' % self.page_no(), align='R')

    pdf = CustomPDF(orientation='P', unit='mm', format='A4')
    pdf.alias_nb_pages()
    # margin reserves room for the branded footer band (Section 4).
    pdf.set_auto_page_break(auto=True, margin=24)

    def _render_entry(pdf, obj, sep=False):
        """Draw one reagent block and advance the cursor. Multiple entries stack
        on a page (like the paper log); a fresh page starts when too little room
        remains for a full block, so an entry never spills into the footer."""
        if pdf.get_y() > 185:
            pdf.add_page()
        elif sep:
            # light separator between stacked entries on the same page
            pdf.set_draw_color(200, 208, 216)
            pdf.line(10, pdf.get_y(), 202, pdf.get_y())
            pdf.set_draw_color(0, 0, 0)
            pdf.ln(3)

        def kv(label, value, w1=32, w2=64):
            pdf.set_font(pdf.fam, 'B', 9)
            pdf.cell(w1, 6, label, border=0)
            pdf.set_font(pdf.fam, '', 9)
            pdf.cell(w2, 6, pdf.t(value or '-'), border=0)

        kv('Month:', obj.month)
        kv('Type:', obj.rtype, 24, 60)
        pdf.ln(6)
        # bulleted reagent line (matches the original controlled record)
        pdf.set_font(pdf.fam, 'B', 9)
        pdf.cell(5, 6, '•' if pdf.fam == 'Calibri' else '-')
        kv('Reagent Name:', obj.reagent_name, 30, 87)
        kv('Reagent No.:', obj.reagent_no, 26, 34)
        pdf.ln(6)
        conc = ((obj.conc_value + ' ' + obj.conc_unit).strip()) if (obj.conc_value or obj.conc_unit) else '-'
        kv('Concentration:', conc, 32, 60)
        kv('Final Volume:', obj.final_volume, 26, 40)
        pdf.ln(9)

        # chemicals table — column labels match the original record exactly
        headers = [('S.#', 12), ('Chemical Name', 52), ('CAT Number', 26), ('LOT Number', 26),
                   ('Quantity', 24), ('Make', 28), ('Expiry Date', 24)]
        pdf.set_font(pdf.fam, 'B', 8)
        pdf.set_fill_color(225, 232, 237)
        for h, w in headers:
            pdf.cell(w, 7, h, border=1, align='C', fill=True)
        pdf.ln(7)
        pdf.set_font(pdf.fam, '', 8)

        def _fit(txt, w):
            txt = pdf.t(txt)
            while txt and pdf.get_string_width(txt) > (w - 2):
                txt = txt[:-1]
            return txt

        for c in obj.chemicals.all():
            exp_dt = _parse_date(c.expiry)
            # defensive CAT/LOT split — a row saved with the combined string in
            # lot_no (and empty cat_no) must still print in the correct columns.
            cat, lot = c.cat_no, c.lot_no
            if (not cat) and lot and 'CAT' in lot.upper():
                scat, slot = _split_cat_lot(lot)
                cat = scat or cat
                lot = slot
            cells = [(str(c.s_no), 12, 'C'), (c.chemical_name, 52, 'L'), (cat or '-', 26, 'C'),
                     (lot or '-', 26, 'C'), (c.quantity or '-', 24, 'C'),
                     (c.make or '-', 28, 'C'), (c.expiry or '-', 24, 'C')]
            for i, (txt, w, al) in enumerate(cells):
                if i == 6 and exp_dt and exp_dt < today:
                    pdf.set_text_color(200, 0, 0)
                pdf.cell(w, 6, _fit(txt, w), border=1, align=al)
                pdf.set_text_color(0, 0, 0)
            pdf.ln(6)
        if not obj.chemicals.exists():
            pdf.cell(sum(w for _h, w in headers), 6, 'No chemicals recorded', border=1, align='C')
            pdf.ln(6)
        pdf.ln(4)

        # description — label matches the original ("Description:")
        pdf.set_font(pdf.fam, 'B', 9)
        pdf.cell(0, 6, 'Description:', ln=1)
        pdf.set_font(pdf.fam, '', 9)
        pdf.multi_cell(0, 5, pdf.t(obj.description or '-'))
        pdf.ln(2)

        # standardisation
        try:
            s = obj.standardisation
            pdf.set_font(pdf.fam, 'B', 9)
            pdf.cell(0, 6, pdf.t('Standardisation (%s):' % (s.location or obj.location)), ln=1)
            pdf.set_font(pdf.fam, '', 9)
            u = s.unit or 'N'
            line = ('Primary std: %s  |  nominal %s %s -> true %s %s  |  factor %s  |  date %s  |  next due %s' % (
                s.primary_std or '-',
                ('%.4f' % s.nominal_N) if s.nominal_N is not None else '-', u,
                ('%.4f' % s.true_N) if s.true_N is not None else '-', u,
                ('%.4f' % s.factor) if s.factor is not None else '-',
                s.std_date.strftime('%d-%m-%Y') if s.std_date else '-',
                s.next_due.strftime('%d-%m-%Y') if s.next_due else '-'))
            pdf.multi_cell(0, 5, pdf.t(line))
            pdf.ln(2)
        except ReagentStandardisation.DoesNotExist:
            pass

        pdf.ln(2)
        pdf.set_font(pdf.fam, 'B', 9)
        dop = obj.dop.strftime('%d-%m-%Y') if obj.dop else '-'
        doe = obj.doe.strftime('%d-%m-%Y') if obj.doe else '-'
        pdf.cell(48, 6, pdf.t('Prepared By: ' + (obj.prepared_by or '-')))
        _vat = getattr(obj, 'verified_at', None)
        if _vat:
            _vname = _user_name(getattr(obj, 'verified_by_user', None)) or (obj.verified_by or '-')
            pdf.cell(90, 6, pdf.t('Verified By: %s on %s' % (_vname, _vat.strftime('%d-%m-%Y'))))
        else:
            pdf.cell(90, 6, pdf.t('Verified By: ' + (obj.verified_by or '-')))
        pdf.ln(6)
        pdf.cell(48, 6, 'D.O.P.: ' + dop)
        if obj.doe and obj.doe < today:
            pdf.set_text_color(200, 0, 0)
        pdf.cell(48, 6, 'D.O.E.: ' + doe)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(10)

    pdf.add_page()
    for i, obj in enumerate(records):
        _render_entry(pdf, obj, sep=(i > 0))
    return pdf


def _pdf_response(pdf, fname):
    out = pdf.output(dest='S')
    if isinstance(out, str):
        out = out.encode('latin-1')
    resp = HttpResponse(bytes(out), content_type='application/pdf')
    resp['Content-Disposition'] = 'inline; filename="%s"' % fname
    return resp


def generate_pdf_for_reagent_prep(obj):
    """Single-record controlled PDF. Draft watermark when unverified (Decision D1)."""
    pdf = _make_reagent_pdf(obj.location, [obj], draft=not _is_verified(obj))
    safe_no = ''.join(ch for ch in str(obj.reagent_no or obj.id) if ch.isalnum() or ch in '-_') or str(obj.id)
    return _pdf_response(pdf, 'ReagentPrep_%s_%s.pdf' % (safe_no, obj.location))


def reagent_prep_pdf_from_list(request, pk=None):
    if pk:
        obj = get_object_or_404(ReagentPrep, id=pk)
        return generate_pdf_for_reagent_prep(obj)
    # No pk: fall back to the list view (full context) rather than a bare render.
    return reagent_prep_list(request)


def reagent_prep_month_pdf(request):
    """Monthly / batch controlled PDF: many records of ONE lab stacked 2-3 per
    page, matching the paper reagent-preparation log. Requires a specific
    location (the control box is per-lab); optional month/search filters."""
    loc = request.GET.get('location')
    if loc not in _LOCS:
        return HttpResponse('Select Karachi or Lahore to print the monthly record.', status=400)
    month = (request.GET.get('month') or '').strip()
    q = (request.GET.get('q') or '').strip()
    qs = ReagentPrep.objects.filter(location=loc)
    if month:
        qs = qs.filter(month__icontains=month)
    if q:
        qs = qs.filter(
            _Q(reagent_name__icontains=q) |
            _Q(reagent_no__icontains=q) |
            _Q(chemicals__chemical_name__icontains=q)).distinct()
    records = list(qs.order_by('reagent_no', 'created_at')[:500])
    if not records:
        return HttpResponse('No preparation records match for %s.' % loc, status=404)
    pdf = _make_reagent_pdf(loc, records)
    safe_m = ''.join(ch for ch in month if ch.isalnum()) or 'all'
    return _pdf_response(pdf, 'ReagentPrep_%s_%s.pdf' % (loc, safe_m))


__all__ = [
    'reagent_prep', 'reagent_prep_save', 'reagent_prep_doc_save', 'reagent_prep_list',
    'reagent_prep_calculator', 'reagent_prep_pdf_from_list', 'reagent_prep_month_pdf',
    'reagent_prep_verify', 'reagent_prep_manual', 'generate_pdf_for_reagent_prep',
]
