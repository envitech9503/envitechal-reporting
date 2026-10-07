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

from QC.models import ControlChart, ControlChartBaseline, ControlChartResult, ControlChartSignoff, ControlChartReviewer
from QC.control_chart_render import render_chart, month_rows, fmt as _fmt, MONTHS as _MONTHS

_CC_LOCS = ['Karachi', 'Lahore']
_CC_FORM = {'doc_no': 'ETAL-LAB-604-FF-11', 'issue_date': '19-03-2022', 'issue_no': '01', 'rev_no': '00'}
_CC_SOP_NOTE = ('The baseline results were established using data from the February intermediate check '
                'activity, as per the procedure ETAL-LAB-P-604 (two intermediate check activities are planned: '
                'one after calibration and the other before PT). Accordingly, the results from the February '
                'activity (conducted before PT) were used to establish the baseline, and the monthly results '
                'are plotted against this baseline.')


def _cc_docctrl(location):
    try:
        obj, _ = InventoryDocControl.objects.get_or_create(
            module='control_chart', location=location,
            defaults={'doc_no': _CC_FORM['doc_no'], 'issue_date': _CC_FORM['issue_date'],
                      'issue_no': _CC_FORM['issue_no'], 'rev_no': _CC_FORM['rev_no']})
        return {'doc_no': obj.doc_no or _CC_FORM['doc_no'], 'issue_date': obj.issue_date or _CC_FORM['issue_date'],
                'issue_no': obj.issue_no or '01', 'rev_no': obj.rev_no or '00'}
    except Exception:
        return dict(_CC_FORM)


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


def _year(request):
    try:
        return int(request.GET.get('year') or _date.today().year)
    except Exception:
        return _date.today().year


def _signoff(chart, year):
    return ControlChartSignoff.objects.filter(chart=chart, year=year).first()


def _year_locked(chart, year, user):
    so = _signoff(chart, year)
    return bool(so and so.locked and not _can_approve(user, chart))


# ---------------------------------------------------------------- list
def control_chart_list(request):
    loc = request.GET.get('location') or _default_loc(request)
    if loc not in _CC_LOCS:
        loc = 'Karachi'
    if request.session.get('cc_loc') != loc:
        request.session['cc_loc'] = loc
    q = (request.GET.get('q') or '').strip()
    year = _year(request)
    qs = ControlChart.objects.filter(active=True, location=loc)
    if q:
        qs = qs.filter(_Q(parameter__icontains=q) | _Q(equipment__icontains=q) | _Q(equipment_id__icontains=q)
                       | _Q(method__icontains=q) | _Q(level__icontains=q))
    charts = list(qs)
    ids = [c.id for c in charts]
    res = {}
    for r in ControlChartResult.objects.filter(chart_id__in=ids, date__year=year).order_by('date'):
        res.setdefault(r.chart_id, []).append(r)
    sos = {s.chart_id: s for s in ControlChartSignoff.objects.filter(chart_id__in=ids, year=year)}
    rows = []
    for c in charts:
        rr = res.get(c.id, [])
        b = c.current_baseline()
        last = rr[-1] if rr else None
        worst = 'ooc' if any(r.status == 'ooc' for r in rr) else ('warning' if any(r.status == 'warning' for r in rr) else ('ok' if rr else 'none'))
        so = sos.get(c.id)
        rows.append({'c': c, 'n': len(rr), 'last': last, 'last_value': _fmt(last.value, c.decimals) if last else '',
                     'worst': worst, 'mean': _fmt(b.mean, c.decimals) if b else '', 'sd': _fmt(b.sd, c.decimals + 1) if b else '',
                     'bver': b.version if b else '', 'reviewed': bool(so and so.reviewed_at), 'approved': bool(so and so.approved_at)})
    years = sorted({d.year for d in ControlChartResult.objects.values_list('date', flat=True)} | {_date.today().year}, reverse=True)
    return render(request, 'control_chart_list.html', {
        'rows': rows, 'loc': loc, 'locs': _CC_LOCS, 'q': q, 'year': year, 'years': years,
        'can_admin': _is_admin(request.user), 'count': len(rows)})


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
    charts = {c.id: c for c in ControlChart.objects.all()}
    pairs = set()
    stats = {}
    for cid, d, st in ControlChartResult.objects.values_list('chart_id', 'date', 'status'):
        pairs.add((cid, d.year))
        s = stats.setdefault((cid, d.year), {'n': 0, 'warning': 0, 'ooc': 0, 'last': None})
        s['n'] += 1
        if st in ('warning', 'ooc'):
            s[st] += 1
        if s['last'] is None or d > s['last']:
            s['last'] = d
    sos = {}
    for so in ControlChartSignoff.objects.select_related('reviewed_by', 'approved_by'):
        pairs.add((so.chart_id, so.year))
        sos[(so.chart_id, so.year)] = so
    rows = []
    for cid, y in pairs:
        c = charts.get(cid)
        if not c:
            continue
        if loc in _CC_LOCS and c.location != loc:
            continue
        if ystr != 'All' and str(y) != ystr:
            continue
        if q and not any(q.lower() in (v or '').lower() for v in (c.parameter, c.level, c.equipment, c.equipment_id, c.method)):
            continue
        s = stats.get((cid, y), {'n': 0, 'warning': 0, 'ooc': 0, 'last': None})
        worst = 'ooc' if s['ooc'] else ('warning' if s['warning'] else ('ok' if s['n'] else 'none'))
        if status_f != 'All' and worst != status_f:
            continue
        so = sos.get((cid, y))
        sign = 'approved' if (so and so.approved_at) else ('reviewed' if (so and so.reviewed_at) else 'open')
        if sign_f != 'All' and sign != sign_f:
            continue
        rows.append({'c': c, 'year': y, 'n': s['n'], 'warn': s['warning'], 'ooc': s['ooc'], 'last': s['last'],
                     'worst': worst, 'sign': sign, 'so': so})
    rows.sort(key=lambda r: (-r['year'], r['c'].location, r['c'].parameter.lower(), r['c'].level))
    years = sorted({y for _, y in pairs}, reverse=True)
    return render(request, 'control_chart_archive.html', {
        'rows': rows, 'loc': loc, 'locs': _CC_LOCS, 'q': q, 'year': ystr, 'years': years,
        'status': status_f, 'signoff': sign_f, 'count': len(rows), 'can_admin': _is_admin(request.user)})


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
    year = _year(request)
    b = chart.current_baseline()
    results = list(ControlChartResult.objects.filter(chart=chart, date__year=year).order_by('date', 'id'))
    rows, extra_base = month_rows(chart, b, results, year)
    lim = b.limits() if b else None
    svg = render_chart(chart, b, results, year, 'svg').decode('utf-8') if b else ''
    so = _signoff(chart, year)
    user = request.user
    lim_f = {k: _fmt(v, chart.decimals) for k, v in (lim or {}).items()}
    if lim:
        lim_f['sd'] = _fmt(lim['sd'], chart.decimals + 1)
    years = sorted({d.year for d in ControlChartResult.objects.filter(chart=chart).values_list('date', flat=True)} | {_date.today().year}, reverse=True)
    return render(request, 'control_chart_detail.html', {
        'chart': chart, 'b': b, 'lim': lim_f, 'rows': rows, 'extra_base': extra_base, 'results': results, 'svg': svg,
        'year': year, 'years': years, 'so': so, 'docctrl': _cc_docctrl(chart.location), 'sop_note': _CC_SOP_NOTE,
        'locked': _year_locked(chart, year, user), 'can_review': _can_review(user, chart), 'can_approve': _can_approve(user, chart),
        'can_admin': _is_admin(user),
        'today': _date.today().strftime('%Y-%m-%d'), 'baselines': chart.baselines.all(),
        'base_values': ', '.join(_fmt(v, chart.decimals) for v in (b.values if b else [])),
    })


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
        return _redirect(f"/qc/control-charts/{pk}/?year={_date.today().year}")
    if _year_locked(chart, d.year, user):
        _msg.error(request, 'Results for %d are approved and locked. Ask an administrator to unapprove them.' % d.year)
        return _redirect(f"{request.path.rsplit('/result/', 1)[0]}/?year={d.year}")
    b = chart.current_baseline()
    status = b.classify(value) if b else 'ok'
    remark = (request.POST.get('remark') or '').strip()
    if status != 'ok' and not remark:
        _msg.error(request, 'This result is %s - a remark / corrective action is required before it can be saved.' % (
            'OUT OF CONTROL (beyond +/-3 SD)' if status == 'ooc' else 'a WARNING (beyond +/-2 SD)'))
        return _redirect(f"/qc/control-charts/{pk}/?year={d.year}&date={d.isoformat()}&value={value}")
    rid = request.POST.get('result_id')
    if rid:
        r = get_object_or_404(ControlChartResult, pk=rid, chart=chart)
        r.date, r.value, r.status, r.remark, r.baseline = d, value, status, remark, b
        r.save()
        _msg.success(request, 'Result updated (%s).' % r.get_status_display())
    else:
        if ControlChartResult.objects.filter(chart=chart, date__year=d.year, date__month=d.month).exists():
            _msg.error(request, 'A result for %s %d already exists - edit it instead.' % (_MONTHS[d.month - 1], d.year))
            return _redirect(f"/qc/control-charts/{pk}/?year={d.year}")
        r = ControlChartResult.objects.create(chart=chart, baseline=b, date=d, value=value, status=status,
                                              remark=remark, performed_by=user if user.is_authenticated else None)
        _msg.success(request, 'Result recorded (%s).' % r.get_status_display())
    # a content change after review/approval clears the sign-off (superuser edits included)
    so = _signoff(chart, d.year)
    if so and (so.reviewed_at or so.approved_at):
        so.reviewed_by = so.approved_by = None
        so.reviewed_at = so.approved_at = None
        so.save()
        _msg.warning(request, 'Review/approval for %d was cleared because a result changed.' % d.year)
    return _redirect(f"/qc/control-charts/{pk}/?year={d.year}")


@_require_POST
def control_chart_result_delete(request, pk, rid):
    chart = get_object_or_404(ControlChart, pk=pk)
    r = get_object_or_404(ControlChartResult, pk=rid, chart=chart)
    if not _can_approve(request.user, chart):
        return HttpResponse('Only an administrator can delete a recorded result.', status=403)
    y = r.date.year
    r.delete()
    _msg.success(request, 'Result deleted.')
    return _redirect(f"/qc/control-charts/{pk}/?year={y}")


# ---------------------------------------------------------------- sign-off
@_require_POST
def control_chart_signoff(request, pk):
    chart = get_object_or_404(ControlChart, pk=pk)
    user = request.user
    try:
        year = int(request.POST.get('year'))
    except Exception:
        return HttpResponse('year required', status=400)
    action = request.POST.get('action')
    if action not in ('review', 'approve', 'unapprove', 'unreview'):
        return HttpResponse('unknown action', status=400)
    so = _signoff(chart, year)
    if action in ('review', 'unreview') and so and so.approved_at:
        _msg.error(request, 'The %d record is approved and locked - unapprove it before changing the review.' % year)
        return _redirect(f"/qc/control-charts/{pk}/?year={year}")
    if so is None:
        so = ControlChartSignoff(chart=chart, year=year)
    if action == 'review':
        if not _can_review(user, chart):
            return HttpResponse('Review is reserved for the QC Manager of the %s laboratory.' % chart.location, status=403)
        if not ControlChartResult.objects.filter(chart=chart, date__year=year).exists():
            _msg.error(request, 'There are no %d results to review yet.' % year)
            return _redirect(f"/qc/control-charts/{pk}/?year={year}")
        so.reviewed_by, so.reviewed_at = user, _tz.now()
    elif action == 'approve':
        if not _can_approve(user, chart):
            return HttpResponse('Approval of %s laboratory charts is reserved for an administrator of that laboratory.' % chart.location, status=403)
        if not so.reviewed_at:
            _msg.error(request, 'The year must be reviewed before it can be approved.')
            return _redirect(f"/qc/control-charts/{pk}/?year={year}")
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
    return _redirect(f"/qc/control-charts/{pk}/?year={year}")


# ---------------------------------------------------------------- baseline (admin)
def control_chart_baseline(request, pk):
    chart = get_object_or_404(ControlChart, pk=pk)
    if not _is_admin(request.user):
        return HttpResponse('Baselines are maintained by an administrator.', status=403)
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
    if not _is_admin(request.user):
        return HttpResponse('Chart masters are maintained by an administrator.', status=403)
    chart = get_object_or_404(ControlChart, pk=pk) if pk else None
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
        chart.save()
        _msg.success(request, 'Chart saved.')
        if chart.current_baseline() is None:
            return _redirect('control_chart_baseline', pk=chart.pk)
        return _redirect(f"/qc/control-charts/{chart.pk}/")
    return render(request, 'control_chart_edit.html', {
        'chart': chart, 'locs': _CC_LOCS, 'activities': ControlChart.ACTIVITIES, 'fields': _CC_FIELDS})


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
    year = _year(request)
    b = chart.current_baseline()
    results = list(ControlChartResult.objects.filter(chart=chart, date__year=year).order_by('date', 'id'))
    rows, extra_base = month_rows(chart, b, results, year)
    lim = b.limits() if b else None
    so = _signoff(chart, year)
    ctrl = _cc_docctrl(chart.location)
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
            self.cell(190, 4.5, '%s LABORATORY  -  %d' % (chart.location.upper(), year), align='C', ln=1)
            self.set_text_color(0, 0, 0)
            self.set_draw_color(*GREEN); self.set_line_width(0.5); self.line(10, 33, 200, 33)
            self.set_line_width(0.2); self.set_draw_color(0, 0, 0); self.set_y(36.5)

        def footer(self):
            self.set_y(-20); self.set_font(self.fam, '', 6.5); self.set_text_color(90, 90, 90)
            self.cell(0, 4, 'ENVI TECH AL  -  Controlled document.  Uncontrolled when printed.', align='C', ln=1)
            self.set_text_color(0, 0, 0); self.set_draw_color(*GREEN); self.set_line_width(0.4)
            yb = self.get_y() + 0.6; self.line(10, yb, 200, yb); self.set_line_width(0.2); self.set_draw_color(0, 0, 0)
            self.set_xy(10, yb + 1.2); self.cell(90, 3.6, 'Tel: +92 310 2288801', align='L')
            self.set_xy(110, yb + 1.2); self.cell(90, 3.6, 'info@envitechal.com   -   www.envitechal.com', align='R')
            self.set_xy(10, yb + 4.8)
            self.cell(0, 3.6, 'Head Office: 345, First Floor, Street-15, Block-3, Bahadurabad, Karachi. 75900, Pakistan.', align='C')

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
    kv_row([('CRM Detail', chart.crm_detail, L1, V1), ('Activity', chart.get_activity_display().split(' (')[0], L2, V2)])
    kv_row([('CRM Certified Value', (chart.crm_value + unit) if chart.crm_value else '', L1, 36.0),
            ('CRM Range', (chart.crm_range + unit) if chart.crm_range else '', 20.0, 24.0),
            ('Baseline', ('v%d  (n = %d, established %s)' % (b.version, b.n, b.established_on.strftime('%d-%m-%Y') if b.established_on else '-')) if b else 'not established', L2, V2)])
    kv_row([('Description', chart.description, L1, 160.0)])
    pdf.ln(2.5)

    # ---- results table
    cols = [('S. No.', 11), ('Date', 21), ('Monthly CRM\nResult%s' % unit, 24), ('Baseline\nResult%s' % unit, 24), ('UL (+3 SD)', 18.5),
            ('UWL (+2 SD)', 18.5), ('LWL (-2 SD)', 18.5), ('LL (-3 SD)', 18.5), ('Baseline\nMean', 18), ('Baseline\nSD', 18)]
    pdf.set_font(f, 'B', 7); pdf.set_fill_color(*GREEN); pdf.set_text_color(255, 255, 255)
    x0, y0 = pdf.get_x(), pdf.get_y()
    for lbl, w in cols:
        x = pdf.get_x(); pdf.set_xy(x, y0)
        pdf.multi_cell(w, 4, lbl if '\n' in lbl else '\n' + lbl, 1, 'C', fill=True); pdf.set_xy(x + w, y0)
    pdf.set_xy(x0, y0 + 8); pdf.set_text_color(0, 0, 0)
    pdf.set_font(f, '', 7.5)
    RH = 4.5
    all_rows = [[str(r['sno']), r['date'] or r['month'], r['value'], r['base'], r['ul'], r['uwl'], r['lwl'], r['ll'], r['mean'], r['sd'], r['status']] for r in rows]
    for i, v in enumerate(extra_base):
        all_rows.append([str(13 + i), '-', '', v, '', '', '', '', '', '', ''])
    for i, vals in enumerate(all_rows):
        st = vals[10]
        if st == 'ooc':
            pdf.set_fill_color(254, 226, 226); pdf.set_text_color(153, 27, 27)
        elif st == 'warning':
            pdf.set_fill_color(254, 249, 195); pdf.set_text_color(133, 77, 14)
        else:
            pdf.set_fill_color(*(GREY_FILL if i % 2 else (255, 255, 255))); pdf.set_text_color(0, 0, 0)
        for j, ((lbl, w), v) in enumerate(zip(cols, vals[:10])):
            if j == 2 and v:
                pdf.set_font(f, 'B', 7.5)
            pdf.cell(w, RH, v, 1, 0, 'C', fill=True)
            pdf.set_font(f, '', 7.5)
        pdf.ln(RH)
    pdf.set_text_color(0, 0, 0); pdf.set_fill_color(*GREY_FILL)
    pdf.set_font(f, 'B', 7.5); pdf.cell(56, RH, 'Mean (Baseline)', 1, 0, 'R', fill=True)
    pdf.set_font(f, '', 7.5); pdf.cell(134, RH, ('  ' + _fmt(lim['mean'], dec)) if lim else '', 1, 1, 'L')
    pdf.set_font(f, 'B', 7.5); pdf.cell(56, RH, 'Standard Deviation (Baseline)', 1, 0, 'R', fill=True)
    pdf.set_font(f, '', 7.5); pdf.cell(134, RH, ('  ' + _fmt(lim['sd'], dec + 1)) if lim else '', 1, 1, 'L')

    # ---- chart (width-limited so the whole form stays on one page)
    if b:
        # size the chart to the space that is left, keeping ~32 mm for the signature block
        n_rem = sum(1 for r in rows if r['remark'])
        reserve = 32.0 + 14.0 + n_rem * 3.8 + (4.2 if n_rem else 0)
        chart_mm = max(62.0, min(100.0, _FOOT_TOP - pdf.get_y() - reserve))
        png = render_chart(chart, b, results, year, 'png', 7.6, round(chart_mm * 7.6 / 176.0, 2))
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
    pdf.ln(0.8); pdf.set_font(f, '', 6.8); pdf.set_text_color(60, 60, 60); pdf.set_x(10)
    pdf.multi_cell(190, 3.4, _CC_SOP_NOTE, new_x='LMARGIN', new_y='NEXT'); pdf.set_text_color(0, 0, 0)

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
    resp['Content-Disposition'] = 'inline; filename="ControlChart_%s_%s_%s_%d.pdf"' % (
        chart.location, chart.parameter.replace(' ', '_'), chart.equipment_id or 'NA', year)
    return resp
