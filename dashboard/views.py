"""EnviTechAL management dashboard - v3 12-07-2026 (fast, cached, executive indicators)."""
import json
from collections import Counter
from datetime import datetime, timedelta
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
from django.core.cache import cache

from EnviTechAlApp.models import (
    DrinkingWaterForm, GaseousEmissionForm, AmbientAirForm, WasteWaterSludge,
    VehiculEmissionForm, LuxAnalysisForm, PackingPolyBagForm, MachineOilForm,
    MicrobialAnalysis, ViscousLiquid, AmbientAir2, WasteWaterForm2, NoiseAnalysis,
    NoiseMonitoring, Calibration, Inspection, Verification,
    Sample_registration, JobCompletionForm, ApprovalStatus)
from detox.models import Detox

REPORT_MODELS = {
    'Drinking Water': DrinkingWaterForm, 'Gaseous Emission': GaseousEmissionForm,
    'Ambient Air': AmbientAirForm, 'Waste Water Sludge': WasteWaterSludge,
    'Vehicular Emission': VehiculEmissionForm, 'Lux Analysis': LuxAnalysisForm,
    'Packing Poly Bag': PackingPolyBagForm, 'Machine Oil': MachineOilForm,
    'Microbial Analysis': MicrobialAnalysis, 'Viscous Liquid': ViscousLiquid,
    'Ambient Air 2': AmbientAir2, 'Waste Water 2': WasteWaterForm2,
    'Noise Analysis': NoiseAnalysis, 'Noise LAeq': NoiseMonitoring, 'Detox': Detox,
}
CERT_MODELS = {'Calibration': Calibration, 'Inspection': Inspection, 'Verification': Verification}
ACTION = {'+': 'Created', '~': 'Edited', '-': 'Deleted'}


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


def _start(filter_type, now):
    if filter_type == 'yearly':
        return now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    if filter_type == 'quarterly':
        qm = 3 * ((now.month - 1) // 3) + 1
        return now.replace(month=qm, day=1, hour=0, minute=0, second=0, microsecond=0)
    return now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def _prev_range(filter_type, now):
    cur = _start(filter_type, now)
    if filter_type == 'yearly':
        prev = cur.replace(year=cur.year - 1)
    elif filter_type == 'quarterly':
        m = cur.month - 3
        prev = cur.replace(year=cur.year - 1, month=m + 12) if m < 1 else cur.replace(month=m)
    else:
        m = cur.month - 1
        prev = cur.replace(year=cur.year - 1, month=12) if m < 1 else cur.replace(month=m)
    return Q(created_at__range=[prev, cur])


def _count_group(models, q):
    total = 0
    for model in models:
        try: total += model.objects.filter(q).count()
        except Exception: continue
    return total


def _parse_rec(v):
    """Receipt dates are free text, e.g. '02/12/2023 , 04:32 pm', '14-Dec-2023 4:49 p.m'."""
    if not v: return None
    import re
    m = re.match(r"\s*(\d{1,2})[./\-\s]+([A-Za-z]{3,9}|\d{1,2})[./\-\s]+(\d{4})", str(v))
    if not m: return None
    d, mo, y = m.group(1), m.group(2), m.group(3)
    try:
        if mo.isdigit():
            return datetime(int(y), int(mo), int(d)).date()
        return datetime.strptime("%s %s %s" % (d, mo[:3].title(), y), "%d %b %Y").date()
    except Exception:
        return None


def _report_stats(period_start, now, limit=15):
    smap = {}
    try:
        srows = Sample_registration.objects.exclude(inp9__isnull=True).exclude(inp9='').values_list('sample_id', 'inp9', 'inp3')
    except Exception:
        srows = [(a, b, None) for a, b in Sample_registration.objects.exclude(inp9__isnull=True).exclude(inp9='').values_list('sample_id', 'inp9')]
    for sid, inp9, inp3 in srows:
        smap[sid] = (inp9, inp3)
    late_all, checked_p, late_p = [], 0, 0
    mon_checked, mon_late = [0]*12, [0]*12
    tat_sum, tat_n = 0, 0
    for name, model in REPORT_MODELS.items():
        try:
            rws = model.objects.filter(created_at__year=now.year).values('sample_id', 'reporting_date', 'report_to', 'lab_report_no', 'created_at')
        except Exception:
            continue
        for r in rws:
            try:
                pair = smap.get(r.get('sample_id'))
                if not pair or not r.get('reporting_date'):
                    continue
                est = datetime.strptime(pair[0], '%d-%m-%Y').date()
                act = datetime.strptime(r['reporting_date'].replace('-', ' '), '%d %B %Y').date()
                ca = r.get('created_at')
                try: in_p = ca is not None and ca >= period_start
                except Exception: in_p = True
                is_late = act > est
                if act.year == now.year:
                    mon_checked[act.month - 1] += 1
                    if is_late: mon_late[act.month - 1] += 1
                if in_p:
                    checked_p += 1
                    if is_late:
                        late_p += 1
                        late_all.append({'type': name, 'sample_id': r.get('sample_id'),
                                         'client': r.get('report_to') or '', 'lab_no': r.get('lab_report_no') or '',
                                         'estimated': est.strftime('%d-%m-%Y'), 'actual': act.strftime('%d-%m-%Y'),
                                         'days_late': (act - est).days})
                    rec = _parse_rec(pair[1])
                    if rec:
                        dd = (act - rec).days
                        if 0 <= dd <= 120:
                            tat_sum += dd; tat_n += 1
            except Exception:
                continue
    late_all.sort(key=lambda x: -x['days_late'])
    ontime_monthly = [(round(100.0 * (mon_checked[i] - mon_late[i]) / mon_checked[i], 1) if mon_checked[i] else None) for i in range(12)]
    avg_tat = round(tat_sum / float(tat_n), 1) if tat_n else None
    return late_all[:limit], checked_p, late_p, ontime_monthly, avg_tat


def _recent_activity(limit=10):
    items = []
    for name, model in list(REPORT_MODELS.items()) + list(CERT_MODELS.items()):
        try:
            for h in model.history.order_by('-history_date')[:3]:
                items.append({'model': name, 'action': ACTION.get(h.history_type, h.history_type),
                              'user': getattr(h.history_user, 'username', None) or 'system',
                              'ref': getattr(h, 'lab_report_no', None) or getattr(h, 'cert_num', None) or ('#%s' % h.id),
                              'when': timezone.localtime(h.history_date).strftime('%d-%m-%Y %H:%M')})
        except Exception:
            continue
    items.sort(key=lambda x: x['when'], reverse=True)
    return items[:limit]


@login_required
def get_reports_data(request):
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Administrator access required'}, status=403)
    if request.method == 'POST':
        try: body = json.loads(request.body.decode('utf-8'))
        except Exception: body = {}
    else:
        body = request.GET.dict()
    filter_type = body.get('filter', 'monthly')
    if filter_type not in ('monthly', 'quarterly', 'yearly'):
        filter_type = 'monthly'
    ck = 'etal_dash5_%s' % filter_type
    cached = cache.get(ck)
    if cached:
        return JsonResponse(cached)
    now = timezone.localtime()
    period_start = _start(filter_type, now)
    date_filter = Q(created_at__range=[period_start, now])
    reports_data, certs_data = {}, {}
    for name, model in REPORT_MODELS.items():
        try: reports_data[name] = model.objects.filter(date_filter).count()
        except Exception: reports_data[name] = 0
    for name, model in CERT_MODELS.items():
        try: certs_data[name] = model.objects.filter(date_filter).count()
        except Exception: certs_data[name] = 0
    monthly_reports, monthly_certs = [0]*12, [0]*12
    for group, target in ((REPORT_MODELS, monthly_reports), (CERT_MODELS, monthly_certs)):
        for model in group.values():
            try:
                qs = model.objects.filter(created_at__year=now.year).annotate(m=TruncMonth('created_at')).values('m').annotate(c=Count('id'))
                for row in qs:
                    if row['m']: target[row['m'].month - 1] += row['c']
            except Exception:
                continue
    industry, clients, office, ucr = Counter(), Counter(), Counter(), Counter()
    for model in REPORT_MODELS.values():
        try:
            for row in model.objects.filter(date_filter).values('industry__name').annotate(c=Count('id')):
                industry[row['industry__name'] or 'Unspecified'] += row['c']
        except Exception: pass
        try:
            for row in model.objects.filter(date_filter).values('created_by__username').annotate(c=Count('id')):
                ucr[row['created_by__username'] or 'Unassigned'] += row['c']
        except Exception: pass
        try:
            for rt, lno in model.objects.filter(date_filter).values_list('report_to', 'lab_report_no'):
                if rt: clients[rt.strip()[:80]] += 1
                l = lno or ''
                if '-KHI' in l: office['Karachi'] += 1
                elif '-LHR' in l: office['Lahore'] += 1
                else: office['Other'] += 1
        except Exception: pass
    team = Counter()
    month_ago = now - timedelta(days=30)
    for model in list(REPORT_MODELS.values()) + list(CERT_MODELS.values()):
        try:
            for row in model.history.filter(history_date__gte=month_ago).values('history_user__username').annotate(c=Count('id')):
                team[row['history_user__username'] or 'system'] += row['c']
        except Exception: continue
    monthly_samples = [0]*12
    try:
        for row in Sample_registration.objects.filter(created_at__year=now.year).annotate(m=TruncMonth('created_at')).values('m').annotate(c=Count('id')):
            if row['m']: monthly_samples[row['m'].month - 1] += row['c']
    except Exception:
        pass
    weekday_load = [0]*7
    try:
        from django.db.models.functions import ExtractWeekDay
        for model in REPORT_MODELS.values():
            try:
                for row in model.objects.filter(created_at__year=now.year).annotate(w=ExtractWeekDay('created_at')).values('w').annotate(c=Count('id')):
                    if row['w']: weekday_load[(int(row['w']) + 5) % 7] += row['c']
            except Exception:
                continue
    except Exception:
        pass
    try: samples = Sample_registration.objects.filter(date_filter).count()
    except Exception: samples = 0
    try: jobs = JobCompletionForm.objects.filter(date_filter).count()
    except Exception: jobs = 0
    pending = None
    try:
        reg = set(Sample_registration.objects.filter(date_filter).values_list('sample_id', flat=True))
        rep = set()
        for model in REPORT_MODELS.values():
            try: rep.update(model.objects.values_list('sample_id', flat=True).distinct())
            except Exception: continue
        pending = len({s for s in reg if s and s not in rep})
    except Exception:
        pending = None
    week_ago = now - timedelta(days=7)
    activity_7d = 0
    for model in list(REPORT_MODELS.values()) + list(CERT_MODELS.values()):
        try: activity_7d += model.history.filter(history_date__gte=week_ago).count()
        except Exception: continue
    late_list, checked, late_total, ontime_monthly, avg_tat = _report_stats(period_start, now)
    prev_q = _prev_range(filter_type, now)
    payload = {
        'filter': filter_type,
        'reports_data': reports_data, 'certs_data': certs_data,
        'totals': {'reports': sum(reports_data.values()), 'certs': sum(certs_data.values()),
                   'samples': samples, 'jobs': jobs},
        'prev': {'reports': _count_group(REPORT_MODELS.values(), prev_q),
                 'certs': _count_group(CERT_MODELS.values(), prev_q)},
        'monthly_reports': monthly_reports, 'monthly_certs': monthly_certs,
        'monthly_samples': monthly_samples, 'weekday_load': weekday_load,
        'industry_data': industry.most_common(10),
        'top_clients': clients.most_common(8),
        'user_created': ucr.most_common(10),
        'office': dict(office),
        'team_30d': team.most_common(8),
        'ontime': {'checked': checked, 'late': late_total,
                   'pct': round(100.0 * (checked - late_total) / checked, 1) if checked else None},
        'ontime_monthly': ontime_monthly,
        'avg_tat': avg_tat,
        'pending_samples': pending,
        'late_reports': late_list,
        'approved_total': ApprovalStatus.objects.count(),
        'activity_7d': activity_7d,
        'recent_activity': _recent_activity(),
        'generated_at': now.strftime('%d-%m-%Y %H:%M'),
        'year': now.year,
    }
    cache.set(ck, payload, 300)
    return JsonResponse(payload)


# --- Audit Trail page (12-07-2026) ---
@login_required
def audit_page(request):
    if not request.user.is_superuser:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden('Administrator access required')
    return render(request, 'audit.html')


def _all_hist():
    return list(REPORT_MODELS.items()) + list(CERT_MODELS.items())


@login_required
def audit_data(request):
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Administrator access required'}, status=403)
    g = request.GET
    user = (g.get('user') or '').strip()
    entity = (g.get('entity') or '').strip()
    action = (g.get('action') or '').strip()
    dfrom, dto = (g.get('from') or '').strip(), (g.get('to') or '').strip()
    try: page = max(1, int(g.get('page', 1)))
    except Exception: page = 1
    per, off = 50, (max(1, page) - 1) * 50
    amap = {'Created': '+', 'Edited': '~', 'Deleted': '-'}
    rows, total = [], 0
    for name, model in _all_hist():
        if entity and entity != name:
            continue
        try:
            qs = model.history.all()
            if user: qs = qs.filter(history_user__username=user)
            if action in amap: qs = qs.filter(history_type=amap[action])
            elif action in ('Login', 'Saved'): continue
            if dfrom: qs = qs.filter(history_date__date__gte=dfrom)
            if dto: qs = qs.filter(history_date__date__lte=dto)
            total += qs.count()
            for h in qs.order_by('-history_date')[:off + per]:
                rows.append({'when': timezone.localtime(h.history_date).strftime('%d-%m-%Y %H:%M:%S'),
                             'sort': h.history_date.isoformat(),
                             'user': getattr(h.history_user, 'username', None) or 'system',
                             'action': ACTION.get(h.history_type, h.history_type),
                             'entity': name,
                             'ref': getattr(h, 'lab_report_no', None) or getattr(h, 'cert_num', None) or ('#%s' % h.id),
                             'hid': h.history_id})
        except Exception:
            continue
    if (not entity or entity == 'Login') and action in ('', 'Login', 'Saved'):
        try:
            from EnviTechAlApp.models import AuditLog
            lq = AuditLog.objects.all()
            if user:
                try: lq = lq.filter(user__username=user)
                except Exception:
                    try: lq = lq.filter(user=user)
                    except Exception: pass
            from django.db.models import F as _F
            try: lq = lq.select_related('user')
            except Exception: pass
            if dfrom: lq = lq.filter(created_at__date__gte=dfrom)
            if dto: lq = lq.filter(created_at__date__lte=dto)
            if action == 'Login': lq = lq.filter(action__icontains='log')
            elif action == 'Saved': lq = lq.exclude(action__icontains='log')
            total += lq.count()
            for a in lq.order_by(_F('created_at').desc(nulls_last=True))[:off + per]:
                try:
                    import re as _re
                    raw = str(a.timestamp)
                    mm = _re.search(r'(\d{4})-(\d{2})-(\d{2}).*?(\d{1,2}):(\d{2}):(\d{2})', raw)
                    if mm:
                        y, mo, dd, hh, mi, ss = mm.groups()
                        iso = '%s-%s-%sT%s:%s:%s' % (y, mo, dd, hh.zfill(2), mi, ss)
                        when = '%s-%s-%s %s:%s:%s' % (dd, mo, y, hh.zfill(2), mi, ss)
                    else:
                        iso = when = raw[:24]
                    u = a.user
                    uname = getattr(u, 'username', None) or (u if isinstance(u, str) else 'system')
                    act = str(a.action or 'Activity').strip()
                    is_login = 'log' in act.lower()
                    rows.append({'when': when, 'sort': iso, 'user': uname,
                                 'action': 'Login' if is_login else 'Saved',
                                 'entity': 'Login / Session' if is_login else act[:44],
                                 'ref': '-', 'hid': None})
                except Exception:
                    continue
        except Exception:
            pass
    rows.sort(key=lambda x: x['sort'], reverse=True)
    out = {'rows': rows[off:off + per], 'total': total, 'page': page,
           'pages': max(1, (total + per - 1) // per)}
    if page == 1 and not (user or entity or action or dfrom or dto):
        from django.contrib.auth.models import User as _U
        out['users'] = list(_U.objects.filter(is_active=True).values_list('username', flat=True).order_by('username'))
        out['entities'] = [n for n, _m in _all_hist()] + ['Login']
    return JsonResponse(out)


@login_required
def audit_detail(request):
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Administrator access required'}, status=403)
    entity = (request.GET.get('entity') or '').strip()
    try: hid = int(request.GET.get('hid'))
    except Exception:
        return JsonResponse({'changes': [], 'note': 'No detail available'})
    for name, model in _all_hist():
        if name != entity: continue
        try:
            h = model.history.get(history_id=hid)
            if h.history_type == '+':
                return JsonResponse({'changes': [], 'note': 'Record created - all fields set at this point.'})
            if h.history_type == '-':
                return JsonResponse({'changes': [], 'note': 'Record deleted - last values were retained in history.'})
            prev = h.prev_record
            if not prev:
                return JsonResponse({'changes': [], 'note': 'No earlier version available for comparison.'})
            delta = h.diff_against(prev)
            chg = []
            for c in delta.changes:
                if 'sign' in c.field.lower() or 'image' in c.field.lower():
                    continue
                chg.append({'field': c.field,
                            'old': (str(c.old)[:140] if c.old is not None else ''),
                            'new': (str(c.new)[:140] if c.new is not None else '')})
            return JsonResponse({'changes': chg, 'note': '' if chg else 'No visible field changes (image/signature fields are excluded).'})
        except Exception:
            return JsonResponse({'changes': [], 'note': 'Detail unavailable'})
    return JsonResponse({'changes': [], 'note': 'Unknown entity'})


# --- Sample lifecycle board (12-07-2026) ---
STATUSES = ['Invoiced', 'Registered', 'In testing', 'QC review', 'Reported']


@login_required
def lifecycle_page(request):
    return render(request, 'lifecycle.html')


@login_required
def lifecycle_data(request):
    from EnviTechAlApp.models import SampleLifecycle
    try: days = min(365, max(7, int(request.GET.get('days', 60))))
    except Exception: days = 60
    now = timezone.localtime()
    since = now - timedelta(days=days)
    regs = list(Sample_registration.objects.filter(created_at__gte=since)
                .values('sample_id', 'inp1', 'inp9', 'created_at').order_by('-created_at')[:400])
    sids = [r['sample_id'] for r in regs if r['sample_id']]
    reported = set()
    for model in REPORT_MODELS.values():
        try: reported.update(model.objects.filter(sample_id__in=sids).values_list('sample_id', flat=True))
        except Exception: continue
    overrides = {o.sample_id: o.status for o in SampleLifecycle.objects.filter(sample_id__in=sids)}
    cols = {st: [] for st in STATUSES}
    for r in regs:
        sid = r['sample_id']
        if not sid: continue
        auto = 'Reported' if sid in reported else 'Registered'
        st = overrides.get(sid) or auto
        if st == 'Registered' and auto == 'Reported': st = 'Reported'
        if st not in cols: st = 'Registered'
        cols[st].append({'sample_id': sid, 'client': (r.get('inp1') or '')[:60],
                         'due': r.get('inp9') or '', 'auto': sid in reported})
    return JsonResponse({'columns': cols, 'statuses': STATUSES, 'days': days,
                         'counts': {k: len(v) for k, v in cols.items()}})


@login_required
def lifecycle_set(request):
    from EnviTechAlApp.models import SampleLifecycle
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    sid = (request.POST.get('sample_id') or '').strip()
    st = (request.POST.get('status') or '').strip()
    if not sid or st not in STATUSES:
        return JsonResponse({'error': 'Bad request'}, status=400)
    obj, _c = SampleLifecycle.objects.update_or_create(
        sample_id=sid, defaults={'status': st, 'updated_by': request.user})
    return JsonResponse({'ok': True, 'sample_id': sid, 'status': st})


# --- Phase 2: equipment register + QR labels (12-07-2026) ---

def _eq_scope(request):
    from EnviTechAlApp.models import Equipment
    loc = (request.GET.get('location') or 'All').strip()
    qs = Equipment.objects.filter(active=True)
    if loc in ('Karachi', 'Lahore'):
        qs = qs.filter(lab__iexact=loc)
    return qs


def _eq_doc(request):
    from EnviTechAlApp.models import InventoryDocControl
    loc = (request.GET.get('location') or 'All').strip()
    if loc not in ('Karachi', 'Lahore'):
        loc = ''
    dc = InventoryDocControl.objects.filter(module='equipment', location=(loc or 'Karachi')).first()
    return loc, dict(doc_no=(dc.doc_no if dc and dc.doc_no else 'TBA'),
                     issue_date=(dc.issue_date if dc and dc.issue_date else 'TBA'),
                     issue_no=(dc.issue_no if dc and dc.issue_no else '01'),
                     rev_no=(dc.rev_no if dc and dc.rev_no else '00'))

@login_required
def equipment_page(request):
    return render(request, 'equipment.html')


def _eq_row(e, today):
    due = None
    state = 'No date'
    days = None
    if e.last_calibrated:
        m = e.frequency_months or 12
        y, mo = e.last_calibrated.year, e.last_calibrated.month + m
        y += (mo - 1) // 12; mo = (mo - 1) % 12 + 1
        dd = min(e.last_calibrated.day, 28)
        from datetime import date as _date
        due = _date(y, mo, dd)
        days = (due - today).days
        state = 'Overdue' if days < 0 else ('Due soon' if days <= 30 else 'OK')
    return {'id': e.id, 'name': e.name, 'serial': e.serial_no, 'location': e.location,
            'freq': e.frequency_months, 'last': e.last_calibrated.strftime('%d-%m-%Y') if e.last_calibrated else '',
            'due': due.strftime('%d-%m-%Y') if due else '', 'days': days, 'state': state,
            'cert': e.cert_ref, 'notes': e.notes, 'lab': e.lab, 'last_iso': e.last_calibrated.strftime('%Y-%m-%d') if e.last_calibrated else ''}


@login_required
def equipment_data(request):
    from EnviTechAlApp.models import Equipment
    today = timezone.localdate()
    loc = (request.GET.get('location') or 'All').strip()
    rows = [_eq_row(e, today) for e in _eq_scope(request).order_by('name')]
    order = {'Overdue': 0, 'Due soon': 1, 'No date': 2, 'OK': 3}
    rows.sort(key=lambda r: (order.get(r['state'], 9), r['days'] if r['days'] is not None else 9999))
    dc = {}
    if loc in ('Karachi', 'Lahore'):
        from EnviTechAlApp.models import InventoryDocControl
        dc = InventoryDocControl.objects.filter(module='equipment', location=loc).values('doc_no', 'issue_date', 'issue_no', 'rev_no').first() or {}
    return JsonResponse({'rows': rows, 'is_admin': request.user.is_superuser, 'location': loc, 'doc': dc,
                         'summary': {k: sum(1 for r in rows if r['state'] == k) for k in order}})


@login_required
def equipment_save(request):
    from EnviTechAlApp.models import Equipment
    from datetime import datetime as _dt
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Administrator access required'}, status=403)
    g = request.POST
    act = (g.get('act') or 'save').strip()
    if act == 'doc':
        from EnviTechAlApp.models import InventoryDocControl
        dloc = (g.get('location') or '').strip()
        if dloc not in ('Karachi', 'Lahore'):
            return JsonResponse({'error': 'Unknown location'}, status=400)
        d, _c = InventoryDocControl.objects.get_or_create(module='equipment', location=dloc)
        d.doc_no = (g.get('doc_no') or '')[:60]
        d.issue_date = (g.get('issue_date') or '')[:20]
        d.issue_no = (g.get('issue_no') or '01')[:10]
        d.rev_no = (g.get('rev_no') or '00')[:10]
        d.updated_by = request.user
        d.save()
        return JsonResponse({'ok': True})
    if act == 'setlab':
        lb = (g.get('lab') or '').strip()
        if lb not in ('Karachi', 'Lahore'):
            return JsonResponse({'error': 'Unknown lab'}, status=400)
        try:
            e = Equipment.objects.get(id=int(g.get('id')))
        except Exception:
            return JsonResponse({'error': 'Not found'}, status=404)
        e.lab = lb
        e.updated_by = request.user
        e.save()
        return JsonResponse({'ok': True})
    if act == 'calibrated':
        try:
            e = Equipment.objects.get(id=int(g.get('id')))
            e.last_calibrated = timezone.localdate()
            if g.get('cert'): e.cert_ref = g.get('cert')[:120]
            e.updated_by = request.user; e.save()
            return JsonResponse({'ok': True})
        except Exception:
            return JsonResponse({'error': 'Not found'}, status=404)
    if act == 'remove':
        try:
            e = Equipment.objects.get(id=int(g.get('id')))
            e.active = False; e.updated_by = request.user; e.save()
            return JsonResponse({'ok': True})
        except Exception:
            return JsonResponse({'error': 'Not found'}, status=404)
    name = (g.get('name') or '').strip()
    if not name:
        return JsonResponse({'error': 'Name is required'}, status=400)
    last = None
    if g.get('last'):
        try: last = _dt.strptime(g.get('last'), '%Y-%m-%d').date()
        except Exception: pass
    try: freq = max(1, min(120, int(g.get('freq') or 12)))
    except Exception: freq = 12
    iid = (g.get('id') or '').strip()
    if act == 'update' and iid:
        try:
            e = Equipment.objects.get(id=int(iid))
        except Exception:
            return JsonResponse({'error': 'Not found'}, status=404)
        e.name = name[:200]
        e.lab = (g.get('lab') or e.lab or 'Karachi')[:20]
        e.serial_no = (g.get('serial') or '')[:120]
        e.location = (g.get('location') or 'Karachi')[:60]
        e.frequency_months = freq
        e.last_calibrated = last
        e.cert_ref = (g.get('cert') or '')[:120]
        e.notes = (g.get('notes') or '')[:300]
        e.updated_by = request.user
        e.save()
        return JsonResponse({'ok': True})
    Equipment.objects.create(name=name[:200], lab=(g.get('lab') or 'Karachi')[:20], serial_no=(g.get('serial') or '')[:120],
                             location=(g.get('location') or 'Karachi')[:60], frequency_months=freq,
                             last_calibrated=last, cert_ref=(g.get('cert') or '')[:120],
                             notes=(g.get('notes') or '')[:300], updated_by=request.user)
    return JsonResponse({'ok': True})


@login_required
def sample_label(request):
    sid = (request.GET.get('sid') or '').strip()[:100]
    reg = Sample_registration.objects.filter(sample_id=sid).values('sample_id', 'inp1', 'inp3', 'inp9').first() or {}
    return render(request, 'label.html', {'sid': sid, 'client': (reg.get('inp1') or '')[:60],
                                          'rec': (reg.get('inp3') or '')[:24], 'due': reg.get('inp9') or ''})


# --- Phase 2: regulatory limits library + checker (12-07-2026) ---
@login_required
def limits_page(request):
    return render(request, 'limits.html')


@login_required
def limits_data(request):
    from EnviTechAlApp.models import RegulatoryLimit
    _q = RegulatoryLimit.objects.filter(active=True)
    _std = (request.GET.get('std') or '').strip().upper()
    if _std:
        _q = _q.filter(standard__istartswith=_std)
    _t = (request.GET.get('q') or '').strip()
    if _t:
        import re as _re2
        _qq = _q.filter(parameter__iexact=_t)
        if not _qq.exists():
            _qq = _q.filter(parameter__iregex=r'\m' + _re2.escape(_t))
        _q = _qq if _qq.exists() else _q.filter(parameter__icontains=_t)
    rows = [{'id': l.id, 'parameter': l.parameter, 'standard': l.standard,
             'min': l.limit_min, 'max': l.limit_max, 'unit': l.unit, 'notes': l.notes}
            for l in _q.order_by('parameter', 'standard')]
    return JsonResponse({'rows': rows, 'is_admin': request.user.is_superuser})


@login_required
def limits_save(request):
    from EnviTechAlApp.models import RegulatoryLimit
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Administrator access required'}, status=403)
    g = request.POST
    if (g.get('act') or '') == 'remove':
        try:
            l = RegulatoryLimit.objects.get(id=int(g.get('id')))
            l.active = False; l.updated_by = request.user; l.save()
            return JsonResponse({'ok': True})
        except Exception:
            return JsonResponse({'error': 'Not found'}, status=404)
    p = (g.get('parameter') or '').strip()[:120]
    st = (g.get('standard') or '').strip().upper()[:20]
    if not p or st.split()[0] not in ('SEQS', 'PEQS', 'NEQS', 'WHO', 'GOTS', 'ZDHC', 'STEP', 'PPWR'):
        return JsonResponse({'error': 'Parameter and a valid standard are required'}, status=400)
    def f(k):
        try: return float(g.get(k)) if (g.get(k) or '').strip() != '' else None
        except Exception: return None
    mn, mx = f('min'), f('max')
    if mn is None and mx is None:
        return JsonResponse({'error': 'Provide at least one of min / max limit'}, status=400)
    import re as _re3
    _np = _re3.sub(r'[^a-z0-9]+', '', p.lower())
    for _ex in RegulatoryLimit.objects.filter(active=True, standard=st).exclude(parameter=p):
        if _re3.sub(r'[^a-z0-9]+', '', _ex.parameter.lower()) == _np:
            return JsonResponse({'error': 'Near-identical parameter already exists in %s: "%s". Edit that entry or choose a clearly distinct name.' % (st, _ex.parameter)}, status=400)
    obj, _c = RegulatoryLimit.objects.update_or_create(
        parameter=p, standard=st,
        defaults={'limit_min': mn, 'limit_max': mx, 'unit': (g.get('unit') or '')[:40],
                  'notes': (g.get('notes') or '')[:200], 'active': True, 'updated_by': request.user})
    return JsonResponse({'ok': True})


@login_required
def limits_check(request):
    from EnviTechAlApp.models import RegulatoryLimit
    p = (request.GET.get('parameter') or '').strip()
    try: v = float(request.GET.get('value'))
    except Exception:
        return JsonResponse({'error': 'Numeric value required'}, status=400)
    out = []
    for l in RegulatoryLimit.objects.filter(active=True, parameter=p):
        exceeds = (l.limit_max is not None and v > l.limit_max) or (l.limit_min is not None and v < l.limit_min)
        rng = ('%s - %s' % (l.limit_min, l.limit_max)) if (l.limit_min is not None and l.limit_max is not None) else \
              ('<= %s' % l.limit_max if l.limit_max is not None else '>= %s' % l.limit_min)
        out.append({'standard': l.standard, 'range': rng, 'unit': l.unit,
                    'result': 'EXCEEDS' if exceeds else 'Within limit'})
    _have = set(x['standard'].split()[0] for x in out)
    for _s in ('SEQS', 'PEQS', 'NEQS', 'WHO', 'GOTS', 'ZDHC', 'STEP', 'PPWR'):
        if _s not in _have:
            out.append({'standard': _s, 'range': 'No limit on record', 'unit': '', 'result': 'Not regulated'})
    return JsonResponse({'parameter': p, 'value': v, 'results': out})


# --- Phase 2: controlled master equipment list report (12-07-2026) ---
@login_required
def equipment_report(request):
    from EnviTechAlApp.models import Equipment
    import re as _re, datetime as _dt
    def tok(n, k):
        m = _re.search(k + r':\s*([^|]+)', n or '')
        return m.group(1).strip() if m else ''
    order = ['Lab Equipment', 'Field Equipment', 'Calibration Instrument']
    groups = {k: [] for k in order}
    for e in _eq_scope(request).order_by('id'):
        g = tok(e.notes, 'Group')
        if g not in groups:
            g = 'Lab Equipment'
        cal = e.last_calibrated
        due = ''
        if cal:
            t = cal.month + (e.frequency_months or 12)
            due = (_dt.date(cal.year + (t - 1) // 12, (t - 1) % 12 + 1, min(cal.day, 28)) - _dt.timedelta(days=1)).strftime('%d-%m-%Y')
        nr = 'Not Required' in (e.notes or '')
        rows = groups[g]
        rows.append(dict(sno=len(rows) + 1, name=e.name, make=tok(e.notes, 'Make'), model=tok(e.notes, 'Model'),
            eid=e.serial_no or 'Not Required', loc=e.location,
            prov=e.cert_ref or ('Not Required' if nr else ''),
            cal=cal.strftime('%d-%m-%Y') if cal else ('Not Required' if nr else ''),
            due=due or ('Not Required' if nr else ''),
            trace=tok(e.notes, 'Traceability') or ('Not Required' if nr else 'N/A'),
            rem='Satisfactory'))
    _loc, _dc = _eq_doc(request)
    ctx = {'groups': [(k, groups[k]) for k in order], 'today': _dt.date.today().strftime('%d-%m-%Y'), 'loc': _loc, 'dc': _dc}
    return render(request, 'equipment_report.html', ctx)


@login_required
def equipment_report_pdf(request):
    from EnviTechAlApp.models import Equipment
    from fpdf import FPDF
    from django.http import HttpResponse
    import re as _re, datetime as _dt
    def tok(n, k):
        m = _re.search(k + r':\s*([^|]+)', n or '')
        return m.group(1).strip() if m else ''
    key = {'Lab Equipment': 0, 'Field Equipment': 1, 'Calibration Instrument': 2}
    order = ['LAB EQUIPMENTS', 'FIELD EQUIPMENTS', 'CALIBRATION INSTRUMENTS']
    data = [[], [], []]
    for e in _eq_scope(request).order_by('id'):
        gi = key.get(tok(e.notes, 'Group'), 0)
        cal = e.last_calibrated
        due = ''
        if cal:
            t = cal.month + (e.frequency_months or 12)
            due = (_dt.date(cal.year + (t - 1) // 12, (t - 1) % 12 + 1, min(cal.day, 28)) - _dt.timedelta(days=1)).strftime('%d-%m-%Y')
        nr = 'Not Required' in (e.notes or '')
        nrv = 'Not Required' if nr else ''
        data[gi].append([str(len(data[gi]) + 1), e.name, tok(e.notes, 'Make'), tok(e.notes, 'Model'),
            e.serial_no or nrv, e.location, e.cert_ref or nrv,
            cal.strftime('%d-%m-%Y') if cal else nrv, due or nrv,
            tok(e.notes, 'Traceability') or ('Not Required' if nr else 'N/A'), 'Satisfactory'])
    today = _dt.date.today().strftime('%d-%m-%Y')
    _loc, _dc = _eq_doc(request)
    class _P(FPDF):
        def header(self):
            try:
                self.image('/home/django/EnviTechAlApp/static/assets/EnviTechAL_LOGO-removebg-preview.png', 12, 6.5, 20, 20)
            except Exception:
                pass
            self.set_font('Arial', 'B', 15)
            self.set_y(8)
            self.cell(0, 7, 'Envi Tech AL', 0, 1, 'C')
            self.set_font('Arial', 'B', 11)
            self.cell(0, 6, 'MASTER LIST OF LAB EQUIPMENT' + ((' - %s LABORATORY' % _loc.upper()) if _loc else ''), 0, 1, 'C')
            self.set_font('Arial', 'I', 7.5)
            self.set_text_color(90, 90, 90)
            self.cell(0, 4, 'Environmental Analytical Laboratory', 0, 1, 'C')
            self.set_text_color(0, 0, 0)
            self.set_font('Arial', '', 7.5)
            self.set_xy(216, 8)
            self.multi_cell(70, 4.6, 'Doc. No: %s\nIssue Date: %s\nIssue No. %s    Rev. No. %s\nPage No: %d of {nb}' % (_dc['doc_no'], _dc['issue_date'], _dc['issue_no'], _dc['rev_no'], self.page_no()), 1, 'L')
            self.set_font('Arial', 'B', 8.5)
            self.set_y(29)
            self.cell(0, 5, 'Calibration Status Year: 2025 - 2026', 0, 1, 'L')
            self.set_draw_color(170, 170, 170)
            self.line(10, 35, 287, 35)
            self.set_draw_color(0, 0, 0)
            self.set_y(37)
        def footer(self):
            self.set_y(-11)
            self.set_font('Arial', 'I', 7)
            self.set_text_color(120, 120, 120)
            self.cell(0, 5, '%s  |  Issue %s Rev. %s  |  Controlled document - generated from the live register on %s' % (_dc['doc_no'], _dc['issue_no'], _dc['rev_no'], today), 0, 0, 'C')
            self.set_text_color(0, 0, 0)
    W = [9, 50, 26, 36, 20, 16, 38, 19, 19, 20, 22]
    HD = ['S.NO', 'Name', 'Make/Type', 'Model', 'Equipment ID', 'Location', 'Calibration Provider', 'Calibration Date', 'Due on', 'Traceability', 'Remarks']
    AL = ['C', 'L', 'L', 'L', 'C', 'C', 'L', 'C', 'C', 'C', 'C']
    pdf = _P('L', 'mm', 'A4')
    pdf.alias_nb_pages('{nb}')
    pdf.set_auto_page_break(False)
    pdf.add_page()
    def fit(s, w):
        s = str(s)
        if pdf.get_string_width(s) <= w - 2.2:
            return s
        while s and pdf.get_string_width(s + '...') > w - 2.2:
            s = s[:-1]
        return s + '...'
    def head_row():
        pdf.set_font('Arial', 'B', 6.6)
        pdf.set_fill_color(229, 231, 235)
        for w, h in zip(W, HD):
            pdf.cell(w, 6, h, 1, 0, 'C', True)
        pdf.ln()
    def band(title):
        pdf.set_font('Arial', 'B', 8.5)
        pdf.set_fill_color(31, 41, 55)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(sum(W), 6.5, ' ' + title, 1, 1, 'L', True)
        pdf.set_text_color(0, 0, 0)
    for gi, title in enumerate(order):
        if pdf.get_y() > 165:
            pdf.add_page()
        band(title)
        head_row()
        pdf.set_font('Arial', '', 7)
        odd = False
        for row in data[gi]:
            if pdf.get_y() > 186:
                pdf.add_page()
                band(title + ' (continued)')
                head_row()
                pdf.set_font('Arial', '', 7)
            if odd:
                pdf.set_fill_color(245, 247, 249)
            for i, (w, v) in enumerate(zip(W, row)):
                pdf.cell(w, 5.5, fit(v, w), 1, 0, AL[i], odd)
            pdf.ln()
            odd = not odd
        pdf.ln(3)
    out = pdf.output(dest='S')
    b = bytes(out) if isinstance(out, (bytes, bytearray)) else out.encode('latin-1')
    resp = HttpResponse(b, content_type='application/pdf')
    resp['Content-Disposition'] = 'inline; filename="%s Master Equipment List%s.pdf"' % (_dc['doc_no'], ((' - ' + _loc) if _loc else ''))
    return resp


# --- Phase 2: chemical & consumable inventory (13-07-2026) ---
CHEM_LOCS = ('Karachi', 'Lahore')
CHEM_CATS = ('Reagent', 'Reference standard', 'Solvent', 'Culture media', 'Glassware', 'Consumable', 'PPE', 'Gas', 'Other')


@login_required
def chemicals_page(request):
    return render(request, 'chemicals.html')


def _chem_lot_balance(lot):
    b = 0.0
    for mv in lot.moves.all():
        if mv.mtype == 'IN':
            b += mv.qty
        elif mv.mtype == 'OUT':
            b -= mv.qty
        else:
            b += mv.qty
    return round(b, 4)


def _chem_exp_state(lot, today):
    if not lot.expiry:
        return ('', None)
    days = (lot.expiry - today).days
    if days < 0:
        return ('Expired', days)
    if days <= 90:
        return ('Expiring', days)
    return ('OK', days)


@login_required
def chemicals_data(request):
    from EnviTechAlApp.models import ChemicalItem, ChemicalLot, InventoryDocControl
    loc = (request.GET.get('location') or 'Karachi').strip()
    if loc not in CHEM_LOCS:
        loc = 'Karachi'
    lot_id = request.GET.get('lot')
    if lot_id:
        try:
            lot = ChemicalLot.objects.get(id=int(lot_id))
        except Exception:
            return JsonResponse({'error': 'Lot not found'}, status=404)
        moves = [{'type': mv.mtype, 'qty': mv.qty,
                  'date': mv.on_date.strftime('%d-%m-%Y') if mv.on_date else mv.at.strftime('%d-%m-%Y'),
                  'by': (mv.by.username if mv.by else ''), 'remarks': mv.remarks}
                 for mv in lot.moves.order_by('at', 'id')]
        return JsonResponse({'lot': {'id': lot.id, 'item': lot.item.name, 'lot_no': lot.lot_no,
                                     'balance': _chem_lot_balance(lot), 'unit': lot.item.unit}, 'moves': moves})
    q = (request.GET.get('q') or '').strip()
    today = timezone.localdate()
    items_qs = ChemicalItem.objects.filter(active=True)
    if q:
        exact = list(items_qs.filter(name__iexact=q))
        if exact:
            items = exact
        else:
            ids = set(items_qs.filter(name__icontains=q).values_list('id', flat=True))
            ids |= set(items_qs.filter(cas_no__iexact=q).values_list('id', flat=True))
            ids |= set(items_qs.filter(grade__icontains=q).values_list('id', flat=True))
            ids |= set(items_qs.filter(category__icontains=q).values_list('id', flat=True))
            items = list(items_qs.filter(id__in=ids))
    else:
        items = list(items_qs)
    items.sort(key=lambda i: i.name.lower())
    rows = []
    n_low = n_exp = n_expiring = n_stock = 0
    for it in items:
        lots_out = []
        total = 0.0
        for lot in it.lots.filter(location=loc).exclude(status='Discarded').prefetch_related('moves').order_by('received', 'id'):
            bal = _chem_lot_balance(lot)
            if bal <= 0 and lot.status != 'Quarantine':
                continue
            state, days = _chem_exp_state(lot, today)
            total += max(bal, 0)
            lots_out.append({'id': lot.id, 'lot_no': lot.lot_no, 'supplier': lot.supplier, 'po_ref': lot.po_ref,
                             'received': lot.received.strftime('%d-%m-%Y') if lot.received else '',
                             'expiry': lot.expiry.strftime('%d-%m-%Y') if lot.expiry else '',
                             'opened': lot.opened.strftime('%d-%m-%Y') if lot.opened else '',
                             'exp_state': state, 'exp_days': days, 'balance': bal,
                             'qty_received': lot.qty_received, 'coa': lot.coa,
                             'status': lot.status, 'remarks': lot.remarks})
            if state == 'Expired':
                n_exp += 1
            elif state == 'Expiring':
                n_expiring += 1
        low = (it.reorder_level is not None and total < it.reorder_level)
        if low:
            n_low += 1
        if total > 0:
            n_stock += 1
        rows.append({'id': it.id, 'name': it.name, 'category': it.category, 'grade': it.grade,
                     'cas': it.cas_no, 'unit': it.unit, 'storage': it.storage, 'hazard': it.hazard,
                     'reorder': it.reorder_level, 'notes': it.notes, 'total': round(total, 4),
                     'low': low, 'lots': lots_out})
    dc = InventoryDocControl.objects.filter(module='chemicals', location=loc).values('doc_no', 'issue_date', 'issue_no', 'rev_no').first() or {}
    return JsonResponse({'rows': rows, 'location': loc, 'is_admin': request.user.is_superuser, 'doc': dc,
                         'summary': {'stocked': n_stock, 'low': n_low, 'expiring': n_expiring, 'expired': n_exp}})


@login_required
def chemicals_save(request):
    from EnviTechAlApp.models import ChemicalItem, ChemicalLot, ChemicalMovement, InventoryDocControl
    from datetime import datetime as _dt
    import re as _re
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    g = request.POST
    act = (g.get('act') or '').strip()

    def _d(key):
        v = (g.get(key) or '').strip()
        if not v:
            return None
        try:
            return _dt.strptime(v, '%Y-%m-%d').date()
        except Exception:
            return None

    def _f(key):
        v = (g.get(key) or '').strip().replace(',', '')
        if not v:
            return None
        try:
            return float(v)
        except Exception:
            return None

    if act == 'doc':
        if not request.user.is_superuser:
            return JsonResponse({'error': 'Administrator access required'}, status=403)
        loc = (g.get('location') or '').strip()
        if loc not in CHEM_LOCS:
            return JsonResponse({'error': 'Unknown location'}, status=400)
        d, _c = InventoryDocControl.objects.get_or_create(module='chemicals', location=loc)
        d.doc_no = (g.get('doc_no') or '')[:60]
        d.issue_date = (g.get('issue_date') or '')[:20]
        d.issue_no = (g.get('issue_no') or '01')[:10]
        d.rev_no = (g.get('rev_no') or '00')[:10]
        d.updated_by = request.user
        d.save()
        return JsonResponse({'ok': True})

    if act == 'item':
        name = (g.get('name') or '').strip()
        if not name:
            return JsonResponse({'error': 'Item name is required'}, status=400)
        norm = _re.sub(r'[^a-z0-9]+', '', name.lower())
        iid = (g.get('id') or '').strip()
        for other in ChemicalItem.objects.filter(active=True):
            if iid and str(other.id) == iid:
                continue
            if _re.sub(r'[^a-z0-9]+', '', other.name.lower()) == norm:
                return JsonResponse({'error': 'An item named "%s" already exists in the catalogue. Edit that entry instead of adding a near-duplicate.' % other.name}, status=400)
        vals = dict(name=name[:200], category=(g.get('category') or 'Reagent')[:40], grade=(g.get('grade') or '')[:80],
                    cas_no=(g.get('cas') or '')[:40], unit=(g.get('unit') or 'g')[:30], storage=(g.get('storage') or '')[:120],
                    hazard=(g.get('hazard') or '')[:120], reorder_level=_f('reorder'), notes=(g.get('notes') or '')[:300],
                    updated_by=request.user)
        if iid:
            try:
                it = ChemicalItem.objects.get(id=int(iid))
            except Exception:
                return JsonResponse({'error': 'Item not found'}, status=404)
            for k, v in vals.items():
                setattr(it, k, v)
            it.save()
        else:
            it = ChemicalItem.objects.create(**vals)
        return JsonResponse({'ok': True, 'id': it.id})

    if act == 'retire':
        if not request.user.is_superuser:
            return JsonResponse({'error': 'Administrator access required'}, status=403)
        try:
            it = ChemicalItem.objects.get(id=int(g.get('id')))
        except Exception:
            return JsonResponse({'error': 'Item not found'}, status=404)
        it.active = False
        it.updated_by = request.user
        it.save()
        return JsonResponse({'ok': True})

    if act == 'receive':
        try:
            it = ChemicalItem.objects.get(id=int(g.get('item')))
        except Exception:
            return JsonResponse({'error': 'Item not found'}, status=404)
        loc = (g.get('location') or '').strip()
        if loc not in CHEM_LOCS:
            return JsonResponse({'error': 'Unknown location'}, status=400)
        qty = _f('qty')
        if not qty or qty <= 0:
            return JsonResponse({'error': 'Received quantity must be a positive number'}, status=400)
        lot = ChemicalLot.objects.create(item=it, location=loc, lot_no=(g.get('lot_no') or '')[:80],
                                         supplier=(g.get('supplier') or '')[:150], po_ref=(g.get('po_ref') or '')[:60],
                                         received=_d('received') or timezone.localdate(), expiry=_d('expiry'),
                                         qty_received=qty, coa=(g.get('coa') == '1'),
                                         remarks=(g.get('remarks') or '')[:200], created_by=request.user)
        ChemicalMovement.objects.create(lot=lot, mtype='IN', qty=qty, on_date=lot.received,
                                        remarks=('Received' + ((' | PO ' + lot.po_ref) if lot.po_ref else ''))[:200], by=request.user)
        return JsonResponse({'ok': True, 'id': lot.id})

    if act == 'move':
        try:
            lot = ChemicalLot.objects.get(id=int(g.get('lot')))
        except Exception:
            return JsonResponse({'error': 'Lot not found'}, status=404)
        mtype = (g.get('mtype') or '').strip().upper()
        if mtype not in ('IN', 'OUT', 'ADJ'):
            return JsonResponse({'error': 'Unknown movement type'}, status=400)
        qty = _f('qty')
        if qty is None or qty == 0:
            return JsonResponse({'error': 'Quantity must be a non-zero number'}, status=400)
        if mtype in ('IN', 'OUT') and qty < 0:
            return JsonResponse({'error': 'Use a positive quantity; use Adjust for corrections'}, status=400)
        bal = _chem_lot_balance(lot)
        if mtype == 'OUT' and qty > bal + 1e-9:
            return JsonResponse({'error': 'Only %g %s left in this lot - cannot issue %g' % (bal, lot.item.unit, qty)}, status=400)
        if mtype == 'ADJ' and bal + qty < -1e-9:
            return JsonResponse({'error': 'Adjustment would make the balance negative (current %g)' % bal}, status=400)
        ChemicalMovement.objects.create(lot=lot, mtype=mtype, qty=qty, on_date=_d('date') or timezone.localdate(),
                                        remarks=(g.get('remarks') or '')[:200], by=request.user)
        if lot.opened is None and mtype == 'OUT':
            lot.opened = timezone.localdate()
        nb = _chem_lot_balance(lot)
        if nb <= 0 and lot.status == 'In use':
            lot.status = 'Finished'
        elif nb > 0 and lot.status == 'Finished':
            lot.status = 'In use'
        lot.save()
        return JsonResponse({'ok': True, 'balance': nb})

    if act == 'lotstatus':
        try:
            lot = ChemicalLot.objects.get(id=int(g.get('lot')))
        except Exception:
            return JsonResponse({'error': 'Lot not found'}, status=404)
        st = (g.get('status') or '').strip()
        if st not in ('In use', 'Quarantine', 'Finished', 'Discarded'):
            return JsonResponse({'error': 'Unknown status'}, status=400)
        lot.status = st
        lot.save()
        return JsonResponse({'ok': True})

    if act == 'retest':
        try:
            lot = ChemicalLot.objects.get(id=int(g.get('lot')))
        except Exception:
            return JsonResponse({'error': 'Lot not found'}, status=404)
        ne = _d('new_expiry')
        if ne is None:
            return JsonResponse({'error': 'A valid new expiry date is required (YYYY-MM-DD)'}, status=400)
        rd = _d('retest_date') or timezone.localdate()
        reason = (g.get('remarks') or '').strip()
        old = lot.expiry
        lot.expiry = ne
        note = '[Retest %s: expiry %s -> %s%s]' % (
            rd.strftime('%d-%m-%Y'),
            old.strftime('%d-%m-%Y') if old else '-',
            ne.strftime('%d-%m-%Y'),
            (' | ' + reason) if reason else '')
        combined = ((lot.remarks + ' ') if lot.remarks else '') + note
        lot.remarks = combined[-200:]
        lot.save()
        return JsonResponse({'ok': True, 'expiry': ne.strftime('%d-%m-%Y')})

    return JsonResponse({'error': 'Unknown action'}, status=400)


def _chem_report_data(loc):
    from EnviTechAlApp.models import ChemicalItem
    today = timezone.localdate()
    groups = {c: [] for c in CHEM_CATS}
    for it in ChemicalItem.objects.filter(active=True).order_by('name'):
        cat = it.category if it.category in CHEM_CATS else 'Other'
        for lot in it.lots.filter(location=loc).exclude(status='Discarded').prefetch_related('moves').order_by('received', 'id'):
            bal = _chem_lot_balance(lot)
            if bal <= 0:
                continue
            state, days = _chem_exp_state(lot, today)
            groups[cat].append({'name': it.name, 'grade': it.grade, 'cas': it.cas_no,
                                'lot_no': lot.lot_no, 'supplier': lot.supplier, 'po_ref': lot.po_ref,
                                'received': lot.received.strftime('%d-%m-%Y') if lot.received else '',
                                'expiry': lot.expiry.strftime('%d-%m-%Y') if lot.expiry else '',
                                'exp_state': state, 'balance': bal, 'unit': it.unit,
                                'storage': it.storage, 'status': lot.status})
    return [(c, groups[c]) for c in CHEM_CATS if groups[c]]


@login_required
def chemicals_report(request):
    from EnviTechAlApp.models import InventoryDocControl
    loc = (request.GET.get('location') or 'Karachi').strip()
    if loc not in CHEM_LOCS:
        loc = 'Karachi'
    dc = InventoryDocControl.objects.filter(module='chemicals', location=loc).first()
    groups = _chem_report_data(loc)
    total = sum(len(g[1]) for g in groups)
    return render(request, 'chemicals_report.html',
                  {'groups': groups, 'loc': loc, 'dc': dc, 'total': total,
                   'today': timezone.localdate().strftime('%d-%m-%Y')})


@login_required
def chemicals_report_pdf(request):
    from EnviTechAlApp.models import InventoryDocControl
    from fpdf import FPDF
    from django.http import HttpResponse
    import datetime as _dt
    loc = (request.GET.get('location') or 'Karachi').strip()
    if loc not in CHEM_LOCS:
        loc = 'Karachi'
    dc = InventoryDocControl.objects.filter(module='chemicals', location=loc).first()
    doc_no = (dc.doc_no if dc and dc.doc_no else 'TBA')
    issue_date = (dc.issue_date if dc and dc.issue_date else 'TBA')
    issue_no = (dc.issue_no if dc and dc.issue_no else '01')
    rev_no = (dc.rev_no if dc and dc.rev_no else '00')
    groups = _chem_report_data(loc)
    total = sum(len(g[1]) for g in groups)
    today = _dt.date.today().strftime('%d-%m-%Y')
    class _P(FPDF):
        def header(self):
            try:
                self.image('/home/django/EnviTechAlApp/static/assets/EnviTechAL_LOGO-removebg-preview.png', 12, 6.5, 20, 20)
            except Exception:
                pass
            self.set_font('Arial', 'B', 15)
            self.set_y(8)
            self.cell(0, 7, 'Envi Tech AL', 0, 1, 'C')
            self.set_font('Arial', 'B', 11)
            self.cell(0, 6, 'CHEMICAL & CONSUMABLE INVENTORY - %s LABORATORY' % loc.upper(), 0, 1, 'C')
            self.set_font('Arial', 'I', 7.5)
            self.set_text_color(90, 90, 90)
            self.cell(0, 4, 'Environmental Analytical Laboratory', 0, 1, 'C')
            self.set_text_color(0, 0, 0)
            self.set_font('Arial', '', 7.5)
            self.set_xy(216, 8)
            self.multi_cell(70, 4.6, 'Doc. No: %s\nIssue Date: %s\nIssue No. %s    Rev. No. %s\nPage No: %d of {nb}' % (doc_no, issue_date, issue_no, rev_no, self.page_no()), 1, 'L')
            self.set_font('Arial', 'B', 8.5)
            self.set_y(29)
            self.cell(0, 5, 'Location: %s Laboratory    |    Lots in stock: %d    |    Stock position as generated on %s' % (loc, total, today), 0, 1, 'L')
            self.set_draw_color(170, 170, 170)
            self.line(10, 35, 287, 35)
            self.set_draw_color(0, 0, 0)
            self.set_y(37)
        def footer(self):
            self.set_y(-11)
            self.set_font('Arial', 'I', 7)
            self.set_text_color(120, 120, 120)
            self.cell(0, 5, '%s  |  Issue %s Rev. %s  |  %s laboratory controlled document - generated from the live inventory on %s' % (doc_no, issue_no, rev_no, loc, today), 0, 0, 'C')
            self.set_text_color(0, 0, 0)
    W = [9, 46, 20, 20, 22, 28, 17, 18, 18, 17, 12, 28, 22]
    HD = ['S.NO', 'Item / Chemical', 'Grade', 'CAS No', 'Lot / Batch', 'Supplier', 'PO Ref', 'Received', 'Expiry', 'Balance', 'Unit', 'Storage', 'Status']
    AL = ['C', 'L', 'L', 'C', 'L', 'L', 'C', 'C', 'C', 'C', 'C', 'L', 'C']
    pdf = _P('L', 'mm', 'A4')
    pdf.alias_nb_pages('{nb}')
    pdf.set_auto_page_break(False)
    pdf.add_page()
    def fit(s, w):
        s = str(s)
        if pdf.get_string_width(s) <= w - 2.2:
            return s
        while s and pdf.get_string_width(s + '...') > w - 2.2:
            s = s[:-1]
        return s + '...'
    def head_row():
        pdf.set_font('Arial', 'B', 6.6)
        pdf.set_fill_color(229, 231, 235)
        for w, h in zip(W, HD):
            pdf.cell(w, 6, h, 1, 0, 'C', True)
        pdf.ln()
    def band(title):
        pdf.set_font('Arial', 'B', 8.5)
        pdf.set_fill_color(31, 41, 55)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(sum(W), 6.5, ' ' + title, 1, 1, 'L', True)
        pdf.set_text_color(0, 0, 0)
    if not groups:
        pdf.set_font('Arial', 'I', 10)
        pdf.cell(0, 10, 'No stock recorded yet for the %s laboratory.' % loc, 0, 1, 'C')
    sr = 0
    for title, rows in groups:
        if pdf.get_y() > 165:
            pdf.add_page()
        band(title.upper())
        head_row()
        pdf.set_font('Arial', '', 7)
        odd = False
        for r in rows:
            if pdf.get_y() > 186:
                pdf.add_page()
                band(title.upper() + ' (continued)')
                head_row()
                pdf.set_font('Arial', '', 7)
            sr += 1
            vals = [str(sr), r['name'], r['grade'], r['cas'], r['lot_no'], r['supplier'], r['po_ref'],
                    r['received'], r['expiry'], ('%g' % r['balance']), r['unit'], r['storage'], r['status']]
            if odd:
                pdf.set_fill_color(245, 247, 249)
            for i, (w, v) in enumerate(zip(W, vals)):
                if i == 8 and r['exp_state'] == 'Expired':
                    pdf.set_text_color(190, 0, 0)
                    pdf.set_font('Arial', 'B', 7)
                    pdf.cell(w, 5.5, fit(v, w), 1, 0, AL[i], odd)
                    pdf.set_text_color(0, 0, 0)
                    pdf.set_font('Arial', '', 7)
                else:
                    pdf.cell(w, 5.5, fit(v, w), 1, 0, AL[i], odd)
            pdf.ln()
            odd = not odd
        pdf.ln(3)
    out = pdf.output(dest='S')
    b = bytes(out) if isinstance(out, (bytes, bytearray)) else out.encode('latin-1')
    resp = HttpResponse(b, content_type='application/pdf')
    resp['Content-Disposition'] = 'inline; filename="%s Chemical Inventory %s.pdf"' % (doc_no, loc)
    return resp
