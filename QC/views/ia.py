"""Quality - Internal Audit (ETAL-QMS-808-FF-01/02/03) and Non-conformance & Corrective Action
(ETAL-QMS-710-FF-01/01A/02) - views. 22-10-2026.

One function for both laboratories, lab-scoped like the control charts and the MOU:
  * Dashboard, Annual Internal Audit Plan, Circulars (audit / witnessing) with attendance,
    Audit Report (ISO/IEC 17025:2017 clause checklist, copy-forward from the previous audit),
    Witnessing record, NC & Corrective Action form with Root Cause Analysis, NC&CA Log,
    bulk signing page, PDFs of every form, document control, deletion log, user manual.
Roles (owner decision 22-10-2026, "as on the forms"): the laboratory's QC / Lab Manager (the
Laboratory Reviewers page) and the CEO / administrator are the Management Representative /
internal auditor side - they plan, issue circulars, audit, raise NCs, follow up and close; any
member of the laboratory is an auditee / concerned department (acknowledges the report, signs
the circular, answers the NC); the CEO / administrator approves the plan and reviews RCAs.
Every signature is the signed-in user's own name and e-signature.
"""
from .shared import *  # noqa: F401,F403
import json as _json
import re as _re
from datetime import date as _date, datetime as _dt, timedelta as _td
from django.utils import timezone as _tz
from django.shortcuts import redirect as _redirect
from django.db.models import Q as _Q
from django.contrib import messages as _msg

from QC.models import IaClause, IaPlan, IaAudit, IaFinding, IaCircular, IaWitness, Ncca, NccaRca, ControlChartDeletion
from QC.views.control_chart import (_CC_LOCS, _CC_OFFICE, _uname, _user_labs, _is_admin, _can_review, _can_approve,
                                    _default_loc, _user_office, _sig_image)

_IA_FORMS = {'plan': ('ETAL-QMS-808-FF-01', 'ANNUAL INTERNAL AUDIT PLAN'), 'report': ('ETAL-QMS-808-FF-02', 'INTERNAL AUDIT REPORT'),
             'circular': ('ETAL-QMS-808-FF-03', 'INTERNAL AUDIT CIRCULAR'), 'nc': ('ETAL-QMS-710-FF-01', 'NON-CONFORMANCE & CORRECTIVE ACTION FORM'),
             'rca': ('ETAL-QMS-710-FF-01A', 'ROOT CAUSE ANALYSIS FORM'), 'log': ('ETAL-QMS-710-FF-02', 'NON-CONFORMANCE & CORRECTIVE ACTION LOG')}
_IA_DEFAULT_CTRL = {'plan': ('05-01-2024', '01', '00'), 'report': ('', '01', '00'), 'circular': ('', '01', '00'),
                    'nc': ('11-03-2023', '03', '02'), 'rca': ('23-08-2021', '01', '00'), 'log': ('05-04-2022', '01', '00')}
_DENIED = 'This action is reserved to the %s laboratory\'s QC / Lab Manager (Management Representative) and the CEO / administrator.'
MONTHS = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
_RESULT_LABEL = dict(IaFinding.RESULTS)
_CAT_LABEL = dict(Ncca.CATEGORIES)


# ---------------------------------------------------------------- helpers
class _Loc:
    def __init__(self, location):
        self.location = location


def _ia_docctrl(form, location, on=None):
    """Document-control box of one IA form for a laboratory (module 'ia_<form>'), as in force on the document's own
    date `on` (plan year / circular issue date / audit date / NC date / RCA date; 23-10-2026: a later revision of
    the form never changes documents dated before it)."""
    from EnviTechAlApp import doccontrol as DC
    d0 = _IA_DEFAULT_CTRL[form]
    dflt = {'doc_no': _IA_FORMS[form][0], 'issue_date': d0[0], 'issue_no': d0[1], 'rev_no': d0[2]}
    d = DC.doc_control('ia_' + form, location, on, default=dflt)
    d['title'] = _IA_FORMS[form][1]
    return d


def _ia_on(obj):
    """The document's own date of an IA record (None: today)."""
    from EnviTechAlApp import doccontrol as DC
    if obj is None:
        return None
    if isinstance(obj, IaPlan):
        return _date(int(obj.year), 1, 1)
    return DC.doc_date(obj, 'issue_date', 'date_start')


def _can_manage(user, location):
    """MR / internal auditor side: the laboratory's QC / Lab Manager or the CEO / administrator."""
    if not (user and user.is_authenticated):
        return False
    return _can_approve(user, _Loc(location)) or location in _user_labs(user)


def _is_member(user, location):
    """A member of the laboratory (e-signature office = the laboratory, or no office on the profile), its manager or the administrator."""
    if not (user and user.is_authenticated):
        return False
    if _can_manage(user, location):
        return True
    labs = _user_labs(user)
    if labs and location not in labs:
        return False
    office = _user_office(user)
    return office == location or not office


def _is_ceo(user, location):
    return bool(user and user.is_authenticated and _can_approve(user, _Loc(location)))


def _loc_of(request):
    loc = request.GET.get('location') or request.session.get('ia_loc') or _default_loc(request)
    if loc not in _CC_LOCS:
        loc = 'Karachi'
    request.session['ia_loc'] = loc
    return loc


def _pdate(txt):
    s = (txt or '').strip()
    for fmt in ('%d-%m-%Y', '%Y-%m-%d', '%d/%m/%Y'):
        try:
            return _dt.strptime(s, fmt).date()
        except ValueError:
            pass
    return None


def _d(d):
    return d.strftime('%d-%m-%Y') if d else ''


def _post_only(request, url):
    return None if request.method == 'POST' else _redirect(url)


def _snap(obj, extra=None):
    from django.core import serializers as _ser
    try:
        data = _json.loads(_ser.serialize('json', [obj]))[0]['fields']
    except Exception:
        data = {}
    if extra:
        data.update(extra)
    return data


def _log_deletion(kind, obj, user, reason, label, extra=None, location=None):
    ControlChartDeletion.objects.create(kind=kind, chart_ref=obj.pk, location=location or getattr(obj, 'location', ''), label=label[:300], reason=reason[:2000],
                                        snapshot=_snap(obj, extra), deleted_by=user)


def _counts(loc):
    today = _date.today()
    open_q = Ncca.objects.filter(location=loc).exclude(status='closed')
    return {'audits': IaAudit.objects.filter(location=loc).count(), 'audits_year': IaAudit.objects.filter(location=loc, year=today.year).count(),
            'open_ncs': open_q.count(), 'overdue': open_q.filter(target_date__lt=today).count() + open_q.filter(target_date__isnull=True, proposed_date__lt=today).count(),
            'drafts': IaAudit.objects.filter(location=loc, status='draft').count() + Ncca.objects.filter(location=loc, status='draft').count(),
            'plan': IaPlan.objects.filter(location=loc, year=today.year).first()}


# ---------------------------------------------------------------- dashboard
def ia_home(request):
    loc = _loc_of(request)
    today = _date.today()
    audits = IaAudit.objects.filter(location=loc).order_by('-date_start', '-id')[:6]
    ncs = Ncca.objects.filter(location=loc).exclude(status='closed').order_by('target_date', 'proposed_date', '-id')[:10]
    for n in ncs:
        due = n.target_date or n.proposed_date
        n.days_left = (due - today).days if due else None
    years = {}
    for a in IaAudit.objects.filter(location=loc):
        y = years.setdefault(a.year, {'audits': 0, 'obs': 0, 'minor': 0, 'major': 0})
        y['audits'] += 1; y['obs'] += a.n_obs; y['minor'] += a.n_minor; y['major'] += a.n_major
    trend = [{'year': y, **v} for y, v in sorted(years.items())]
    by_clause = {}
    for n in Ncca.objects.filter(location=loc, category__in=('minor', 'major', 'critical')):
        key = (n.clause or '?').split('.')[0].strip() or '?'
        by_clause[key] = by_clause.get(key, 0) + 1
    plan = IaPlan.objects.filter(location=loc, year=today.year).first()
    plan_months = []
    if plan:
        for row in plan.rows:
            for m, v in (row.get('months') or {}).items():
                if v.get('due'):
                    plan_months.append({'dept': row.get('department', ''), 'month': MONTHS[int(m) - 1], 'done': bool(v.get('done'))})
    sign_todo = _signing_rows(request.user, loc)
    return render(request, 'ia_home.html', {
        'loc': loc, 'locs': _CC_LOCS, 'c': _counts(loc), 'audits': audits, 'ncs': ncs, 'trend': trend, 'trend_json': _json.dumps(trend),
        'by_clause': [(k, v, int(round(100.0 * v / max(by_clause.values())))) for k, v in sorted(by_clause.items(), key=lambda x: (len(x[0]), x[0]))] if by_clause else [], 'plan': plan, 'plan_months': plan_months, 'today': today,
        'can_manage': _can_manage(request.user, loc), 'is_member': _is_member(request.user, loc), 'is_ceo': _is_ceo(request.user, loc),
        'todo': len(sign_todo), 'ctrl': _ia_docctrl('report', loc)})


# ---------------------------------------------------------------- annual plan (FF-01)
def ia_plans(request):
    loc = _loc_of(request)
    plans = IaPlan.objects.filter(location=loc).select_related('mr_by', 'ceo_by')
    return render(request, 'ia_plans.html', {'loc': loc, 'locs': _CC_LOCS, 'plans': plans, 'can_manage': _can_manage(request.user, loc), 'months': MONTHS,
                                             'year': _date.today().year, 'ctrl': _ia_docctrl('plan', loc)})


def _plan_rows_from_post(P):
    rows = []
    for i in range(0, 40):
        dept = (P.get('dept%d' % i) or '').strip()[:120]
        if not dept:
            continue
        months = {}
        for m in range(1, 13):
            due = P.get('r%d_m%d_due' % (i, m)) == '1'
            done = P.get('r%d_m%d_done' % (i, m)) == '1'
            if due or done:
                months[str(m)] = {'due': due, 'done': done}
        rows.append({'department': dept, 'months': months})
    return rows


def ia_plan_edit(request, pk=None):
    user = request.user
    if pk:
        plan = get_object_or_404(IaPlan, pk=pk)
        loc = plan.location
    else:
        loc = _loc_of(request)
        plan = IaPlan(location=loc, year=_date.today().year + (1 if _date.today().month >= 11 else 0), created_by=user,
                      rows=[{'department': 'Environmental Laboratory', 'months': {}}])
    if not _can_manage(user, loc):
        return HttpResponse(_DENIED % loc, status=403)
    if plan.pk and plan.locked:
        _msg.error(request, 'An approved plan is locked. The CEO / administrator can unapprove it with a reason.')
        return _redirect('ia_plan_detail', plan.pk)
    if request.method == 'POST':
        P = request.POST
        errors = []
        try:
            year = plan.year if plan.pk else int(P.get('year') or 0)        # the year of an existing plan cannot change
            if not (2020 <= year <= 2100):
                raise ValueError
        except ValueError:
            errors.append('Year must be a four-digit year.'); year = plan.year
        if not plan.pk and IaPlan.objects.filter(location=loc, year=year).exists():
            errors.append('The %s plan for %d already exists.' % (loc, year))
        rows = _plan_rows_from_post(P)
        if not rows:
            errors.append('Enter at least one department.')
        plan.year, plan.rows, plan.remarks = year, rows, (P.get('remarks') or '').strip()[:2000]
        if errors:
            for e in errors:
                _msg.error(request, e)
        else:
            if plan.status == 'signed':          # edited after the MR signature -> signature cleared
                plan.status, plan.mr_by, plan.mr_at, plan.mr_name, plan.mr_date = 'draft', None, None, '', None
            plan.save()
            _msg.success(request, 'Annual plan %d saved.' % plan.year)
            return _redirect('ia_plan_detail', plan.pk)
    rows = plan.rows or []
    while len(rows) < 6:
        rows = rows + [{'department': '', 'months': {}}]
    return render(request, 'ia_plan_edit.html', {'plan': plan, 'loc': loc, 'rows': rows, 'months': MONTHS, 'mrange': range(1, 13)})


def ia_plan_detail(request, pk):
    plan = get_object_or_404(IaPlan.objects.select_related('mr_by', 'ceo_by', 'created_by'), pk=pk)
    user = request.user
    audits = IaAudit.objects.filter(location=plan.location, year=plan.year)
    return render(request, 'ia_plan_detail.html', {
        'plan': plan, 'loc': plan.location, 'months': MONTHS, 'audits': audits, 'ctrl': _ia_docctrl('plan', plan.location, _ia_on(plan)),
        'can_edit': _can_manage(user, plan.location) and not plan.locked, 'can_mark': _can_manage(user, plan.location),
        'can_sign_mr': plan.status == 'draft' and _can_manage(user, plan.location),
        'can_approve': plan.status == 'signed' and _is_ceo(user, plan.location),
        'can_unapprove': plan.status == 'approved' and _is_ceo(user, plan.location),
        'can_delete': _can_manage(user, plan.location) and plan.status != 'approved'})


def _apply_plan_action(user, plan, act, reason=''):
    now = _tz.now()
    if act == 'sign_mr':
        if plan.status != 'draft':
            return 'error', 'The plan is already signed.'
        if not _can_manage(user, plan.location):
            return 'forbidden', _DENIED % plan.location
        if not plan.rows:
            return 'error', 'The plan has no departments / months.'
        plan.status, plan.mr_by, plan.mr_at, plan.mr_name, plan.mr_date = 'signed', user, now, _uname(user), now.date()
        plan.save()
        return 'ok', 'Signed as Management Representative. The plan awaits the CEO\'s approval.'
    if act == 'approve':
        if plan.status != 'signed' or not _is_ceo(user, plan.location):
            return 'forbidden', 'Approval of the annual plan is reserved to the CEO / administrator of the %s laboratory, after the MR has signed.' % plan.location
        plan.status, plan.ceo_by, plan.ceo_at, plan.ceo_name, plan.ceo_date = 'approved', user, now, _uname(user), now.date()
        plan.save()
        return 'ok', 'Annual plan %d approved and locked.' % plan.year
    if act == 'unapprove':
        if plan.status != 'approved' or not _is_ceo(user, plan.location):
            return 'forbidden', 'Only the CEO / administrator can unapprove a plan.'
        if len((reason or '').strip()) < 5:
            return 'error', 'Give the reason for unapproving (at least 5 characters).'
        plan.status, plan.ceo_by, plan.ceo_at, plan.ceo_name, plan.ceo_date = 'signed', None, None, '', None
        plan.remarks = (plan.remarks + '\n' if plan.remarks else '') + 'Unapproved %s by %s: %s' % (_d(now.date()), _uname(user), reason.strip()[:500])
        plan.save()
        return 'ok', 'Plan unapproved; it is back at the MR-signed stage.'
    if act == 'delete':
        if not _can_manage(user, plan.location):
            return 'forbidden', _DENIED % plan.location
        if plan.status == 'approved':
            return 'error', 'An approved plan is locked; unapprove it first.'
        if len((reason or '').strip()) < 5:
            return 'error', 'Give the reason for deletion (at least 5 characters).'
        _log_deletion('ia_plan', plan, user, reason, 'Annual Internal Audit Plan %d - %s' % (plan.year, plan.location))
        plan.delete()
        return 'deleted', 'Plan deleted; a copy is kept in the deletion log.'
    if act == 'mark_done':
        # the MR marks an audit month as completed (the plan may be approved: 'Done' is a record of execution, not a change of the plan)
        if not _can_manage(user, plan.location):
            return 'forbidden', _DENIED % plan.location
        try:
            ri, m = int(reason.split(':')[0]), int(reason.split(':')[1])
            if not (0 <= ri < len(plan.rows) and 1 <= m <= 12):
                raise ValueError
            cell = plan.rows[ri].setdefault('months', {}).setdefault(str(m), {'due': False, 'done': False})
            cell['done'] = not cell.get('done')
            plan.save()
            return 'ok', '%s %s marked %s.' % (plan.rows[ri]['department'], MONTHS[m - 1], 'done' if cell['done'] else 'not done')
        except Exception:
            return 'error', 'Bad cell.'
    return 'error', 'Unknown action.'


def ia_plan_action(request, pk):
    plan = get_object_or_404(IaPlan, pk=pk)
    back = _post_only(request, '/qc/ia/plans/%d/' % pk)
    if back:
        return back
    st, text = _apply_plan_action(request.user, plan, request.POST.get('action'), request.POST.get('reason') or '')
    if st == 'forbidden':
        return HttpResponse(text, status=403)
    if st == 'deleted':
        _msg.success(request, text)
        return _redirect('/qc/ia/plans/?location=%s' % plan.location)
    (_msg.success if st == 'ok' else _msg.error)(request, text)
    return _redirect('ia_plan_detail', pk)


# ---------------------------------------------------------------- circulars (FF-03)
def ia_circulars(request):
    loc = _loc_of(request)
    rows = IaCircular.objects.filter(location=loc).select_related('audit', 'issued_by')
    return render(request, 'ia_circulars.html', {'loc': loc, 'locs': _CC_LOCS, 'rows': rows, 'can_manage': _can_manage(request.user, loc), 'ctrl': _ia_docctrl('circular', loc)})


def _sessions_from_post(P):
    out = []
    idx = sorted({int(m.group(1)) for k in P for m in [_re.match(r'^s(\d+)_day$', k)] if m})[:12]
    for i in idx:
        g = lambda f: (P.get('s%d_%s' % (i, f)) or '').strip()
        if not (g('day') or g('scope')):
            continue
        out.append({'sr': g('sr')[:6], 'day': g('day')[:60], 'time_from': g('time_from')[:40], 'time_to': g('time_to')[:80], 'scope': g('scope')[:400],
                    'criteria': g('criteria')[:200], 'auditors': g('auditors')[:120], 'auditee': g('auditee')[:160]})
    return out


def _attendance_from_post(P, old):
    keep = {a.get('name', ''): a for a in old}
    out = []
    idx = sorted({int(m.group(1)) for k in P for m in [_re.match(r'^a(\d+)_name$', k)] if m})[:30]
    for i in idx:
        name = (P.get('a%d_name' % i) or '').strip()[:120]
        if not name:
            continue
        prev = keep.get(name, {})
        out.append({'name': name, 'designation': (P.get('a%d_designation' % i) or '').strip()[:120], 'user_id': prev.get('user_id'), 'signed_at': prev.get('signed_at')})
    return out


def ia_circular_edit(request, pk=None):
    user = request.user
    if pk:
        c = get_object_or_404(IaCircular, pk=pk)
        loc = c.location
    else:
        loc = _loc_of(request)
        kind = request.GET.get('kind') if request.GET.get('kind') in ('audit', 'witness') else 'audit'
        c = IaCircular(location=loc, kind=kind, created_by=user, issue_date=_date.today())
        aid = request.GET.get('audit')
        if aid and aid.isdigit():
            a = IaAudit.objects.filter(pk=int(aid), location=loc).first()
            if a:
                c.audit, c.audit_no = a, a.audit_no
                c.audit_date_text = '%s - %s' % (_d(a.date_start), _d(a.date_end)) if a.date_start else ''
        if not c.sessions:
            crit = 'Compliance will be checked & inspected against checklist of ISO 17025:2017'
            if kind == 'audit':
                c.sessions = [{'sr': '01', 'day': '', 'time_from': '10:00 am', 'time_to': '04:00 pm', 'scope': 'To check all clauses of ISO/IEC 17025:2017 (Technical & management) and to evaluate the performance of testing activities.', 'criteria': crit, 'auditors': '', 'auditee': ''},
                              {'sr': '02', 'day': '', 'time_from': '10:00 am', 'time_to': '04:00 pm', 'scope': 'To check all clauses of ISO/IEC 17025:2017 (Technical & management), Reporting & closing Meeting.', 'criteria': crit, 'auditors': '', 'auditee': ''}]
            else:
                c.sessions = [{'sr': '', 'day': '', 'time_from': '', 'time_to': '', 'scope': 'Witnessing of ', 'criteria': crit, 'auditors': '', 'auditee': ''}]
        if not c.attendance:
            last = IaCircular.objects.filter(location=loc, kind=kind).order_by('-issue_date', '-id').first()
            c.attendance = [{'name': a['name'], 'designation': a['designation'], 'user_id': None, 'signed_at': None} for a in (last.attendance if last else [])]
    if not _can_manage(user, loc):
        return HttpResponse(_DENIED % loc, status=403)
    if c.pk and c.locked:
        _msg.error(request, 'An issued circular is locked. Withdraw it first (MR) to edit.')
        return _redirect('ia_circular_detail', c.pk)
    if request.method == 'POST':
        P = request.POST
        errors = []
        c.kind = P.get('kind') if P.get('kind') in ('audit', 'witness') else c.kind
        c.audit_no = (P.get('audit_no') or '').strip()[:20]
        aid = P.get('audit')
        c.audit = IaAudit.objects.filter(pk=int(aid), location=loc).first() if (aid or '').isdigit() else None
        c.issue_date = _pdate(P.get('issue_date'))
        if not c.issue_date:
            errors.append('Circular issue date is required (dd-mm-yyyy).')
        c.audit_date_text = (P.get('audit_date_text') or '').strip()[:80]
        c.to_text = (P.get('to_text') or '').strip()[:160] or c.to_text
        c.from_text = (P.get('from_text') or '').strip()[:120] or c.from_text
        c.ceo_name = (P.get('ceo_name') or '').strip()[:120]
        c.sessions = _sessions_from_post(P)
        if not c.sessions:
            errors.append('Enter at least one schedule row.')
        c.attendance = _attendance_from_post(P, c.attendance or [])
        if errors:
            for e in errors:
                _msg.error(request, e)
        else:
            c.save()
            _msg.success(request, 'Circular saved.')
            return _redirect('ia_circular_detail', c.pk)
    audits = IaAudit.objects.filter(location=loc).order_by('-year', '-seq')
    sessions = list(c.sessions or [])
    while len(sessions) < 6:
        sessions.append({'sr': '', 'day': '', 'time_from': '', 'time_to': '', 'scope': '', 'criteria': '', 'auditors': '', 'auditee': ''})
    att = list(c.attendance or [])
    while len(att) < 10:
        att.append({'name': '', 'designation': ''})
    return render(request, 'ia_circular_edit.html', {'c': c, 'loc': loc, 'audits': audits, 'sessions': sessions, 'att': att})


def ia_circular_detail(request, pk):
    c = get_object_or_404(IaCircular.objects.select_related('audit', 'issued_by'), pk=pk)
    user = request.user
    my_row = None
    if user.is_authenticated:
        un = _uname(user).strip().lower()
        for i, a in enumerate(c.attendance or []):
            if a.get('user_id') == user.id or (not a.get('user_id') and a.get('name', '').strip().lower() in (un, user.username.lower())):
                my_row = i
                break
    signed = sum(1 for a in (c.attendance or []) if a.get('signed_at'))
    return render(request, 'ia_circular_detail.html', {
        'c': c, 'loc': c.location, 'ctrl': _ia_docctrl('circular', c.location, _ia_on(c)), 'signed': signed,
        'can_edit': _can_manage(user, c.location) and not c.locked, 'can_issue': c.status == 'draft' and _can_manage(user, c.location),
        'can_withdraw': c.status == 'issued' and _can_manage(user, c.location), 'can_delete': _can_manage(user, c.location) and c.status != 'issued',
        'can_sign': c.status == 'issued' and _is_member(user, c.location) and (my_row is not None) and not (c.attendance[my_row].get('signed_at')),
        'can_add_self': c.status == 'issued' and _is_member(user, c.location) and my_row is None and not c.inducted, 'my_row': my_row})


def _apply_circular_action(user, c, act, reason=''):
    now = _tz.now()
    if act == 'issue':
        if c.status != 'draft':
            return 'error', 'Already issued.'
        if not _can_manage(user, c.location):
            return 'forbidden', _DENIED % c.location
        c.status, c.issued_by, c.issued_at = 'issued', user, now
        c.save()
        return 'ok', 'Circular issued and signed by you as Management Representative. Attendees now sign receipt on this page or on the Signing page.'
    if act == 'withdraw':
        if c.status != 'issued' or not _can_manage(user, c.location):
            return 'forbidden', _DENIED % c.location
        if len((reason or '').strip()) < 5:
            return 'error', 'Give the reason for withdrawing (at least 5 characters).'
        c.status, c.issued_by, c.issued_at = 'draft', None, None
        for a in c.attendance:
            a['signed_at'] = None; a['user_id'] = None
        c.legacy = dict(c.legacy or {}); c.legacy.setdefault('withdrawals', []).append({'by': _uname(user), 'at': _d(now.date()), 'reason': reason.strip()[:500]})
        c.save()
        return 'ok', 'Circular withdrawn to draft; receipt signatures cleared.'
    if act == 'delete':
        if not _can_manage(user, c.location):
            return 'forbidden', _DENIED % c.location
        if c.status == 'issued':
            return 'error', 'An issued circular is locked; withdraw it first.'
        if len((reason or '').strip()) < 5:
            return 'error', 'Give the reason for deletion (at least 5 characters).'
        _log_deletion('ia_circ', c, user, reason, '%s circular %s (%s) - %s' % (c.get_kind_display(), c.audit_no, _d(c.issue_date), c.location))
        c.delete()
        return 'deleted', 'Circular deleted; a copy is kept in the deletion log.'
    if act == 'sign':
        if c.status != 'issued':
            return 'error', 'The circular is not issued yet.'
        if not _is_member(user, c.location):
            return 'forbidden', 'Receipt of the %s circular is signed by %s laboratory staff.' % (c.location, c.location)
        un = _uname(user).strip().lower()
        for a in c.attendance:
            if a.get('user_id') == user.id:
                return 'error', 'You have already signed receipt of this circular.'
        for a in c.attendance:
            if not a.get('user_id') and a.get('name', '').strip().lower() in (un, user.username.lower()):
                a['user_id'], a['signed_at'] = user.id, now.isoformat()
                c.save()
                return 'ok', 'Receipt signed (%s).' % _tz.localtime(now).strftime('%d-%m-%Y %H:%M')
        if c.inducted:
            return 'error', 'You are not named on the attendance list of this historic circular (%s).' % ', '.join(a.get('name', '') for a in c.attendance)
        c.attendance = list(c.attendance) + [{'name': _uname(user), 'designation': '', 'user_id': user.id, 'signed_at': now.isoformat()}]
        c.save()
        return 'ok', 'Added to the attendance list and receipt signed (%s).' % _tz.localtime(now).strftime('%d-%m-%Y %H:%M')
    return 'error', 'Unknown action.'


def ia_circular_action(request, pk):
    c = get_object_or_404(IaCircular, pk=pk)
    back = _post_only(request, '/qc/ia/circulars/%d/' % pk)
    if back:
        return back
    st, text = _apply_circular_action(request.user, c, request.POST.get('action'), request.POST.get('reason') or '')
    if st == 'forbidden':
        return HttpResponse(text, status=403)
    if st == 'deleted':
        _msg.success(request, text)
        return _redirect('/qc/ia/circulars/?location=%s' % c.location)
    (_msg.success if st == 'ok' else _msg.error)(request, text)
    return _redirect('ia_circular_detail', pk)


# ---------------------------------------------------------------- audit report (FF-02)
def _next_audit_no(loc, year):
    n = IaAudit.objects.filter(location=loc, year=year).count() + 1
    while IaAudit.objects.filter(location=loc, audit_no='%02d/%d' % (n, year)).exists():
        n += 1
    return '%02d/%d' % (n, year), n


def _seed_findings(audit, source=None):
    """Checklist rows of a new audit: copy-forward from the laboratory's previous audit (references
    and findings pre-filled for the auditor to revise, results cleared), else from the master list."""
    rows = []
    if source is not None:
        for i, f in enumerate(source.findings.select_related('clause')):
            rows.append(IaFinding(audit=audit, order=(i + 1) * 10, clause=f.clause, label=f.label, requirement=f.requirement, ref=f.ref, finding=f.finding, result='', tag=''))
    else:
        for i, c in enumerate(IaClause.objects.filter(active=True)):
            rows.append(IaFinding(audit=audit, order=(i + 1) * 10, clause=c, label='' if c.code.startswith('PNAC') else c.code,
                                  requirement=c.title if (c.is_heading or not c.requirement) else c.requirement, ref='', finding='', result='', tag=''))
    IaFinding.objects.bulk_create(rows)
    return len(rows)


def ia_audits(request):
    loc = _loc_of(request)
    rows = IaAudit.objects.filter(location=loc).select_related('auditor_signed_by', 'auditee_signed_by').prefetch_related('ncs', 'witnessings')
    return render(request, 'ia_audits.html', {'loc': loc, 'locs': _CC_LOCS, 'rows': rows, 'can_manage': _can_manage(request.user, loc), 'ctrl': _ia_docctrl('report', loc)})


def ia_audit_new(request):
    loc = _loc_of(request)
    user = request.user
    if not _can_manage(user, loc):
        return HttpResponse(_DENIED % loc, status=403)
    if request.method != 'POST':
        return _redirect('/qc/ia/audits/?location=%s' % loc)
    P = request.POST
    year = int(P.get('year')) if (P.get('year') or '').isdigit() else _date.today().year
    audit_no, seq = _next_audit_no(loc, year)
    prev = IaAudit.objects.filter(location=loc).order_by('-year', '-seq').first()
    src = prev if (P.get('seed') != 'master' and prev) else None
    a = IaAudit(location=loc, audit_no=audit_no, year=year, seq=seq, created_by=user, auditor=_uname(user), auditor_user=user,
                address=(prev.address if prev else ''), auditee_title=(prev.auditee_title if prev else ''), auditor_title=(prev.auditor_title if prev else ''),
                timeframe=(prev.timeframe if prev else ''), scope=(prev.scope if prev else IaAudit._meta.get_field('scope').default))
    if not a.address:
        a.address = _CC_OFFICE.get(loc, {}).get('address', '')
    a.save()
    n = _seed_findings(a, src)
    _msg.success(request, 'Audit %s created with %d checklist rows %s. Enter the dates, the auditee and the findings.' % (
        audit_no, n, ('carried forward from audit %s (results cleared)' % src.audit_no) if src else 'from the master checklist'))
    return _redirect('ia_audit_edit', a.pk)


def _can_edit_audit(user, a):
    return _can_manage(user, a.location) and not a.locked


def ia_audit_edit(request, pk):
    a = get_object_or_404(IaAudit, pk=pk)
    user = request.user
    if not _can_manage(user, a.location):
        return HttpResponse(_DENIED % a.location, status=403)
    if a.locked:
        _msg.error(request, 'A signed report is locked. Reopen it (auditor, with a reason) to edit.')
        return _redirect('ia_audit_detail', a.pk)
    findings = list(a.findings.select_related('clause'))
    if request.method == 'POST':
        P = request.POST
        errors = []
        a.date_start, a.date_end = _pdate(P.get('date_start')), _pdate(P.get('date_end'))
        if P.get('date_start') and not a.date_start:
            errors.append('Audit start date must be dd-mm-yyyy.')
        if P.get('date_end') and not a.date_end:
            errors.append('Audit end date must be dd-mm-yyyy.')
        if a.date_start and a.date_end and a.date_end < a.date_start:
            errors.append('The audit end date is before the start date.')
        if errors:                                   # nothing is saved; the page re-renders with the typed values
            for e in errors:
                _msg.error(request, e)
            a.auditor, a.auditee = (P.get('auditor') or a.auditor), (P.get('auditee') or a.auditee)
            return render(request, 'ia_audit_edit.html', {'a': a, 'loc': a.location, 'findings': findings, 'results': IaFinding.RESULTS, 'ctrl': _ia_docctrl('report', a.location, _ia_on(a))})
        a.days = max(1, (a.date_end - a.date_start).days + 1) if (a.date_start and a.date_end) else (int(P.get('days')) if (P.get('days') or '').isdigit() else a.days)
        for fld, n in (('auditor', 120), ('auditor_title', 120), ('auditee', 160), ('auditee_title', 120), ('address', 250), ('scope', 300), ('timeframe', 400)):
            setattr(a, fld, (P.get(fld) or '').strip()[:n])
        a.conclusion = (P.get('conclusion') or '').strip()[:4000]
        a.remarks = (P.get('remarks') or '').strip()[:4000]
        a.auditor_sign_date, a.auditee_sign_date = _pdate(P.get('auditor_sign_date')), _pdate(P.get('auditee_sign_date'))
        # findings
        keep = []
        for f in findings:
            if P.get('f%d_drop' % f.pk) == '1':
                f.delete(); continue
            f.ref = (P.get('f%d_ref' % f.pk) or '').strip()[:400]
            f.finding = (P.get('f%d_finding' % f.pk) or '').strip()[:6000]
            r = P.get('f%d_result' % f.pk) or ''
            f.result = r if r in _RESULT_LABEL else ''
            f.tag = (P.get('f%d_tag' % f.pk) or '').strip()[:40]
            if f.clause is None or P.get('f%d_label' % f.pk) is not None:
                f.label = (P.get('f%d_label' % f.pk) if P.get('f%d_label' % f.pk) is not None else f.label).strip()[:12]
                f.requirement = (P.get('f%d_req' % f.pk) if P.get('f%d_req' % f.pk) is not None else f.requirement).strip()[:4000]
            keep.append(f)
        IaFinding.objects.bulk_update(keep, ['ref', 'finding', 'result', 'tag', 'label', 'requirement'])
        # new rows (after a given row)
        idx = sorted({int(m.group(1)) for k in P for m in [_re.match(r'^n(\d+)_label$', k)] if m})[:40]
        for i in idx:
            lab = (P.get('n%d_label' % i) or '').strip()[:12]; req = (P.get('n%d_req' % i) or '').strip()[:4000]
            if not (lab or req):
                continue
            after = P.get('n%d_after' % i)
            base = next((f.order for f in keep if str(f.pk) == after), (keep[-1].order if keep else 0))
            cl = IaClause.objects.filter(code=lab).first()
            IaFinding.objects.create(audit=a, order=base + 1, clause=cl, label=lab, requirement=req or (cl.requirement if cl else ''),
                                     ref=(P.get('n%d_ref' % i) or '').strip()[:400], finding=(P.get('n%d_finding' % i) or '').strip()[:6000],
                                     result=P.get('n%d_result' % i) if P.get('n%d_result' % i) in _RESULT_LABEL else '')
        for i, f in enumerate(a.findings.all()):          # renumber
            if f.order != (i + 1) * 10:
                IaFinding.objects.filter(pk=f.pk).update(order=(i + 1) * 10)
        a.recount(save=False)
        a.save()
        _msg.success(request, 'Audit %s saved (%d observation(s), %d minor, %d major).' % (a.audit_no, a.n_obs, a.n_minor, a.n_major))
        if P.get('then') == 'detail':
            return _redirect('ia_audit_detail', a.pk)
        return _redirect('ia_audit_edit', a.pk)
    return render(request, 'ia_audit_edit.html', {'a': a, 'loc': a.location, 'findings': findings, 'results': IaFinding.RESULTS, 'ctrl': _ia_docctrl('report', a.location, _ia_on(a))})


def ia_audit_detail(request, pk):
    a = get_object_or_404(IaAudit.objects.select_related('auditor_signed_by', 'auditee_signed_by', 'created_by'), pk=pk)
    user = request.user
    findings = list(a.findings.select_related('clause'))
    show = request.GET.get('show') or 'all'
    if show == 'findings':
        findings = [f for f in findings if f.result in ('obs', 'minor', 'major')]
    ncs = list(a.ncs.prefetch_related('rcas').order_by('nc_no'))
    wits = list(a.witnessings.all())
    circs = list(a.circulars.all())
    is_member = _is_member(user, a.location)
    return render(request, 'ia_audit_detail.html', {
        'a': a, 'loc': a.location, 'findings': findings, 'show': show, 'ncs': ncs, 'wits': wits, 'circs': circs, 'ctrl': _ia_docctrl('report', a.location, _ia_on(a)),
        'legacy': (a.legacy or {}) if a.inducted else {}, 'can_edit': _can_edit_audit(user, a), 'can_manage': _can_manage(user, a.location),
        'can_sign_auditor': a.status == 'draft' and _can_manage(user, a.location),
        'can_sign_auditee': a.status == 'auditor' and is_member and (a.auditor_signed_by_id != user.id),
        'can_reopen': a.status != 'draft' and _can_manage(user, a.location), 'can_delete': _can_manage(user, a.location),
        'can_raise_nc': _can_manage(user, a.location), 'is_member': is_member, 'result_label': _RESULT_LABEL})


def _apply_audit_action(user, a, act, reason=''):
    now = _tz.now()
    if act == 'sign_auditor':
        if a.status != 'draft':
            return 'error', 'The report is already signed by the auditor.'
        if not _can_manage(user, a.location):
            return 'forbidden', _DENIED % a.location
        if not (a.date_start and a.date_end):
            return 'error', 'Enter the audit dates before signing.'
        if not a.auditee.strip():
            return 'error', 'Enter the auditee before signing.'
        a.recount(save=False)
        a.status, a.auditor_signed_by, a.auditor_signed_at = 'auditor', user, now
        a.auditor_sign_date = a.auditor_sign_date or now.date()
        if not a.auditor.strip():
            a.auditor = _uname(user)
        a.save()
        return 'ok', 'Report %s signed by you as internal auditor. The auditee now signs acknowledgement (study page or Signing page).' % a.audit_no
    if act == 'sign_auditee':
        if a.status != 'auditor':
            return 'error', 'The auditor signs first.' if a.status == 'draft' else 'The report is already signed by the auditee.'
        if not _is_member(user, a.location):
            return 'forbidden', 'The %s audit report is acknowledged by %s laboratory staff.' % (a.location, a.location)
        if a.auditor_signed_by_id == user.id:
            return 'error', 'The auditor cannot also sign as auditee.'
        a.status, a.auditee_signed_by, a.auditee_signed_at = 'closed', user, now
        a.auditee_sign_date = a.auditee_sign_date or now.date()
        if not a.auditee.strip():
            a.auditee = _uname(user)
        a.save()
        return 'ok', 'Report %s signed by you as auditee. The report is closed.' % a.audit_no
    if act == 'reopen':
        if a.status == 'draft' or not _can_manage(user, a.location):
            return 'forbidden', _DENIED % a.location
        if len((reason or '').strip()) < 5:
            return 'error', 'Give the reason for reopening (at least 5 characters).'
        a.status = 'draft'
        a.auditor_signed_by = a.auditor_signed_at = a.auditee_signed_by = a.auditee_signed_at = None
        a.remarks = (a.remarks + '\n' if a.remarks else '') + 'Reopened %s by %s: %s' % (_d(now.date()), _uname(user), reason.strip()[:500])
        a.save()
        return 'ok', 'Report reopened as draft; both signatures cleared.'
    return 'error', 'Unknown action.'


def ia_audit_action(request, pk):
    a = get_object_or_404(IaAudit, pk=pk)
    back = _post_only(request, '/qc/ia/audits/%d/' % pk)
    if back:
        return back
    st, text = _apply_audit_action(request.user, a, request.POST.get('action'), request.POST.get('reason') or '')
    if st == 'forbidden':
        return HttpResponse(text, status=403)
    (_msg.success if st == 'ok' else _msg.error)(request, text)
    return _redirect('ia_audit_detail', pk)


def ia_audit_delete(request, pk):
    a = get_object_or_404(IaAudit, pk=pk)
    back = _post_only(request, '/qc/ia/audits/%d/' % pk)
    if back:
        return back
    user = request.user
    if not _can_manage(user, a.location):
        return HttpResponse(_DENIED % a.location, status=403)
    why = (request.POST.get('reason') or '').strip()
    if len(why) < 5:
        _msg.error(request, 'Give the reason for deletion (at least 5 characters).')
        return _redirect('ia_audit_detail', pk)
    if a.ncs.exists():
        _msg.error(request, 'The report has %d NC&CA record(s) linked; delete or unlink them first.' % a.ncs.count())
        return _redirect('ia_audit_detail', pk)
    extra = {'findings': [{'label': f.label, 'ref': f.ref, 'finding': f.finding, 'result': f.result} for f in a.findings.all()],
             'witnessings': [{'date': _d(w.date), 'rows': w.rows} for w in a.witnessings.all()]}
    _log_deletion('ia_audit', a, user, why, 'Internal audit %s - %s (%s)' % (a.audit_no, a.location, _d(a.date_start)), extra)
    loc = a.location
    a.delete()
    _msg.success(request, 'Audit deleted; a copy is kept in the deletion log.')
    return _redirect('/qc/ia/audits/?location=%s' % loc)


# ---------------------------------------------------------------- witnessing record
def _witness_rows_from_post(P):
    out = []
    idx = sorted({int(m.group(1)) for k in P for m in [_re.match(r'^w(\d+)_parameter$', k)] if m})[:20]
    for i in idx:
        g = lambda f: (P.get('w%d_%s' % (i, f)) or '').strip()
        if not g('parameter'):
            continue
        out.append({'parameter': g('parameter')[:80], 'performed_by': g('performed_by')[:120], 'range': g('range')[:80], 'assigned': g('assigned')[:60],
                    'obtained': g('obtained')[:60], 'remarks': g('remarks')[:3000]})
    return out


def ia_witness_edit(request, audit_pk, pk=None):
    a = get_object_or_404(IaAudit, pk=audit_pk)
    user = request.user
    if not _can_manage(user, a.location):
        return HttpResponse(_DENIED % a.location, status=403)
    if a.locked:
        _msg.error(request, 'The audit report is signed; reopen it (with a reason) before adding or editing a witnessing record.')
        return _redirect('ia_audit_detail', a.pk)
    w = get_object_or_404(IaWitness, pk=pk, audit=a) if pk else IaWitness(audit=a, auditor=_uname(user), date=_date.today())
    if w.pk and w.locked:
        _msg.error(request, 'A signed witnessing record is locked. Reopen it first.')
        return _redirect('ia_audit_detail', a.pk)
    if request.method == 'POST':
        P = request.POST
        w.date = _pdate(P.get('date'))
        w.auditor = (P.get('auditor') or '').strip()[:120]
        cid = P.get('circular')
        w.circular = IaCircular.objects.filter(pk=int(cid), location=a.location).first() if (cid or '').isdigit() else None
        w.rows = _witness_rows_from_post(P)
        names = [n.strip()[:120] for n in (P.get('auditees') or '').split(',') if n.strip()]
        old = {x.get('name'): x for x in (w.auditees or [])}
        w.auditees = [dict(old.get(n, {}), name=n) for n in names]
        if not w.date:
            _msg.error(request, 'Date of witnessing is required (dd-mm-yyyy).')
        elif not w.rows:
            _msg.error(request, 'Enter at least one witnessed test.')
        else:
            w.save()
            _msg.success(request, 'Witnessing record saved.')
            return _redirect('ia_audit_detail', a.pk)
    rows = list(w.rows or [])
    while len(rows) < 6:
        rows.append({'parameter': '', 'performed_by': '', 'range': '', 'assigned': '', 'obtained': '', 'remarks': ''})
    circs = IaCircular.objects.filter(location=a.location, kind='witness')
    return render(request, 'ia_witness_edit.html', {'a': a, 'w': w, 'rows': rows, 'circs': circs, 'loc': a.location, 'auditees_text': ', '.join(x.get('name', '') for x in (w.auditees or []))})


def _apply_witness_action(user, w, act, reason=''):
    now = _tz.now()
    a = w.audit
    if act == 'sign_auditor':
        if w.status != 'draft':
            return 'error', 'Already signed by the auditor.'
        if not _can_manage(user, a.location):
            return 'forbidden', _DENIED % a.location
        w.status, w.auditor_signed_by, w.auditor_signed_at = 'auditor', user, now
        w.sign_date = w.sign_date or now.date()
        if not w.auditor:
            w.auditor = _uname(user)
        w.save()
        return 'ok', 'Witnessing record signed by you as auditor; the analysts witnessed now sign.'
    if act == 'sign_analyst':
        if w.status == 'draft':
            return 'error', 'The auditor signs first.'
        if w.status == 'closed':
            return 'error', 'All analysts have signed.'
        if not _is_member(user, a.location):
            return 'forbidden', 'The %s witnessing record is signed by %s laboratory staff.' % (a.location, a.location)
        un = _uname(user).strip().lower()
        for x in w.auditees:
            if x.get('user_id') == user.id:
                return 'error', 'You have already signed this witnessing record.'
        hit = None
        for x in w.auditees:
            if not x.get('user_id') and x.get('name', '').strip().lower() in (un, user.username.lower()):
                hit = x; break
        if hit is None:
            named = {r.get('performed_by', '').strip().lower().replace('ms. ', '').replace('mr. ', '') for r in w.rows}
            if un.replace('ms. ', '') in named or not w.auditees:
                hit = {'name': _uname(user)}; w.auditees = list(w.auditees) + [hit]
            else:
                return 'error', 'You are not named on this witnessing record (%s).' % ', '.join(x.get('name', '') for x in w.auditees)
        hit['user_id'], hit['signed_at'] = user.id, now.isoformat()
        if all(x.get('user_id') for x in w.auditees):
            w.status = 'closed'
        w.save()
        return 'ok', 'Witnessing record signed by you (%s).' % _tz.localtime(now).strftime('%d-%m-%Y %H:%M')
    if act == 'reopen':
        if w.status == 'draft' or not _can_manage(user, a.location):
            return 'forbidden', _DENIED % a.location
        if len((reason or '').strip()) < 5:
            return 'error', 'Give the reason for reopening (at least 5 characters).'
        w.status, w.auditor_signed_by, w.auditor_signed_at, w.sign_date = 'draft', None, None, None
        for x in w.auditees:
            x['user_id'] = None; x['signed_at'] = None
        w.legacy = dict(w.legacy or {}); w.legacy.setdefault('reopened', []).append({'by': _uname(user), 'at': _d(now.date()), 'reason': reason.strip()[:500]})
        w.save()
        return 'ok', 'Witnessing record reopened; signatures cleared.'
    if act == 'delete':
        if not _can_manage(user, a.location):
            return 'forbidden', _DENIED % a.location
        if a.locked:
            return 'error', 'The audit report is signed; reopen it before deleting a witnessing record.'
        if len((reason or '').strip()) < 5:
            return 'error', 'Give the reason for deletion (at least 5 characters).'
        _log_deletion('ia_witness', w, user, reason, 'Witnessing %s of audit %s - %s' % (_d(w.date), a.audit_no, a.location), location=a.location)
        w.delete()
        return 'ok', 'Witnessing record deleted; a copy is kept in the deletion log.'
    return 'error', 'Unknown action.'


def ia_witness_action(request, pk):
    w = get_object_or_404(IaWitness.objects.select_related('audit'), pk=pk)
    back = _post_only(request, '/qc/ia/audits/%d/' % w.audit_id)
    if back:
        return back
    st, text = _apply_witness_action(request.user, w, request.POST.get('action'), request.POST.get('reason') or '')
    if st == 'forbidden':
        return HttpResponse(text, status=403)
    (_msg.success if st == 'ok' else _msg.error)(request, text)
    return _redirect('ia_audit_detail', w.audit_id)


# ---------------------------------------------------------------- NC & corrective action (710-FF-01) + log (710-FF-02)
def _next_nc_no(loc, source, year):
    """Suggested number: NC-<n>/<source>/<yy> per laboratory, source and year (the record's own style)."""
    yy = '%03d' % (year % 1000)
    tag = {'IA': 'IA', 'EA': 'EA', 'CC': 'CC', 'TEST': 'T', 'CAL': 'CAL', 'OTHER': 'MS'}.get(source, source)
    n = Ncca.objects.filter(location=loc, source=source, date__year=year).count() + 1
    while Ncca.objects.filter(location=loc, nc_no='NC-%02d/%s/%s' % (n, tag, yy)).exists():
        n += 1
    return 'NC-%02d/%s/%s' % (n, tag, yy)


def ia_ncs(request):
    loc = _loc_of(request)
    show = request.GET.get('show') or 'open'
    show = show if show in ('open', 'all', 'closed', 'year', 'incomplete', 'unverified') else 'open'
    year = int(request.GET.get('year')) if (request.GET.get('year') or '').isdigit() else _date.today().year
    src = request.GET.get('source') or ''
    qs = Ncca.objects.filter(location=loc).select_related('audit', 'raised_user', 'closed_by').prefetch_related('rcas')
    if show == 'open':
        qs = qs.exclude(status='closed')
    elif show == 'closed':
        qs = qs.filter(status='closed')
    elif show == 'year':
        qs = qs.filter(date__year=year)
    if src in dict(Ncca.SOURCES):
        qs = qs.filter(source=src)
    rows = list(qs.order_by('log_sno', 'date', 'id'))
    if show == 'incomplete':
        rows = [n for n in rows if n.form_gaps]
    elif show == 'unverified':
        rows = [n for n in rows if n.inducted and not n.verified]
    today = _date.today()
    for n in rows:
        due = n.target_date or n.proposed_date
        n.overdue = bool(due and n.status != 'closed' and due < today)
    counts = {'open': Ncca.objects.filter(location=loc).exclude(status='closed').count(), 'all': Ncca.objects.filter(location=loc).count(),
              'closed': Ncca.objects.filter(location=loc, status='closed').count(),
              'incomplete': 0, 'unverified': 0}
    for n in Ncca.objects.filter(location=loc).only('legacy', 'log_only', 'details', 'root_cause', 'corrective', 'completion_date', 'satisfactory', 'followup_desc'):
        counts['incomplete'] += bool(n.form_gaps)
        counts['unverified'] += bool(n.inducted and not n.verified)
    years = sorted({d.year for d in Ncca.objects.filter(location=loc, date__isnull=False).values_list('date', flat=True)}, reverse=True)
    return render(request, 'ia_ncs.html', {'loc': loc, 'locs': _CC_LOCS, 'rows': rows, 'show': show, 'year': year, 'years': years, 'src': src, 'sources': Ncca.SOURCES,
                                           'counts': counts, 'can_manage': _can_manage(request.user, loc), 'is_member': _is_member(request.user, loc),
                                           'ctrl': _ia_docctrl('log', loc), 'cat_label': _CAT_LABEL})


def ia_witnessing(request):
    """Register of witnessing records (annex of the audit report, ETAL-QMS-808-FF-02) - 23-10-2026."""
    loc = _loc_of(request)
    rows = list(IaWitness.objects.filter(audit__location=loc).select_related('audit', 'circular').order_by('-date', '-id'))
    audits = list(IaAudit.objects.filter(location=loc).order_by('-year', '-seq')) if _can_manage(request.user, loc) else []
    for w in rows:
        w.n_rows = len(w.rows or [])
        w.n_signed = sum(1 for a in (w.auditees or []) if a.get('signed_at'))
    return render(request, 'ia_witnessing.html', {'loc': loc, 'locs': _CC_LOCS, 'rows': rows, 'audits': audits,
                                                  'can_manage': _can_manage(request.user, loc), 'ctrl': _ia_docctrl('report', loc)})


def ia_rcas(request):
    """Register of root cause analyses (ETAL-QMS-710-FF-01A) and the NC&CAs still without one - 23-10-2026."""
    loc = _loc_of(request)
    rows = list(NccaRca.objects.filter(nc__location=loc).select_related('nc').order_by('-date', '-id'))
    pending = list(Ncca.objects.filter(location=loc, rcas__isnull=True, log_only=False).exclude(status__in=('draft', 'closed')).order_by('date', 'id'))
    return render(request, 'ia_rcas.html', {'loc': loc, 'locs': _CC_LOCS, 'rows': rows, 'pending': pending,
                                            'can_manage': _can_manage(request.user, loc), 'ctrl': _ia_docctrl('rca', loc)})


_NC_RECORD_FIELDS = ('nc_no', 'date', 'department', 'raised_by', 'clause', 'source', 'audit_id', 'category', 'details', 'proposed_date', 'due_other', 'evaluated_date',
                     'priority', 'risk_type', 'severity', 'impact_past', 'sig_legal', 'sig_risk', 'sig_halt', 'sig_preventive', 'sig_non_significant',
                     'category_also_critical', 'due_audit_internal', 'due_audit_external', 'due_testing', 'due_cal_internal', 'due_cal_external',
                     'due_complaint', 'assigned_to', 'target_date', 'root_cause', 'corrective', 'completion_date', 'followup_with', 'satisfactory',
                     'followup_date', 'next_followup_date', 'followup_desc', 'remarks', 'closed_by_name', 'closing_date')


def _nc_sections(user, n):
    """Which sections of the NC form the user may edit now (as on the paper form)."""
    mgr, member = _can_manage(user, n.location), _is_member(user, n.location)
    head = mgr and n.status in ('draft', 'open')
    dept = member and n.status in ('draft', 'open', 'responded') and not n.locked
    mr = mgr and n.status in ('responded', 'open') and not n.locked
    return {'head': head, 'dept': dept, 'mr': mr, 'any': head or dept or mr}


def ia_nc_edit(request, pk=None):
    user = request.user
    if pk:
        n = get_object_or_404(Ncca.objects.select_related('audit', 'finding'), pk=pk)
        loc = n.location
    else:
        loc = _loc_of(request)
        if not _can_manage(user, loc):
            return HttpResponse(_DENIED % loc, status=403)
        n = Ncca(location=loc, created_by=user, raised_by=_uname(user), raised_user=user, date=_date.today(), department='Lab', due_audit_internal=True, due_other='Management System')
        fid = request.GET.get('finding')
        if (fid or '').isdigit():
            f = IaFinding.objects.select_related('audit').filter(pk=int(fid), audit__location=loc).first()
            if f:
                n.audit, n.finding, n.clause = f.audit, f, '%s (ISO/IEC 17025:2017)' % (f.label or (f.clause.code if f.clause else ''))
                n.details = f.finding; n.category = f.result if f.result in ('obs', 'minor', 'major') else 'major'
                n.raised_by = f.audit.auditor or n.raised_by
        aid = request.GET.get('audit')
        if (aid or '').isdigit():
            n.audit = IaAudit.objects.filter(pk=int(aid), location=loc).first() or n.audit
        n.source = 'IA' if n.audit else (request.GET.get('source') if request.GET.get('source') in dict(Ncca.SOURCES) else 'IA')
        n.nc_no = _next_nc_no(loc, n.source, n.date.year)
    sec = _nc_sections(user, n) if n.pk else {'head': True, 'dept': True, 'mr': False, 'any': True}
    # Complete an inducted form from the paper record (complaint 26-10-2026: inducted forms showed empty sections because those
    # sections were not in the record supplied). The location's manager types in what the paper form says; the status and the
    # paper signatures stay as they are and every change is listed in the record trail (legacy.completed) and in the history.
    record = bool(n.pk) and n.inducted and _can_manage(user, loc) and (request.GET.get('record') == '1' or request.POST.get('record') == '1')
    if record:
        sec = {'head': True, 'dept': True, 'mr': True, 'any': True, 'record': True}
    if not sec['any']:
        if n.locked:
            _msg.error(request, 'A closed NC&CA record is locked. The MR can reopen it with a reason.')
        else:
            return HttpResponse('You cannot edit this NC&CA record at its current stage.', status=403)
        return _redirect('ia_nc_detail', n.pk)
    if request.method == 'POST':
        P = request.POST
        errors = []
        head_changed = False
        snap0 = {f: getattr(n, f) for f in _NC_RECORD_FIELDS} if record else None
        if sec['head'] and 'details' in P:
            before = (n.nc_no, n.date, n.department, n.raised_by, n.clause, n.source, n.audit_id, n.category, n.details, n.proposed_date, n.due_other, n.evaluated_date,
                      n.priority, n.risk_type, n.severity, n.impact_past, n.sig_legal, n.sig_risk, n.sig_halt, n.sig_preventive, n.sig_non_significant, n.category_also_critical,
                      n.due_audit_internal, n.due_audit_external, n.due_testing, n.due_cal_internal, n.due_cal_external, n.due_complaint)
            n.nc_no = (P.get('nc_no') or '').strip()[:40] or n.nc_no
            if Ncca.objects.filter(location=loc, nc_no=n.nc_no).exclude(pk=n.pk).exists():
                errors.append('NC&CA number %s already exists for %s.' % (n.nc_no, loc))
            n.date = _pdate(P.get('date')) or n.date
            n.department = (P.get('department') or '').strip()[:80]
            n.raised_by = (P.get('raised_by') or '').strip()[:120]
            n.clause = (P.get('clause') or '').strip()[:60]
            n.source = P.get('source') if P.get('source') in dict(Ncca.SOURCES) else n.source
            aid = P.get('audit')
            n.audit = IaAudit.objects.filter(pk=int(aid), location=loc).first() if (aid or '').isdigit() else None
            if n.finding and n.finding.audit_id != (n.audit.pk if n.audit else None):
                n.finding = None
            for b in ('due_audit_internal', 'due_audit_external', 'due_testing', 'due_cal_internal', 'due_cal_external', 'due_complaint',
                      'category_also_critical', 'sig_legal', 'sig_risk', 'sig_halt', 'sig_preventive', 'sig_non_significant', 'impact_past'):
                setattr(n, b, P.get(b) == '1')
            n.due_other = (P.get('due_other') or '').strip()[:120]
            n.category = P.get('category') if P.get('category') in _CAT_LABEL else n.category
            for lv in ('priority', 'risk_type', 'severity'):
                setattr(n, lv, P.get(lv) if P.get(lv) in dict(Ncca.LEVELS) else getattr(n, lv))
            n.evaluated_date = _pdate(P.get('evaluated_date')) if 'evaluated_date' in P else n.evaluated_date
            n.details = (P.get('details') or '').strip()[:6000]
            n.proposed_date = _pdate(P.get('proposed_date'))
            n.assigned_to = (P.get('assigned_to') or '').strip()[:120]
            n.target_date = _pdate(P.get('target_date')) or n.proposed_date
            if not n.details:
                errors.append('Non-conformity / observation details are required.')
            head_changed = before != (n.nc_no, n.date, n.department, n.raised_by, n.clause, n.source, n.audit_id, n.category, n.details, n.proposed_date, n.due_other, n.evaluated_date,
                                      n.priority, n.risk_type, n.severity, n.impact_past, n.sig_legal, n.sig_risk, n.sig_halt, n.sig_preventive, n.sig_non_significant, n.category_also_critical,
                                      n.due_audit_internal, n.due_audit_external, n.due_testing, n.due_cal_internal, n.due_cal_external, n.due_complaint)
        if sec['dept'] and 'root_cause' in P:
            changed = (n.root_cause, n.corrective, n.completion_date) != ((P.get('root_cause') or '').strip()[:6000], (P.get('corrective') or '').strip()[:6000], _pdate(P.get('completion_date')))
            n.root_cause = (P.get('root_cause') or '').strip()[:6000]
            n.corrective = (P.get('corrective') or '').strip()[:6000]
            n.completion_date = _pdate(P.get('completion_date'))
            if changed and n.status == 'responded' and not record:          # the department's section changed after the HOD signed -> signature cleared, back to 'open'
                n.status, n.hod_signed_by, n.hod_signed_at = 'open', None, None
                _msg.warning(request, 'The department section was changed after the Head of Department signed: that signature is cleared and the response must be signed again.')
        if sec['head'] and 'details' in P and n.status == 'open' and n.mr_signed_at and head_changed and not record:   # the header changed after the MR signed: the editor re-signs it
            n.mr_signed_by, n.mr_signed_at = user, _tz.now()
            n.raised_by = n.raised_by or _uname(user)
        if sec['mr'] and 'followup_with' in P:
            n.followup_with = (P.get('followup_with') or '').strip()[:120]
            n.satisfactory = {'1': True, '0': False}.get(P.get('satisfactory'))
            n.followup_date = _pdate(P.get('followup_date'))
            n.next_followup_date = _pdate(P.get('next_followup_date'))
            n.followup_desc = (P.get('followup_desc') or '').strip()[:4000]
            n.remarks = (P.get('remarks') or '').strip()[:300]
        close_record = False
        if record and 'closed_by_name' in P:
            n.closed_by_name = (P.get('closed_by_name') or '').strip()[:120]
            n.closing_date = _pdate(P.get('closing_date'))
            if n.status != 'closed' and P.get('close_record') == '1':
                if not (n.closing_date and n.closed_by_name and n.root_cause.strip() and n.corrective.strip()):
                    errors.append('To mark the NC&CA closed as per the paper record, enter the root cause, the corrective action, the closing date and who closed it.')
                else:
                    close_record = True
        if errors:
            for e in errors:
                _msg.error(request, e)
        else:
            if record:
                if n.details.strip() and n.details.strip() != Ncca.LOG_ONLY_TEXT:
                    n.log_only = False              # the paper form is now in the system, not only its log row
                changed = [f for f in _NC_RECORD_FIELDS if getattr(n, f) != snap0[f]]
                prev = n.status
                if close_record:
                    n.status = 'closed'
                    changed.append('status')
                if changed:
                    n.legacy = dict(n.legacy or {})
                    if n.legacy.get('verified'):          # changed after the paper-form sign-off: it must be verified again
                        n.legacy.setdefault('verified_cleared', []).append(n.legacy.pop('verified'))
                        _msg.warning(request, 'The record was changed after it was verified against the paper form: please verify and sign it again.')
                    n.legacy.setdefault('completed', []).append({'by': _uname(user), 'at': _tz.localtime().strftime('%d-%m-%Y %H:%M'),
                                                                 'fields': changed, 'from_status': prev, 'to_status': n.status})
                n.save()
                if changed:
                    _msg.success(request, 'NC&CA %s completed from the paper record (%d field%s); the change is listed in the record trail.'
                                 % (n.nc_no, len(changed), '' if len(changed) == 1 else 's'))
                else:
                    _msg.info(request, 'Nothing was changed.')
                return _redirect('ia_nc_detail', n.pk)
            n.save()
            _msg.success(request, 'NC&CA %s saved.' % n.nc_no)
            return _redirect('ia_nc_detail', n.pk)
    audits = IaAudit.objects.filter(location=loc).order_by('-year', '-seq')
    return render(request, 'ia_nc_edit.html', {'n': n, 'loc': loc, 'sec': sec, 'record': record, 'audits': audits, 'sources': Ncca.SOURCES, 'cats': Ncca.CATEGORIES, 'levels': Ncca.LEVELS,
                                              'ctrl': _ia_docctrl('nc', loc)})


def ia_nc_detail(request, pk):
    n = get_object_or_404(Ncca.objects.select_related('audit', 'finding', 'raised_user', 'evaluated_by', 'mr_signed_by', 'hod_signed_by', 'closed_by', 'created_by'), pk=pk)
    user = request.user
    rcas = list(NccaRca.objects.filter(nc=n).select_related('performed_by', 'reviewed_by').order_by('part', 'id'))
    rca = rcas[0] if rcas else None
    is_ceo, mgr = _is_ceo(user, n.location), _can_manage(user, n.location)
    for r in rcas:              # per-RCA actions (an NC&CA may carry one RCA per root cause - 26-10-2026)
        r.can_reopen = r.status != 'draft' and (is_ceo or (r.status == 'performed' and mgr))
        r.can_edit = mgr and n.status != 'draft' and not r.locked
    sec = _nc_sections(user, n)
    today = _date.today()
    due = n.target_date or n.proposed_date
    return render(request, 'ia_nc_detail.html', {
        'n': n, 'loc': n.location, 'rca': rca, 'rcas': rcas, 'sec': sec, 'ctrl': _ia_docctrl('nc', n.location, _ia_on(n)), 'cat_label': _CAT_LABEL,
        'overdue': bool(due and n.status != 'closed' and due < today), 'due': due,
        'can_manage': _can_manage(user, n.location), 'is_member': _is_member(user, n.location), 'is_ceo': _is_ceo(user, n.location),
        'can_raise': n.status == 'draft' and _can_manage(user, n.location),
        'can_respond': n.status == 'open' and _is_member(user, n.location),
        'can_close': n.status == 'responded' and _can_manage(user, n.location),
        'can_reopen': n.status in ('responded', 'closed') and _can_manage(user, n.location),
        'can_reopen_rca': bool(rca) and rca.status != 'draft' and (_is_ceo(user, n.location) or (rca.status == 'performed' and _can_manage(user, n.location))),
        'can_record': n.inducted and mgr, 'gaps': n.form_gaps, 'can_verify': n.inducted and mgr and not n.verified,
        'can_delete': _can_manage(user, n.location), 'can_rca': _can_manage(user, n.location) and n.status != 'draft' and not (rca and rca.locked),
        'can_add_rca': mgr and n.status not in ('draft', 'closed') and bool(rcas)})


def _apply_nc_action(user, n, act, reason=''):
    now = _tz.now()
    if act == 'raise':
        if n.status != 'draft':
            return 'error', 'The NC&CA is already raised.'
        if not _can_manage(user, n.location):
            return 'forbidden', _DENIED % n.location
        if not n.details.strip():
            return 'error', 'Enter the non-conformity / observation details first.'
        n.status, n.mr_signed_by, n.mr_signed_at = 'open', user, now
        n.evaluated_by, n.evaluated_at = user, now
        n.evaluated_date = n.evaluated_date or now.date()
        n.raised_user = n.raised_user or user
        if not n.raised_by.strip():
            n.raised_by = _uname(user)
        n.assigned_date = n.assigned_date or now.date()
        n.target_date = n.target_date or n.proposed_date
        n.save()
        return 'ok', 'NC&CA %s raised and signed by you as MR / designee. The concerned department now records the root cause and corrective action.' % n.nc_no
    if act == 'respond':
        if n.status != 'open':
            return 'error', 'The NC&CA is not awaiting the department\'s response.' if n.status != 'draft' else 'The NC&CA has not been raised yet.'
        if not _is_member(user, n.location):
            return 'forbidden', 'The %s laboratory\'s concerned department responds to this NC&CA.' % n.location
        if not (n.root_cause.strip() and n.corrective.strip()):
            return 'error', 'Enter the root cause and the corrective action before signing.'
        n.status, n.hod_signed_by, n.hod_signed_at = 'responded', user, now
        n.completion_date = n.completion_date or now.date()
        n.save()
        return 'ok', 'Department response signed by you as concerned Head of Department. The MR now follows up and closes.'
    if act == 'close':
        if n.status != 'responded':
            return 'error', 'The department must respond (root cause, corrective action) before the MR closes the NC&CA.'
        if not _can_manage(user, n.location):
            return 'forbidden', _DENIED % n.location
        if n.satisfactory is None:
            return 'error', 'Record whether the follow-up is satisfactory (Yes / No) before closing.'
        if n.satisfactory is False and not n.next_followup_date:
            return 'error', 'Not satisfactory: enter the next follow-up date (the NC stays open).'
        if n.satisfactory is False:
            n.save()
            return 'ok', 'Follow-up recorded as not satisfactory; next follow-up on %s.' % _d(n.next_followup_date)
        n.status, n.closed_by, n.closed_at = 'closed', user, now
        n.closing_date = n.closing_date or now.date()
        n.followup_date = n.followup_date or now.date()
        if not n.closed_by_name.strip():
            n.closed_by_name = _uname(user)
        if not n.followup_with.strip():
            n.followup_with = _uname(user)
        n.save()
        return 'ok', 'NC&CA %s followed up and closed by you as MR.' % n.nc_no
    if act == 'verify_record':          # the manager confirms the inducted record matches the signed paper form (26-10-2026)
        if not (n.inducted and _can_manage(user, n.location)):
            return 'forbidden', _DENIED % n.location
        if n.verified:
            return 'error', 'This record is already verified against the paper form.'
        n.legacy = dict(n.legacy or {})
        n.legacy['verified'] = {'by': _uname(user), 'user': user.pk, 'at': _tz.localtime(now).strftime('%d-%m-%Y %H:%M'), 'gaps': n.form_gaps}
        n.save()
        return 'ok', 'NC&CA %s verified against the signed paper form and signed by you.' % n.nc_no
    if act == 'reopen':
        if n.status not in ('responded', 'closed') or not _can_manage(user, n.location):
            return 'forbidden', _DENIED % n.location
        if len((reason or '').strip()) < 5:
            return 'error', 'Give the reason for reopening (at least 5 characters).'
        prev = n.status
        n.status = 'open'
        n.hod_signed_by = n.hod_signed_at = n.closed_by = n.closed_at = None
        n.closing_date = n.followup_date = n.satisfactory = n.completion_date = None
        n.closed_by_name = ''
        n.legacy = dict(n.legacy or {})
        if n.legacy.get('verified'):
            n.legacy.setdefault('verified_cleared', []).append(n.legacy.pop('verified'))
        n.legacy.setdefault('reopened', []).append({'by': _uname(user), 'at': _d(now.date()), 'from': prev, 'reason': reason.strip()[:500]})
        n.save()
        return 'ok', 'NC&CA reopened (awaiting the department\'s response); department and closing signatures cleared.'
    return 'error', 'Unknown action.'


def ia_nc_action(request, pk):
    n = get_object_or_404(Ncca, pk=pk)
    back = _post_only(request, '/qc/ia/ncs/%d/' % pk)
    if back:
        return back
    st, text = _apply_nc_action(request.user, n, request.POST.get('action'), request.POST.get('reason') or '')
    if st == 'forbidden':
        return HttpResponse(text, status=403)
    (_msg.success if st == 'ok' else _msg.error)(request, text)
    return _redirect('ia_nc_detail', pk)


def ia_nc_delete(request, pk):
    n = get_object_or_404(Ncca, pk=pk)
    back = _post_only(request, '/qc/ia/ncs/%d/' % pk)
    if back:
        return back
    user = request.user
    if not _can_manage(user, n.location):
        return HttpResponse(_DENIED % n.location, status=403)
    why = (request.POST.get('reason') or '').strip()
    if len(why) < 5:
        _msg.error(request, 'Give the reason for deletion (at least 5 characters).')
        return _redirect('ia_nc_detail', pk)
    extra = {}
    rcas = list(NccaRca.objects.filter(nc=n).order_by('part', 'id'))
    if rcas:
        extra['rca'] = _snap(rcas[0])
        if len(rcas) > 1:
            extra['rcas'] = [_snap(r) for r in rcas]
    _log_deletion('ia_nc', n, user, why, 'NC&CA %s - %s (%s)' % (n.nc_no, n.location, _d(n.date)), extra)
    loc = n.location
    n.delete()
    _msg.success(request, 'NC&CA record deleted; a copy is kept in the deletion log.')
    return _redirect('/qc/ia/ncs/?location=%s&show=all' % loc)


# ---------------------------------------------------------------- root cause analysis (710-FF-01A)
def ia_rca_edit(request, nc_pk):
    n = get_object_or_404(Ncca, pk=nc_pk)
    user = request.user
    if not _can_manage(user, n.location):
        return HttpResponse(_DENIED % n.location, status=403)
    existing = list(NccaRca.objects.filter(nc=n).order_by('part', 'id'))
    want = request.GET.get('rca') or request.POST.get('rca_pk') or ''
    add = (request.GET.get('new') or request.POST.get('new')) == '1' and bool(existing)
    if want.isdigit():
        r = next((x for x in existing if x.pk == int(want)), None)
        if r is None:
            return HttpResponse('RCA not found for this NC&CA.', status=404)
    else:
        r = None if add else (existing[0] if existing else None)
    if r is None and (n.status == 'draft' or n.locked):
        _msg.error(request, 'The root cause analysis is prepared once the NC&CA is raised and before it is closed.')
        return _redirect('ia_nc_detail', n.pk)
    if r is None:
        base = ('R' + n.nc_no[3:]) if n.nc_no.startswith('NC-') else ('RCA-' + n.nc_no)
        part = ''
        if add:             # another root cause of the same NC&CA: parts a, b, c ... (the first one becomes "a")
            used = {x.part for x in existing}
            if not existing[0].part:
                used.add('a')           # the first RCA becomes "a" when this one is saved
            part = next(ch for ch in 'abcdefghijklmnopqrstuvwxyz' if ch not in used)
        r = NccaRca(nc=n, part=part, clause=n.clause.split(' (')[0], deputed=_uname(user), date=_date.today(), statement=n.details if not add else '',
                    rca_no=base + ('(%s)' % part if part else ''), whys=['', '', '', '', '', ''], performed_name=_uname(user), reviewed_name='')
    if r.pk and r.locked:
        _msg.error(request, 'A reviewed RCA is locked. Reopen it first (CEO / administrator).')
        return _redirect('ia_nc_detail', n.pk)
    if request.method == 'POST':
        P = request.POST
        r.rca_no = (P.get('rca_no') or '').strip()[:40]
        r.clause = (P.get('clause') or '').strip()[:60]
        r.deputed = (P.get('deputed') or '').strip()[:120]
        r.date = _pdate(P.get('date'))
        causes = {}
        for main, subs in NccaRca.MAIN_CAUSES:
            key = _re.sub(r'[^a-z]', '', main.lower())
            picked = [s for i, s in enumerate(subs) if P.get('c_%s_%d' % (key, i)) == '1']
            other = (P.get('c_%s_other' % key) or '').strip()[:200]
            if P.get('c_%s' % key) == '1' or picked or other:
                causes[main] = picked
                if other:
                    causes[main + ':other'] = other
        r.causes = causes
        r.other = (P.get('other') or '').strip()[:300]
        r.six_why = P.get('six_why') != '0'
        r.statement = (P.get('statement') or '').strip()[:4000]
        r.whys = [(P.get('why%d' % i) or '').strip()[:1500] for i in range(1, 7)]
        r.conclusion = (P.get('conclusion') or '').strip()[:4000]
        r.performed_name = (P.get('performed_name') or '').strip()[:120]
        r.reviewed_name = (P.get('reviewed_name') or '').strip()[:120]
        if r.status == 'performed':          # edited after the performer's signature -> signature cleared
            r.status, r.performed_by, r.performed_at = 'draft', None, None
        if not r.statement.strip():
            _msg.error(request, 'The statement of problem is required.')
        else:
            r.save()
            if add and existing and not existing[0].part:
                existing[0].part = 'a'; existing[0].save(update_fields=['part'])
            _msg.success(request, 'Root cause analysis saved.')
            return _redirect('ia_nc_detail', n.pk)
    mains = []
    for main, subs in NccaRca.MAIN_CAUSES:
        key = _re.sub(r'[^a-z]', '', main.lower())
        mains.append({'main': main, 'key': key, 'subs': [(i, s, s in (r.causes.get(main) or [])) for i, s in enumerate(subs)], 'on': main in r.causes, 'other': r.causes.get(main + ':other', '')})
    whys = list(r.whys or []) + [''] * 6
    return render(request, 'ia_rca_edit.html', {'n': n, 'r': r, 'add': add and not r.pk, 'loc': n.location, 'mains': mains, 'whys': whys[:6], 'ctrl': _ia_docctrl('rca', n.location, _ia_on(r) if r is not None and r.date else _ia_on(n))})


def _apply_rca_action(user, r, act, reason=''):
    now = _tz.now(); n = r.nc
    if act == 'perform':
        if r.status != 'draft':
            return 'error', 'The RCA is already signed by the performer.'
        if not _can_manage(user, n.location):
            return 'forbidden', _DENIED % n.location
        if not any(w.strip() for w in r.whys) and not r.conclusion.strip():
            return 'error', 'Enter the Why chain or the conclusion before signing.'
        r.status, r.performed_by, r.performed_at = 'performed', user, now
        r.performed_date = r.performed_date or now.date()
        if not r.performed_name.strip():
            r.performed_name = _uname(user)
        r.save()
        return 'ok', 'RCA signed by you as performer. The CEO now reviews.'
    if act == 'review':
        if r.status != 'performed':
            return 'error', 'The performer signs first.' if r.status == 'draft' else 'Already reviewed.'
        if not _is_ceo(user, n.location):
            return 'forbidden', 'Review of the RCA is reserved to the CEO / administrator.'
        if r.performed_by_id == user.id and not _is_admin(user):
            return 'error', 'The performer cannot also review.'
        r.status, r.reviewed_by, r.reviewed_at = 'reviewed', user, now
        r.reviewed_date = r.reviewed_date or now.date()
        if not r.reviewed_name.strip():
            r.reviewed_name = _uname(user)
        r.save()
        return 'ok', 'RCA reviewed and signed by you as CEO.'
    if act == 'reopen':
        if r.status == 'draft' or not (_is_ceo(user, n.location) or (_can_manage(user, n.location) and r.status == 'performed')):
            return 'forbidden', 'Only the CEO / administrator (or the performer before review) can reopen the RCA.'
        if len((reason or '').strip()) < 5:
            return 'error', 'Give the reason for reopening (at least 5 characters).'
        r.status, r.performed_by, r.performed_at, r.reviewed_by, r.reviewed_at = 'draft', None, None, None, None
        r.performed_name, r.performed_date, r.reviewed_name, r.reviewed_date = '', None, '', None
        r.legacy = dict(r.legacy or {}); r.legacy.setdefault('reopened', []).append({'by': _uname(user), 'at': _d(now.date()), 'reason': reason.strip()[:500]})
        r.save()
        return 'ok', 'RCA reopened; signatures cleared.'
    return 'error', 'Unknown action.'


def ia_rca_action(request, pk):
    r = get_object_or_404(NccaRca.objects.select_related('nc'), pk=pk)
    back = _post_only(request, '/qc/ia/ncs/%d/' % r.nc_id)
    if back:
        return back
    st, text = _apply_rca_action(request.user, r, request.POST.get('action'), request.POST.get('reason') or '')
    if st == 'forbidden':
        return HttpResponse(text, status=403)
    (_msg.success if st == 'ok' else _msg.error)(request, text)
    return _redirect('ia_nc_detail', r.nc_id)


# ---------------------------------------------------------------- bulk signing
def _signing_rows(user, loc):
    """Everything the signed-in user can sign now in this laboratory, one row per record and action."""
    if not (user and user.is_authenticated):
        return []
    rows = []
    mgr, member, ceo = _can_manage(user, loc), _is_member(user, loc), _is_ceo(user, loc)
    un = _uname(user).strip().lower()
    if ceo:
        for p in IaPlan.objects.filter(location=loc, status='signed'):
            rows.append({'key': 'plan:%d:approve' % p.pk, 'kind': 'Annual plan', 'label': 'Annual Internal Audit Plan %d' % p.year, 'url': '/qc/ia/plans/%d/' % p.pk, 'action': 'Approve as CEO', 'stage': 'approve'})
    if mgr:
        for p in IaPlan.objects.filter(location=loc, status='draft').exclude(rows=[]):
            rows.append({'key': 'plan:%d:sign_mr' % p.pk, 'kind': 'Annual plan', 'label': 'Annual Internal Audit Plan %d' % p.year, 'url': '/qc/ia/plans/%d/' % p.pk, 'action': 'Sign as MR', 'stage': 'sign'})
        for c in IaCircular.objects.filter(location=loc, status='draft'):
            rows.append({'key': 'circ:%d:issue' % c.pk, 'kind': 'Circular', 'label': '%s circular %s (%s)' % (c.get_kind_display(), c.audit_no, _d(c.issue_date)), 'url': '/qc/ia/circulars/%d/' % c.pk, 'action': 'Issue as MR', 'stage': 'sign'})
        for a in IaAudit.objects.filter(location=loc, status='draft'):
            rows.append({'key': 'audit:%d:sign_auditor' % a.pk, 'kind': 'Audit report', 'label': 'Internal Audit %s (%s)' % (a.audit_no, _d(a.date_start)), 'url': '/qc/ia/audits/%d/' % a.pk, 'action': 'Sign as internal auditor', 'stage': 'sign'})
        for w in IaWitness.objects.filter(audit__location=loc, status='draft').select_related('audit'):
            rows.append({'key': 'wit:%d:sign_auditor' % w.pk, 'kind': 'Witnessing', 'label': 'Witnessing %s of audit %s' % (_d(w.date), w.audit.audit_no), 'url': '/qc/ia/audits/%d/' % w.audit_id, 'action': 'Sign as auditor', 'stage': 'sign'})
        for n in Ncca.objects.filter(location=loc, status='draft').exclude(details=''):
            rows.append({'key': 'nc:%d:raise' % n.pk, 'kind': 'NC&CA', 'label': 'NC&CA %s - %s' % (n.nc_no, n.clause), 'url': '/qc/ia/ncs/%d/' % n.pk, 'action': 'Raise & sign as MR', 'stage': 'sign'})
        for n in Ncca.objects.filter(location=loc, status='responded'):
            rows.append({'key': 'nc:%d:close' % n.pk, 'kind': 'NC&CA', 'label': 'NC&CA %s - %s' % (n.nc_no, n.clause), 'url': '/qc/ia/ncs/%d/' % n.pk, 'action': 'Follow-up & close as MR', 'stage': 'close'})
        for r in NccaRca.objects.filter(nc__location=loc, status='draft').select_related('nc'):
            rows.append({'key': 'rca:%d:perform' % r.pk, 'kind': 'RCA', 'label': 'RCA %s of %s' % (r.rca_no, r.nc.nc_no), 'url': '/qc/ia/ncs/%d/' % r.nc_id, 'action': 'Sign as performer', 'stage': 'sign'})
    if ceo:
        for r in NccaRca.objects.filter(nc__location=loc, status='performed').select_related('nc'):
            rows.append({'key': 'rca:%d:review' % r.pk, 'kind': 'RCA', 'label': 'RCA %s of %s' % (r.rca_no, r.nc.nc_no), 'url': '/qc/ia/ncs/%d/' % r.nc_id, 'action': 'Review as CEO', 'stage': 'approve'})
    if member:
        for c in IaCircular.objects.filter(location=loc, status='issued'):
            mine = [x for x in c.attendance if x.get('user_id') == user.id]
            named = [x for x in c.attendance if not x.get('user_id') and x.get('name', '').strip().lower() in (un, user.username.lower())]
            if not mine and (named or not c.inducted):          # an inducted (historic) circular is signed only by the persons named on it
                rows.append({'key': 'circ:%d:sign' % c.pk, 'kind': 'Circular receipt', 'label': '%s circular %s (%s)' % (c.get_kind_display(), c.audit_no, _d(c.issue_date)), 'url': '/qc/ia/circulars/%d/' % c.pk,
                             'action': 'Sign receipt' + ('' if named else ' (add me to the attendance)'), 'stage': 'ack'})
        for a in IaAudit.objects.filter(location=loc, status='auditor').exclude(auditor_signed_by=user):
            rows.append({'key': 'audit:%d:sign_auditee' % a.pk, 'kind': 'Audit report', 'label': 'Internal Audit %s (%s)' % (a.audit_no, _d(a.date_start)), 'url': '/qc/ia/audits/%d/' % a.pk, 'action': 'Sign as auditee', 'stage': 'ack'})
        for w in IaWitness.objects.filter(audit__location=loc, status='auditor').select_related('audit'):
            if not any(x.get('user_id') == user.id for x in w.auditees):
                rows.append({'key': 'wit:%d:sign_analyst' % w.pk, 'kind': 'Witnessing', 'label': 'Witnessing %s of audit %s' % (_d(w.date), w.audit.audit_no), 'url': '/qc/ia/audits/%d/' % w.audit_id, 'action': 'Sign as analyst witnessed', 'stage': 'ack'})
        for n in Ncca.objects.filter(location=loc, status='open').exclude(root_cause='').exclude(corrective=''):
            rows.append({'key': 'nc:%d:respond' % n.pk, 'kind': 'NC&CA', 'label': 'NC&CA %s - %s' % (n.nc_no, n.clause), 'url': '/qc/ia/ncs/%d/' % n.pk, 'action': 'Sign department response (HOD)', 'stage': 'ack'})
    return rows


_ACTION_FN = {'plan': (IaPlan, _apply_plan_action), 'circ': (IaCircular, _apply_circular_action), 'audit': (IaAudit, _apply_audit_action),
              'wit': (IaWitness, _apply_witness_action), 'nc': (Ncca, _apply_nc_action), 'rca': (NccaRca, _apply_rca_action)}


def ia_signing(request):
    user = request.user
    loc = request.GET.get('location') or _user_office(user) or _default_loc(request)
    loc = loc if loc in _CC_LOCS else 'Karachi'
    if request.method == 'POST':
        allowed = {r['key'] for r in _signing_rows(user, loc)}
        done, problems = 0, []
        for key in request.POST.getlist('rec')[:300]:
            if key not in allowed:
                continue
            kind, pk, act = key.split(':')
            model, fn = _ACTION_FN[kind]
            obj = model.objects.filter(pk=int(pk)).first()
            if obj is None:
                continue
            st, text = fn(user, obj, act)
            if st == 'ok':
                done += 1
            else:
                problems.append(text)
        if done:
            _msg.success(request, '%d record%s signed.' % (done, '' if done == 1 else 's'))
        for t in problems[:8]:
            _msg.error(request, t)
        if not done and not problems:
            _msg.info(request, 'Tick at least one record.')
        return _redirect(request.get_full_path())
    rows = _signing_rows(user, loc)
    return render(request, 'ia_signing.html', {'rows': rows, 'loc': loc, 'locs': _CC_LOCS})


# ---------------------------------------------------------------- document control, deletion log, clauses, manual
def ia_doccontrol(request):
    user = request.user
    if not (user.is_authenticated and _is_admin(user)):
        return HttpResponse('Document control is reserved to the administrator.', status=403)
    if request.method == 'POST':
        P = request.POST
        form, loc = P.get('form'), P.get('location')
        if form in _IA_FORMS and loc in _CC_LOCS:
            obj, _ = InventoryDocControl.objects.get_or_create(module='ia_' + form, location=loc)
            obj.doc_no = (P.get('doc_no') or '').strip()[:40]; obj.issue_date = (P.get('issue_date') or '').strip()[:20]
            obj.issue_no = (P.get('issue_no') or '').strip()[:10]; obj.rev_no = (P.get('rev_no') or '').strip()[:10]
            obj.save()
            _msg.success(request, 'Document control of %s (%s) saved.' % (_IA_FORMS[form][0], loc))
        return _redirect('ia_doccontrol')
    rows = [{'form': f, 'title': _IA_FORMS[f][1], 'per_loc': [(loc, _ia_docctrl(f, loc)) for loc in _CC_LOCS]} for f in _IA_FORMS]
    return render(request, 'ia_doccontrol.html', {'rows': rows, 'locs': _CC_LOCS, 'loc': _loc_of(request)})


def ia_deletions(request):
    user = request.user
    if not user.is_authenticated:
        return _redirect('/login/')
    labs = _user_labs(user)
    if not (_is_admin(user) or labs):
        return HttpResponse('The deletion log is available to the QC / Lab Managers and the CEO / administrator.', status=403)
    qs = ControlChartDeletion.objects.filter(kind__startswith='ia_').select_related('deleted_by')
    if labs and not _is_admin(user):
        qs = qs.filter(location__in=labs)
    return render(request, 'ia_deletions.html', {'rows': qs[:500], 'loc': _loc_of(request)})


def ia_clauses(request):
    user = request.user
    loc = _loc_of(request)
    can = user.is_authenticated and (_is_admin(user) or bool(_user_labs(user)))
    if request.method == 'POST':
        if not can:
            return HttpResponse('The master checklist is maintained by the QC / Lab Managers and the administrator.', status=403)
        P = request.POST
        act = P.get('action')
        if act == 'add':
            code = (P.get('code') or '').strip()[:12]
            if not code or IaClause.objects.filter(code=code).exists():
                _msg.error(request, 'Clause code missing or already present.')
            else:
                after = IaClause.objects.filter(code=(P.get('after') or '').strip()).first()
                order = (after.order + 1) if after else (IaClause.objects.order_by('-order').first().order + 10 if IaClause.objects.exists() else 10)
                IaClause.objects.create(code=code, title=(P.get('title') or '').strip()[:400], requirement=(P.get('requirement') or '').strip()[:4000],
                                        level=code.count('.') + 1, order=order)
                _msg.success(request, 'Clause %s added.' % code)
        elif act == 'save' and (P.get('id') or '').isdigit():
            c = get_object_or_404(IaClause, pk=int(P.get('id')))
            c.title = (P.get('title') or '').strip()[:400]; c.requirement = (P.get('requirement') or '').strip()[:4000]; c.active = P.get('active') == '1'
            c.save()
            _msg.success(request, 'Clause %s saved.' % c.code)
        return _redirect('ia_clauses')
    return render(request, 'ia_clauses.html', {'rows': IaClause.objects.all(), 'can': can, 'loc': loc, 'edit': request.GET.get('edit') or ''})


def ia_manual(request):
    return render(request, 'ia_manual.html', {'loc': _loc_of(request)})
