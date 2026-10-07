"""Seed CRM control charts from the laboratory's Excel control-chart workbooks
(form ETAL-LAB-604-FF-11, one sheet per parameter / level / instrument).

    python manage.py seed_control_charts <folder-with-xlsx | charts.json> --location Karachi [--dry-run]
    python manage.py seed_control_charts --export charts.json <folder-with-xlsx>   # parse only, write JSON

A JSON file (list of parsed sheets, as written by --export) can be used instead of
the workbooks, e.g. on a server without the Excel files.

Idempotent: a chart is matched on (location, activity, parameter, level,
equipment_id); an existing chart is left untouched (reported as 'exists').
Baseline values are the 'Results For Base Line' column (D) of each sheet; the
monthly results column is NOT imported (owner decision, 07-10-2026).
"""
import glob
import os
import re
import datetime

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from QC.models import ControlChart, ControlChartBaseline


def _clean(s):
    return re.sub(r'\s+', ' ', (s or '').replace('_', ' ')).strip(' ,:')


def parse_sheet(ws):
    """Return a dict describing one control-chart sheet, or None if it is not one."""
    hdr7 = [str(c.value or '') for c in ws[7]]
    if not any('Base Line' in h for h in hdr7):
        return None
    a3, a4, a5 = (str(ws['A3'].value or ''), str(ws['A4'].value or ''), str(ws['A5'].value or ''))
    eq = re.search(r'Equipment\s*:_*\s*([^_]+?)\s*_', a3)
    eid = re.search(r'ID:_*\s*([A-Za-z0-9\-]+)', a3)
    par = re.search(r'Parameter:_*\s*([^_]+?)_', a4)
    meth = re.search(r'Method\s*:\s*_*([^_,]+?)\s*[_,]', a4 + '_')
    crm = re.search(r'CRM Detail:\s*(.+)', a4)
    cv = re.search(r'CRM \((?:C\.V|Value)\):_*\s*([\d.]+)', a5)
    rng = re.search(r'RANGE:\s*([\d.]+)\s*-\s*([\d.]+)\s*([A-Za-z/]*)', a5)
    unit = ''
    u = re.search(r'Results\s*\(([^)]+)\)', ' '.join(hdr7))
    if u:
        unit = u.group(1).strip()
    elif rng and rng.group(3):
        unit = rng.group(3)
    base = []
    for r in range(8, ws.max_row + 1):
        a = ws.cell(r, 1).value
        if isinstance(a, str) and a.strip().lower().startswith(('mean', 'standard')):
            break
        d = ws.cell(r, 4).value
        if isinstance(d, (int, float)):
            base.append(float(d))
    parameter = _clean(par.group(1)) if par else _clean(ws.title)
    parameter = re.split(r'\s+Method\b', parameter)[0].strip(' ,')
    parameter = re.sub(r'\s*\(\s*[\d.]+\s*ppm\s*\)\s*', '', parameter, flags=re.I).strip()  # "(1ppm)" lives in level
    if parameter.lower() == 'ph':
        unit = ''
    level = ''
    m = re.search(r'([\d.]+)\s*ppm', ws.title, flags=re.I)
    if m:
        level = ('%g ppm' % float(m.group(1)))
    equipment = _clean(eq.group(1)) if eq else ''
    if equipment.lower().startswith('not applicable'):
        equipment = 'Not Applicable'
    return dict(
        parameter=parameter, level=level, unit=('' if parameter.lower() == 'ph' else (unit or 'mg/l')),
        equipment=equipment, equipment_id=(eid.group(1) if eid and eid.group(1) != '-' else ''),
        method=re.split(r'\s*CRM Detail', _clean(meth.group(1)))[0].strip(' ,') if meth else '',
        crm_detail=_clean(crm.group(1)) if crm else '',
        crm_value=('%g' % float(cv.group(1))) if cv else '', crm_range_low=rng.group(1) if rng else '',
        crm_range_high=rng.group(2) if rng else '', baseline=base, sheet=ws.title,
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
        created = exists = 0
        with transaction.atomic():
            for f, d in sheets:
                if True:
                    key = dict(location=o['location'], activity='CRM', parameter=d['parameter'],
                               level=d['level'], equipment_id=d['equipment_id'])
                    if ControlChart.objects.filter(**key).exists():
                        exists += 1
                        self.stdout.write('exists  %-22s %-8s %-6s' % (d['parameter'], d['level'], d['equipment_id']))
                        continue
                    dec = 4 if d['equipment_id'] == 'AS-13' else (3 if d['parameter'].lower().startswith(('ph', 'fluor', 'nitr')) else 2)
                    self.stdout.write('create  %-22s %-8s %-6s n=%d  %s' % (
                        d['parameter'], d['level'], d['equipment_id'], len(d['baseline']), str(f)[-40:]))
                    if o['dry_run']:
                        continue
                    fields = {k: v for k, v in d.items() if k not in ('baseline', 'sheet', 'source')}
                    fields.update(key)
                    ch = ControlChart.objects.create(decimals=dec, **fields)
                    b = ControlChartBaseline(chart=ch, version=1, established_on=est, values=d['baseline'],
                                             note='February 2026 intermediate check (seeded from Excel sheet "%s")' % d['sheet'])
                    b.compute(); b.save()
                    created += 1
            if o['dry_run']:
                transaction.set_rollback(True)
        self.stdout.write(self.style.SUCCESS('%s: %d created, %d already existed' % (
            'DRY RUN' if o['dry_run'] else 'DONE', created, exists)))
