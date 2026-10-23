"""Management Review (ISO/IEC 17025:2017 clause 8.9) - Management Records module (owner request 23-10-2026).

Records of the procedure ETAL-QMS-P-809, one set per laboratory:
  * Management Review Plan of the year (809-FF-03) - departments x months, Due / Done; MR signs, CEO approves.
  * Management Review Meeting:
      - Circular (809-FF-01): meeting no., date, time, venue, agenda, distribution and the receiving attendance;
        prepared by the MR, issued (signed) by the CEO; each person listed signs receipt.
      - Checklist (809-FF-04): every input of 8.9.2 a) - o) discussed / referenced, or justified.
      - Minutes (809-FF-02): participants, roles, agenda rows (inputs, outputs / decisions, resources, responsibility,
        target date) and an addendum; prepared and signed by the MR, approved and locked by the CEO.
  * Action tracker: every minutes row with a responsibility and a target date is followed up until done - the input
    "status of actions from previous management reviews" (8.9.2 d) of the next meeting.
Same roles as Internal Audit: the laboratory's QC / Lab Manager (MR side) prepares, the CEO / administrator approves.
"""
from .shared import *  # noqa: F401,F403
import json as _json
import re as _re
from datetime import date as _date, datetime as _dt

from django.contrib import messages as _msg
from django.db import transaction as _tx
from django.shortcuts import redirect as _redirect
from django.utils import timezone as _tz

from QC.models import MrmPlan, MrmMeeting, MrmItem, MRM_INPUTS
from QC.views.control_chart import _CC_LOCS, _uname
from QC.views.ia import (_can_manage, _is_member, _is_ceo, _loc_of, _pdate, _d, _post_only, _log_deletion, MONTHS)

_DENIED = 'This action is reserved to the %s laboratory\'s QC / Lab Manager (Management Representative) and the CEO / administrator.'
_FORMS = {'plan': ('ETAL-QMS-809-FF-03', 'MANAGEMENT REVIEW MEETING PLAN'), 'circular': ('ETAL-QMS-809-FF-01', 'CIRCULAR OF MANAGEMENT REVIEW MEETING'),
          'minutes': ('ETAL-QMS-809-FF-02', 'MINUTES OF MANAGEMENT REVIEW MEETING'), 'checklist': ('ETAL-QMS-809-FF-04', 'MANAGEMENT REVIEW MEETING (MRM) CHECKLIST')}
_DEFAULT_CTRL = {   # as printed on the laboratories' forms (inducted 23-10-2026)
    ('plan', 'Karachi'): ('04-04-2022', '01', '00'), ('circular', 'Karachi'): ('04-04-2022', '02', '01'), ('minutes', 'Karachi'): ('04-04-2022', '02', '01'),
    ('plan', 'Lahore'): ('05-01-2024', '01', '00'), ('circular', 'Lahore'): ('05-01-2024', '01', '00'), ('minutes', 'Lahore'): ('05-01-2024', '01', '00'),
    ('checklist', 'Lahore'): ('25-04-2025', '01', '00'),
}
DEFAULT_AGENDA = ['Review of Previous MRM Report', 'Review of Internal Audit Reports', 'Changes in internal and external issues that are relevant to the laboratory',
                  'Fulfilment of objectives', 'Status of actions from previous management reviews', 'Outcome of recent internal audits', 'Corrective actions',
                  'Assessments by external bodies', 'Customer and personnel feedback', 'Complaints', 'Effectiveness of any implemented improvements',
                  'Adequacy of resources', 'Results of risk identification', 'Outcomes of the assurance of the validity of results',
                  'Other relevant factors, such as monitoring activities and training']
_NA_TARGET = _re.compile(r'^\s*(n\.?\s*a\.?|not applicable|-+|nil|none|continuous|ongoing)\s*$', _re.I)


def mrm_docctrl(form, location, on=None):
    """Document-control box of an MRM form (module 'mrm_<form>') as in force on the document's own date."""
    from EnviTechAlApp import doccontrol as DC
    d0 = _DEFAULT_CTRL.get((form, location))
    dflt = {'doc_no': _FORMS[form][0], 'issue_date': d0[0], 'issue_no': d0[1], 'rev_no': d0[2]} if d0 else {'doc_no': _FORMS[form][0]}
    d = DC.doc_control('mrm_' + form, location, on, default=dflt)
    d['title'] = _FORMS[form][1]
    return d


def _on(obj, form=''):
    if isinstance(obj, MrmPlan):
        return _date(int(obj.year), 1, 1)
    if form == 'circular':
        return obj.circular_date or obj.meeting_date
    if form == 'checklist':
        return obj.checklist_date or obj.meeting_date
    return obj.meeting_date


_MONTHS_RE = r'(january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|jun|jul|aug|sep|sept|oct|nov|dec)'


def parse_target(txt):
    """The target date printed in a minutes row -> date, or None (N.A, Continuous, ...). Accepts 12.03.2026, 12-03-2026,
    12/3/26, 2026-03-12, 31-Dec-2026, 15th March 2026, July 2025 / December, 2026 (a month gives its last day)."""
    import calendar
    s = (txt or '').strip()
    if not s or _NA_TARGET.match(s):
        return None
    low = s.lower()
    m = _re.search(r'\b(\d{4})-(\d{1,2})-(\d{1,2})\b', low)
    if m:
        y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
    else:
        m = _re.search(r'\b(\d{1,2})[./-](\d{1,2})[./-](\d{2}|\d{4})\b', low)
        if m:
            d, mo, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
            y = y + 2000 if y < 100 else y
        else:
            m = _re.search(r'\b(?:(\d{1,2})(?:st|nd|rd|th)?[\s.,-]*)?' + _MONTHS_RE + r'\b[\s.,-]*(\d{4})\b', low)
            if not m:
                return None
            months = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6, 'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12}
            y, mo = int(m.group(3)), months[m.group(2)[:3]]
            d = int(m.group(1)) if m.group(1) else calendar.monthrange(y, mo)[1]
    try:
        return _date(y, mo, d)
    except ValueError:
        return None


def _is_action(item):
    return bool((item.responsibility or '').strip() and not _NA_TARGET.match(item.responsibility or '') and item.target_date)


# ---------------------------------------------------------------- home / register
def _counts(loc):
    today = _date.today()
    acts = MrmItem.objects.filter(meeting__location=loc, action_status='open')
    plan = MrmPlan.objects.filter(location=loc, year=today.year).first()
    due = []
    if plan:
        for r in plan.rows:
            for m, v in (r.get('months') or {}).items():
                if v.get('due'):
                    due.append({'dept': r.get('department', ''), 'month': int(m), 'label': MONTHS[int(m) - 1], 'done': bool(v.get('done'))})
    return {'meetings': MrmMeeting.objects.filter(location=loc).count(), 'meetings_year': MrmMeeting.objects.filter(location=loc, year=today.year).count(),
            'open': acts.count(), 'overdue': acts.filter(target_date__lt=today).count(), 'plan': plan,
            'plan_due': sorted({d['month']: (d['month'], d['label'], all(x['done'] for x in due if x['month'] == d['month'])) for d in due}.values()),
            'awaiting': MrmMeeting.objects.filter(location=loc, status='prepared').count() + MrmPlan.objects.filter(location=loc, status='signed').count()}


def mrm_home(request):
    loc = _loc_of(request)
    meetings = MrmMeeting.objects.filter(location=loc).prefetch_related('items')
    today = _date.today()
    rows = []
    for m in meetings:
        acts = [i for i in m.items.all() if i.action_status in ('open', 'done')]
        rows.append({'m': m, 'n_items': len(m.items.all()), 'open': sum(1 for i in acts if i.action_status == 'open'),
                     'overdue': sum(1 for i in acts if i.action_status == 'open' and i.target_date and i.target_date < today),
                     'done': sum(1 for i in acts if i.action_status == 'done'), 'att': len(m.attendance or []),
                     'signed': sum(1 for a in (m.attendance or []) if a.get('signed_at')), 'chk': m.checklist_complete() if m.checklist else None})
    return render(request, 'mrm_home.html', {'loc': loc, 'locs': _CC_LOCS, 'rows': rows, 'c': _counts(loc), 'today': today,
                                             'plans': MrmPlan.objects.filter(location=loc), 'can_manage': _can_manage(request.user, loc),
                                             'is_ceo': _is_ceo(request.user, loc), 'todo': len(_signing_rows(request.user, loc)), 'mrm_page': 'home'})


# ---------------------------------------------------------------- plan (809-FF-03)
def _plan_rows_from_post(P):
    rows = []
    for i in range(0, 20):
        dept = (P.get('dept%d' % i) or '').strip()[:120]
        if not dept:
            continue
        months = {}
        for m in range(1, 13):
            due, done = P.get('r%d_m%d_due' % (i, m)) == '1', P.get('r%d_m%d_done' % (i, m)) == '1'
            if due or done:
                months[str(m)] = {'due': due, 'done': done}
        rows.append({'department': dept, 'months': months})
    return rows


def mrm_plan_edit(request, pk=None):
    user = request.user
    if pk:
        plan = get_object_or_404(MrmPlan, pk=pk)
        loc = plan.location
    else:
        loc = _loc_of(request)
        last = MrmPlan.objects.filter(location=loc).order_by('-year').first()
        plan = MrmPlan(location=loc, year=_date.today().year + (1 if _date.today().month >= 11 else 0), created_by=user,
                       rows=[{'department': r.get('department', ''), 'months': {}} for r in (last.rows if last else [])] or [{'department': 'Environmental Laboratory', 'months': {}}])
    if not _can_manage(user, loc):
        return HttpResponse(_DENIED % loc, status=403)
    if plan.pk and plan.locked:
        _msg.error(request, 'An approved plan is locked. The CEO / administrator can unapprove it with a reason.')
        return _redirect('mrm_plan_detail', plan.pk)
    if request.method == 'POST':
        P = request.POST
        errors = []
        try:
            year = plan.year if plan.pk else int(P.get('year') or 0)
            if not (2020 <= year <= 2100):
                raise ValueError
        except ValueError:
            errors.append('Year must be a four-digit year.'); year = plan.year
        if not plan.pk and MrmPlan.objects.filter(location=loc, year=year).exists():
            errors.append('The %s Management Review Plan for %d already exists.' % (loc, year))
        rows = _plan_rows_from_post(P)
        if not rows:
            errors.append('Enter at least one department.')
        elif not any(v.get('due') for r in rows for v in r['months'].values()):
            errors.append('Mark at least one month as Due (planned review).')
        plan.year, plan.rows, plan.remarks = year, rows, (P.get('remarks') or '').strip()[:2000]
        if errors:
            for e in errors:
                _msg.error(request, e)
        else:
            if plan.status == 'signed':
                plan.status, plan.mr_by, plan.mr_at, plan.mr_name, plan.mr_date = 'draft', None, None, '', None
            plan.save()
            _msg.success(request, 'Management Review Plan %d saved.' % plan.year)
            return _redirect('mrm_plan_detail', plan.pk)
    rows = list(plan.rows or [])
    while len(rows) < 6:
        rows.append({'department': '', 'months': {}})
    return render(request, 'mrm_plan_edit.html', {'plan': plan, 'loc': loc, 'rows': rows, 'months': MONTHS, 'mrange': range(1, 13), 'mrm_page': 'plans'})


def mrm_plan_detail(request, pk):
    plan = get_object_or_404(MrmPlan.objects.select_related('mr_by', 'ceo_by'), pk=pk)
    user = request.user
    meetings = MrmMeeting.objects.filter(location=plan.location, year=plan.year).order_by('meeting_date')
    grid = []
    for ri, r in enumerate(plan.rows or []):
        cells = []
        for mi in range(1, 13):
            v = (r.get('months') or {}).get(str(mi), {})
            cells.append({'m': mi, 'due': bool(v.get('due')), 'done': bool(v.get('done'))})
        grid.append({'ri': ri, 'department': r.get('department', ''), 'cells': cells})
    return render(request, 'mrm_plan_detail.html', {
        'plan': plan, 'loc': plan.location, 'months': MONTHS, 'grid': grid, 'meetings': meetings, 'ctrl': mrm_docctrl('plan', plan.location, _on(plan)),
        'can_edit': _can_manage(user, plan.location) and not plan.locked, 'can_mark': _can_manage(user, plan.location),
        'can_sign_mr': plan.status == 'draft' and _can_manage(user, plan.location), 'can_approve': plan.status == 'signed' and _is_ceo(user, plan.location),
        'can_unapprove': plan.status == 'approved' and _is_ceo(user, plan.location),
        'can_delete': _can_manage(user, plan.location) and plan.status != 'approved', 'mrm_page': 'plans'})


def _apply_plan_action(user, plan, act, reason=''):
    now = _tz.now()
    if act == 'sign_mr':
        if plan.status != 'draft':
            return 'error', 'The plan is already signed.'
        if not _can_manage(user, plan.location):
            return 'forbidden', _DENIED % plan.location
        plan.status, plan.mr_by, plan.mr_at, plan.mr_name, plan.mr_date = 'signed', user, now, _uname(user)[:120], _tz.localdate()
        plan.save()
        return 'ok', 'Signed as Management Representative. The plan awaits the CEO\'s approval.'
    if act == 'approve':
        if plan.status != 'signed' or not _is_ceo(user, plan.location):
            return 'forbidden', 'Approval of the Management Review Plan is reserved to the CEO / administrator, after the MR has signed.'
        plan.status, plan.ceo_by, plan.ceo_at, plan.ceo_name, plan.ceo_date = 'approved', user, now, _uname(user)[:120], _tz.localdate()
        plan.save()
        return 'ok', 'Management Review Plan %d approved and locked.' % plan.year
    if act == 'unapprove':
        if plan.status != 'approved' or not _is_ceo(user, plan.location):
            return 'forbidden', 'Only the CEO / administrator can unapprove a plan.'
        if len((reason or '').strip()) < 5:
            return 'error', 'Give the reason for unapproving (at least 5 characters).'
        plan.status, plan.ceo_by, plan.ceo_at, plan.ceo_name, plan.ceo_date = 'signed', None, None, '', None
        plan.remarks = (plan.remarks + '\n' if plan.remarks else '') + 'Unapproved %s by %s: %s' % (_d(_tz.localdate()), _uname(user), reason.strip()[:500])
        plan.save()
        return 'ok', 'Plan unapproved; it is back at the MR-signed stage.'
    if act == 'delete':
        if not _can_manage(user, plan.location):
            return 'forbidden', _DENIED % plan.location
        if plan.status == 'approved':
            return 'error', 'An approved plan is locked; unapprove it first.'
        if len((reason or '').strip()) < 5:
            return 'error', 'Give the reason for deletion (at least 5 characters).'
        _log_deletion('mrm_plan', plan, user, reason, 'Management Review Plan %d - %s' % (plan.year, plan.location))
        plan.delete()
        return 'deleted', 'Plan deleted; a copy is kept in the deletion log.'
    if act == 'mark_done':
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


def mrm_plan_action(request, pk):
    plan = get_object_or_404(MrmPlan, pk=pk)
    back = _post_only(request, '/qc/mrm/plans/%d/' % pk)
    if back:
        return back
    st, text = _apply_plan_action(request.user, plan, request.POST.get('action'), request.POST.get('reason') or '')
    if st == 'forbidden':
        return HttpResponse(text, status=403)
    if st == 'deleted':
        _msg.success(request, text)
        return _redirect('/qc/mrm/?location=%s' % plan.location)
    (_msg.success if st == 'ok' else _msg.error)(request, text)
    return _redirect('mrm_plan_detail', pk)


# ---------------------------------------------------------------- meeting (circular + checklist + minutes)
def _next_no(loc, year):
    nums = [m.seq for m in MrmMeeting.objects.filter(location=loc, year=year)]
    seq = (max(nums) + 1) if nums else 1
    return seq, '%02d/%d' % (seq, year)


def _list_from_post(P, prefix, n=40, maxlen=300):
    out = []
    for i in range(n):
        v = (P.get('%s%d' % (prefix, i)) or '').strip()[:maxlen]
        if v:
            out.append(v)
    return out


def _people_from_post(P, prefix, old=None, n=40):
    keep = {(a.get('name') or '').strip().lower(): a for a in (old or [])}
    out = []
    for i in range(n):
        name = (P.get('%s%d_name' % (prefix, i)) or '').strip()[:120]
        if not name:
            continue
        prev = keep.get(name.lower(), {})
        row = {'name': name, 'designation': (P.get('%s%d_designation' % (prefix, i)) or '').strip()[:120]}
        if old is not None:
            row.update({'user_id': prev.get('user_id'), 'signed_at': prev.get('signed_at')})
        out.append(row)
    return out


def _items_from_post(P, part):
    rows = []
    idx = sorted({int(m.group(1)) for k in P for m in [_re.match(r'^%s(\d+)_agenda$' % part[0], k)] if m})
    for i in idx[:80]:
        g = lambda f: (P.get('%s%d_%s' % (part[0], i, f)) or '').strip()
        if not any(g(f) for f in ('sno', 'agenda', 'inputs', 'outputs', 'resources', 'responsibility', 'target')):
            continue
        rows.append({'id': g('id'), 'sno': g('sno')[:12], 'clause': g('clause')[:12], 'agenda': g('agenda')[:2000], 'inputs': g('inputs')[:8000],
                     'outputs': g('outputs')[:8000], 'resources': g('resources')[:2000], 'responsibility': g('responsibility')[:1000], 'target': g('target')[:60]})
    return rows


def _save_items(meeting, part, rows):
    """Replace the rows of one part, keeping the follow-up of a row whose id is posted back."""
    old = {i.pk: i for i in meeting.items.filter(part=part)}
    keep = set()
    for order, r in enumerate(rows):
        it = old.get(int(r['id'])) if (r.get('id') or '').isdigit() else None
        if it is None:
            it = MrmItem(meeting=meeting, part=part)
        it.order, it.sno, it.clause, it.agenda, it.inputs, it.outputs = order, r['sno'], r['clause'], r['agenda'], r['inputs'], r['outputs']
        it.resources, it.responsibility, it.target_text = r['resources'], r['responsibility'], r['target']
        it.target_date = parse_target(r['target'])
        if it.action_status not in ('done', 'na'):
            it.action_status = 'open' if _is_action(it) else ''
        it.save()
        keep.add(it.pk)
    for pk, it in old.items():
        if pk not in keep:
            it.delete()


def mrm_meeting_edit(request, pk=None):
    user = request.user
    if pk:
        m = get_object_or_404(MrmMeeting, pk=pk)
        loc = m.location
    else:
        loc = _loc_of(request)
        y = _date.today().year
        seq, no = _next_no(loc, y)
        last = MrmMeeting.objects.filter(location=loc).order_by('-meeting_date', '-id').first()
        m = MrmMeeting(location=loc, year=y, seq=seq, meeting_no=no, created_by=user, circular_date=_date.today(), agenda=list(DEFAULT_AGENDA),
                       distribute_to=['CEO', 'Display on notice board', 'All Employees'],
                       venue=last.venue if last else ('Conference room of Envi Tech AL' if loc == 'Karachi' else 'Lahore Office'),
                       time_text=last.time_text if last else '10:00 am to 02:00 pm', chair=last.chair if last else '', facilitator=last.facilitator if last else '',
                       minutes_taker=last.minutes_taker if last else '', documenter=last.documenter if last else '',
                       participants=list(last.participants) if last else [],
                       attendance=[{'name': a['name'], 'designation': a.get('designation', ''), 'user_id': None, 'signed_at': None} for a in (last.attendance if last else [])],
                       circular_signer=last.circular_signer if last else 'Syed Imran Ali Kazmi')
    if not _can_manage(user, loc):
        return HttpResponse(_DENIED % loc, status=403)
    if m.pk and m.locked:
        _msg.error(request, 'Approved minutes are locked. The CEO / administrator can unapprove them with a reason.')
        return _redirect('mrm_meeting_detail', m.pk)
    if request.method == 'POST':
        P = request.POST
        errors = []
        no = (P.get('meeting_no') or '').strip()[:20]
        mm = _re.match(r'^(\d{1,2})/(\d{4})$', no)
        if not mm:
            errors.append('Meeting # must read like 01/2026.')
        else:
            m.seq, m.year, m.meeting_no = int(mm.group(1)), int(mm.group(2)), '%02d/%s' % (int(mm.group(1)), mm.group(2))
            if MrmMeeting.objects.filter(location=loc, meeting_no=m.meeting_no).exclude(pk=m.pk).exists():
                errors.append('Meeting %s already exists for %s.' % (m.meeting_no, loc))
        m.meeting_date = _pdate(P.get('meeting_date'))
        if not m.meeting_date:
            errors.append('Meeting date is required (dd-mm-yyyy).')
        m.time_text = (P.get('time_text') or '').strip()[:80]
        m.venue = (P.get('venue') or '').strip()[:200]
        m.review_type = (P.get('review_type') or '').strip()[:120]
        m.subject = (P.get('subject') or '').strip()[:200] or 'Management Review Meeting'
        if not m.circular_locked:
            m.circular_date = _pdate(P.get('circular_date'))
            m.circular_intro = (P.get('circular_intro') or '').strip()[:4000]
            m.agenda = _list_from_post(P, 'ag', 30)
            m.distribute_to = _list_from_post(P, 'dist', 10, 120)
            m.attendance = _people_from_post(P, 'att', m.attendance or [])
            m.circular_signer = (P.get('circular_signer') or '').strip()[:120]
            if not m.agenda:
                errors.append('Enter at least one agenda item.')
        m.participants = _people_from_post(P, 'par')
        for f in ('chair', 'facilitator', 'minutes_taker', 'documenter'):
            setattr(m, f, (P.get(f) or '').strip()[:120])
        m.next_mrm = (P.get('next_mrm') or '').strip()[:60]
        m.distributed_to = (P.get('distributed_to') or '').strip()[:200]
        m.addendum_date = _pdate(P.get('addendum_date'))
        m.remarks = (P.get('remarks') or '').strip()[:4000]
        minutes, addendum = _items_from_post(P, 'minutes'), _items_from_post(P, 'addendum')
        if errors:
            for e in errors:
                _msg.error(request, e)
        else:
            with _tx.atomic():
                if m.status == 'prepared':            # edited after the MR signature -> signature cleared
                    m.status, m.mr_by, m.mr_at, m.mr_name, m.mr_date = 'draft', None, None, '', None
                m.save()
                _save_items(m, 'minutes', minutes)
                _save_items(m, 'addendum', addendum)
            _msg.success(request, 'MRM %s saved.' % m.meeting_no)
            return _redirect('mrm_meeting_detail', m.pk)
        items = [MrmItem(pk=int(r['id']) if (r['id'] or '').isdigit() else None, sno=r['sno'], clause=r['clause'], agenda=r['agenda'], inputs=r['inputs'], outputs=r['outputs'], resources=r['resources'],
                         responsibility=r['responsibility'], target_text=r['target']) for r in minutes]
        add = [MrmItem(pk=int(r['id']) if (r['id'] or '').isdigit() else None, part='addendum', sno=r['sno'], clause=r['clause'], agenda=r['agenda'], inputs=r['inputs'], outputs=r['outputs'], resources=r['resources'],
                       responsibility=r['responsibility'], target_text=r['target']) for r in addendum]
    else:
        items = list(m.items.filter(part='minutes')) if m.pk else []
        add = list(m.items.filter(part='addendum')) if m.pk else []
        if not m.pk:
            items = [MrmItem(sno='%s)' % chr(97 + i), agenda=a) for i, a in enumerate(m.agenda)]
    pad = lambda lst, n, part: lst + [MrmItem(part=part) for _ in range(max(0, n - len(lst)))]
    att = list(m.attendance or []) + [{'name': '', 'designation': ''}] * max(0, 12 - len(m.attendance or []))
    par = list(m.participants or []) + [{'name': '', 'designation': ''}] * max(0, 12 - len(m.participants or []))
    agenda = list(m.agenda or []) + [''] * max(0, 18 - len(m.agenda or []))
    dist = list(m.distribute_to or []) + [''] * max(0, 5 - len(m.distribute_to or []))
    return render(request, 'mrm_meeting_edit.html', {'m': m, 'loc': loc, 'items': pad(items, len(items) + 4, 'minutes'), 'add': pad(add, len(add) + 2, 'addendum'),
                                                     'att': att, 'par': par, 'agenda': agenda, 'dist': dist, 'inputs': MRM_INPUTS, 'mrm_page': 'meetings'})


def _my_att_row(m, user):
    if not (user and user.is_authenticated):
        return None
    un = _uname(user).strip().lower()
    for i, a in enumerate(m.attendance or []):
        if a.get('user_id') == user.id or (not a.get('user_id') and (a.get('name') or '').strip().lower() in (un, user.username.lower())):
            return i
    return None


def mrm_meeting_detail(request, pk):
    m = get_object_or_404(MrmMeeting.objects.select_related('mr_by', 'ceo_by', 'circular_by'), pk=pk)
    user = request.user
    my_row = _my_att_row(m, user)
    items = list(m.items.all())
    prev = MrmMeeting.objects.filter(location=m.location, meeting_date__lt=m.meeting_date).order_by('-meeting_date').first() if m.meeting_date else None
    prev_actions = list(prev.items.exclude(action_status='')) if prev else []
    manage, ceo = _can_manage(user, m.location), _is_ceo(user, m.location)
    return render(request, 'mrm_meeting_detail.html', {
        'm': m, 'loc': m.location, 'minutes': [i for i in items if i.part == 'minutes'], 'addendum': [i for i in items if i.part == 'addendum'],
        'checklist': m.checklist_rows(), 'chk_done': m.checklist_complete(), 'prev': prev, 'prev_actions': prev_actions, 'today': _date.today(),
        'signed': sum(1 for a in (m.attendance or []) if a.get('signed_at')),
        'ctrl_c': mrm_docctrl('circular', m.location, _on(m, 'circular')), 'ctrl_m': mrm_docctrl('minutes', m.location, _on(m)),
        'ctrl_k': mrm_docctrl('checklist', m.location, _on(m, 'checklist')),
        'can_edit': manage and not m.locked, 'can_issue': m.circular_status == 'draft' and ceo, 'can_withdraw': m.circular_status == 'issued' and ceo and not m.locked and not m.inducted,
        'can_sign': m.circular_status == 'issued' and _is_member(user, m.location) and my_row is not None and not (m.attendance[my_row].get('signed_at')),
        'can_add_self': m.circular_status == 'issued' and _is_member(user, m.location) and my_row is None and not m.inducted and not m.locked,
        'can_checklist': manage and not m.locked, 'can_prepare': m.status == 'draft' and manage, 'can_approve': m.status == 'prepared' and ceo,
        'can_unapprove': m.status == 'approved' and ceo, 'can_follow': manage, 'can_delete': manage and m.status == 'draft' and m.circular_status == 'draft',
        'mrm_page': 'meetings'})


def mrm_checklist_edit(request, pk):
    m = get_object_or_404(MrmMeeting, pk=pk)
    user = request.user
    if not _can_manage(user, m.location):
        return HttpResponse(_DENIED % m.location, status=403)
    if m.locked:
        _msg.error(request, 'Approved minutes are locked (the checklist is part of the record).')
        return _redirect('mrm_meeting_detail', m.pk)
    if request.method == 'POST':
        P = request.POST
        rows = []
        for i, (code, item) in enumerate(MRM_INPUTS):
            d = P.get('d%d' % i) if P.get('d%d' % i) in ('yes', 'no') else ''
            rows.append({'code': code, 'item': item, 'discussed': d, 'remarks': (P.get('r%d' % i) or '').strip()[:1000],
                         'justification': (P.get('j%d' % i) or '').strip()[:1000]})
        m.checklist = rows
        m.checklist_date = _pdate(P.get('checklist_date')) or m.meeting_date
        missing = [r['code'] for r in rows if r['discussed'] != 'yes' and not r['justification'].strip()]
        if m.status == 'prepared':
            m.status, m.mr_by, m.mr_at, m.mr_name, m.mr_date = 'draft', None, None, '', None
        m.save()
        if missing:
            _msg.warning(request, 'Checklist saved. Not yet complete: %s - each input must be discussed / referenced, or the reason recorded.' % ', '.join(missing))
        else:
            _msg.success(request, 'Checklist saved: every input of 8.9.2 is discussed or justified.')
        return _redirect('/qc/mrm/meetings/%d/#checklist' % m.pk)
    # suggest the minutes rows that reference each input
    refs = {}
    for it in m.items.all():
        if it.clause:
            refs.setdefault(it.clause.replace(' ', ''), []).append(it.sno or it.agenda[:40])
    rows = m.checklist_rows()
    for r in rows:
        r['refs'] = refs.get(r['code'].replace(' ', ''), [])
    return render(request, 'mrm_checklist_edit.html', {'m': m, 'loc': m.location, 'rows': rows, 'mrm_page': 'meetings'})


def _apply_meeting_action(user, m, act, reason='', request=None):
    now = _tz.now()
    manage, ceo = _can_manage(user, m.location), _is_ceo(user, m.location)
    if act == 'issue':
        if m.circular_status != 'draft':
            return 'error', 'The circular is already issued.'
        if not ceo:
            return 'forbidden', 'The circular of the Management Review Meeting is issued (signed) by the CEO / administrator.'
        if not (m.agenda and m.meeting_date and m.circular_date):
            return 'error', 'Complete the circular first: circular date, meeting date and the agenda.'
        m.circular_status, m.circular_by, m.circular_at = 'issued', user, now
        m.circular_signer = _uname(user)[:120]
        m.legacy = dict(m.legacy or {}); m.legacy['circ_snap'] = circ_snapshot(m)    # what the signed circular says
        m.save()
        return 'ok', 'Circular issued and signed by you. The persons listed now sign receipt on this page or on the Signing page.'
    if act == 'withdraw':
        if m.circular_status != 'issued' or not ceo:
            return 'forbidden', 'Withdrawing an issued circular is reserved to the CEO / administrator.'
        if m.locked or m.inducted:
            return 'error', 'The circular of approved minutes or of an inducted record cannot be withdrawn.'
        if len((reason or '').strip()) < 5:
            return 'error', 'Give the reason for withdrawing (at least 5 characters).'
        m.circular_status, m.circular_by, m.circular_at = 'draft', None, None
        for a in m.attendance:
            a['signed_at'] = None; a['user_id'] = None
        m.legacy = dict(m.legacy or {}); m.legacy.setdefault('withdrawals', []).append({'by': _uname(user), 'at': _d(_tz.localdate()), 'reason': reason.strip()[:500]})
        m.save()
        return 'ok', 'Circular withdrawn to draft; receipt signatures cleared.'
    if act in ('sign', 'add_self'):
        if m.circular_status != 'issued' or not _is_member(user, m.location):
            return 'forbidden', 'Only members of the %s laboratory sign receipt of an issued circular.' % m.location
        i = _my_att_row(m, user)
        if i is None:
            if act != 'add_self' or m.inducted or m.locked:
                return 'error', 'You are not listed on this circular.'
            m.attendance.append({'name': _uname(user)[:120], 'designation': '', 'user_id': user.id, 'signed_at': _tz.localtime(now).isoformat()})
        else:
            if m.attendance[i].get('signed_at'):
                return 'error', 'Already signed.'
            m.attendance[i]['user_id'], m.attendance[i]['signed_at'] = user.id, _tz.localtime(now).isoformat()
        m.save()
        return 'ok', 'Receipt of the circular signed.'
    if act == 'prepare':
        if m.status != 'draft' or not manage:
            return 'forbidden', _DENIED % m.location
        if not m.items.filter(part='minutes').exists():
            return 'error', 'The minutes have no agenda rows yet.'
        if not m.participants:
            return 'error', 'Record the participants of the meeting.'
        m.status, m.mr_by, m.mr_at, m.mr_name, m.mr_date = 'prepared', user, now, _uname(user)[:120], _tz.localdate()
        m.save()
        note = '' if (not m.checklist or m.checklist_complete()) else ' Note: the 8.9.2 checklist is not complete.'
        return 'ok', 'Minutes signed as prepared by the Management Representative. They await the CEO\'s approval.' + note
    if act == 'approve':
        if m.status != 'prepared' or not ceo:
            return 'forbidden', 'Approval of the minutes is reserved to the CEO / administrator, after the MR has signed.'
        m.status, m.ceo_by, m.ceo_at, m.ceo_name, m.ceo_date = 'approved', user, now, _uname(user)[:120], _tz.localdate()
        m.save()
        _mark_plan_done(m)
        return 'ok', 'Minutes of MRM %s approved and locked. The actions are followed up on the Action tracker.' % m.meeting_no
    if act == 'unapprove':
        if m.status != 'approved' or not ceo:
            return 'forbidden', 'Only the CEO / administrator can unapprove the minutes.'
        if len((reason or '').strip()) < 5:
            return 'error', 'Give the reason for unapproving (at least 5 characters).'
        m.status, m.ceo_by, m.ceo_at, m.ceo_name, m.ceo_date = 'prepared', None, None, '', None
        m.remarks = (m.remarks + '\n' if m.remarks else '') + 'Unapproved %s by %s: %s' % (_d(_tz.localdate()), _uname(user), reason.strip()[:500])
        m.save()
        return 'ok', 'Minutes unapproved; they are back at the MR-signed stage.'
    if act == 'delete':
        if not manage:
            return 'forbidden', _DENIED % m.location
        if m.status != 'draft' or m.circular_status != 'draft':
            return 'error', 'Only a draft meeting whose circular is not issued can be deleted.'
        if len((reason or '').strip()) < 5:
            return 'error', 'Give the reason for deletion (at least 5 characters).'
        _log_deletion('mrm_meet', m, user, reason, 'MRM %s (%s) - %s' % (m.meeting_no, _d(m.meeting_date), m.location),
                      extra={'items': [dict(part=i.part, sno=i.sno, clause=i.clause, agenda=i.agenda, inputs=i.inputs, outputs=i.outputs, resources=i.resources,
                                            responsibility=i.responsibility, target=i.target_text, action_status=i.action_status, done_note=i.done_note)
                                       for i in m.items.all()]})
        m.delete()
        return 'deleted', 'Meeting deleted; a copy is kept in the deletion log.'
    return 'error', 'Unknown action.'


def circ_snapshot(m):
    return {'meeting_no': m.meeting_no, 'meeting_date': m.meeting_date.isoformat() if m.meeting_date else '', 'time': m.time_text, 'venue': m.venue,
            'subject': m.subject}


def _mark_plan_done(m):
    """The month of an approved meeting is marked Done on the plan of its year (when that month is planned)."""
    if not m.meeting_date:
        return
    plan = MrmPlan.objects.filter(location=m.location, year=m.meeting_date.year).first()
    if not plan:
        return
    changed = False
    for r in plan.rows or []:
        cell = (r.get('months') or {}).get(str(m.meeting_date.month))
        if cell and cell.get('due') and not cell.get('done'):
            cell['done'] = True; changed = True
    if changed:
        plan.save()


def mrm_meeting_action(request, pk):
    m = get_object_or_404(MrmMeeting, pk=pk)
    back = _post_only(request, '/qc/mrm/meetings/%d/' % pk)
    if back:
        return back
    st, text = _apply_meeting_action(request.user, m, request.POST.get('action'), request.POST.get('reason') or '', request)
    if st == 'forbidden':
        return HttpResponse(text, status=403)
    if st == 'deleted':
        _msg.success(request, text)
        return _redirect('/qc/mrm/?location=%s' % m.location)
    (_msg.success if st == 'ok' else _msg.error)(request, text)
    return _redirect('mrm_meeting_detail', pk)


# ---------------------------------------------------------------- action tracker (8.9.2 d)
def mrm_actions(request):
    loc = _loc_of(request)
    show = request.GET.get('show') if request.GET.get('show') in ('open', 'done', 'all') else 'open'
    qs = MrmItem.objects.filter(meeting__location=loc).exclude(action_status='').exclude(action_status='na').select_related('meeting', 'done_by').prefetch_related('meeting__items')
    if show != 'all':
        qs = qs.filter(action_status=show)
    rows = sorted(qs, key=lambda i: (i.action_status != 'open', i.target_date or _date(2100, 1, 1), i.meeting.meeting_date or _date(2000, 1, 1)))
    today = _date.today()
    for r in rows:
        r.days_left = (r.target_date - today).days if (r.target_date and r.action_status == 'open') else None
        r.overdue = -r.days_left if (r.days_left is not None and r.days_left < 0) else 0
        before = sorted((x for x in r.meeting.items.all() if x.part == r.part and x.order < r.order and x.agenda), key=lambda x: -x.order)
        r.topic = r.agenda or (before[0].agenda if before else '')
    return render(request, 'mrm_actions.html', {'loc': loc, 'locs': _CC_LOCS, 'rows': rows, 'show': show, 'can_follow': _can_manage(request.user, loc),
                                                'c': _counts(loc), 'mrm_page': 'actions'})


def mrm_action_update(request, pk):
    it = get_object_or_404(MrmItem.objects.select_related('meeting'), pk=pk)
    back = _post_only(request, '/qc/mrm/actions/')
    if back:
        return back
    if not _can_manage(request.user, it.meeting.location):
        return HttpResponse(_DENIED % it.meeting.location, status=403)
    act = request.POST.get('action')
    note = (request.POST.get('note') or '').strip()[:500]
    if act == 'done':
        if len(note) < 5:
            _msg.error(request, 'Record how the action was completed / its effectiveness (at least 5 characters).')
        else:
            it.action_status, it.done_note, it.done_by, it.done_at = 'done', note, request.user, _tz.now()
            it.save()
            _msg.success(request, 'Action marked done.')
    elif act == 'reopen':
        it.action_status, it.done_by, it.done_at = 'open', None, None
        it.done_note = ('%s | reopened %s by %s: %s' % (it.done_note, _d(_date.today()), _uname(request.user), note))[-500:]
        it.save()
        _msg.success(request, 'Action reopened.')
    elif act == 'na':
        it.action_status = 'na'
        it.save()
        _msg.success(request, 'Row marked as not an action.')
    nxt = request.POST.get('next') or ''
    return _redirect(nxt if nxt.startswith('/qc/mrm/') else '/qc/mrm/actions/?location=%s' % it.meeting.location)


# ---------------------------------------------------------------- signing
def _signing_rows(user, loc):
    if not (user and user.is_authenticated):
        return []
    rows = []
    mgr, member, ceo = _can_manage(user, loc), _is_member(user, loc), _is_ceo(user, loc)
    un = _uname(user).strip().lower()
    if ceo:
        for p in MrmPlan.objects.filter(location=loc, status='signed'):
            rows.append({'kind': 'MRM plan', 'label': 'Management Review Plan %d' % p.year, 'url': '/qc/mrm/plans/%d/' % p.pk, 'action': 'Approve as CEO'})
        for m in MrmMeeting.objects.filter(location=loc, status='prepared'):
            rows.append({'kind': 'Minutes', 'label': 'MRM %s (%s)' % (m.meeting_no, _d(m.meeting_date)), 'url': '/qc/mrm/meetings/%d/' % m.pk, 'action': 'Approve minutes as CEO'})
        for m in MrmMeeting.objects.filter(location=loc, circular_status='draft').exclude(agenda=[]):
            rows.append({'kind': 'Circular', 'label': 'MRM %s circular' % m.meeting_no, 'url': '/qc/mrm/meetings/%d/' % m.pk, 'action': 'Issue circular as CEO'})
    if mgr:
        for p in MrmPlan.objects.filter(location=loc, status='draft').exclude(rows=[]):
            rows.append({'kind': 'MRM plan', 'label': 'Management Review Plan %d' % p.year, 'url': '/qc/mrm/plans/%d/' % p.pk, 'action': 'Sign as MR'})
        for m in MrmMeeting.objects.filter(location=loc, status='draft', meeting_date__lte=_date.today()):
            rows.append({'kind': 'Minutes', 'label': 'MRM %s (%s)' % (m.meeting_no, _d(m.meeting_date)), 'url': '/qc/mrm/meetings/%d/' % m.pk, 'action': 'Complete & sign as MR'})
    if member:
        for m in MrmMeeting.objects.filter(location=loc, circular_status='issued'):
            mine = [x for x in m.attendance if x.get('user_id') == user.id]
            named = [x for x in m.attendance if not x.get('user_id') and (x.get('name') or '').strip().lower() in (un, user.username.lower())]
            if not mine and (named or not m.inducted):
                rows.append({'kind': 'Circular receipt', 'label': 'MRM %s circular' % m.meeting_no, 'url': '/qc/mrm/meetings/%d/' % m.pk,
                             'action': 'Sign receipt' + ('' if named else ' (add me)')})
    return rows


def mrm_signing(request):
    loc = _loc_of(request)
    return render(request, 'mrm_signing.html', {'loc': loc, 'locs': _CC_LOCS, 'rows': _signing_rows(request.user, loc), 'mrm_page': 'signing'})


def mrm_deletions(request):
    from QC.models import ControlChartDeletion
    from QC.views.control_chart import _user_labs, _is_admin
    user = request.user
    if not user.is_authenticated:
        return _redirect('/login/')
    labs = _user_labs(user)
    if not (_is_admin(user) or labs):
        return HttpResponse('The deletion log is available to the QC / Lab Managers and the CEO / administrator.', status=403)
    qs = ControlChartDeletion.objects.filter(kind__startswith='mrm_').select_related('deleted_by')
    if labs and not _is_admin(user):
        qs = qs.filter(location__in=labs)
    return render(request, 'mrm_deletions.html', {'rows': qs[:500], 'loc': _loc_of(request), 'mrm_page': 'deletions'})
