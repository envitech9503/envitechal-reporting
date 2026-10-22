"""Quality - Measurement of Uncertainty (form ETAL-LAB-706-FF-01) - views. 21-10-2026.

One function for both laboratories (Karachi / Lahore), lab-scoped like the control charts:
  * Register of studies (current approved U per parameter / level / sample kind, drafts, history)
  * Study page: master data, operators x replicates, uncertainty budget - live calculation
    through /qc/mou/api/calc/ so the browser never re-implements the arithmetic (QC/mou_calc.py)
  * Workflow: draft -> submitted for review -> reviewed (Lab Manager) -> approved (CEO); a repeat
    study is a new version that supersedes the approved one when it is approved itself
  * Uncertainty-source library per laboratory (Lab Manager); studies copy the values they use
  * PDF form, document-control numbers per laboratory, deletion log, user manual, JSON lookup
Roles reuse the control-chart assignments (Laboratory Reviewers page): review = the lab's
QC / Lab Manager, approve = CEO / administrator, delete = either, with a reason.
"""
from .shared import *  # noqa: F401,F403
import json as _json
import re as _re
import math as _math
from datetime import date as _date, datetime as _dt
from django.utils import timezone as _tz
from django.shortcuts import redirect as _redirect
from django.db.models import Q as _Q
from django.contrib import messages as _msg
from django.views.decorators.csrf import csrf_exempt as _csrf_exempt

from QC.models import MouSource, MouStudy, MouOperator, MouComponent, ControlChartDeletion, ControlChartReviewer
from QC import mou_calc as _calc
from QC.views.control_chart import (_CC_LOCS, _CC_OFFICE, _uname, _user_labs, _is_admin, _can_review, _can_approve,
                                    _default_loc, _user_office, _sig_image, _sig_panels, _SIG_MIN, _FOOT_TOP)

_MOU_FORM = {'doc_no': 'ETAL-LAB-706-FF-01', 'issue_date': '', 'issue_no': '01', 'rev_no': '00'}
_MOU_MODULE = 'mou'
_MAX_OPS, _MAX_REPS = 5, 15
_DENIED = 'This action is reserved to the %s laboratory\'s QC / Lab Manager and the CEO / administrator.'


# ---------------------------------------------------------------- helpers
def _mou_docctrl(location):
    """Document-control numbers of the MOU form for a laboratory. The Karachi number is known to
    the system (ETAL-LAB-706-FF-01); Lahore enters its own on the Document control page."""
    known = location == 'Karachi'
    dflt = dict(_MOU_FORM) if known else {'doc_no': '', 'issue_date': '', 'issue_no': '01', 'rev_no': '00'}
    try:
        obj, _ = InventoryDocControl.objects.get_or_create(module=_MOU_MODULE, location=location, defaults=dflt)
        return {'doc_no': obj.doc_no or (dflt['doc_no'] or 'TBA'), 'issue_date': obj.issue_date or '-',
                'issue_no': obj.issue_no or '01', 'rev_no': obj.rev_no or '00', 'set': bool(obj.doc_no or dflt['doc_no'])}
    except Exception:
        d = dict(dflt); d['doc_no'] = d['doc_no'] or 'TBA'; d['issue_date'] = d['issue_date'] or '-'; d['set'] = known
        return d


class _Loc:
    """Minimal object with .location for the control-chart role helpers."""
    def __init__(self, location):
        self.location = location


def _can_manage(user, location):
    """Library, deletion, return-to-draft: the laboratory's QC / Lab Manager or the CEO / administrator."""
    if not (user and user.is_authenticated):
        return False
    return _can_approve(user, _Loc(location)) or location in _user_labs(user)


def _can_edit(user, st):
    """Draft: the chemist who created it, any colleague of that laboratory (e-signature office; a user
    without an office on the profile is not restricted), the lab's manager or the administrator. Submitted for review: the manager / administrator only
    (a chemist asks for it to be returned). Reviewed / approved / superseded: nobody."""
    if not (user and user.is_authenticated) or st.locked:
        return False
    if _can_manage(user, st.location):
        return True
    if st.status != 'draft':
        return False
    if st.created_by_id == user.id:
        return True
    labs = _user_labs(user)
    if labs and st.location not in labs:               # a manager of the other laboratory
        return False
    office = _user_office(user)
    return office == st.location or not office         # no office on the profile: not restricted by laboratory


def _loc_of(request):
    loc = request.GET.get('location') or request.session.get('mou_loc') or _default_loc(request)
    if loc not in _CC_LOCS:
        loc = 'Karachi'
    request.session['mou_loc'] = loc
    return loc


def _num(txt, errors=None, label='', required=False, positive=False):
    s = (txt if txt is not None else '').strip() if isinstance(txt, str) else txt
    if s in ('', None):
        if required and errors is not None:
            errors.append('%s is required.' % label)
        return None
    try:
        v = float(str(s).replace(',', ''))
        if _math.isnan(v) or _math.isinf(v):
            raise ValueError
        if positive and v <= 0:
            raise ValueError
        return v
    except ValueError:
        if errors is not None:
            errors.append('%s must be a %snumber.' % (label, 'positive ' if positive else ''))
        return None


def _pdate(txt):
    s = (txt or '').strip()
    for fmt in ('%d-%m-%Y', '%Y-%m-%d', '%d/%m/%Y'):
        try:
            return _dt.strptime(s, fmt).date()
        except ValueError:
            pass
    return None


def _key_q(st):
    return _Q(location=st.location, parameter__iexact=st.parameter.strip(), level__iexact=st.level.strip(), sample_kind=st.sample_kind)


def _fmt(v, dp=4):
    return _calc.fmt_sig(v, dp)


def _rows_for_view(st, r):
    """Budget / replicate rows for the templates and the PDF from a compute() result."""
    comps = []
    for c, m in zip(st.components.all(), r['components']):
        comps.append({'obj': c, 'kind': m['kind'], 'name': c.name, 'unit': c.unit or '-', 'range': _fmt(m['range']) if m['range'] else '-',
                      'magnitude': (c.magnitude if m['kind'] == _calc.KIND_B else _fmt(m['magnitude'])), 'magnitude_val': _fmt(m['magnitude']),
                      'rel': _fmt(m['rel']), 'dist': (_calc.DIST_PRINT.get(m['dist'], m['dist']) if m['kind'] == _calc.KIND_B else 'Normal'),
                      'divisor': m['divisor'] or '-', 'ci': _fmt(m['ci']), 'u': _fmt(m['u']), 'included': m['included'], 'note': m['note'] or c.note,
                      'source': c.source})
    ops = []
    for o, m in zip(st.operators.all(), r['operators']):
        ops.append({'obj': o, 'label': o.label, 'analyst': o.analyst, 'date': o.date, 'values': o.values, 'n': m['n'],
                    'mean': _calc.fmt_fix(m['mean'], st.decimals) if m['mean'] is not None else '-',
                    'sd': _calc.fmt_fix(m['sd'], st.decimals + 2) if m['sd'] is not None else '-'})
    return ops, comps


def _legacy_panel(st, r):
    """Workbook figures vs recomputed (induction)."""
    lg = st.legacy or {}
    if not lg:
        return None
    def diff(a, b):
        if a is None or b in (None, 0):
            return ''
        return '%+.1f %%' % ((b - a) / a * 100.0) if a else ''
    rows = [('Relative combined uc', lg.get('uc'), r['uc']), ('Relative expanded U (k=2)', lg.get('U'), r['U']),
            ('Expanded U, absolute', lg.get('U_abs'), r['U_abs']), ('Expanded U, %', lg.get('U_pct'), r['U_pct'])]
    out = [{'label': l, 'printed': _fmt(a), 'now': _fmt(b), 'diff': diff(a, b)} for l, a, b in rows]
    sds = lg.get('sd') or []
    for i, o in enumerate(r['operators']):
        if i < len(sds) and sds[i] is not None and o['sd'] is not None:
            out.append({'label': 'SD operator %s' % o['label'], 'printed': _fmt(sds[i]), 'now': _fmt(o['sd']), 'diff': diff(sds[i], o['sd'])})
    return {'rows': out, 'notes': lg.get('notes') or [], 'file': lg.get('file', ''), 'inducted': lg.get('inducted', '')}


# ---------------------------------------------------------------- register
def mou_list(request):
    loc = _loc_of(request)
    q = (request.GET.get('q') or '').strip()
    show = request.GET.get('show') or 'current'
    if show not in ('current', 'open', 'all'):
        show = 'current'
    qs = MouStudy.objects.filter(location=loc).select_related('created_by', 'submitted_by', 'reviewed_by', 'approved_by')
    if q:
        qs = qs.filter(_Q(parameter__icontains=q) | _Q(level__icontains=q) | _Q(method__icontains=q) | _Q(sample_ref__icontains=q) | _Q(instrument__icontains=q))
    if show == 'current':
        qs = qs.filter(status='approved')
    elif show == 'open':
        qs = qs.filter(status__in=('draft', 'review', 'reviewed'))
    rows = list(qs.order_by('parameter', 'level', 'sample_kind', '-version'))
    counts = {'current': MouStudy.objects.filter(location=loc, status='approved').count(),
              'open': MouStudy.objects.filter(location=loc, status__in=('draft', 'review', 'reviewed')).count(),
              'all': MouStudy.objects.filter(location=loc).count()}
    todo = {'sign': MouStudy.objects.filter(location=loc, status__in=('review', 'reviewed'), submitted_by__isnull=True).count(),
            'review': MouStudy.objects.filter(location=loc, status='review', submitted_by__isnull=False).count(), 'approve': MouStudy.objects.filter(location=loc, status='reviewed').count()}
    return render(request, 'mou_list.html', {
        'rows': rows, 'loc': loc, 'locs': _CC_LOCS, 'q': q, 'show': show, 'counts': counts, 'todo': todo,
        'can_review': _can_review(request.user, _Loc(loc)), 'can_approve': _can_approve(request.user, _Loc(loc)),
        'can_manage': _can_manage(request.user, loc), 'can_admin': _is_admin(request.user), 'ctrl': _mou_docctrl(loc)})


# ---------------------------------------------------------------- study: view
def mou_detail(request, pk):
    st = get_object_or_404(MouStudy.objects.select_related('created_by', 'reviewed_by', 'approved_by', 'submitted_by', 'supersedes'), pk=pk)
    r = _calc.compute(st.as_calc())
    ops, comps = _rows_for_view(st, r)
    user = request.user
    versions = MouStudy.objects.filter(_key_q(st)).order_by('-version')
    return render(request, 'mou_detail.html', {
        'st': st, 'r': r, 'ops': ops, 'comps': comps, 'legacy': _legacy_panel(st, r), 'versions': versions,
        'res': {'uc': _fmt(r['uc']), 'U': _fmt(r['U']), 'U_abs': _fmt(r['U_abs']), 'U_pct': _fmt(r['U_pct']),
                'mean': _calc.fmt_fix(r['grand']['mean'], st.decimals) if r['grand']['mean'] is not None else '-', 'n': r['grand']['n']},
        'rep_cols': range(1, max([len(o['values']) for o in ops] + [10]) + 1),
        'can_edit': _can_edit(user, st), 'can_submit': (st.status == 'draft' and not r['errors'] and _can_edit(user, st)),
        'can_sign': _can_sign(user, st), 'unsigned': (st.status in ('review', 'reviewed') and not st.submitted_by_id),
        'can_review': st.status == 'review' and _can_review(user, st) and bool(st.submitted_by_id), 'can_approve': st.status == 'reviewed' and _can_approve(user, st) and bool(st.submitted_by_id),
        'can_return': st.status in ('review', 'reviewed') and _can_manage(user, st.location),
        'can_unapprove': st.status == 'approved' and _is_admin(user), 'can_delete': _can_manage(user, st.location),
        'can_repeat': st.status in ('approved', 'superseded') and user.is_authenticated, 'ctrl': _mou_docctrl(st.location)})


# ---------------------------------------------------------------- study: edit / new
def _parse_study_form(request, st, errors):
    P = request.POST
    st.location = P.get('location') if P.get('location') in _CC_LOCS else st.location
    st.parameter = (P.get('parameter') or '').strip()[:80]
    if not st.parameter:
        errors.append('Parameter is required.')
    st.level = (P.get('level') or '').strip()[:60]
    st.unit = (P.get('unit') or '').strip()[:20]
    st.sample_kind = P.get('sample_kind') if P.get('sample_kind') in dict(MouStudy.KINDS) else 'CRM'
    st.sample_ref = (P.get('sample_ref') or '').strip()[:200]
    st.method = (P.get('method') or '').strip()[:120]
    st.instrument = (P.get('instrument') or '').strip()[:120]
    st.equipment_id = (P.get('equipment_id') or '').strip()[:60]
    st.range_value = _num(P.get('range_value'), errors, 'Range (x)', required=True, positive=True)
    st.env_temp = _num(P.get('env_temp'), errors, 'Environmental temperature')
    st.study_date = _pdate(P.get('study_date')) if (P.get('study_date') or '').strip() else None
    if (P.get('study_date') or '').strip() and not st.study_date:
        errors.append('Study date must be dd-mm-yyyy.')
    k = _num(P.get('k'), errors, 'Coverage factor k', positive=True)
    st.k = k if k else 2.0
    try:
        st.decimals = max(0, min(6, int(P.get('decimals') or 3)))
    except ValueError:
        st.decimals = 3
    st.remarks = (P.get('remarks') or '').strip()[:4000]
    # operators
    ops = []
    op_idx = sorted({int(m.group(1)) for k in P for m in [_re.match(r'^op(\d+)_present$', k)] if m})
    if len(op_idx) > _MAX_OPS:
        errors.append('At most %d operators.' % _MAX_OPS)
    for i in op_idx[:_MAX_OPS]:
        vals = []
        for j in range(_MAX_REPS):
            t = (P.get('op%d_v%d' % (i, j)) or '').strip()
            if not t:
                continue
            v = _num(t, errors, 'Operator %s replicate %d' % (chr(65 + i), j + 1))
            if v is not None:
                vals.append(v)
        d = _pdate(P.get('op%d_date' % i)) if (P.get('op%d_date' % i) or '').strip() else None
        if (P.get('op%d_date' % i) or '').strip() and not d:
            errors.append('Operator %s date must be dd-mm-yyyy.' % chr(65 + i))
        ops.append({'order': i, 'label': (P.get('op%d_label' % i) or chr(65 + i)).strip()[:4] or chr(65 + i),
                    'analyst': (P.get('op%d_analyst' % i) or '').strip()[:80], 'date': d, 'values': vals})
    # components
    comps = []
    c_idx = sorted({int(m.group(1)) for k in P for m in [_re.match(r'^c(\d+)_kind$', k)] if m})
    if len(c_idx) > 60:
        errors.append('At most 60 budget rows.')
    for i in c_idx[:60]:
        kind = P.get('c%d_kind' % i)
        if kind not in ('a_rep', 'a_repro', 'b'):
            continue
        name = (P.get('c%d_name' % i) or '').strip()[:160]
        if kind == 'b' and not name and not (P.get('c%d_magnitude' % i) or '').strip():
            continue                                             # empty spare row
        if kind == 'b' and not name:
            errors.append('Type B row %d has no source name.' % (i + 1))
        src = None
        if (P.get('c%d_source' % i) or '').isdigit():
            src = MouSource.objects.filter(pk=int(P['c%d_source' % i]), location=st.location).first()
        comps.append({'order': i, 'kind': kind, 'source': src, 'name': name or dict(MouComponent.KINDS)[kind],
                      'unit': (P.get('c%d_unit' % i) or '').strip()[:20], 'range_value': _num(P.get('c%d_range' % i)) if kind == 'b' else None,
                      'magnitude': (P.get('c%d_magnitude' % i) or '').strip()[:60] if kind == 'b' else '',
                      'dist': P.get('c%d_dist' % i) if P.get('c%d_dist' % i) in _calc.DIST_DIV else 'normal',
                      'ci': _num(P.get('c%d_ci' % i)) if (P.get('c%d_ci' % i) or '').strip() else 1.0,
                      'included': kind != 'b' or bool(P.get('c%d_included' % i)), 'note': (P.get('c%d_note' % i) or '').strip()[:300]})
    if not any(c['kind'] == 'a_rep' for c in comps):
        comps.insert(0, {'order': 0, 'kind': 'a_rep', 'source': None, 'name': 'Type A - repeatability (u rep)', 'unit': st.unit, 'range_value': None,
                         'magnitude': '', 'dist': 'normal', 'ci': 1.0, 'included': True, 'note': ''})
    if not any(c['kind'] == 'a_repro' for c in comps):
        comps.insert(1, {'order': 1, 'kind': 'a_repro', 'source': None, 'name': 'Type A - reproducibility (u repro)', 'unit': st.unit, 'range_value': None,
                         'magnitude': '', 'dist': 'normal', 'ci': 1.0, 'included': True, 'note': ''})
    return ops, comps


def _calc_from_post(request, st):
    """compute() straight from the posted form (live calculation / error display before saving)."""
    errors = []
    tmp = MouStudy(location=st.location if st else 'Karachi')
    ops, comps = _parse_study_form(request, tmp, errors)
    study = {'range': tmp.range_value, 'k': tmp.k, 'operators': [{'label': o['label'], 'values': o['values']} for o in ops],
             'components': [{'kind': c['kind'], 'name': c['name'], 'unit': c['unit'], 'range': c['range_value'], 'magnitude': c['magnitude'],
                             'dist': c['dist'], 'ci': c['ci'], 'included': c['included']} for c in comps]}
    r = _calc.compute(study)
    return tmp, ops, comps, r, errors


def _library_json(location):
    out = []
    for s in MouSource.objects.filter(location=location, active=True):
        out.append({'id': s.pk, 'category': s.get_category_display(), 'name': s.name, 'unit': s.unit, 'range': s.range_value,
                    'magnitude': s.magnitude, 'dist': s.dist, 'ci': s.ci, 'reference': s.reference, 'validity': s.validity,
                    'valid_until': s.valid_until.strftime('%d-%m-%Y') if s.valid_until else ''})
    return out


def mou_edit(request, pk=None):
    st = get_object_or_404(MouStudy, pk=pk) if pk else None
    user = request.user
    if st is not None and not _can_edit(user, st):
        return HttpResponse('This study is %s and can no longer be edited%s.' % (
            st.get_status_display().lower(), '' if st.locked else ' by you'), status=403)
    if st is None and not (user.is_authenticated and user.is_active):
        return _redirect('/login/')
    errors = []
    if request.method == 'POST':
        new = st is None
        obj = st or MouStudy(created_by=user, location=_loc_of(request))
        ops, comps = _parse_study_form(request, obj, errors)
        office = _user_office(user)
        if office and obj.location != office and not _can_manage(user, obj.location):
            errors.append('Studies of the %s laboratory are entered by its own staff; your profile is %s.' % (obj.location, office))
        from django.utils.html import escape as _esc
        errors[:] = [_esc(e) for e in errors]          # the template renders this list unescaped (one message carries a link)
        if obj.range_value and obj.range_value > 0:
            allv = [v for o in ops for v in o['values']]
            if allv and sum(allv) / len(allv) > obj.range_value:
                errors.append('The range (x) must be at least the measured mean (%.4g): enter the method / calibration range, not the level.' % (sum(allv) / len(allv)))
        if not errors:
            # one open version per parameter / level / sample kind (new studies and key changes on edit);
            # a new study of an existing key is its next version and supersedes the approved one
            same = MouStudy.objects.filter(_key_q(obj))
            if not new:
                same = same.exclude(pk=obj.pk)
            open_v = same.filter(status__in=('draft', 'review', 'reviewed')).first()
            if open_v:
                errors.append('%s (%s) already has an open version %d (%s) - <a href="/qc/mou/%d/">open it</a> instead of starting another.' % (
                    _esc(obj.title), obj.sample_kind, open_v.version, open_v.get_status_display().lower(), open_v.pk))
            else:
                top = same.order_by('-version').first()
                if new or (top and top.version >= obj.version):
                    obj.version = (top.version + 1) if top else 1
                    obj.supersedes = same.filter(status='approved').order_by('-version').first()
        if not errors:
            obj.save()
            obj.operators.all().delete()
            for o in ops:
                MouOperator.objects.create(study=obj, **o)
            obj.components.all().delete()
            for c in comps:
                MouComponent.objects.create(study=obj, **c)
            r = obj.recompute()
            _msg.success(request, 'Study %s v%d saved.%s' % (obj.title, obj.version, ' Correct the calculation notes before submitting it for review.' if r['errors'] else ''))
            return _redirect('mou_detail', obj.pk)
        f = _form_ctx_from_post(request, obj, ops, comps)
    else:
        f = _form_ctx(st, request)
    loc = f['location']
    return render(request, 'mou_edit.html', {
        'st': st, 'f': f, 'errors': errors, 'locs': _CC_LOCS, 'kinds': MouStudy.KINDS, 'dists': _calc.DISTRIBUTIONS,
        'library': _library_json(loc), 'rep_cols': range(_MAX_REPS), 'max_ops': _MAX_OPS, 'can_manage': _can_manage(user, loc)})


def _form_ctx(st, request):
    if st is None:
        loc = _loc_of(request)
        return {'location': loc, 'parameter': '', 'level': '', 'unit': 'mg/L', 'sample_kind': 'CRM', 'sample_ref': '', 'method': '', 'instrument': '',
                'equipment_id': '', 'range_value': '', 'env_temp': '', 'study_date': _date.today().strftime('%d-%m-%Y'), 'k': '2', 'decimals': 3, 'remarks': '',
                'operators': [{'order': i, 'label': chr(65 + i), 'analyst': '', 'date': '', 'values': []} for i in range(3)],
                'components': [{'order': 0, 'kind': 'a_rep', 'name': 'Type A - repeatability (u rep)', 'unit': 'mg/L', 'range_value': '', 'magnitude': '', 'dist': 'normal', 'ci': '1', 'included': True, 'note': '', 'source': ''},
                               {'order': 1, 'kind': 'a_repro', 'name': 'Type A - reproducibility (u repro)', 'unit': 'mg/L', 'range_value': '', 'magnitude': '', 'dist': 'normal', 'ci': '1', 'included': True, 'note': '', 'source': ''}]}
    return {'location': st.location, 'parameter': st.parameter, 'level': st.level, 'unit': st.unit, 'sample_kind': st.sample_kind, 'sample_ref': st.sample_ref,
            'method': st.method, 'instrument': st.instrument, 'equipment_id': st.equipment_id, 'range_value': _calc.fmt_sig(st.range_value, 8) if st.range_value else '',
            'env_temp': _calc.fmt_sig(st.env_temp, 6) if st.env_temp is not None else '', 'study_date': st.study_date.strftime('%d-%m-%Y') if st.study_date else '',
            'k': _calc.fmt_sig(st.k, 4), 'decimals': st.decimals, 'remarks': st.remarks,
            'operators': [{'order': o.order, 'label': o.label, 'analyst': o.analyst, 'date': o.date.strftime('%d-%m-%Y') if o.date else '', 'values': o.values} for o in st.operators.all()],
            'components': [{'order': c.order, 'kind': c.kind, 'name': c.name, 'unit': c.unit, 'range_value': _calc.fmt_sig(c.range_value, 8) if c.range_value else '',
                            'magnitude': c.magnitude, 'dist': c.dist, 'ci': _calc.fmt_sig(c.ci, 4), 'included': c.included, 'note': c.note, 'source': c.source_id or ''} for c in st.components.all()]}


def _form_ctx_from_post(request, obj, ops, comps):
    P = request.POST
    return {'location': obj.location, 'parameter': obj.parameter, 'level': obj.level, 'unit': obj.unit, 'sample_kind': obj.sample_kind, 'sample_ref': obj.sample_ref,
            'method': obj.method, 'instrument': obj.instrument, 'equipment_id': obj.equipment_id, 'range_value': P.get('range_value', ''), 'env_temp': P.get('env_temp', ''),
            'study_date': P.get('study_date', ''), 'k': P.get('k', '2'), 'decimals': obj.decimals, 'remarks': obj.remarks,
            'operators': [{'order': o['order'], 'label': o['label'], 'analyst': o['analyst'], 'date': P.get('op%d_date' % o['order'], ''),
                           'values': [P.get('op%d_v%d' % (o['order'], j), '') for j in range(_MAX_REPS)]} for o in ops],
            'components': [{'order': c['order'], 'kind': c['kind'], 'name': c['name'], 'unit': c['unit'], 'range_value': P.get('c%d_range' % c['order'], ''),
                            'magnitude': c['magnitude'], 'dist': c['dist'], 'ci': P.get('c%d_ci' % c['order'], '1'), 'included': c['included'], 'note': c['note'],
                            'source': c['source'].pk if c['source'] else ''} for c in comps]}


# ---------------------------------------------------------------- live calculation (JSON)
def mou_api_calc(request):
    """POST the study form; returns the computed budget so the page shows the figures as they are typed.
    Nothing is saved."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)
    tmp, ops, comps, r, errors = _calc_from_post(request, None)
    dp = tmp.decimals
    out = {'errors': errors + r['errors'], 'warnings': r['warnings'],
           'operators': [{'label': o['label'], 'n': o['n'], 'mean': _calc.fmt_fix(o['mean'], dp) if o['mean'] is not None else '-',
                          'sd': _calc.fmt_fix(o['sd'], dp + 2) if o['sd'] is not None else '-'} for o in r['operators']],
           'grand': {'n': r['grand']['n'], 'mean': _calc.fmt_fix(r['grand']['mean'], dp) if r['grand']['mean'] is not None else '-'},
           'components': [{'order': c['order'], 'magnitude': _fmt(m['magnitude']), 'rel': _fmt(m['rel']), 'divisor': m['divisor'] or '-', 'u': _fmt(m['u']),
                           'included': m['included'], 'note': m['note']} for c, m in zip(comps, r['components'])],
           'uc': _fmt(r['uc']), 'U': _fmt(r['U']), 'U_abs': _fmt(r['U_abs']), 'U_pct': _fmt(r['U_pct']), 'unit': tmp.unit}
    return JsonResponse(out)


def mou_api_lookup(request):
    """Current (approved) expanded uncertainty: ?location=&parameter=&level=[&kind=] -> one study;
    without parameter -> all current studies of the laboratory. For the test-report link later."""
    loc = request.GET.get('location') or 'Karachi'
    qs = MouStudy.objects.filter(location=loc, status='approved')
    par, lvl, kind = (request.GET.get('parameter') or '').strip(), (request.GET.get('level') or '').strip(), (request.GET.get('kind') or '').strip()
    if par:
        qs = qs.filter(parameter__iexact=par)
    if lvl:
        qs = qs.filter(level__iexact=lvl)
    if kind:
        qs = qs.filter(sample_kind=kind)
    rows = [{'id': s.pk, 'location': s.location, 'parameter': s.parameter, 'level': s.level, 'sample_kind': s.sample_kind, 'unit': s.unit,
             'method': s.method, 'version': s.version, 'mean': s.mean, 'uc_rel': s.uc, 'U_rel': s.u_exp, 'U_abs': s.u_abs, 'U_pct': s.u_pct, 'k': s.k,
             'approved_on': s.approved_at.strftime('%d-%m-%Y') if s.approved_at else ''} for s in qs.order_by('parameter', 'level')]
    return JsonResponse({'count': len(rows), 'studies': rows})


# ---------------------------------------------------------------- workflow
def _post_only(request, pk):
    if request.method != 'POST':
        return _redirect('mou_detail', pk)
    return None


def _can_sign(user, st):
    """Sign as preparer (studies inducted from the workbooks carry no preparer): the laboratory's own
    staff - a user whose e-signature office is that laboratory (or who has no office on the profile),
    the lab's manager or the administrator. Owner request 22-10-2026."""
    if not (user and user.is_authenticated) or st.locked or st.submitted_by_id or st.status not in ('review', 'reviewed'):
        return False
    if _can_manage(user, st.location):
        return True
    labs = _user_labs(user)
    if labs and st.location not in labs:
        return False
    office = _user_office(user)
    return office == st.location or not office


def _apply_action(user, st, act, reason=''):
    """One workflow action on one study. Returns (status, message) with status 'ok' | 'error' |
    'forbidden'. Shared by the study page buttons and the bulk signing page, so both apply exactly
    the same checks. Every signature is the signed-in user's own (name + e-signature on the PDF)."""
    now = _tz.now()
    r = _calc.compute(st.as_calc())
    if act == 'submit':
        if st.status != 'draft':
            return 'error', 'Only a draft can be submitted.'
        if not _can_edit(user, st):
            return 'forbidden', 'Only the laboratory\'s own staff may submit this study for review.'
        if r['errors']:
            return 'error', 'The study cannot be submitted until the calculation notes are resolved: ' + ' '.join(r['errors'])
        st.status, st.submitted_by, st.submitted_at = 'review', user, now
        st.recompute(save=False); st.save()
        return 'ok', 'Signed as prepared by you and submitted for review by the %s QC / Lab Manager.' % st.location
    if act == 'sign':
        if st.submitted_by_id:
            return 'error', 'This study already carries a Prepared-by signature (%s).' % _uname(st.submitted_by)
        if not _can_sign(user, st):
            return 'forbidden', 'Prepared-by signing of %s studies is reserved to the %s laboratory\'s own staff.' % (st.location, st.location)
        st.submitted_by, st.submitted_at = user, now
        if st.reviewed_at:                    # a review made before the record was signed is not valid
            st.reviewed_by = st.reviewed_at = None
            st.status = 'review'
        st.save()
        return 'ok', 'Signed as prepared by you (%s).' % _tz.localtime(now).strftime('%d-%m-%Y %H:%M')
    if act == 'review':
        if st.status != 'review' or not _can_review(user, st):
            return 'forbidden', _DENIED % st.location
        if not st.submitted_by_id:
            return 'error', 'Cannot review yet: the study carries no Prepared-by signature (inducted record) - the preparing chemist signs first.'
        st.status, st.reviewed_by, st.reviewed_at = 'reviewed', user, now
        st.recompute(save=False); st.save()
        return 'ok', 'Reviewed and signed. The study now awaits the CEO\'s approval.'
    if act == 'approve':
        if st.status != 'reviewed' or not _can_approve(user, st):
            return 'forbidden', _DENIED % st.location
        if not st.submitted_by_id:
            return 'error', 'Cannot approve: the study carries no Prepared-by signature.'
        st.status, st.approved_by, st.approved_at = 'approved', user, now
        st.recompute(save=False); st.save()
        n = MouStudy.objects.filter(_key_q(st)).filter(status='approved').exclude(pk=st.pk).update(status='superseded')
        # earlier versions still open (e.g. an inducted 2025 workbook beside its 2026 repeat) are closed as well
        m = MouStudy.objects.filter(_key_q(st)).filter(status__in=('draft', 'review', 'reviewed'), version__lt=st.version).exclude(pk=st.pk).update(status='superseded')
        return 'ok', 'Approved and locked.%s%s' % (' The previous approved version is now superseded.' if n else '',
                                                   (' %d earlier open version(s) closed as superseded.' % m) if m else '')
    if act == 'return':
        if st.status not in ('review', 'reviewed') or not _can_manage(user, st.location):
            return 'forbidden', _DENIED % st.location
        why = (reason or '').strip()
        if len(why) < 5:
            return 'error', 'Give the reason for returning the study (at least 5 characters).'
        st.status = 'draft'
        st.reviewed_by = st.reviewed_at = None
        st.remarks = (st.remarks + '\n' if st.remarks else '') + 'Returned to draft %s by %s: %s' % (now.strftime('%d-%m-%Y'), _uname(user), why[:500])
        st.save()
        return 'ok', 'Returned to draft; the reason is recorded in the remarks.'
    if act == 'unapprove':
        if st.status != 'approved' or not _can_approve(user, st):
            return 'forbidden', 'Only the CEO / administrator can unapprove a study.'
        why = (reason or '').strip()
        if len(why) < 5:
            return 'error', 'Give the reason for unapproving (at least 5 characters).'
        st.status, st.approved_by, st.approved_at = 'reviewed', None, None
        st.remarks = (st.remarks + '\n' if st.remarks else '') + 'Unapproved %s by %s: %s' % (now.strftime('%d-%m-%Y'), _uname(user), why[:500])
        st.save()
        return 'ok', 'Unapproved. The study is back at the reviewed stage; the register has no current value for it until it is approved again.'
    return 'error', 'Unknown action.'


def mou_action(request, pk):
    back = _post_only(request, pk)
    if back:
        return back
    st = get_object_or_404(MouStudy, pk=pk)
    status, text = _apply_action(request.user, st, request.POST.get('action'), request.POST.get('reason') or '')
    if status == 'forbidden':
        return HttpResponse(text, status=403)
    (_msg.success if status == 'ok' else _msg.error)(request, text)
    return _redirect('mou_detail', pk)


# ---------------------------------------------------------------- bulk signing (22-10-2026, as the control charts)
def mou_signing(request):
    """Sign-off of many studies at once: the preparing chemist signs the inducted studies as
    Prepared by, the QC / Lab Manager reviews and the CEO / administrator approves and locks.
    Every study goes through exactly the same checks as the buttons on the study page."""
    user = request.user
    loc = request.GET.get('location') or _user_office(user) or _default_loc(request)
    loc = loc if loc in _CC_LOCS else 'Karachi'
    show = request.GET.get('show') or 'sign'
    show = show if show in ('sign', 'review', 'approve', 'all') else 'sign'
    if request.method == 'POST':
        action = request.POST.get('action')
        if action not in ('sign', 'review', 'approve'):
            return HttpResponse('unknown action', status=400)
        ids = [int(x) for x in request.POST.getlist('rec')[:500] if x.isdigit()]
        done, problems = 0, []
        for st in MouStudy.objects.filter(pk__in=ids, location=loc).select_related('submitted_by').order_by('parameter', 'level', 'version'):
            status, text = _apply_action(user, st, action)
            if status == 'ok':
                done += 1
            else:
                problems.append('%s (%s) v%d: %s' % (st.title, st.sample_kind, st.version, text))
        verb = {'sign': 'signed as prepared by you', 'review': 'reviewed and signed', 'approve': 'approved and locked'}[action]
        if done:
            _msg.success(request, '%d stud%s %s.' % (done, 'y' if done == 1 else 'ies', verb))
        for t in problems[:8]:
            _msg.error(request, t)
        if len(problems) > 8:
            _msg.error(request, '... and %d more stud(ies) were skipped.' % (len(problems) - 8))
        if not done and not problems:
            _msg.info(request, 'Tick at least one study.')
        return _redirect(request.get_full_path())
    qs = MouStudy.objects.filter(location=loc).exclude(status__in=('draft', 'superseded')).select_related('submitted_by', 'reviewed_by', 'approved_by')
    rows = []
    for st in qs.order_by('parameter', 'level', 'sample_kind', '-version'):
        stage = 'approved' if st.status == 'approved' else 'sign' if not st.submitted_by_id else 'approve' if st.status == 'reviewed' else 'review'
        if show != 'all' and stage != show:
            continue
        rows.append({'st': st, 'stage': stage})
    probe = _Loc(loc)
    return render(request, 'mou_signing.html', {
        'rows': rows, 'loc': loc, 'locs': _CC_LOCS, 'show': show,
        'can_sign': _can_manage(user, loc) or ((not _user_labs(user) or loc in _user_labs(user)) and (_user_office(user) in (loc, '', None))),
        'can_review': _can_review(user, probe), 'can_approve': _can_approve(user, probe), 'ctrl': _mou_docctrl(loc)})


def mou_repeat(request, pk):
    """New version of an approved / superseded study: same master and budget, Type B rows refreshed
    from the library (a re-calibrated source carries its new values), replicates empty."""
    back = _post_only(request, pk)
    if back:
        return back
    old = get_object_or_404(MouStudy, pk=pk)
    user = request.user
    if not user.is_authenticated:
        return _redirect('/login/')
    labs, office = _user_labs(user), _user_office(user)
    allowed = _can_manage(user, old.location) or (labs and old.location in labs) or (not labs and (not office or office == old.location))
    if not allowed:
        return HttpResponse(_DENIED % old.location, status=403)
    open_v = MouStudy.objects.filter(_key_q(old)).filter(status__in=('draft', 'review', 'reviewed')).first()
    if open_v:
        _msg.warning(request, 'Version %d of this study is already open (%s).' % (open_v.version, open_v.get_status_display().lower()))
        return _redirect('mou_detail', open_v.pk)
    top = MouStudy.objects.filter(_key_q(old)).order_by('-version').first()
    st = MouStudy(location=old.location, parameter=old.parameter, level=old.level, unit=old.unit, sample_kind=old.sample_kind, sample_ref=old.sample_ref,
                  method=old.method, instrument=old.instrument, equipment_id=old.equipment_id, range_value=old.range_value, env_temp=None,
                  study_date=_date.today(), k=old.k, decimals=old.decimals, version=(top.version if top else old.version) + 1,
                  supersedes=(MouStudy.objects.filter(_key_q(old)).filter(status='approved').order_by('-version').first() or old),
                  created_by=user, remarks='Repeat of v%d.' % old.version)
    st.save()
    for o in old.operators.all():
        MouOperator.objects.create(study=st, order=o.order, label=o.label, analyst='', date=None, values=[])
    refreshed = 0
    for c in old.components.all():
        d = {'order': c.order, 'kind': c.kind, 'source': c.source, 'name': c.name, 'unit': c.unit, 'range_value': c.range_value, 'magnitude': c.magnitude,
             'dist': c.dist, 'ci': c.ci, 'included': c.included, 'note': ''}
        if c.kind == 'b' and c.source and c.source.active:
            s = c.source
            if (s.magnitude, s.range_value, s.dist, s.ci, s.unit) != (c.magnitude, c.range_value, c.dist, c.ci, c.unit):
                refreshed += 1
                d['note'] = 'refreshed from the library %s' % _date.today().strftime('%d-%m-%Y')
            d.update(name=s.name, unit=s.unit, range_value=s.range_value, magnitude=s.magnitude, dist=s.dist, ci=s.ci)
        MouComponent.objects.create(study=st, **d)
    st.recompute()
    _msg.success(request, 'Version %d created as a draft: enter the new replicates.%s' % (st.version, (' %d Type B row(s) took updated values from the library.' % refreshed) if refreshed else ''))
    return _redirect('mou_edit', st.pk)


def _snap_study(st):
    return {'study': {f.name: (getattr(st, f.attname).isoformat() if hasattr(getattr(st, f.attname), 'isoformat') else getattr(st, f.attname)) for f in st._meta.concrete_fields},
            'operators': [{'label': o.label, 'analyst': o.analyst, 'date': o.date.isoformat() if o.date else None, 'values': o.values} for o in st.operators.all()],
            'components': [{'kind': c.kind, 'name': c.name, 'unit': c.unit, 'range': c.range_value, 'magnitude': c.magnitude, 'dist': c.dist, 'ci': c.ci,
                            'included': c.included, 'note': c.note, 'source': c.source_id} for c in st.components.all()]}


def mou_delete(request, pk):
    back = _post_only(request, pk)
    if back:
        return back
    st = get_object_or_404(MouStudy, pk=pk)
    if not _can_manage(request.user, st.location):
        return HttpResponse(_DENIED % st.location, status=403)
    reason = (request.POST.get('reason') or '').strip()
    if len(reason) < 5:
        _msg.error(request, 'Nothing was deleted: a reason (at least 5 characters) is required.')
        return _redirect('mou_detail', pk)
    label = '%s %s [%s] v%d - %s MOU (%s)' % (st.parameter, st.level, st.sample_kind, st.version, st.location, st.status)
    ControlChartDeletion.objects.create(kind='mou_study', chart_ref=st.pk, location=st.location, activity='MOU', label=label[:300], reason=reason[:2000],
                                        snapshot=_json.loads(_json.dumps(_snap_study(st), default=str)), deleted_by=request.user)
    loc = st.location
    st.delete()
    _msg.success(request, 'Study deleted: %s. The reason and a copy of the data are kept in the deletion log.' % label)
    return _redirect('/qc/mou/?location=%s&show=all' % loc)


def mou_deletions(request):
    user = request.user
    labs = _user_labs(user)
    if not (_is_admin(user) or labs):
        return HttpResponse('The deletion log is available to the QC / Lab Managers and the CEO / administrator.', status=403)
    qs = ControlChartDeletion.objects.filter(kind__startswith='mou').select_related('deleted_by')
    if labs and not (_is_admin(user) and not labs):
        qs = qs.filter(location__in=labs)
    return render(request, 'mou_deletions.html', {'rows': qs[:500]})


# ---------------------------------------------------------------- library
def mou_library(request):
    loc = _loc_of(request)
    user = request.user
    can = _can_manage(user, loc)
    edit = MouSource.objects.filter(pk=int(request.GET['edit']), location=loc).first() if (request.GET.get('edit') or '').isdigit() else None
    if request.method == 'POST':
        if not can:
            return HttpResponse(_DENIED % loc, status=403)
        P = request.POST
        act = P.get('action')
        if act in ('deactivate', 'activate'):
            s = get_object_or_404(MouSource, pk=int(P.get('id') or 0) if (P.get('id') or '').isdigit() else 0, location=loc)
            s.active = act == 'activate'
            s.save(update_fields=['active', 'updated_at'])
            _msg.success(request, '%s %s.' % (s.name, 'reactivated' if s.active else 'deactivated (kept for the studies that use it)'))
            return _redirect('/qc/mou/library/?location=%s' % loc)
        errors = []
        s = MouSource.objects.filter(pk=int(P['id']), location=loc).first() if (P.get('id') or '').isdigit() else MouSource(location=loc, created_by=user)
        s.category = P.get('category') if P.get('category') in dict(MouSource.CATEGORIES) else 'other'
        s.name = (P.get('name') or '').strip()[:160]
        if not s.name:
            errors.append('Name is required.')
        s.unit = (P.get('unit') or '').strip()[:20]
        s.range_value = _num(P.get('range_value'), errors, 'Range (x)', required=True, positive=True) or 0
        s.magnitude = (P.get('magnitude') or '').strip()[:60]
        try:
            if _calc.eval_expr(s.magnitude) < 0:
                errors.append('Magnitude must not be negative.')
        except ValueError:
            errors.append('Magnitude must be a number or an expression such as 0.08/2.')
        s.dist = P.get('dist') if P.get('dist') in _calc.DIST_DIV else 'normal'
        s.ci = _num(P.get('ci'), errors, 'Sensitivity coefficient') or 1.0
        s.reference = (P.get('reference') or '').strip()[:160]
        s.calibrated_on = _pdate(P.get('calibrated_on'))
        s.valid_until = _pdate(P.get('valid_until'))
        for fld in ('calibrated_on', 'valid_until'):
            if (P.get(fld) or '').strip() and not getattr(s, fld):
                errors.append('%s must be dd-mm-yyyy.' % fld.replace('_', ' ').capitalize())
        s.note = (P.get('note') or '').strip()[:300]
        if errors:
            for e in errors:
                _msg.error(request, e)
            edit = s
        else:
            s.save()
            _msg.success(request, 'Library entry saved: %s.' % s.name)
            return _redirect('/qc/mou/library/?location=%s' % loc)
    q = (request.GET.get('q') or '').strip()
    qs = MouSource.objects.filter(location=loc)
    if q:
        qs = qs.filter(_Q(name__icontains=q) | _Q(reference__icontains=q) | _Q(category__icontains=q))
    rows = []
    for s in qs:
        rows.append({'s': s, 'uses': s.uses.count(), 'mag': _fmt(s.magnitude_value), 'validity': s.validity})
    return render(request, 'mou_library.html', {'rows': rows, 'loc': loc, 'locs': _CC_LOCS, 'q': q, 'can': can, 'edit': edit,
                                                'cats': MouSource.CATEGORIES, 'dists': _calc.DISTRIBUTIONS, 'count': len(rows)})


# ---------------------------------------------------------------- document control (admin) / manual
def mou_doccontrol(request):
    if not _is_admin(request.user):
        return HttpResponse('Document-control numbers are maintained by an administrator.', status=403)
    if request.method == 'POST':
        loc = request.POST.get('location')
        if loc not in _CC_LOCS:
            return HttpResponse('bad request', status=400)
        obj, _ = InventoryDocControl.objects.get_or_create(module=_MOU_MODULE, location=loc)
        obj.doc_no = (request.POST.get('doc_no') or '').strip()[:60]
        obj.issue_date = (request.POST.get('issue_date') or '').strip()[:20]
        obj.issue_no = (request.POST.get('issue_no') or '').strip()[:10] or '01'
        obj.rev_no = (request.POST.get('rev_no') or '').strip()[:10] or '00'
        obj.updated_by = request.user
        obj.save()
        _msg.success(request, 'Document control updated for the %s MOU form.' % loc)
        return _redirect('mou_doccontrol')
    grid = []
    for loc in _CC_LOCS:
        d = _mou_docctrl(loc)
        raw = InventoryDocControl.objects.filter(module=_MOU_MODULE, location=loc).first()
        grid.append({'location': loc, 'doc_no': raw.doc_no if raw else '', 'issue_date': raw.issue_date if raw else '', 'issue_no': d['issue_no'],
                     'rev_no': d['rev_no'], 'shown': d['doc_no'], 'set': d['set'], 'updated': raw.updated_at if raw else None, 'by': raw.updated_by if raw else None})
    return render(request, 'mou_doccontrol.html', {'grid': grid, 'office': _CC_OFFICE})


def mou_manual(request):
    return render(request, 'mou_manual.html', {})


# ---------------------------------------------------------------- PDF (form ETAL-LAB-706-FF-01)
def mou_pdf(request, pk):
    import os as _os
    st = get_object_or_404(MouStudy.objects.select_related('reviewed_by', 'approved_by', 'submitted_by', 'created_by'), pk=pk)
    r = _calc.compute(st.as_calc())
    ops, comps = _rows_for_view(st, r)
    legacy = _legacy_panel(st, r)
    ctrl = _mou_docctrl(st.location)
    office = _CC_OFFICE.get(st.location, _CC_OFFICE['Karachi'])
    from django.conf import settings as _settings
    _base = str(getattr(_settings, 'BASE_DIR', '') or '')
    _LOGO, _CAL, _CALB = [_os.path.join(_base, p_) if _base else p_ for p_ in ('static/assets/EnviTechAL LOGO.png', 'static/fonts/calibri.ttf', 'static/fonts/calibrib.ttf')]
    GREEN, GREY_FILL, LINE = (15, 81, 50), (242, 245, 243), (120, 120, 120)
    wm = {'approved': '', 'superseded': 'SUPERSEDED'}.get(st.status, 'NOT APPROVED')
    sub = '%s LABORATORY  -  %s  -  %s  -  v%d' % (st.location.upper(), st.parameter.upper(), (st.level or '').upper(), st.version)

    class PDF(FPDF):
        def __init__(self):
            super().__init__('P', 'mm', 'A4')
            self.fam = 'Helvetica'
            try:
                if _os.path.exists(_CAL):
                    self.add_font('Calibri', '', _CAL); self.add_font('Calibri', 'B', _CALB if _os.path.exists(_CALB) else _CAL)
                    self.fam = 'Calibri'
            except Exception:
                pass

        def header(self):
            if wm:
                self.set_font(self.fam, 'B', 54); self.set_text_color(238, 238, 238)
                try:
                    with self.rotation(45, self.w / 2, self.h / 2):
                        self.text(self.w / 2 - self.get_string_width(wm) / 2, self.h / 2 + 10, wm)
                except Exception:
                    pass
                self.set_text_color(0, 0, 0)
            if _os.path.exists(_LOGO):
                try:
                    self.image(_LOGO, 10, 8, 20, 22)
                except Exception:
                    pass
            lines = ['Doc. No: %s' % ctrl['doc_no'], 'Issue Date: %s' % ctrl['issue_date'],
                     'Issue No. %s    Rev. No. %s' % (ctrl['issue_no'], ctrl['rev_no']), 'Page No: %d of {nb}' % self.page_no()]
            self.set_font(self.fam, '', 7)
            bw = max(self.get_string_width(l.replace('{nb}', '99')) for l in lines) + 5.0
            bx, by, lh = 200.0 - bw, 8.0, 4.4
            self.set_draw_color(*LINE); self.set_fill_color(*GREY_FILL)
            self.rect(bx, by, bw, lh * len(lines) + 1.6, 'DF')
            for i, l in enumerate(lines):
                self.set_xy(bx + 2.0, by + 0.8 + i * lh); self.cell(bw - 4.0, lh, l, 0, 0, 'L')
            self.set_text_color(*GREEN)
            self.set_xy(10, 8.5); self.set_font(self.fam, 'B', 15); self.cell(190, 7, 'ENVI TECH AL', align='C', ln=1)
            self.set_x(10); self.set_font(self.fam, '', 8); self.set_text_color(70, 70, 70)
            self.cell(190, 4.5, 'Analytical Laboratory - Environmental & Water Testing', align='C', ln=1)
            self.set_x(10); self.set_font(self.fam, 'B', 10.5); self.set_text_color(0, 0, 0)
            self.cell(190, 5.5, 'MEASUREMENT OF UNCERTAINTY RECORD', align='C', ln=1)
            self.set_x(10); self.set_font(self.fam, 'B', 8.5); self.set_text_color(*GREEN)
            self.cell(190, 4.5, sub, align='C', ln=1)
            self.set_text_color(0, 0, 0)
            self.set_draw_color(*GREEN); self.set_line_width(0.5); self.line(10, 33, 200, 33)
            self.set_line_width(0.2); self.set_draw_color(0, 0, 0); self.set_y(36.5)

        def footer(self):
            self.set_y(-20); self.set_font(self.fam, '', 6.5); self.set_text_color(90, 90, 90)
            self.cell(0, 4, 'ENVI TECH AL  -  Controlled document.  Uncontrolled when printed.', align='C', ln=1)
            self.set_text_color(0, 0, 0); self.set_draw_color(*GREEN); self.set_line_width(0.4)
            yb = self.get_y() + 0.6; self.line(10, yb, 200, yb); self.set_line_width(0.2); self.set_draw_color(0, 0, 0)
            self.set_xy(10, yb + 1.2); self.cell(90, 3.6, office['tel'], align='L')
            self.set_xy(110, yb + 1.2); self.cell(90, 3.6, 'info@envitechal.com   -   www.envitechal.com', align='R')
            self.set_xy(10, yb + 4.8)
            self.cell(0, 3.6, office['address'], align='C')

    pdf = PDF(); pdf.alias_nb_pages(); pdf.set_auto_page_break(True, 30); pdf.add_page()
    f = pdf.fam
    unit = st.unit or '-'
    pdf.set_draw_color(*LINE)
    L1, V1, L2, V2 = 32.0, 78.0, 30.0, 50.0

    def kv_row(items, h=5.4):
        for lbl, val, wl, wv in items:
            pdf.set_font(f, 'B', 7.8); pdf.set_fill_color(*GREY_FILL)
            pdf.cell(wl, h, lbl, 1, 0, 'L', fill=True)
            txt = str(val) if val not in (None, '') else '-'
            fs = 8.0
            pdf.set_font(f, '', fs)
            while pdf.get_string_width(txt) > wv - 1.6 and fs > 6.0:
                fs -= 0.25; pdf.set_font(f, '', fs)
            if pdf.get_string_width(txt) > wv - 1.6:
                while pdf.get_string_width(txt + '...') > wv - 1.6 and len(txt) > 4:
                    txt = txt[:-1]
                txt += '...'
            pdf.cell(wv, h, txt, 1, 0, 'L')
        pdf.ln(h)

    kv_row([('Parameter', st.parameter, L1, V1), ('Level', st.level, L2, V2)])
    kv_row([('Sample', '%s: %s' % (st.get_sample_kind_display(), st.sample_ref) if st.sample_ref else st.get_sample_kind_display(), L1, V1), ('Unit of measurand', unit, L2, V2)])
    kv_row([('Method', st.method, L1, V1), ('Range (x)', '%s %s' % (_calc.fmt_sig(st.range_value, 8), unit) if st.range_value else '-', L2, V2)])
    kv_row([('Equipment', '%s%s' % (st.instrument, (' [%s]' % st.equipment_id) if st.equipment_id else ''), L1, V1),
            ('Environmental temp.', ('%s °C' % _calc.fmt_sig(st.env_temp, 4)) if st.env_temp is not None else '-', L2, V2)])
    kv_row([('Study date', st.study_date.strftime('%d-%m-%Y') if st.study_date else '-', L1, V1),
            ('Coverage factor', 'k = %s (95 %% C.L.)' % _calc.fmt_sig(st.k, 3), L2, V2)])
    kv_row([('Status', '%s - version %d%s' % (st.get_status_display(), st.version, (' (repeat of v%d)' % st.supersedes.version) if st.supersedes_id else ''), L1, V1),
            ('Record', 'Form %s' % ctrl['doc_no'], L2, V2)])
    pdf.ln(2.5)

    # ---- replicates
    ncol = max([len(o['values']) for o in ops] + [10])
    pdf.set_font(f, 'B', 8.5); pdf.set_text_color(*GREEN); pdf.cell(190, 5, 'Repeatability data (replicates per operator)', 0, 1); pdf.set_text_color(0, 0, 0)
    wl, wn, wm_, ws = 24.0, 9.0, 17.0, 17.0
    wx = (190.0 - wl - wn - wm_ - ws) / ncol
    pdf.set_font(f, 'B', 6.8); pdf.set_fill_color(*GREEN); pdf.set_text_color(255, 255, 255)
    pdf.cell(wl, 5, 'Operator', 1, 0, 'C', fill=True)
    for j in range(ncol):
        pdf.cell(wx, 5, 'x%d' % (j + 1), 1, 0, 'C', fill=True)
    pdf.cell(wn, 5, 'n', 1, 0, 'C', fill=True); pdf.cell(wm_, 5, 'Mean', 1, 0, 'C', fill=True); pdf.cell(ws, 5, 'SD', 1, 1, 'C', fill=True)
    pdf.set_text_color(0, 0, 0)
    for i, o in enumerate(ops):
        pdf.set_fill_color(*(GREY_FILL if i % 2 else (255, 255, 255)))
        pdf.set_font(f, 'B', 7); lab = o['label'] + ((' - ' + o['analyst']) if o['analyst'] else '')
        while pdf.get_string_width(lab) > wl - 2 and len(lab) > 2:
            lab = lab[:-1]
        pdf.cell(wl, 4.8, lab, 1, 0, 'L', fill=True)
        pdf.set_font(f, '', 7)
        for j in range(ncol):
            v = o['values'][j] if j < len(o['values']) else None
            pdf.cell(wx, 4.8, _calc.fmt_fix(v, st.decimals) if v is not None else '', 1, 0, 'C', fill=True)
        pdf.cell(wn, 4.8, str(o['n']), 1, 0, 'C', fill=True); pdf.cell(wm_, 4.8, o['mean'], 1, 0, 'C', fill=True); pdf.cell(ws, 4.8, o['sd'], 1, 1, 'C', fill=True)
    dates = ', '.join('%s %s' % (o['label'], o['date'].strftime('%d-%m-%Y')) for o in ops if o['date'])
    pdf.set_font(f, '', 6.8); pdf.set_text_color(60, 60, 60)
    pdf.cell(190, 4, 'Grand mean of all replicates: %s %s   (n = %d)%s' % (_calc.fmt_fix(r['grand']['mean'], st.decimals) if r['grand']['mean'] is not None else '-', unit, r['grand']['n'],
                                                                     ('     Dates: ' + dates) if dates else ''), 0, 1)
    pdf.set_text_color(0, 0, 0); pdf.ln(1.5)

    # ---- budget
    pdf.set_font(f, 'B', 8.5); pdf.set_text_color(*GREEN); pdf.cell(190, 5, 'Uncertainty budget (relative uncertainty)', 0, 1); pdf.set_text_color(0, 0, 0)
    cols = [('Source of uncertainty', 62), ('Unit', 11), ('Range (x)', 16), ('Magnitude (a)', 22), ('Rel. factor\n(a/x)', 19),
            ('Distribution\n(divisor)', 22), ('ci', 8), ('Rel. std. unc.\nu = a/x / div x ci', 30)]
    pdf.set_font(f, 'B', 6.6); pdf.set_fill_color(*GREEN); pdf.set_text_color(255, 255, 255)
    x0, y0 = pdf.get_x(), pdf.get_y()
    for lbl, w in cols:
        x = pdf.get_x(); pdf.set_xy(x, y0)
        pdf.multi_cell(w, 4, lbl if '\n' in lbl else '\n' + lbl, 1, 'C', fill=True); pdf.set_xy(x + w, y0)
    pdf.set_xy(x0, y0 + 8); pdf.set_text_color(0, 0, 0)
    RH = 5.2
    for i, c in enumerate(comps):
        if pdf.get_y() + RH > _FOOT_TOP - 4:
            pdf.add_page()
        pdf.set_fill_color(*(GREY_FILL if i % 2 else (255, 255, 255)))
        grey = not c['included']
        pdf.set_text_color(*((150, 150, 150) if grey else (0, 0, 0)))
        name = c['name'] + ('' if c['included'] else '  (not included)')
        pdf.set_font(f, 'B' if c['kind'] != 'b' else '', 6.8)
        while pdf.get_string_width(name) > cols[0][1] - 2 and len(name) > 4:
            name = name[:-1]
        pdf.cell(cols[0][1], RH, name, 1, 0, 'L', fill=True)
        pdf.set_font(f, '', 6.8)
        vals = [c['unit'], c['range'], c['magnitude'] + (('  = ' + c['magnitude_val']) if (c['kind'] == 'b' and not _re.match(r'^[\d.]+$', c['magnitude'] or '')) else ''),
                c['rel'], '%s (%s)' % (c['dist'], c['divisor'] if f == 'Calibri' else c['divisor'].replace('\u221a', 'sqrt')), c['ci'], c['u']]
        for (lbl, w), v in zip(cols[1:], vals):
            t = str(v)
            while pdf.get_string_width(t) > w - 1.5 and len(t) > 3:
                t = t[:-1]
            pdf.cell(w, RH, t, 1, 0, 'C', fill=True)
        pdf.ln(RH)
    pdf.set_text_color(0, 0, 0)
    # results
    pdf.ln(1.0)
    pdf.set_fill_color(*GREY_FILL)
    res = [('Combined relative uncertainty  uc = sqrt(sum u^2)', '± %s' % _fmt(r['uc'])),
           ('Expanded relative uncertainty  U = k x uc  (k = %s, 95 %% C.L.)' % _calc.fmt_sig(st.k, 3), '± %s' % _fmt(r['U'])),
           ('Expanded uncertainty in absolute unit  U x mean', '± %s %s' % (_fmt(r['U_abs']), unit)),
           ('Expanded uncertainty in percent of the measured value', '± %s %%' % _fmt(r['U_pct']))]
    for lbl, val in res:
        pdf.set_font(f, 'B', 7.6); pdf.cell(120, 5.2, lbl, 1, 0, 'L', fill=True)
        pdf.set_font(f, 'B', 8.2); pdf.cell(70, 5.2, val, 1, 1, 'C')
    if r['errors']:
        pdf.set_font(f, '', 6.8); pdf.set_text_color(153, 27, 27)
        pdf.multi_cell(190, 3.6, 'Calculation incomplete: ' + ' '.join(r['errors']), new_x='LMARGIN', new_y='NEXT'); pdf.set_text_color(0, 0, 0)
    notes = []
    if legacy:
        notes.append('Inducted from the laboratory workbook (%s). Figures recomputed from the replicates; the workbook printed uc %s, U %s.' % (
            legacy['file'].split('/')[-1][:70], legacy['rows'][0]['printed'], legacy['rows'][1]['printed']))
        notes += legacy['notes']
    if st.remarks:
        notes.append('Remarks: ' + st.remarks.replace('\n', '  |  '))
    if notes:
        pdf.ln(1.0); pdf.set_font(f, 'B', 7); pdf.cell(190, 4, 'Record notes', 0, 1)
        pdf.set_font(f, '', 6.6); pdf.set_text_color(60, 60, 60)
        for n in notes[:14]:
            pdf.set_x(10); pdf.multi_cell(190, 3.3, '- ' + n, new_x='LMARGIN', new_y='NEXT')
        pdf.set_text_color(0, 0, 0)
    pdf.set_font(f, '', 6.6); pdf.set_text_color(60, 60, 60); pdf.set_x(10)
    pdf.multi_cell(190, 3.3, 'Type A: u rep = (SD of the first operator / x) / sqrt(n); u repro = (sqrt(sum SD^2) / x) / sqrt(sum n). '
                             'Type B: u = (a / x) / divisor x ci; divisor 1 normal (k=1), 2 normal (k=2), sqrt3 rectangular, sqrt6 triangular. '
                             'Combined uc = sqrt(sum u^2); expanded U = k x uc; absolute U = U x grand mean.', new_x='LMARGIN', new_y='NEXT')
    pdf.set_text_color(0, 0, 0)

    # ---- signatures
    MIN_H, MAX_H = _SIG_MIN, 40.0
    top = pdf.get_y() + 2.5
    avail = _FOOT_TOP - top
    if avail < MIN_H - 0.05:
        pdf.add_page(); top = pdf.get_y() + 2; avail = _FOOT_TOP - top
    blk_h = max(MIN_H, min(MAX_H, avail))
    top = _FOOT_TOP - blk_h
    pdf.set_auto_page_break(False)
    # Prepared By = the user who prepared / signed the study on the system (owner decision 22-10-2026);
    # the analysts named on the operators are printed in the replicate table, not in the panel.
    prep = st.submitted_by if st.submitted_by_id else None
    panels = [('Prepared By', '(Chemist)', _uname(prep) if prep else '', _sig_image(prep) if prep else None),
              ('Reviewed By', '(QC / Lab Manager)', _uname(st.reviewed_by) if st.reviewed_at else '', _sig_image(st.reviewed_by) if st.reviewed_at else None),
              ('Approved By', '(CEO)', _uname(st.approved_by) if st.approved_at else '', _sig_image(st.approved_by) if st.approved_at else None)]
    _sig_panels(pdf, f, panels, top, blk_h, LINE, GREY_FILL)
    pdf.set_draw_color(0, 0, 0)
    out = pdf.output(dest='S')
    data = bytes(out) if not isinstance(out, str) else out.encode('latin-1')
    resp = HttpResponse(data, content_type='application/pdf')
    resp['Content-Disposition'] = 'inline; filename="MOU_%s_%s_%s_v%d.pdf"' % (
        st.location, _re.sub(r'[^A-Za-z0-9]+', '_', st.parameter).strip('_'), _re.sub(r'[^A-Za-z0-9.]+', '_', st.level).strip('_') or 'NA', st.version)
    return resp
