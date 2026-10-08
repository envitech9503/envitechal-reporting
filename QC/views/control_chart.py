"""QC Control Charts (form ETAL-LAB-604-FF-11) - views. 07-10-2026.

Roles: any logged-in user records a monthly result (stamped as Performed By);
'review' = superuser, Django group "QC Manager", or a Signatures role containing
"QC"/"Manager"; 'approve' (and baseline / chart master changes) = superuser.
An approved year is locked for everyone except superusers.
"""
from .shared import *  # noqa: F401,F403
import json as _json
import math as _math
from datetime import date as _date, datetime as _dt
from django.utils import timezone as _tz
from django.shortcuts import redirect as _redirect
from django.db.models import Q as _Q
from django.contrib import messages as _msg
from django.views.decorators.http import require_POST as _require_POST

from QC.models import ControlChart, ControlChartBaseline, ControlChartResult, ControlChartSignoff, ControlChartReviewer, run_limits, classify_value
from QC.control_chart_render import render_chart, period_rows, period_label as _plabel, fmt as _fmt, MONTHS as _MONTHS

_CC_LOCS = ['Karachi', 'Lahore']
_CC_ACTS = ['CRM', 'RM', 'IC']
_CC_FORM = {'doc_no': 'ETAL-LAB-604-FF-11', 'issue_date': '19-03-2022', 'issue_no': '01', 'rev_no': '00'}
# Document-control rows are kept per laboratory AND per form type (CRM / RM / IC):
# InventoryDocControl(module=<key below>, location=<lab>). Only the Karachi CRM form
# number is known to the system; the others are entered by an administrator on
# the Document control page and show as 'TBA' until then (08-10-2026).
_CC_DOC_MODULES = {'CRM': 'control_chart', 'RM': 'control_chart_rm', 'IC': 'control_chart_ic'}
_CC_OFFICE = {
    'Karachi': {'tel': 'Tel: +92 310 2288801',
                'address': 'Head Office: 345, First Floor, Street-15, Block-3, Bahadurabad, Karachi. 75900, Pakistan.'},
    'Lahore': {'tel': 'Tel: +92 42 32296099',
               'address': 'Lahore Office: 87-E Madina Height, Office # A/30 & A/31, 8th Floor, Johar Town, Lahore, Pakistan.'},
}
_CC_SOP_NOTE = ('The baseline results were established using data from the February intermediate check '
                'activity, as per the procedure ETAL-LAB-P-604 (two intermediate check activities are planned: '
                'one after calibration and the other before PT). Accordingly, the results from the February '
                'activity (conducted before PT) were used to establish the baseline, and the monthly results '
                'are plotted against this baseline.')


def _cc_docctrl(location, activity='CRM'):
    """Document-control numbers of the form for this laboratory and form type."""
    known = (location == 'Karachi' and activity == 'CRM')
    dflt = dict(_CC_FORM) if known else {'doc_no': '', 'issue_date': '', 'issue_no': '01', 'rev_no': '00'}
    try:
        obj, _ = InventoryDocControl.objects.get_or_create(
            module=_CC_DOC_MODULES.get(activity, 'control_chart'), location=location, defaults=dflt)
        return {'doc_no': obj.doc_no or (dflt['doc_no'] or 'TBA'), 'issue_date': obj.issue_date or (dflt['issue_date'] or '-'),
                'issue_no': obj.issue_no or '01', 'rev_no': obj.rev_no or '00', 'set': bool(obj.doc_no or dflt['doc_no'])}
    except Exception:
        d = dict(dflt); d['doc_no'] = d['doc_no'] or 'TBA'; d['issue_date'] = d['issue_date'] or '-'; d['set'] = known
        return d


def _uname(user):
    try:
        return (user.get_full_name() or user.get_username() or '').strip() if user else ''
    except Exception:
        return ''


def _user_labs(user):
    """Laboratories this user is assigned to as QC / Lab Manager (empty = none)."""
    try:
        if not (user and user.is_authenticated):
            return set()
        return set(ControlChartReviewer.objects.filter(user=user).values_list('location', flat=True))
    except Exception:
        return set()


def _is_admin(user):
    return bool(user and user.is_authenticated and user.is_superuser)


def _can_create(user):
    """Any signed-in laboratory user (chemist) may add a new control chart
    (opened 08-10-2026 at the owner's request)."""
    return bool(user and user.is_authenticated and user.is_active)


def _can_edit_master(user, chart):
    """Chart masters: administrators; additionally the chemist who created the
    chart, until its first result has been recorded."""
    if _is_admin(user):
        return True
    if not (user and user.is_authenticated and chart is not None):
        return False
    return chart.created_by_id == user.id and not ControlChartResult.objects.filter(chart=chart).exists()


def _can_set_baseline(user, chart):
    """Baselines: administrators; additionally the chemist who created the
    chart may establish its FIRST baseline (v1). Re-baselining stays with
    administrators."""
    if _is_admin(user):
        return True
    if not (user and user.is_authenticated and chart is not None):
        return False
    return chart.created_by_id == user.id and chart.current_baseline() is None


def _can_approve(user, chart=None):
    """Approve & lock, delete results, edit masters: superusers. A superuser who
    is assigned to a laboratory is treated as that lab's manager and may not
    approve the other laboratory's charts (added 07-10-2026)."""
    if not _is_admin(user):
        return False
    if chart is None:
        return True
    labs = _user_labs(user)
    return (not labs) or (chart.location in labs)


def _can_review(user, chart=None):
    """Review: a user assigned to a laboratory reviews that laboratory's charts
    only; otherwise superusers, the "QC Manager" group or a QC/Manager
    signature role (global, legacy behaviour)."""
    if not (user and user.is_authenticated):
        return False
    labs = _user_labs(user)
    if labs:
        return chart is None or chart.location in labs
    if _is_admin(user):
        return True
    try:
        if user.groups.filter(name__iexact='QC Manager').exists():
            return True
        role = (Signatures.objects.filter(user=user).first() or Signatures()).role
        r = (getattr(role, 'role', '') or '').lower()
        return ('qc' in r) or ('manager' in r)
    except Exception:
        return False


def _default_loc(request):
    """Laboratory the selector opens on: the user's last choice (session), else
    the user's assigned laboratory, else a 'lahore' username hint, else Karachi."""
    loc = request.session.get('cc_loc')
    if loc in _CC_LOCS:
        return loc
    labs = sorted(_user_labs(request.user))
    if labs:
        return labs[0]
    try:
        if 'lahore' in (request.user.get_username() or '').lower():
            return 'Lahore'
    except Exception:
        pass
    return 'Karachi'


def _year(request, chart=None):
    """Record year: ?year=, else the current cycle of the chart (calendar year for IC)."""
    today_y = chart.cycle_of(_date.today()) if (chart is not None and not chart.period_is_month) else _date.today().year
    try:
        return int(request.GET.get('year') or today_y)
    except Exception:
        return today_y


def _month(request, chart, year, results_qs=None):
    """Record month for IC charts (0 for the others): ?month=, else the latest
    month of that year holding readings, else the current month / December."""
    if not chart.period_is_month:
        return 0
    try:
        m = int(request.GET.get('month') or 0)
    except Exception:
        m = 0
    if 1 <= m <= 12:
        return m
    months = sorted({d.month for d in ControlChartResult.objects.filter(chart=chart, date__year=year).values_list('date', flat=True)})
    if months:
        return months[-1]
    return _date.today().month if year == _date.today().year else 12


def _period_results(chart, year, month=0):
    if chart.period_is_month:
        qs = ControlChartResult.objects.filter(chart=chart, date__year=year)
        if month:
            qs = qs.filter(date__month=month)
    else:
        a, b = chart.cycle_range(year)
        qs = ControlChartResult.objects.filter(chart=chart, date__gte=a, date__lte=b)
    return list(qs.order_by('date', 'id'))


def _chart_years(chart):
    ys = {chart.cycle_of(d) if not chart.period_is_month else d.year
          for d in ControlChartResult.objects.filter(chart=chart).values_list('date', flat=True)}
    ys.add(chart.cycle_of(_date.today()) if not chart.period_is_month else _date.today().year)
    return sorted(ys, reverse=True)


def _limits(chart, baseline, results):
    """Limits of a record period: from the run's own readings (IC) or the baseline."""
    if chart.self_limited:
        return run_limits([r.value for r in results])
    return baseline.limits() if baseline else None


def _restatus_run(chart, year, month):
    """IC: re-judge every reading of the run against the run's own mean / SD."""
    rs = _period_results(chart, year, month)
    lim = run_limits([r.value for r in rs])
    for r in rs:
        st = classify_value(lim, r.value)
        if st != r.status:
            ControlChartResult.objects.filter(pk=r.pk).update(status=st)
    return lim


def _signoff(chart, year, month=0):
    return ControlChartSignoff.objects.filter(chart=chart, year=year, month=month or 0).first()


def _year_locked(chart, year, user, month=0):
    so = _signoff(chart, year, month)
    return bool(so and so.locked and not _can_approve(user, chart))


def _qs_period(chart, d):
    """(year, month) record period a result date belongs to."""
    if chart.period_is_month:
        return d.year, d.month
    return chart.cycle_of(d), 0


def _pq(year, month=0):
    return '?year=%d' % year + ('&month=%d' % month if month else '')


# ---------------------------------------------------------------- list
def control_chart_list(request):
    loc = request.GET.get('location') or _default_loc(request)
    if loc not in _CC_LOCS:
        loc = 'Karachi'
    if request.session.get('cc_loc') != loc:
        request.session['cc_loc'] = loc
    q = (request.GET.get('q') or '').strip()
    year = _year(request)
    act = request.GET.get('activity') or request.session.get('cc_act') or 'All'
    if act not in _CC_ACTS:
        act = 'All'
    request.session['cc_act'] = act
    qs = ControlChart.objects.filter(active=True, location=loc)
    if act != 'All':
        qs = qs.filter(activity=act)
    if q:
        qs = qs.filter(_Q(parameter__icontains=q) | _Q(equipment__icontains=q) | _Q(equipment_id__icontains=q)
                       | _Q(method__icontains=q) | _Q(level__icontains=q))
    charts = list(qs)
    ids = [c.id for c in charts]
    cmap = {c.id: c for c in charts}
    res = {}
    for r in ControlChartResult.objects.filter(chart_id__in=ids, date__year__in=[year, year + 1]).order_by('date'):
        c = cmap[r.chart_id]
        if (r.date.year if c.period_is_month else c.cycle_of(r.date)) == year:
            res.setdefault(r.chart_id, []).append(r)
    sos = {}
    for s_ in ControlChartSignoff.objects.filter(chart_id__in=ids, year=year):
        sos.setdefault(s_.chart_id, {})[s_.month] = s_
    rows = []
    order = {'CRM': 0, 'RM': 1, 'IC': 2}
    for c in sorted(charts, key=lambda c: (order.get(c.activity, 9), c.parameter, c.level, c.equipment_id)):
        rr = res.get(c.id, [])
        b = c.current_baseline()
        last = rr[-1] if rr else None
        worst = 'ooc' if any(r.status == 'ooc' for r in rr) else ('warning' if any(r.status == 'warning' for r in rr) else ('ok' if rr else 'none'))
        if c.self_limited:
            # the list shows the latest run of the year (its own mean / SD / sign-off)
            m = last.date.month if last else 0
            run = [r for r in rr if r.date.month == m]
            lim = run_limits([r.value for r in run]) or {}
            so = sos.get(c.id, {}).get(m)
            mean, sd, n, of, runs = lim.get('mean'), lim.get('sd'), len(run), '', len({r.date.month for r in rr})
        else:
            so = sos.get(c.id, {}).get(0)
            mean, sd, n, of, runs = (b.mean if b else None), (b.sd if b else None), len(rr), (' / 12' if c.cadence == 'monthly' else ''), 0
        rows.append({'c': c, 'n': n, 'of': of, 'runs': runs, 'last': last, 'last_value': _fmt(last.value, c.decimals) if last else '',
                     'worst': worst, 'mean': _fmt(mean, c.decimals) if mean is not None else '', 'sd': _fmt(sd, c.decimals + 1) if sd is not None else '',
                     'bver': b.version if b else '', 'reviewed': bool(so and so.reviewed_at), 'approved': bool(so and so.approved_at),
                     'month': _MONTHS[last.date.month - 1] if (c.self_limited and last) else '', 'cycle': c.cycle_label(year) if not c.period_is_month else str(year)})
    allc = {c.id: c for c in ControlChart.objects.all()}
    years = sorted({(allc[cid].cycle_of(d) if (cid in allc and not allc[cid].period_is_month) else d.year)
                    for cid, d in ControlChartResult.objects.values_list('chart_id', 'date')} | {_date.today().year}, reverse=True)
    counts = {a: ControlChart.objects.filter(active=True, location=loc, activity=a).count() for a in _CC_ACTS}
    return render(request, 'control_chart_list.html', {
        'rows': rows, 'loc': loc, 'locs': _CC_LOCS, 'q': q, 'year': year, 'years': years, 'act': act, 'acts': _CC_ACTS, 'counts': counts,
        'can_admin': _is_admin(request.user), 'can_create': _can_create(request.user), 'count': len(rows)})


# ---------------------------------------------------------------- archive (all laboratories / all years)
def control_chart_archive(request):
    """Record list: one row per chart-year that holds results or a sign-off,
    across both laboratories, with filters - the module's 'List' page from
    which any past record can be recalled (view / PDF). 07-10-2026."""
    loc = request.GET.get('location') or 'All'
    q = (request.GET.get('q') or '').strip()
    ystr = request.GET.get('year') or 'All'
    status_f = request.GET.get('status') or 'All'
    sign_f = request.GET.get('signoff') or 'All'
    act_f = request.GET.get('activity') or 'All'
    charts = {c.id: c for c in ControlChart.objects.all()}
    pairs = set()
    stats = {}
    for cid, d, st in ControlChartResult.objects.values_list('chart_id', 'date', 'status'):
        c = charts.get(cid)
        key = (cid, d.year, d.month) if (c and c.period_is_month) else (cid, c.cycle_of(d) if c else d.year, 0)
        pairs.add(key)
        s = stats.setdefault(key, {'n': 0, 'warning': 0, 'ooc': 0, 'last': None})
        s['n'] += 1
        if st in ('warning', 'ooc'):
            s[st] += 1
        if s['last'] is None or d > s['last']:
            s['last'] = d
    sos = {}
    for so in ControlChartSignoff.objects.select_related('reviewed_by', 'approved_by'):
        pairs.add((so.chart_id, so.year, so.month))
        sos[(so.chart_id, so.year, so.month)] = so
    rows = []
    for cid, y, m in pairs:
        c = charts.get(cid)
        if not c:
            continue
        if loc in _CC_LOCS and c.location != loc:
            continue
        if act_f in _CC_ACTS and c.activity != act_f:
            continue
        if ystr != 'All' and str(y) != ystr:
            continue
        if q and not any(q.lower() in (v or '').lower() for v in (c.parameter, c.level, c.equipment, c.equipment_id, c.method)):
            continue
        s = stats.get((cid, y, m), {'n': 0, 'warning': 0, 'ooc': 0, 'last': None})
        worst = 'ooc' if s['ooc'] else ('warning' if s['warning'] else ('ok' if s['n'] else 'none'))
        if status_f != 'All' and worst != status_f:
            continue
        so = sos.get((cid, y, m))
        sign = 'approved' if (so and so.approved_at) else ('reviewed' if (so and so.reviewed_at) else 'open')
        if sign_f != 'All' and sign != sign_f:
            continue
        rows.append({'c': c, 'year': y, 'month': m, 'period': _plabel(c, y, m), 'pq': _pq(y, m), 'of': (' / 12' if c.cadence == 'monthly' else ''),
                     'n': s['n'], 'warn': s['warning'], 'ooc': s['ooc'], 'last': s['last'], 'worst': worst, 'sign': sign, 'so': so})
    rows.sort(key=lambda r: (-r['year'], -r['month'], r['c'].location, {'CRM': 0, 'RM': 1, 'IC': 2}.get(r['c'].activity, 9), r['c'].parameter.lower(), r['c'].level))
    years = sorted({y for _, y, _m in pairs}, reverse=True)
    return render(request, 'control_chart_archive.html', {
        'rows': rows, 'loc': loc, 'locs': _CC_LOCS, 'q': q, 'year': ystr, 'years': years, 'act': act_f, 'acts': _CC_ACTS,
        'status': status_f, 'signoff': sign_f, 'count': len(rows), 'can_admin': _is_admin(request.user)})


# ---------------------------------------------------------------- document control (admin)
def control_chart_doccontrol(request):
    """Document-control numbers of the three forms, per laboratory (08-10-2026).
    Karachi and Lahore use different controlled-document numbers."""
    if not _is_admin(request.user):
        return HttpResponse('Document-control numbers are maintained by an administrator.', status=403)
    if request.method == 'POST':
        loc, act = request.POST.get('location'), request.POST.get('activity')
        if loc not in _CC_LOCS or act not in _CC_ACTS:
            return HttpResponse('bad request', status=400)
        obj, _ = InventoryDocControl.objects.get_or_create(module=_CC_DOC_MODULES[act], location=loc)
        obj.doc_no = (request.POST.get('doc_no') or '').strip()[:60]
        obj.issue_date = (request.POST.get('issue_date') or '').strip()[:20]
        obj.issue_no = (request.POST.get('issue_no') or '').strip()[:10] or '01'
        obj.rev_no = (request.POST.get('rev_no') or '').strip()[:10] or '00'
        obj.updated_by = request.user
        obj.save()
        _msg.success(request, 'Document control updated for the %s %s form.' % (loc, act))
        return _redirect('control_chart_doccontrol')
    grid = []
    for loc in _CC_LOCS:
        for act in _CC_ACTS:
            d = _cc_docctrl(loc, act)
            raw = InventoryDocControl.objects.filter(module=_CC_DOC_MODULES[act], location=loc).first()
            grid.append({'location': loc, 'activity': act, 'name': dict(ControlChart.ACTIVITIES)[act],
                         'doc_no': raw.doc_no if raw else '', 'issue_date': raw.issue_date if raw else '',
                         'issue_no': d['issue_no'], 'rev_no': d['rev_no'], 'shown': d['doc_no'], 'set': d['set'],
                         'updated': raw.updated_at if raw else None, 'by': raw.updated_by if raw else None})
    return render(request, 'control_chart_doccontrol.html', {'grid': grid, 'office': _CC_OFFICE})


# ---------------------------------------------------------------- user manual
def control_chart_manual(request):
    """Self-contained searchable user manual for the module (same pattern as the
    reagent-preparation manual; rendered so the unified navigation bar appears)."""
    return render(request, 'control_chart_manual.html', {})


# ---------------------------------------------------------------- reviewers (admin)
def control_chart_reviewers(request):
    """Assign QC / Lab Managers to a laboratory (superuser only)."""
    if not _is_admin(request.user):
        return HttpResponse('Reviewer assignments are maintained by an administrator.', status=403)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            try:
                u = User.objects.get(pk=int(request.POST.get('user')))
            except Exception:
                _msg.error(request, 'Select a user.')
                return _redirect('control_chart_reviewers')
            loc = request.POST.get('location')
            if loc not in _CC_LOCS:
                _msg.error(request, 'Select a laboratory.')
                return _redirect('control_chart_reviewers')
            _, created = ControlChartReviewer.objects.get_or_create(user=u, location=loc, defaults={'created_by': request.user})
            _msg.success(request, '%s assigned to %s laboratory.' % (_uname(u), loc) if created else 'Already assigned.')
        elif action == 'remove':
            try:
                n, _ = ControlChartReviewer.objects.filter(pk=int(request.POST.get('id') or 0)).delete()
            except (TypeError, ValueError):
                n = 0
            (_msg.success if n else _msg.error)(request, 'Assignment removed.' if n else 'Assignment not found.')
        return _redirect('control_chart_reviewers')
    return render(request, 'control_chart_reviewers.html', {
        'rows': ControlChartReviewer.objects.select_related('user'), 'locs': _CC_LOCS,
        'users': User.objects.filter(is_active=True).order_by('username')})


# ---------------------------------------------------------------- detail
def control_chart_detail(request, pk):
    chart = get_object_or_404(ControlChart, pk=pk)
    year = _year(request, chart)
    month = _month(request, chart, year)
    b = chart.current_baseline()
    results = _period_results(chart, year, month)
    lim = _limits(chart, b, results)
    rows, extra_base = period_rows(chart, lim, b.values if (b and not chart.self_limited) else [], results, year, month)
    svg = render_chart(chart, lim, results, year, month, 'svg').decode('utf-8') if (lim or (chart.self_limited and results)) else ''
    so = _signoff(chart, year, month)
    user = request.user
    lim_f = {k: _fmt(v, chart.decimals) for k, v in (lim or {}).items()}
    if lim:
        lim_f['sd'] = _fmt(lim['sd'], chart.decimals + 1)
    years = [{'y': y, 'label': _plabel(chart, y)} for y in _chart_years(chart)]
    months = []
    if chart.period_is_month:
        have = {d.month for d in ControlChartResult.objects.filter(chart=chart, date__year=year).values_list('date', flat=True)}
        months = [{'m': i, 'name': _MONTHS[i - 1], 'has': i in have} for i in range(1, 13)]
    return render(request, 'control_chart_detail.html', {
        'chart': chart, 'b': b, 'lim': lim_f, 'lim_n': (lim or {}).get('n', 0), 'rows': rows, 'nrows': len(rows), 'extra_base': extra_base, 'results': results, 'svg': svg,
        'year': year, 'years': years, 'month': month, 'months': months, 'period': _plabel(chart, year, month), 'pq': _pq(year, month),
        'so': so, 'docctrl': _cc_docctrl(chart.location, chart.activity), 'sop_note': _CC_SOP_NOTE if chart.activity == 'CRM' else '',
        'locked': _year_locked(chart, year, user, month), 'can_review': _can_review(user, chart), 'can_approve': _can_approve(user, chart),
        'can_admin': _is_admin(user), 'can_edit_master': _can_edit_master(user, chart), 'can_set_baseline': _can_set_baseline(user, chart) and not chart.self_limited,
        'today': _date.today().strftime('%Y-%m-%d'), 'baselines': chart.baselines.all(),
        'base_values': ', '.join(_fmt(v, chart.decimals) for v in (b.values if b else [])),
        'month_names': _MONTHS, 'cycle_name': chart.cycle_name,
    })


@_require_POST
def control_chart_cycle(request, pk):
    """Set the first month of the chart's 12-month record cycle (any signed-in
    user, owner decision 08-10-2026). Results keep their dates; they are simply
    re-grouped into the new cycle. Sign-offs of the old cycle years are cleared
    because the records they signed no longer exist in that form."""
    chart = get_object_or_404(ControlChart, pk=pk)
    if not _can_create(request.user):
        return HttpResponse(status=403)
    if chart.period_is_month:
        _msg.info(request, 'Intermediate-check charts are recorded per calendar month; the cycle setting does not apply.')
        return _redirect(f"/qc/control-charts/{pk}/")
    try:
        m = int(request.POST.get('start_month'))
        if not 1 <= m <= 12:
            raise ValueError
    except Exception:
        return HttpResponse('start_month 1-12 required', status=400)
    if m == chart.sm:
        return _redirect(f"/qc/control-charts/{pk}/")
    if ControlChartSignoff.objects.filter(chart=chart, approved_at__isnull=False).exists() and not _can_approve(request.user, chart):
        _msg.error(request, 'This chart has approved (locked) records; only an administrator can change its cycle.')
        return _redirect(f"/qc/control-charts/{pk}/")
    chart.start_month = m
    chart.save()
    n = ControlChartSignoff.objects.filter(chart=chart, month=0).exclude(reviewed_at=None, approved_at=None).count()
    ControlChartSignoff.objects.filter(chart=chart, month=0).delete()
    _msg.success(request, 'Record cycle set to %s. Existing results were re-grouped into the new cycle%s.' % (
        chart.cycle_name, ('; %d sign-off(s) of the old cycle were cleared and must be redone' % n) if n else ''))
    return _redirect(f"/qc/control-charts/{pk}/?year={chart.cycle_of(_date.today())}")


# ---------------------------------------------------------------- results
@_require_POST
def control_chart_result_save(request, pk):
    chart = get_object_or_404(ControlChart, pk=pk)
    user = request.user
    try:
        d = _dt.strptime(request.POST.get('date', ''), '%Y-%m-%d').date()
        value = float(str(request.POST.get('value', '')).replace(',', '').strip())
        if not _math.isfinite(value) or value < 0:
            raise ValueError('not a valid concentration')
    except Exception:
        _msg.error(request, 'Date and a non-negative numeric result are required.')
        return _redirect('control_chart_detail', pk=pk)
    if d > _date.today() or d.year < 2000:
        _msg.error(request, 'The result date must be between 01-01-2000 and today.')
        return _redirect(f"/qc/control-charts/{pk}/")
    py, pm = _qs_period(chart, d)
    plabel = _plabel(chart, py, pm)
    if _year_locked(chart, py, user, pm):
        _msg.error(request, 'Results for %s are approved and locked. Ask an administrator to unapprove them.' % plabel)
        return _redirect(f"/qc/control-charts/{pk}/{_pq(py, pm)}")
    rid = request.POST.get('result_id')
    r = get_object_or_404(ControlChartResult, pk=rid, chart=chart) if rid else None
    if r is None:
        if chart.cadence == 'monthly' and ControlChartResult.objects.filter(chart=chart, date__year=d.year, date__month=d.month).exists():
            _msg.error(request, 'A result for %s %d already exists - edit it instead.' % (_MONTHS[d.month - 1], d.year))
            return _redirect(f"/qc/control-charts/{pk}/{_pq(py, pm)}")
        if chart.cadence != 'monthly' and ControlChartResult.objects.filter(chart=chart, date=d).exists():
            _msg.error(request, 'A result dated %s already exists - edit it instead.' % d.strftime('%d-%m-%Y'))
            return _redirect(f"/qc/control-charts/{pk}/{_pq(py, pm)}")
    b = chart.current_baseline()
    if chart.self_limited:
        # IC: limits come from the run itself, including this reading
        others = [x.value for x in _period_results(chart, py, pm) if not (r and x.pk == r.pk)]
        lim = run_limits(others + [value])
        status = classify_value(lim, value)
        if r is not None and _qs_period(chart, r.date) != (py, pm):
            old_py, old_pm = _qs_period(chart, r.date)
        else:
            old_py = old_pm = None
    else:
        status = b.classify(value) if b else 'ok'
        old_py = old_pm = None
    remark = (request.POST.get('remark') or '').strip()
    if status != 'ok' and not remark:
        _msg.error(request, 'This result is %s - a remark / corrective action is required before it can be saved.' % (
            'OUT OF CONTROL (beyond +/-3 SD)' if status == 'ooc' else 'a WARNING (beyond +/-2 SD)'))
        return _redirect(f"/qc/control-charts/{pk}/{_pq(py, pm)}&date={d.isoformat()}&value={value}")
    if r is not None:
        r.date, r.value, r.status, r.remark, r.baseline = d, value, status, remark, (None if chart.self_limited else b)
        r.save()
        _msg.success(request, 'Result updated (%s).' % r.get_status_display())
    else:
        r = ControlChartResult.objects.create(chart=chart, baseline=(None if chart.self_limited else b), date=d, value=value, status=status,
                                              remark=remark, performed_by=user if user.is_authenticated else None)
        _msg.success(request, 'Result recorded (%s).' % r.get_status_display())
    if chart.self_limited:
        _restatus_run(chart, py, pm)
        if old_py:
            _restatus_run(chart, old_py, old_pm)
    # a content change after review/approval clears the sign-off (superuser edits included)
    for sy, sm in {(py, pm), (old_py, old_pm)} - {(None, None)}:
        so = _signoff(chart, sy, sm)
        if so and (so.reviewed_at or so.approved_at):
            so.reviewed_by = so.approved_by = None
            so.reviewed_at = so.approved_at = None
            so.save()
            _msg.warning(request, 'Review/approval for %s was cleared because a result changed.' % _plabel(chart, sy, sm))
    return _redirect(f"/qc/control-charts/{pk}/{_pq(py, pm)}")


@_require_POST
def control_chart_result_delete(request, pk, rid):
    chart = get_object_or_404(ControlChart, pk=pk)
    r = get_object_or_404(ControlChartResult, pk=rid, chart=chart)
    if not _can_approve(request.user, chart):
        return HttpResponse('Only an administrator can delete a recorded result.', status=403)
    py, pm = _qs_period(chart, r.date)
    r.delete()
    if chart.self_limited:
        _restatus_run(chart, py, pm)
    _msg.success(request, 'Result deleted.')
    return _redirect(f"/qc/control-charts/{pk}/{_pq(py, pm)}")


# ---------------------------------------------------------------- sign-off
@_require_POST
def control_chart_signoff(request, pk):
    chart = get_object_or_404(ControlChart, pk=pk)
    user = request.user
    try:
        year = int(request.POST.get('year'))
        month = int(request.POST.get('month') or 0) if chart.period_is_month else 0
        if chart.period_is_month and not (1 <= month <= 12):
            raise ValueError('month')
    except Exception:
        return HttpResponse('year (and month for intermediate checks) required', status=400)
    action = request.POST.get('action')
    if action not in ('review', 'approve', 'unapprove', 'unreview'):
        return HttpResponse('unknown action', status=400)
    plabel = _plabel(chart, year, month)
    back = f"/qc/control-charts/{pk}/{_pq(year, month)}"
    so = _signoff(chart, year, month)
    if action in ('review', 'unreview') and so and so.approved_at:
        _msg.error(request, 'The %s record is approved and locked - unapprove it before changing the review.' % plabel)
        return _redirect(back)
    if so is None:
        so = ControlChartSignoff(chart=chart, year=year, month=month)
    if action == 'review':
        if not _can_review(user, chart):
            return HttpResponse('Review is reserved for the QC Manager of the %s laboratory.' % chart.location, status=403)
        if not _period_results(chart, year, month):
            _msg.error(request, 'There are no %s results to review yet.' % plabel)
            return _redirect(back)
        so.reviewed_by, so.reviewed_at = user, _tz.now()
    elif action == 'approve':
        if not _can_approve(user, chart):
            return HttpResponse('Approval of %s laboratory charts is reserved for an administrator of that laboratory.' % chart.location, status=403)
        if not so.reviewed_at:
            _msg.error(request, 'The record must be reviewed before it can be approved.')
            return _redirect(back)
        so.approved_by, so.approved_at = user, _tz.now()
    elif action == 'unapprove':
        if not _can_approve(user, chart):
            return HttpResponse('Only an administrator can unapprove.', status=403)
        so.approved_by, so.approved_at = None, None
    elif action == 'unreview':
        if not _can_review(user, chart):
            return HttpResponse(status=403)
        so.reviewed_by, so.reviewed_at = None, None
        so.approved_by, so.approved_at = None, None
    so.save()
    _msg.success(request, 'Sign-off updated.')
    return _redirect(back)


# ---------------------------------------------------------------- baseline (admin)
def control_chart_baseline(request, pk):
    chart = get_object_or_404(ControlChart, pk=pk)
    if chart.self_limited:
        _msg.info(request, 'Intermediate-check charts have no separate baseline: the limits of each monthly run are computed from its own readings.')
        return _redirect(f"/qc/control-charts/{pk}/")
    if not _can_set_baseline(request.user, chart):
        return HttpResponse('Baselines are maintained by an administrator (the chemist who created a chart may set its first baseline).', status=403)
    cur = chart.current_baseline()
    if request.method == 'POST':
        raw = request.POST.get('values', '')
        vals = []
        for tok in raw.replace('\n', ',').replace(';', ',').split(','):
            tok = tok.strip()
            if tok:
                try:
                    vals.append(float(tok))
                except ValueError:
                    _msg.error(request, 'Not a number: %r' % tok)
                    return _redirect('control_chart_baseline', pk=pk)
        if len(vals) < 3:
            _msg.error(request, 'At least 3 baseline values are required.')
            return _redirect('control_chart_baseline', pk=pk)
        try:
            est = _dt.strptime(request.POST.get('established_on', ''), '%Y-%m-%d').date()
        except Exception:
            est = _date.today()
        chart.baselines.update(is_current=False)
        b = ControlChartBaseline(chart=chart, version=(cur.version + 1 if cur else 1), established_on=est,
                                 note=(request.POST.get('note') or '').strip()[:300], values=vals, is_current=True,
                                 created_by=request.user)
        b.compute(); b.save()
        _msg.success(request, 'Baseline v%d established (n=%d, mean %s, SD %s). Earlier results keep the baseline they were judged against.' % (
            b.version, b.n, _fmt(b.mean, chart.decimals), _fmt(b.sd, chart.decimals + 1)))
        return _redirect(f"/qc/control-charts/{pk}/")
    return render(request, 'control_chart_baseline.html', {
        'chart': chart, 'cur': cur, 'baselines': chart.baselines.all(), 'today': _date.today().strftime('%Y-%m-%d'),
        'cur_values': ', '.join(_fmt(v, chart.decimals) for v in (cur.values if cur else []))})


# ---------------------------------------------------------------- chart master (admin)
_CC_FIELDS = ['location', 'activity', 'parameter', 'level', 'unit', 'equipment', 'equipment_id', 'method',
              'crm_detail', 'crm_value', 'crm_range_low', 'crm_range_high', 'description', 'decimals']


def control_chart_edit(request, pk=None):
    chart = get_object_or_404(ControlChart, pk=pk) if pk else None
    if chart is None:
        if not _can_create(request.user):
            return HttpResponse('Please sign in to add a control chart.', status=403)
    elif not _can_edit_master(request.user, chart):
        return HttpResponse('Chart masters are maintained by an administrator once results have been recorded.', status=403)
    if request.method == 'POST':
        data = {f: (request.POST.get(f) or '').strip() for f in _CC_FIELDS}
        try:
            data['decimals'] = max(0, min(6, int(data['decimals'] or 3)))
        except ValueError:
            data['decimals'] = 3
        if not data['parameter']:
            _msg.error(request, 'Parameter is required.')
            return _redirect(request.path)
        if chart is None:
            chart = ControlChart(created_by=request.user)
        for f in _CC_FIELDS:
            setattr(chart, f, data[f])
        chart.active = bool(request.POST.get('active', '1' if pk is None else ''))
        try:
            sm = int(request.POST.get('start_month') or chart.start_month or 1)
            chart.start_month = sm if 1 <= sm <= 12 else 1
        except ValueError:
            pass
        chart.save()
        _msg.success(request, 'Chart saved.')
        if chart.current_baseline() is None and not chart.self_limited:
            return _redirect('control_chart_baseline', pk=chart.pk)
        return _redirect(f"/qc/control-charts/{chart.pk}/")
    return render(request, 'control_chart_edit.html', {
        'chart': chart, 'locs': _CC_LOCS, 'activities': ControlChart.ACTIVITIES, 'fields': _CC_FIELDS, 'month_names': _MONTHS})


# ---------------------------------------------------------------- PDF
_SIG_W = 62.0          # three signature panels across the 190 mm text width
_FOOT_TOP = 270.0      # top of the footer band (footer draws at h-20 = 277; keep 7 mm air)


def _sig_image(user):
    """Path of the user's e-signature image, or None."""
    try:
        s = Signatures.objects.filter(user=user).first()
        if s and s.signature and _os_path_exists(s.signature.path):
            return s.signature.path
    except Exception:
        pass
    return None


def _os_path_exists(p):
    import os
    return os.path.exists(p)


def control_chart_pdf(request, pk):
    import os as _os
    chart = get_object_or_404(ControlChart, pk=pk)
    year = _year(request, chart)
    month = _month(request, chart, year)
    b = chart.current_baseline()
    results = _period_results(chart, year, month)
    lim = _limits(chart, b, results)
    rows, extra_base = period_rows(chart, lim, b.values if (b and not chart.self_limited) else [], results, year, month)
    so = _signoff(chart, year, month)
    ctrl = _cc_docctrl(chart.location, chart.activity)
    office = _CC_OFFICE.get(chart.location, _CC_OFFICE['Karachi'])
    plabel = _plabel(chart, year, month)
    ref = chart.ref_label
    _LOGO, _CAL, _CALB = 'static/assets/EnviTechAL LOGO.png', 'static/fonts/calibri.ttf', 'static/fonts/calibrib.ttf'
    approved = bool(so and so.approved_at)
    GREEN, GREY_FILL, LINE = (15, 81, 50), (242, 245, 243), (120, 120, 120)

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
            if not approved:
                self.set_font(self.fam, 'B', 54); self.set_text_color(238, 238, 238)
                try:
                    with self.rotation(45, self.w / 2, self.h / 2):
                        self.text(self.w / 2 - self.get_string_width('NOT APPROVED') / 2, self.h / 2 + 10, 'NOT APPROVED')
                except Exception:
                    pass
                self.set_text_color(0, 0, 0)
            if _os.path.exists(_LOGO):
                try:
                    self.image(_LOGO, 10, 8, 20, 22)
                except Exception:
                    pass
            # Document-control box: sized to its text, flush with the right margin (x = 200)
            lines = ['Doc. No: %s' % ctrl['doc_no'], 'Issue Date: %s' % ctrl['issue_date'],
                     'Issue No. %s    Rev. No. %s' % (ctrl['issue_no'], ctrl['rev_no']), 'Page No: %d of {nb}' % self.page_no()]
            self.set_font(self.fam, '', 7)
            bw = max(self.get_string_width(l.replace('{nb}', '99')) for l in lines) + 5.0
            bx, by, lh = 200.0 - bw, 8.0, 4.4
            self.set_draw_color(*LINE); self.set_fill_color(*GREY_FILL)
            self.rect(bx, by, bw, lh * len(lines) + 1.6, 'DF')
            for i, l in enumerate(lines):
                self.set_xy(bx + 2.0, by + 0.8 + i * lh); self.cell(bw - 4.0, lh, l, 0, 0, 'L')
            # Title block centred on the page (logo at left, control box at right stay clear of it)
            self.set_text_color(*GREEN)
            self.set_xy(10, 8.5); self.set_font(self.fam, 'B', 15); self.cell(190, 7, 'ENVI TECH AL', align='C', ln=1)
            self.set_x(10); self.set_font(self.fam, '', 8); self.set_text_color(70, 70, 70)
            self.cell(190, 4.5, 'Analytical Laboratory - Environmental & Water Testing', align='C', ln=1)
            self.set_x(10); self.set_font(self.fam, 'B', 10.5); self.set_text_color(0, 0, 0)
            self.cell(190, 5.5, 'CONTROL CHARTS (For Quality Control Activities)', align='C', ln=1)
            self.set_x(10); self.set_font(self.fam, 'B', 8.5); self.set_text_color(*GREEN)
            self.cell(190, 4.5, '%s LABORATORY  -  %s  -  %s' % (chart.location.upper(), chart.activity_short.upper(), plabel), align='C', ln=1)
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
    dec = chart.decimals
    unit = (' %s' % chart.unit) if chart.unit else ''

    # ---- header grid: fixed column widths so every label/value edge lines up
    L1, V1, L2, V2 = 30.0, 80.0, 28.0, 52.0      # = 190
    pdf.set_draw_color(*LINE)

    def kv_row(items, h=5.4):
        """items: list of (label, value, label_w, value_w)."""
        for lbl, val, wl, wv in items:
            pdf.set_font(f, 'B', 7.8); pdf.set_fill_color(*GREY_FILL)
            pdf.cell(wl, h, lbl, 1, 0, 'L', fill=True)
            pdf.set_font(f, '', 8)
            txt = str(val) if val not in (None, '') else '-'
            while pdf.get_string_width(txt) > wv - 2 and len(txt) > 4:
                txt = txt[:-2]
            pdf.cell(wv, h, txt, 1, 0, 'L')
        pdf.ln(h)

    kv_row([('Name of Equipment', chart.equipment, L1, V1), ('Equipment ID', chart.equipment_id, L2, V2)])
    kv_row([('Parameter', chart.title, L1, V1), ('Method', chart.method, L2, V2)])
    kv_row([('%s Detail' % ref, chart.crm_detail, L1, V1), ('Activity', chart.activity_short, L2, V2)])
    if chart.self_limited:
        lim_txt = ('run n=%d, mean %s, SD %s' % (lim['n'], _fmt(lim['mean'], dec), _fmt(lim['sd'], dec + 1))) if lim else 'fewer than 2 readings'
        kv_row([('%s Value' % ref, (chart.crm_value + unit) if chart.crm_value else '', L1, 36.0),
                ('Range', (chart.crm_range + unit) if chart.crm_range else '', 20.0, 24.0),
                ('Limits', lim_txt, L2, V2)])
    else:
        kv_row([('%s Certified Value' % ref, (chart.crm_value + unit) if chart.crm_value else '', L1, 36.0),
                ('%s Range' % ref, (chart.crm_range + unit) if chart.crm_range else '', 20.0, 24.0),
                ('Baseline', ('v%d  (n = %d, established %s)' % (b.version, b.n, b.established_on.strftime('%d-%m-%Y') if b.established_on else '-')) if b else 'not established', L2, V2)])
    kv_row([('Description', chart.description, L1, 160.0)])
    pdf.ln(2.5)

    # ---- results table
    rl = {'RM': 'Weekly RM\nResult%s', 'IC': 'Reading%s'}.get(chart.activity, 'Monthly CRM\nResult%s') % unit
    if chart.self_limited:
        cols = [('S. No.', 11), ('Date', 27), (rl, 30), ('UL (+3 SD)', 20.5), ('UWL (+2 SD)', 20.5), ('LWL (-2 SD)', 20.5),
                ('LL (-3 SD)', 20.5), ('Run\nMean', 20), ('Run\nSD', 20)]
    else:
        cols = [('S. No.', 11), ('Date', 21), (rl, 24), ('Baseline\nResult%s' % unit, 24), ('UL (+3 SD)', 18.5),
                ('UWL (+2 SD)', 18.5), ('LWL (-2 SD)', 18.5), ('LL (-3 SD)', 18.5), ('Baseline\nMean', 18), ('Baseline\nSD', 18)]
    pdf.set_font(f, 'B', 7); pdf.set_fill_color(*GREEN); pdf.set_text_color(255, 255, 255)
    x0, y0 = pdf.get_x(), pdf.get_y()
    for lbl, w in cols:
        x = pdf.get_x(); pdf.set_xy(x, y0)
        pdf.multi_cell(w, 4, lbl if '\n' in lbl else '\n' + lbl, 1, 'C', fill=True); pdf.set_xy(x + w, y0)
    pdf.set_xy(x0, y0 + 8); pdf.set_text_color(0, 0, 0)
    pdf.set_font(f, '', 7.5)
    RH = 4.5
    if chart.self_limited:
        all_rows = [[str(r['sno']), r['date'], r['value'], r['ul'], r['uwl'], r['lwl'], r['ll'], r['mean'], r['sd'], r['status']] for r in rows]
    else:
        all_rows = [[str(r['sno']), r['date'] or r['month'], r['value'], r['base'], r['ul'], r['uwl'], r['lwl'], r['ll'], r['mean'], r['sd'], r['status']] for r in rows]
        for i, v in enumerate(extra_base):
            all_rows.append([str(len(rows) + 1 + i), '-', '', v, '', '', '', '', '', '', ''])
    ncol = len(cols)
    for i, vals in enumerate(all_rows):
        st = vals[-1]
        if st == 'ooc':
            pdf.set_fill_color(254, 226, 226); pdf.set_text_color(153, 27, 27)
        elif st == 'warning':
            pdf.set_fill_color(254, 249, 195); pdf.set_text_color(133, 77, 14)
        else:
            pdf.set_fill_color(*(GREY_FILL if i % 2 else (255, 255, 255))); pdf.set_text_color(0, 0, 0)
        for j, ((lbl, w), v) in enumerate(zip(cols, vals[:ncol])):
            if j == 2 and v:
                pdf.set_font(f, 'B', 7.5)
            pdf.cell(w, RH, v, 1, 0, 'C', fill=True)
            pdf.set_font(f, '', 7.5)
        pdf.ln(RH)
    pdf.set_text_color(0, 0, 0); pdf.set_fill_color(*GREY_FILL)
    src = 'Run' if chart.self_limited else 'Baseline'
    pdf.set_font(f, 'B', 7.5); pdf.cell(56, RH, 'Mean (%s)' % src, 1, 0, 'R', fill=True)
    pdf.set_font(f, '', 7.5); pdf.cell(134, RH, ('  ' + _fmt(lim['mean'], dec)) if lim else '', 1, 1, 'L')
    pdf.set_font(f, 'B', 7.5); pdf.cell(56, RH, 'Standard Deviation (%s)' % src, 1, 0, 'R', fill=True)
    pdf.set_font(f, '', 7.5); pdf.cell(134, RH, ('  ' + _fmt(lim['sd'], dec + 1)) if lim else '', 1, 1, 'L')

    # ---- chart (width-limited so the whole form stays on one page)
    if lim:
        # size the chart to the space that is left, keeping ~32 mm for the signature block
        n_rem = sum(1 for r in rows if r['remark'])
        reserve = 32.0 + 14.0 + n_rem * 3.8 + (4.2 if n_rem else 0)
        chart_mm = max(62.0, min(100.0, _FOOT_TOP - pdf.get_y() - reserve))
        png = render_chart(chart, lim, results, year, month, 'png', 7.6, round(chart_mm * 7.6 / 176.0, 2))
        import tempfile as _tf
        tmp = _tf.NamedTemporaryFile(suffix='.png', delete=False)
        try:
            tmp.write(png); tmp.close()
            pdf.ln(1.5); pdf.image(tmp.name, x=17, w=176)
        finally:
            try:
                _os.unlink(tmp.name)
            except OSError:
                pass

    # ---- remarks + SOP note
    rem = [(r['date'], r['status'], r['remark']) for r in rows if r['remark']]
    if rem:
        pdf.ln(0.5); pdf.set_font(f, 'B', 7.5); pdf.set_x(10); pdf.cell(0, 4.2, 'Remarks / corrective actions', ln=1); pdf.set_font(f, '', 7.2)
        for d, st, t in rem:
            pdf.set_x(10)
            pdf.multi_cell(190, 3.8, '%s  (%s):  %s' % (d, 'Out of control' if st == 'ooc' else 'Warning' if st == 'warning' else 'Note', t),
                           new_x='LMARGIN', new_y='NEXT')
    note = {'CRM': _CC_SOP_NOTE,
            'RM': 'The baseline results were established from the first twelve RM results of the exercise (procedure ETAL-LAB-P-604); '
                  'the weekly RM results are plotted against this baseline (mean +/- 2 SD warning, +/- 3 SD action).',
            'IC': 'Intermediate check of the equipment (procedure ETAL-LAB-P-604): the readings of the month are plotted against the mean '
                  'and standard deviation of that run (+/- 2 SD warning, +/- 3 SD action).'}.get(chart.activity, '')
    pdf.ln(0.8); pdf.set_font(f, '', 6.8); pdf.set_text_color(60, 60, 60); pdf.set_x(10)
    pdf.multi_cell(190, 3.4, note, new_x='LMARGIN', new_y='NEXT'); pdf.set_text_color(0, 0, 0)

    # ---- e-signature block: fills whatever remains above the footer (min 24 mm)
    MIN_H, MAX_H = 24.0, 46.0
    top = pdf.get_y() + 2.5
    avail = _FOOT_TOP - top
    if avail < MIN_H:
        pdf.add_page(); top = pdf.get_y() + 2; avail = _FOOT_TOP - top
    blk_h = max(MIN_H, min(MAX_H, avail))
    top = _FOOT_TOP - blk_h                      # anchor the block to the footer
    pdf.set_auto_page_break(False)               # the block is positioned absolutely
    performed_users = []
    for r in results:
        if r.performed_by and r.performed_by not in performed_users:
            performed_users.append(r.performed_by)
    perf_names = ', '.join(_uname(u) for u in performed_users)
    perf_sig = _sig_image(performed_users[0]) if len(performed_users) == 1 else None
    perf_when = max((r.performed_at for r in results if r.performed_by), default=None)
    panels = [('Performed By', '(Chemist)', perf_names, perf_sig, perf_when),
              ('Reviewed By', '(QC Manager)', _uname(so.reviewed_by) if so and so.reviewed_at else '',
               _sig_image(so.reviewed_by) if so and so.reviewed_at else None, so.reviewed_at if so and so.reviewed_at else None),
              ('Approved By', '(CEO)', _uname(so.approved_by) if approved else '',
               _sig_image(so.approved_by) if approved else None, so.approved_at if approved else None)]
    LBL_H, NAME_H, ROLE_H = 5.0, 4.6, 4.0
    img_h = blk_h - LBL_H - NAME_H - ROLE_H - 2.0
    pdf.set_draw_color(*LINE)
    for i, (lbl, role, who, sig, when) in enumerate(panels):
        x = 10 + i * (_SIG_W + 2.0)
        pdf.rect(x, top, _SIG_W, blk_h)
        pdf.set_fill_color(*GREY_FILL); pdf.rect(x, top, _SIG_W, LBL_H, 'F')
        pdf.set_xy(x, top); pdf.set_font(f, 'B', 8); pdf.cell(_SIG_W, LBL_H, lbl, 0, 0, 'C')
        iy = top + LBL_H + 1.0
        if sig:
            try:
                from PIL import Image as _Im
                with _Im.open(sig) as im:
                    iw, ih = im.size
                w = _SIG_W - 8; h = w * ih / iw
                if h > img_h:
                    h = img_h; w = h * iw / ih
                pdf.image(sig, x + (_SIG_W - w) / 2, iy + (img_h - h) / 2, w, h)
            except Exception:
                sig = None
        if not sig and who:
            pdf.set_xy(x, iy + img_h / 2 - 2); pdf.set_font(f, '', 6.5); pdf.set_text_color(110, 110, 110)
            pdf.cell(_SIG_W, 4, 'Electronically signed', 0, 0, 'C'); pdf.set_text_color(0, 0, 0)
        ny = top + LBL_H + 1.0 + img_h + 0.5
        pdf.line(x + 4, ny, x + _SIG_W - 4, ny)
        pdf.set_xy(x, ny); pdf.set_font(f, 'B', 7.8)
        nm = who or ''
        while pdf.get_string_width(nm) > _SIG_W - 4 and len(nm) > 3:
            nm = nm[:-2]
        pdf.cell(_SIG_W, NAME_H, nm, 0, 0, 'C')
        pdf.set_xy(x, ny + NAME_H); pdf.set_font(f, '', 6.8); pdf.set_text_color(70, 70, 70)
        pdf.cell(_SIG_W, ROLE_H, role + (('   ' + _tz.localtime(when).strftime('%d-%m-%Y %H:%M')) if when else ''), 0, 0, 'C')
        pdf.set_text_color(0, 0, 0)
    pdf.set_draw_color(0, 0, 0)

    out = pdf.output(dest='S')
    data = bytes(out) if not isinstance(out, str) else out.encode('latin-1')
    resp = HttpResponse(data, content_type='application/pdf')
    resp['Content-Disposition'] = 'inline; filename="ControlChart_%s_%s_%s_%s_%s.pdf"' % (
        chart.location, chart.activity, chart.parameter.replace(' ', '_'), chart.equipment_id or 'NA', plabel.replace('-', '_'))
    return resp
