"""Karachi 13-10-2026: CRM / RM baseline-study records and Working Standard charts (Jan-Sep 2026)."""
import json, re, statistics as st, datetime as dt
from collections import defaultdict

D = json.load(open('/home/claude/k13/out.json'))
ANOM = []


def vals(x, col='c'):
    return [r[col] for r in x['rows'] if r[col] is not None]


def dates(x):
    return [r['date'] for r in x['rows'] if r['c'] is not None]


def sheet(file_part, sheet_name, kind):
    hits = [x for x in D if file_part in x['file'] and x['sheet'].strip() == sheet_name.strip() and kind in x['file']]
    assert len(hits) == 1, (file_part, sheet_name, len(hits))
    return hits[0]


def study(x, est=None, note=''):
    v, ds = vals(x), dates(x)
    assert len(v) == len(ds) and all(ds), x['sheet']
    return dict(values=v, dates=ds, established_on=est or max(ds), note=note)


# ------------------------------------------------------------------ CRM / RM corrections (production ids)
CRM = [  # (target id, match parameter, equipment_id, file part, sheet)
    (10, 'pH', 'MP-01', 'Alk & PH', 'pH Meter (pH)'),
    (1, 'Alkalinity', '', 'Alk & PH', 'Alkalinity'),
    (16, 'Calcium Hardness', '', 'Calcium-hardness', 'Calcium Hardness'),
    (17, 'Chloride', '', '( Chloride)', 'Chloride'),
    (9, 'COD', 'DB-73 & UV-72', 'Flouride,COD', 'Spectrophotometer (COD)'),
    (3, 'Nitrate', 'UV-72', 'Flouride,COD', 'Spectrophotometer (Nitrate)'),
    (12, 'Sulphate', 'UV-72', 'Flouride,COD', 'Spectrophotometer (Sulphate)'),
    (6, 'Fluoride', 'UV-72', 'Flouride,COD', 'Spectrophotometer (Flouride)'),
    (7, 'Hardness', '', 'Hardness- CRM', 'Hardness'),
    (4, 'TDS (Total Dissolved Solids)', 'DO-07', '2 TDS', '(TDS)'),
]
RM = [
    (145, 'COD', 'COD.xlsx', 'Spectrophotometer (COD)'), (150, 'Iron', 'Fe, Ni', 'Iron'), (151, 'Nickel', 'Fe, Ni', 'Nickel'),
    (152, 'Lead', 'Fe, Ni', 'Lead'), (153, 'Cadmium', 'Fe, Ni', 'Cadmium'), (154, 'Copper', 'Fe, Ni', 'Copper'),
    (155, 'Manganese', 'Fe, Ni', 'Manganese'), (156, 'Zinc', 'Fe, Ni', 'Zinc'), (162, 'Hardness', 'TDS  Hardness', 'Hardness'),
    (163, 'Fluoride', 'TDS  Hardness', '(Flouride)'), (161, 'TDS (Total Dissolved Solids)', 'TDS  Hardness', '(TDS)'),
    (146, 'pH', 'pH SO4', 'pH Meter (pH)'), (147, 'Sulphate', 'pH SO4', 'Spectrophotometer (Sulphate)'),
    (159, 'Alkalinity', 'Alkalinity-Base', 'ALKALINITY'), (158, 'Calcium', 'Calcium, Nitrate', 'Calcium'),
    (160, 'Nitrate', 'Calcium, Nitrate', '(Nitrate)'), (157, 'Chloride', 'Chloride-Base', 'Chloride'),
    (149, 'Magnesium', 'Magnesium Sodium', 'Magnesium'), (148, 'Sodium', 'Magnesium Sodium', 'Sodium'),
]


def head(x):
    return re.sub(r'\s+', ' ', ' '.join(x['head']))


charts = []
for tid, par, eid, fp, sh in CRM:
    x = sheet(fp, sh, 'CRM')
    b = study(x, est='2026-02-28', note='Baseline study - CRM exercise Feb-2026 (laboratory record received 13-10-2026)')
    charts.append(dict(key='CRM %s %s' % (par, eid), activity='CRM', target_id=tid, match=dict(activity='CRM', parameter=par),
                       master={}, keep_current=True, results=[], baselines=[dict(b, key='study', replace_version=1)]))
for tid, par, fp, sh in RM:
    x = sheet(fp, sh, 'RM')
    h = head(x)
    month = 'Jul-2026' if 'July' in h else 'Jun-2026'
    b = study(x, note='Baseline study - RM exercise %s (laboratory record received 13-10-2026)' % month)
    master = {}
    if par in ('Magnesium', 'Sodium'):
        cv = re.search(r'Certified Value:\s*([\d.]+)', h).group(1)
        lo, hi = re.search(r'Acceptance Range:\s*([\d.]+)\s*-\s*([\d.]+)', h).groups()
        det = re.search(r'RM Detail:\s*(.+?)\s*Description', h).group(1)
        master = dict(crm_value=cv, crm_range_low=lo, crm_range_high=hi, crm_detail=det)
    charts.append(dict(key='RM %s' % par, activity='RM', target_id=tid, match=dict(activity='RM', parameter=par),
                       master=master, keep_current=True, results=[], baselines=[dict(b, key='study', replace_version=1)]))

# ------------------------------------------------------------------ Working Standard charts
WS_NOTE_V2 = 'Baseline study - working standard exercise Feb-2026 (laboratory record received 13-10-2026)'
WS_NOTE_V1 = ('Baseline in force in January 2026, as printed on the January 2026 working-standard forms '
              '(the dates of these baseline results are not recorded on the forms)')
SER = [
    # key, sheet title, header method test, parameter, level, unit, equipment, equipment id, method, study (file part, sheet), decimals
    ('Alk50', 'Alkalinity 50 ppm', None, 'Alkalinity', '50 ppm', 'mg/l', '', '', 'ASTM D 1067-16', ('Alk & NO3', 'Alkalinity'), 0),
    ('COD200H', 'COD 200 ppm', 'HACH', 'COD', '200 ppm', 'mg/l', 'Digestor Block & Spectrophotometer', 'DB-73, VS-03', 'HACH 8000',
     ('COD Base Line', 'Spectrophotometer (COD 200)'), 0),
    ('COD200A', 'COD 200 ppm', 'APHA', 'COD', '200 ppm', 'mg/l', 'Digestor Block & UV-Visible Spectrophotometer', 'DB-73, UV-72',
     'APHA 5220 D', ('COD Base Line', 'Spectrophotometer (COD 200) (2)'), 3),
    ('CaH100', 'Calcium Hardness 100 ppm', None, 'Calcium Hardness', '100 ppm', 'mg/l', '', '', 'ASTM D 1126/APHA 3500-Ca-B',
     ('Calcium-hardness', 'Calcium Hardness'), 0),
    ('Cl100', 'Chloride 100 ppm', None, 'Chloride', '100 ppm', 'mg/l', '', '', 'APHA 4500 Cl- B', ('( Chloride)', 'Chloride'), 2),
    ('NO3H', 'Nitrate 1 ppm', 'HACH', 'Nitrate', '1 ppm', 'mg/l', 'Spectrophotometer', 'VS-03', 'HACH 8039',
     ('Alk & NO3', 'Spectrophotometer (Nitrate) (2)'), 1),
    ('NO3A', 'Nitrate 1 ppm', 'APHA', 'Nitrate', '1 ppm', 'mg/l', 'UV-Visible Spectrophotometer', 'UV-72', 'APHA 4500 NO3-B',
     ('Alk & NO3', 'Spectrophotometer (Nitrate)'), 3),
    ('SO4H', 'Sulphate 20 ppm', 'HACH', 'Sulphate', '20 ppm', 'mg/l', 'Spectrophotometer', 'VS-03', 'HACH 8051',
     ('SO4 Base', 'Spectrophotometer (Sulphate 20)'), 0),
    ('SO4A', 'Sulphate 20 ppm', 'APHA', 'Sulphate', '20 ppm', 'mg/l', 'UV-Visible Spectrophotometer', 'UV-72', 'APHA 4500 SO4-E',
     ('SO4 Base', 'Spectrophotometer (Sulphate (2)'), 3),
    ('TDS500', 'TDS 500 ppm', None, 'TDS (Total Dissolved Solids)', '500 ppm', 'mg/l', 'Drying Oven, Analytical Balance, Water Bath',
     'DO-07, AB-02, WB-08', 'APHA 2540 C', ('Flouride , TDS', 'TDS'), 0),
    ('pH4', 'pH 4.004', None, 'pH', '4.004', '', 'Multiparameter Meter', 'MP-01', 'APHA 4500 H B', ('pH Base', 'pH Meter (pH 4.004)'), 2),
    ('pH7', 'pH 7.415', None, 'pH', '7.415', '', 'Multiparameter Meter', 'MP-01', 'APHA 4500 H B', ('pH Base', 'pH Meter (pH 7.415)'), 2),
    ('pH10', 'pH 10.014', None, 'pH', '10.014', '', 'Multiparameter Meter', 'MP-01', 'APHA 4500 H B', ('pH Base', 'pH Meter (pH 10.014)'), 2),
    ('FH', 'Fluoride 0.5 ppm', 'HACH', 'Fluoride', '0.5 ppm', 'mg/l', 'Spectrophotometer', 'VS-03', 'HACH 8029',
     ('Flouride , TDS', 'Spectrophotometer (Fluoride (2)'), 2),
    ('FA', 'Fluoride 0.5 ppm', 'APHA', 'Fluoride', '0.5 ppm', 'mg/l', 'UV-Visible Spectrophotometer', 'UV-72', 'APHA 4500 F-D',
     ('Flouride , TDS', 'Spectrophotometer (Fluoride)'), 3),
    # January-only standards (different concentrations)
    ('COD100', 'COD 100 ppm', None, 'COD', '100 ppm', 'mg/l', 'COD Reactor & Spectrophotometer', 'CR-04, VS-03', 'HACH 8000', None, 0),
    ('SO4_60', 'Sulphate 60 ppm', None, 'Sulphate', '60 ppm', 'mg/l', 'Spectrophotometer', 'VS-03', 'HACH 8051', None, 0),
]
MONTH_OF = {'WS jan 2026': 1, '1. Feb 2026': 2, '2. March 2026': 3, '3.April 2026': 4, '4. May 2026': 5, '5. Jun 2026': 6,
            '6. July 2026': 7, '7. Aug 2026': 8, '8. Sep 2026': 9}


def ws_sheets(title, mtest):
    out = []
    for x in D:
        if 'WS Results' not in x['file'] or x['sheet'].replace(' (2)', '').strip() != title:
            continue
        h = head(x)
        meth = re.search(r'Method\s*:[\s_]*([A-Z]+)', h).group(1)
        if mtest and not meth.startswith(mtest):
            continue
        out.append(x)
    return out


def hdr_field(h, pat):
    m = re.search(pat, h)
    return m.group(1).strip(' _,') if m else None


for key, title, mtest, par, level, unit, eq, eid, meth, stu, dec in SER:
    sheets = ws_sheets(title, mtest)
    assert sheets, key
    h0 = head(sheets[-1])
    cv = hdr_field(h0, r'\(C\.V\)\s*:[\s_]*([\d.]+)')
    rng = None
    for x in sheets:
        rng = hdr_field(head(x), r'RANGE\s*:\s*([\d.]+\s*-\s*[\d.]+)') or rng
    lo, hi = [s.strip() for s in rng.split('-')]
    detail = hdr_field(h0, r'Working Standard Detail\s*:\s*(.+?)\s*(?:Working|$)')
    detail = re.sub(r'WS-\s*-?\s*', 'WS-', detail).replace(' -200', ' 200').replace('-200', ' 200')
    bl = []
    jan = [x for x in sheets if x['dir'] == 'WS jan 2026']
    if jan:
        jv = vals(jan[0], 'd')
        tail = ' '.join(jan[0]['tail'])
        jm = float(re.search(r'Mean \(Base Line\)\s*([\d.]+)', tail).group(1))
        js = float(re.search(r'Standard Deviation \(Base Line\)\s*([\d.]+)', tail).group(1))
        if len(jv) >= 12:
            assert abs(st.mean(jv) - jm) < 1e-6 and abs(st.stdev(jv) - js) < 1e-6, (key, jv, jm, js)
            bl.append(dict(key='jan', established_on='2025-12-31', values=jv, dates=[], note=WS_NOTE_V1))
        else:
            bl.append(dict(key='jan', established_on='2025-12-31', values=[], dates=[], stats_only=True, mean=jm, sd=js, n=0,
                           note=WS_NOTE_V1 + '; only %d of the baseline results are printed - mean and SD as stated on the form' % len(jv)))
            ANOM.append('%s: January form prints only %d baseline results; January baseline kept as stated mean %.4g / SD %.4g' % (key, len(jv), jm, js))
    if stu:
        sx = sheet(stu[0], stu[1], 'WS Excercise')
        b = study(sx, note=WS_NOTE_V2)
        bl.append(dict(b, key='feb'))
        # check the monthly forms print the same baseline
        for x in sheets:
            if x['dir'] == 'WS jan 2026':
                continue
            pv = vals(x, 'd')
            if pv and pv != b['values'][:len(pv)]:
                ANOM.append('%s %s: baseline column on the monthly form (mean %.5g) differs from the baseline study (mean %.5g) - study used'
                            % (key, x['dir'], st.mean(pv), st.mean(b['values'])))
    own = set()     # (date, value) rows printed on the form of their own month
    for x in sheets:
        for r in x['rows']:
            if r['c'] is not None and r['date'] and int(r['date'][5:7]) == MONTH_OF[x['dir']] and r['date'][:4] == '2026':
                own.add((r['date'], r['c']))
    carried = defaultdict(int)
    res = []
    for x in sorted(sheets, key=lambda x: (MONTH_OF[x['dir']], x['sheet'])):
        mon = MONTH_OF[x['dir']]
        for r in x['rows']:
            if r['c'] is None:
                continue
            d0 = r['date']
            if not d0:
                ANOM.append('%s %s row %d: result %s without a date - not imported' % (key, x['dir'], r['sno'], r['craw']))
                continue
            d = dt.date.fromisoformat(d0)
            remark = ''
            if d.year != 2026 or d.month != mon:
                if (d0, r['c']) in own:
                    carried[x['dir']] += 1          # row carried over from an earlier month's form - already recorded there
                    continue
                if d.year < 2026 and mon == 1:
                    ANOM.append('%s January form row %d: result %s dated %s (2025) left on the template - not imported'
                                % (key, r['sno'], r['craw'], d.strftime('%d-%m-%Y')))
                    continue
                fixed = None
                for cand in ((2026, mon, d.day), (2026, mon, d.month)):
                    try:
                        fixed = dt.date(*cand)
                        break
                    except ValueError:
                        pass
                ANOM.append('%s %s row %d: date printed %s on the %s form - recorded as %s' % (
                    key, x['dir'], r['sno'], d.strftime('%d-%m-%Y'), dt.date(2026, mon, 1).strftime('%B'), fixed.strftime('%d-%m-%Y')))
                remark = '[Date printed on the form as %s; recorded in the %s form]' % (d.strftime('%d-%m-%Y'), fixed.strftime('%B %Y'))
                d = fixed
            res.append(dict(date=d.isoformat(), value=r['c'], baseline='jan' if mon == 1 else 'feb', remark=remark))
    for k, n in carried.items():
        ANOM.append('%s %s form: %d row(s) repeat results of an earlier month (same date and value) - not imported twice' % (key, k, n))
    # duplicate dates
    seen = defaultdict(list)
    for r in res:
        seen[r['date']].append(r['value'])
    for k, v in seen.items():
        if len(v) > 1:
            ANOM.append('%s: %d results dated %s (%s) - only the first is kept (one result per date)' % (key, len(v), k, v))
    keep, used = [], set()
    for r in res:
        if r['date'] in used:
            continue
        used.add(r['date'])
        keep.append(r)
    charts.append(dict(key='WS ' + key, activity='WS', target_id=None,
                       match=dict(activity='WS', parameter=par, level=level, equipment_id=eid),
                       master=dict(parameter=par, level=level, unit=unit, equipment=eq, equipment_id=eid, method=meth, crm_detail=detail,
                                   crm_value=cv, crm_range_low=lo, crm_range_high=hi, decimals=dec,
                                   description='Working Standard Results during Monthly Exercise', start_month=1),
                       baselines=bl, results=keep, coverage_months=[]))

spec = dict(location='Karachi', created='2026-10-13', charts=charts)
json.dump(spec, open('karachi_baselines_ws_2026_spec.json', 'w'), separators=(',', ':'))
for c in charts:
    if c['activity'] == 'WS':
        print('%-10s %-30s %-8s %-14s res=%3d  baselines=%s' % (c['key'], c['master']['parameter'], c['master']['level'], c['master']['equipment_id'],
              len(c['results']), ','.join('%s(n=%d)' % (b['key'], len(b['values'])) for b in c['baselines'])))
print('\nANOMALIES (%d)' % len(ANOM))
for a in ANOM:
    print(' -', a)
