"""EnviTechAL management dashboard - rebuilt 12-07-2026 (fast, cached)."""
import json
from calendar import monthrange
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


def _period(filter_type, now):
    if filter_type == 'yearly':
        start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        end = now
    elif filter_type == 'quarterly':
        qm = 3 * ((now.month - 1) // 3) + 1
        start = now.replace(month=qm, day=1, hour=0, minute=0, second=0, microsecond=0)
        end = now
    else:
        start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end = now
    return Q(created_at__range=[start, end])


def _late_reports(date_filter, limit=15):
    sample_map = {}
    for sid, inp9 in Sample_registration.objects.exclude(inp9__isnull=True).exclude(inp9='').values_list('sample_id', 'inp9'):
        sample_map[sid] = inp9
    out = []
    for name, model in REPORT_MODELS.items():
        try:
            rows = model.objects.filter(date_filter).values('sample_id', 'reporting_date', 'report_to', 'lab_report_no')
        except Exception:
            continue
        for r in rows:
            try:
                est_raw = sample_map.get(r.get('sample_id'))
                if not est_raw or not r.get('reporting_date'):
                    continue
                est = datetime.strptime(est_raw, '%d-%m-%Y').date()
                act = datetime.strptime(r['reporting_date'].replace('-', ' '), '%d %B %Y').date()
                if act > est:
                    out.append({'type': name, 'sample_id': r.get('sample_id'),
                                'client': r.get('report_to') or '', 'lab_no': r.get('lab_report_no') or '',
                                'estimated': est.strftime('%d-%m-%Y'), 'actual': act.strftime('%d-%m-%Y'),
                                'days_late': (act - est).days})
            except Exception:
                continue
    out.sort(key=lambda x: -x['days_late'])
    return out[:limit]


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
@csrf_exempt
def get_reports_data(request):
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Administrator access required'}, status=403)
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8'))
        except Exception:
            body = {}
    else:
        body = request.GET.dict()
    filter_type = body.get('filter', 'monthly')
    if filter_type not in ('monthly', 'quarterly', 'yearly'):
        filter_type = 'monthly'
    ck = 'etal_dash_%s' % filter_type
    cached = cache.get(ck)
    if cached:
        return JsonResponse(cached)
    now = timezone.localtime()
    date_filter = _period(filter_type, now)
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
    try: samples = Sample_registration.objects.filter(date_filter).count()
    except Exception: samples = 0
    try: jobs = JobCompletionForm.objects.filter(date_filter).count()
    except Exception: jobs = 0
    week_ago = now - timedelta(days=7)
    activity_7d = 0
    for model in list(REPORT_MODELS.values()) + list(CERT_MODELS.values()):
        try: activity_7d += model.history.filter(history_date__gte=week_ago).count()
        except Exception: continue
    payload = {
        'filter': filter_type,
        'reports_data': reports_data,
        'certs_data': certs_data,
        'totals': {'reports': sum(reports_data.values()), 'certs': sum(certs_data.values()),
                   'samples': samples, 'jobs': jobs},
        'monthly_reports': monthly_reports, 'monthly_certs': monthly_certs,
        'late_reports': _late_reports(date_filter),
        'approved_total': ApprovalStatus.objects.count(),
        'activity_7d': activity_7d,
        'recent_activity': _recent_activity(),
        'generated_at': now.strftime('%d-%m-%Y %H:%M'),
        'year': now.year,
    }
    cache.set(ck, payload, 300)
    return JsonResponse(payload)
