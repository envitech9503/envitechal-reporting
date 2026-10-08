"""Seed control charts from the laboratory's Excel control-chart workbooks
(form ETAL-LAB-604-FF-11, one sheet per parameter / level / instrument).
Recognises three sheet layouts (08-10-2026): CRM (monthly results + baseline
column), RM (weekly results + baseline column) and Intermediate Check (one
monthly run of readings; limits from the run itself, no baseline).

    python manage.py seed_control_charts <folder-with-xlsx | charts.json> --location Karachi [--dry-run]
    python manage.py seed_control_charts --export charts.json <folder-with-xlsx>   # parse only, write JSON

A JSON file (list of parsed sheets, as written by --export) can be used instead of
the workbooks, e.g. on a server without the Excel files.

Idempotent: a chart is matched on (location, activity, parameter, level,
equipment_id); an existing chart is left untouched (reported as 'exists').
Baseline values are the 'Results For Base Line' column (D) of each sheet; the
monthly results column is parsed into 'results' ([date, value] pairs) but only
imported when --with-results is given (owner decision 07-10-2026: real data only).
"""
import glob
import os
import re
import datetime

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from QC.models import ControlChart, ControlChartBaseline, ControlChartResult, run_limits, classify_value


def _clean(s):
    return re.sub(r'\s+', ' ', (s or '').replace('_', ' ')).strip(' ,:')


def _find_header(ws):
    """Return (header_row, col_offset, headers) - the row holding 'Date' and the
    0-based column offset (the IC sheets start in column B)."""
    for r in range(5, 10):
        cells = [str(ws.cell(r, c).value or '') for c in range(1, 14)]
        for off, h in enumerate(cells[:3]):
            if h.strip().lower().startswith('s. no') or h.strip().lower().startswith('s.no'):
                return r, off, cells[off:]
    return None, 0, []


def _num(v):
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        try:
            return float(v.replace(',', '').strip())
        except ValueError:
            return None
    return None


def _grab(text, label_rx, stop_rx=r'\s{2,}|_{2,}|$'):
    """Value after `label_rx` up to a double space / underscore run / end."""
    m = re.search(label_rx + r'\s*:?\s*_*\s*(.+?)(?=' + stop_rx + ')', text)
    return _clean(m.group(1)) if m else ''


def parse_sheet(ws):
    """Return a dict describing one control-chart sheet (CRM, RM or IC), or None."""
    hr, off, hdr = _find_header(ws)
    if hr is None:
        return None
    hdr_join = ' '.join(hdr)
    rows_text = [str(ws.cell(r, 1 + off).value or '') for r in range(1, hr)]
    text = '  '.join(rows_text)
    text = re.sub(r'[\u00a0]', ' ', text)
    is_ic = bool(re.search(r'Intermediate check', text, re.I)) or bool(re.search(r'^Month\s*:', rows_text[2] if len(rows_text) > 2 else '', re.I))
    is_rm = (not is_ic) and bool(re.search(r'\bRM (Detail|\(C\.V)|RM RANGE|RM Results', text))
    activity = 'IC' if is_ic else ('RM' if is_rm else 'CRM')
    ref = 'CRM/RM' if is_ic else activity

    equipment = _grab(text, r'Name of Equipment', r'\s{2,}|_{2,}|Equipment ID|$')
    equipment = re.split(r'\s*Equipment ID', equipment)[0].strip(' _,:')
    eid = _grab(text, r'Equipment ID', r'\s{2,}|_{2,}|$').strip(' _')
    parameter = _grab(text, r'Parameter', r'\s{2,}|_{2,}|\s+Method\b|$')
    parameter = re.split(r'\s+Method\b', parameter)[0].strip(' ,_')
    method = _grab(text, r'Method', r'\s{2,}|_{2,}|,|CRM|RM Detail|$').strip(' _,')
    if method.lower().startswith('not applicable'):
        method = 'Not Applicable'
    detail = _grab(text, r'(?:CRM|RM) Detail', r'\s{3,}|_{2,}|\s+(?:CRM|RM)\s*\(|$')
    m = re.search(r'(?:Certified|Diluted) Value\s*:\s*_*\s*([\d.]+)', text) or re.search(r'(?:CRM|RM)\s*\((?:C\.V|Value)\)\s*:\s*_*\s*([\d.]+)', text)
    cv = ('%g' % float(m.group(1))) if m else ''
    m = re.search(r'(?:RANGE|Range)\s*:\s*_*\s*([\d.]+)\s*[-\u2013]\s*([\d.]+)\s*([A-Za-z/]*)', text)
    rlo, rhi, runit = (m.group(1), m.group(2), m.group(3)) if m else ('', '', '')
    unit = ''
    u = re.search(r'Results\s*\(([^)]+)\)', hdr_join)
    if u:
        unit = u.group(1).strip()
    elif runit:
        unit = runit
    unit = {'mg/L': 'mg/l'}.get(unit, unit)
    desc = _grab(text, r'Description', r'_{2,}|\s{3,}|$').strip(' _')
    month = None
    m = re.search(r'Month\s*:\s*_*\s*([A-Za-z]{3,9})[\s_-]*(\d{2,4})', text)
    if m:
        try:
            mo = datetime.datetime.strptime(m.group(1)[:3], '%b').month
            yr = int(m.group(2)); yr = yr + 2000 if yr < 100 else yr
            month = '%04d-%02d' % (yr, mo)
        except ValueError:
            pass
    base, results = [], []
    c_date, c_val, c_base = 2 + off, 3 + off, 4 + off
    has_base = any('Base Line' in h for h in hdr)
    for r in range(hr + 1, ws.max_row + 1):
        a = ws.cell(r, 1 + off).value
        if isinstance(a, str) and a.strip().lower().startswith(('mean', 'standard')):
            break
        if has_base:
            d = _num(ws.cell(r, c_base).value)
            if d is not None:
                base.append(d)
        dt, mv = ws.cell(r, c_date).value, _num(ws.cell(r, c_val).value)
        if isinstance(dt, datetime.datetime) and mv is not None:
            results.append([dt.date().isoformat(), mv])
    # parameter / level clean-up
    parameter = re.sub(r'\s*\(\s*[\d.]+\s*ppm\s*\)\s*', '', parameter, flags=re.I).strip()
    parameter = re.sub(r'\(\s*', '(', parameter); parameter = re.sub(r'\s*\)', ')', parameter)
    parameter = re.sub(r'(\w)\(', r'\1 (', parameter)
    if parameter.lower() in ('ph',):
        parameter, unit = 'pH', ''
    parameter = parameter.replace('Flouride', 'Fluoride').replace('Mangnese', 'Manganese').replace('Temperture', 'Temperature')
    parameter = re.sub(r'Temperature\s*°C', 'Temperature', parameter)
    if unit in ('°C', 'gm', 'g'):
        unit = 'g' if unit == 'gm' else unit
        parameter = 'Temperature' if unit == '°C' else 'Weight'
    level = ''
    m = re.search(r'([\d.]+)\s*ppm', ws.title, flags=re.I)
    if m:
        level = ('%g ppm' % float(m.group(1)))
    if equipment.lower().startswith('not applicable') or equipment.upper() in ('N/A', 'NA', '-'):
        equipment = 'Not Applicable'
    if eid.upper() in ('N/A', 'NA'):
        eid = ''
    equipment = re.sub(r'Spectrophotomter|Spectrphotometer|Spectrophotmeter', 'Spectrophotometer', equipment)
    equipment = equipment.replace('Spectrophotometer(AAS)', 'Spectrophotometer (AAS)')
    if is_ic and not level:
        m = re.search(r'\(\s*([\d.]+)\s*gm?\s*\)', ws.title)
        if m:
            level = '%g g' % float(m.group(1))
    if is_ic and month is None and results:
        month = results[0][0][:7]
    return dict(
        activity=activity, parameter=parameter, level=level, unit=unit if unit or parameter == 'pH' else 'mg/l',
        equipment=equipment, equipment_id=(eid if eid and eid != '-' else ''),
        method=re.split(r'\s*(?:CRM|RM) Detail', method)[0].strip(' ,'),
        crm_detail=detail, crm_value=cv, crm_range_low=rlo, crm_range_high=rhi,
        description=desc, run_month=month, baseline=base, results=results, sheet=ws.title, ref_label=ref,
    )


class Command(BaseCommand):
    help = __doc__

    def add_arguments(self, parser):
        parser.add_argument('folder')
        parser.add_argument('--location', default='Karachi')
        parser.add_argument('--dry-run', action='store_true')
        parser.add_argument('--established', default='2026-02-28',
                            help='baseline established_on date (YYYY-MM-DD)')
        parser.add_argument('--export', default='', help='write the parsed sheets to this JSON file and stop')
        parser.add_argument('--with-results', action='store_true',
                            help='also import the monthly results found in the sheets (one per month; existing months kept)')

    def handle(self, *args, **o):
        import json
        sheets = []   # list of (source_label, parsed dict)
        if o['folder'].lower().endswith('.json'):
            for d in json.load(open(o['folder'])):
                sheets.append((d.get('source', 'json'), d))
        else:
            import openpyxl
            files = sorted(glob.glob(os.path.join(o['folder'], '*.xlsx')))
            if not files:
                raise CommandError('no .xlsx files in %s' % o['folder'])
            for f in files:
                wb = openpyxl.load_workbook(f, data_only=True)
                for ws in wb.worksheets:
                    d = parse_sheet(ws)
                    if d:
                        d['source'] = os.path.basename(f)
                        sheets.append((os.path.basename(f), d))
        if o['export']:
            json.dump([d for _, d in sheets], open(o['export'], 'w'), indent=1)
            self.stdout.write(self.style.SUCCESS('exported %d sheets to %s' % (len(sheets), o['export'])))
            return
        est = datetime.date.fromisoformat(o['established'])
        created = exists = imported = 0
        with transaction.atomic():
            for f, d in sheets:
                if True:
                    act = d.get('activity') or 'CRM'
                    key = dict(location=o['location'], activity=act, parameter=d['parameter'],
                               level=d['level'], equipment_id=d['equipment_id'])
                    ch = ControlChart.objects.filter(**key).first()
                    if ch is not None:
                        exists += 1
                        self.stdout.write('exists  %-22s %-8s %-6s' % (d['parameter'], d['level'], d['equipment_id']))
                        if o['with_results'] and not o['dry_run']:
                            imported += self._import_results(ch, d.get('results') or [])
                        elif o['with_results']:
                            imported += len(d.get('results') or [])
                        continue
                    dec = 4 if (d['equipment_id'] == 'AS-13' or d['parameter'].lower().startswith('weight')) else (3 if d['parameter'].lower().startswith(('ph', 'fluor', 'nitr')) else 2)
                    self.stdout.write('create  %-22s %-8s %-6s n=%d  %s' % (
                        d['parameter'], d['level'], d['equipment_id'], len(d['baseline']), str(f)[-40:]))
                    if o['dry_run']:
                        continue
                    fields = {k: v for k, v in d.items() if k not in ('baseline', 'results', 'sheet', 'source', 'run_month', 'ref_label', 'activity')}
                    fields.update(key)
                    if not fields.get('description'):
                        fields['description'] = {'RM': 'RM Results during Weekly RM Exercise', 'IC': 'Control chart of Intermediate check'}.get(act, 'CRM Results during Monthly CRM Exercise')
                    ch = ControlChart.objects.create(decimals=dec, **fields)
                    if d['baseline']:
                        b_est = est
                        if act == 'RM' and d.get('results'):
                            try:   # RM baseline = the July exercise: date it just before the first weekly result
                                b_est = min(datetime.date.fromisoformat(x[0]) for x in d['results']) - datetime.timedelta(days=1)
                            except Exception:
                                pass
                        b = ControlChartBaseline(chart=ch, version=1, established_on=b_est, values=d['baseline'],
                                                 note=('February 2026 intermediate check' if act == 'CRM' else 'Baseline of the RM exercise')
                                                      + ' (seeded from Excel sheet "%s")' % d['sheet'])
                        b.compute(); b.save()
                    created += 1
                    if o['with_results']:
                        imported += self._import_results(ch, d.get('results') or [])
            if o['dry_run']:
                transaction.set_rollback(True)
        self.stdout.write(self.style.SUCCESS('%s: %d created, %d already existed, %d monthly results imported' % (
            'DRY RUN' if o['dry_run'] else 'DONE', created, exists, imported)))

    def _import_results(self, ch, results):
        """Import [date, value] pairs: CRM one per calendar month, RM / IC one per
        date (existing ones kept). CRM / RM status is judged against the current
        baseline; IC readings are judged against their month's run afterwards.
        Warning / OOC rows get a note that no remark was recorded in the workbook."""
        b = ch.current_baseline() if not ch.self_limited else None
        n = 0
        touched = set()
        for iso, val in results:
            d = datetime.date.fromisoformat(iso)
            if ch.cadence == 'monthly':
                if ControlChartResult.objects.filter(chart=ch, date__year=d.year, date__month=d.month).exists():
                    continue
            elif ControlChartResult.objects.filter(chart=ch, date=d).exists():
                continue
            st = b.classify(val) if b else 'ok'
            ControlChartResult.objects.create(
                chart=ch, baseline=b, date=d, value=val, status=st,
                remark='' if st == 'ok' else 'Imported from the Excel workbook - no remark was recorded there.')
            touched.add((d.year, d.month))
            n += 1
        if ch.self_limited:
            for y, m in touched:
                rs = list(ControlChartResult.objects.filter(chart=ch, date__year=y, date__month=m))
                lim = run_limits([r.value for r in rs])
                for r in rs:
                    st = classify_value(lim, r.value)
                    ControlChartResult.objects.filter(pk=r.pk).update(
                        status=st, remark='' if st == 'ok' else 'Imported from the Excel workbook - no remark was recorded there.')
        for r in ControlChartResult.objects.filter(chart=ch).order_by('date'):
            self.stdout.write('   result %s %s -> %s' % (r.date.strftime('%d-%m-%Y'), r.value, r.status))
        return n
