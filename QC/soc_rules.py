"""Decision rule / statement of conformity - parameter tables and report lookups (26-10-2026).

The drinking-water (DrinkingWaterForm) and waste-water (WasteWaterForm2) test reports keep one text result per
parameter and the specification limits of the standard are printed from the report forms; nothing in those models
carries the measurement uncertainty. This module maps a report's results to the Statement of Conformity Record:
parameter name, method, unit, the SEQS limit as printed, and the expanded uncertainty in force in the MOU register.
"""
import re

# (field of the report, parameter as on the record, unit, SEQS limit as printed, accredited on the report (***), MOU register names)
DW_PARAMS = [
    ('water_sr1', 'pH', '-', '6.5 - 8.5', True, ['ph']),
    ('water_sr2', 'TDS', 'mg/L', '<1000', True, ['tds', 'total dissolved solids']),
    ('water_sr3', 'Hardness', 'mg/L', '<500', True, ['hardness', 'total hardness']),
    ('water_sr4', 'Color', 'TCU', '<= 15', False, ['color', 'colour']),
    ('water_sr5', 'Turbidity', 'NTU', '<= 5', False, ['turbidity']),
    ('water_sr6', 'Nitrite', 'mg/L', '<= 3', False, ['nitrite']),
    ('water_sr7', 'Nitrate', 'mg/L', '<= 50', True, ['nitrate']),
    ('water_sr8', 'Taste', '-', 'Non-Objectionable', False, []),
    ('water_sr9', 'Odor', '-', 'Non-Objectionable', False, []),
    ('water_sr10', 'Chloride', 'mg/L', '<= 250', True, ['chloride']),
    ('water_sr11', 'Fluoride', 'mg/L', '<= 1.5', True, ['fluoride']),
    ('water_sr12', 'Aluminum', 'mg/L', '<= 0.2', False, ['aluminum', 'aluminium']),
    ('water_sr13', 'Nickel', 'mg/L', '<= 0.02', True, ['nickel']),
    ('water_sr14', 'Lead', 'mg/L', '<= 0.05', False, ['lead']),
    ('water_sr15', 'Barium', 'mg/L', '0.7', False, ['barium']),
    ('water_sr16', 'Antimony', 'mg/L', '<= 0.005', False, ['antimony']),
    ('water_sr17', 'Arsenic', 'mg/L', '<= 0.05', False, ['arsenic']),
    ('water_sr18', 'Boron', 'mg/L', '0.3', False, ['boron']),
    ('water_sr19', 'Cadmium', 'mg/L', '0.01', False, ['cadmium']),
    ('water_sr20', 'Chromium', 'mg/L', '<= 0.05', False, ['chromium']),
    ('water_sr21', 'Selenium', 'mg/L', '0.01', False, ['selenium']),
    ('water_sr22', 'Copper', 'mg/L', '2', False, ['copper']),
    ('water_sr23', 'Cyanide', 'mg/L', '<= 0.05', False, ['cyanide']),
    ('water_sr24', 'Mercury', 'mg/L', '<= 0.001', False, ['mercury']),
    ('water_sr25', 'Manganese', 'mg/L', '<= 0.5', False, ['manganese']),
    ('water_sr26', 'Zinc', 'mg/L', '<= 5.0', False, ['zinc']),
    ('water_sr27', 'Residual Chlorine', 'mg/L', '0.2 - 0.5', False, ['residual chlorine', 'chlorine']),
    ('water_sr28', 'Phenolic Compounds', 'mg/L', '-', False, ['phenol']),
]
# waste water: outlet result field, name, unit, SEQS limit (column 1 - inland waters), accredited, MOU names
WW_PARAMS = [
    ('result_1_1', 'Temperature', 'C', '<= 3C', False, ['temperature']),
    ('result_2_2', 'pH', '-', '6-9', True, ['ph']),
    ('result_3_3', 'Sulphide', 'mg/L', '1', False, ['sulphide', 'sulfide']),
    ('result_4_4', 'BOD', 'mg/L', '80', False, ['bod', 'biological oxygen demand', 'biochemical oxygen demand']),
    ('result_5_5', 'COD', 'mg/L', '150', True, ['cod', 'chemical oxygen demand']),
    ('result_6_6', 'TDS', 'mg/L', '3500', True, ['tds', 'total dissolved solids']),
    ('result_7_7', 'TSS', 'mg/L', '200', False, ['tss', 'total suspended solids']),
    ('result_8_8', 'Oil & Grease', 'mg/L', '10', False, ['oil & grease', 'oil and grease']),
    ('result_9_9', 'Cadmium', 'mg/L', '0.1', False, ['cadmium']),
    ('result_10_10', 'Copper', 'mg/L', '1', False, ['copper']),
    ('result_11_11', 'Iron', 'mg/L', '8', False, ['iron']),
    ('result_12_12', 'Lead', 'mg/L', '0.5', False, ['lead']),
    ('result_13_13', 'Manganese', 'mg/L', '1.5', False, ['manganese']),
    ('result_14_14', 'Mercury', 'mg/L', '0.01', False, ['mercury']),
    ('result_15_15', 'Nickel', 'mg/L', '1', False, ['nickel']),
    ('result_16_16', 'Selenium', 'mg/L', '0.5', False, ['selenium']),
    ('result_17_17', 'Chromium', 'mg/L', '1', False, ['chromium']),
    ('result_18_18', 'Zinc', 'mg/L', '5', False, ['zinc']),
    ('result_19_19', 'Arsenic', 'mg/L', '1', False, ['arsenic']),
    ('result_20_20', 'Chlorine', 'mg/L', '1', False, ['chlorine']),
    ('result_21_21', 'Chloride', 'mg/L', '1000', False, ['chloride']),
    ('result_22_22', 'Cyanide', 'mg/L', '1', False, ['cyanide']),
    ('result_23_23', 'Fluoride', 'mg/L', '10', False, ['fluoride']),
    ('result_24_24', 'Ammonia', 'mg/L', '40', False, ['ammonia']),
    ('result_26_26', 'Sulphate', 'mg/L', '600', False, ['sulphate', 'sulfate']),
    ('result_27_27', 'MBAS', 'mg/L', '20', False, ['mbas', 'anionic detergent']),
    ('result_29_29', 'Phenolic Compounds', 'mg/L', '0.1', False, ['phenol']),
    ('result_30_30', 'Boron', 'mg/L', '6', False, ['boron']),
    ('result_31_31', 'Barium', 'mg/L', '1.5', False, ['barium']),
]
# parameters in the accreditation scope (***) per laboratory and report, as printed on the reports / decision-rule formats
ACCREDITED = {('Karachi', 'dw'): {'pH', 'TDS', 'Hardness', 'Nitrate', 'Chloride', 'Fluoride', 'Nickel'},
              ('Karachi', 'ww2'): {'pH', 'COD', 'TDS'},
              ('Lahore', 'dw'): {'pH', 'Turbidity', 'TDS', 'Chloride', 'Hardness', 'Nitrate', 'Alkalinity', 'Sulphate', 'Calcium'},
              ('Lahore', 'ww2'): {'pH', 'TDS', 'Chloride', 'Sulphate'}}
STANDARD = {'SEQS': 'Sindh Environmental Quality Standard 2016', 'PEQS': 'Punjab Environmental Quality Standard 2016',
            'NEQS': 'National Environmental Quality Standard'}


def parse_limit(text):
    """'6-9' / '6.5 - 8.5' / '6 to 9' -> (lower, upper); '<1000' / '<= 250' / '≤ 250' / '150' / '1,000' -> (None, upper);
    '>= 5' / '≥ 5' / '> 5' -> (lower, None); else (None, None)."""
    s = (text or '').strip().replace('\u2264', '<=').replace('\u2265', '>=').replace('\u2013', '-').replace('\u2014', '-')
    s = re.sub(r'(?<=\d),(?=\d{3}\b)', '', s)
    m = re.match(r'^\s*([\d.]+)\s*(?:-|to)\s*([\d.]+)\s*$', s)
    if m:
        return float(m.group(1)), float(m.group(2))
    m = re.match(r'^\s*(?:<=|<|=<)?\s*([\d.]+)\s*$', s)
    if m:
        return None, float(m.group(1))
    m = re.match(r'^\s*(?:>=|>|=>)\s*([\d.]+)\s*$', s)
    if m:
        return float(m.group(1)), None
    return None, None


def limit_text(text, lower, upper):
    """The limit as printed: the text typed / taken from the report when it says what is judged, else rebuilt from the
    lower / upper specification actually used (so the printed limit never contradicts the decision)."""
    t = (text or '').strip()
    if t and parse_limit(t) == (lower, upper):
        return t
    def f(v):
        return ('%.6f' % v).rstrip('0').rstrip('.')
    if lower is not None and upper is not None:
        return '%s - %s' % (f(lower), f(upper))
    if upper is not None:
        return '\u2264 %s' % f(upper)
    if lower is not None:
        return '\u2265 %s' % f(lower)
    return t


def name_matches(name, alias):
    """A parameter / study name matches an alias as a whole word: 'ph' matches 'pH @ 25 C' but not 'Sulphate'."""
    n = re.sub(r'\s+', ' ', (name or '').lower().replace('***', '')).strip()
    a = (alias or '').lower().strip()
    return bool(a) and bool(re.search(r'(^|[^a-z])%s($|[^a-z])' % re.escape(a), n))


def aliases_for(name):
    """MOU-register names of a parameter: its alias list from the DW / WW tables ('TDS' -> tds, total dissolved solids)."""
    n = (name or '').strip().lower()
    out = [n] if n else []
    for table in (DW_PARAMS, WW_PARAMS):
        for f, nm, u, l, acc, names in table:
            if nm.lower() == n or name_matches(name, nm.lower()):
                out += [x for x in [nm.lower()] + list(names) if x not in out]
    return out


def is_accredited(name, acc_set):
    """A report parameter name against the laboratory's accredited set ('Alkalinity as CaCO3' -> Alkalinity)."""
    if not acc_set:
        return False
    n = (name or '').split('(')[0].strip().lower()
    return any(n == a.lower() or n.startswith(a.lower() + ' ') for a in acc_set)


def to_float(text):
    """A report result as a number; '<0.01', 'N.D.', 'Tasteless' -> None."""
    s = str(text if text is not None else '').strip().replace(',', '')
    m = re.match(r'^[+-]?\d+(\.\d+)?$', s)
    return float(s) if m else None


_LT = re.compile(r'^\s*(<|\u2264|&lt;|less than)\s*([+-]?\d+(?:\.\d+)?)\s*$', re.I)


def parse_result(text):
    """A result as (value, text): '7.36' -> (7.36, ''); '<0.0080' -> (0.008, '<0.0080') - a result below the limit of
    quantification is judged at the LOQ and shown as written; 'N.D.' -> (None, '')."""
    s = str(text if text is not None else '').strip().replace(',', '')
    v = to_float(s)
    if v is not None:
        return v, ''
    m = _LT.match(s)
    if m:
        return float(m.group(2)), '<' + m.group(2)
    return None, ''


def mou_u(location, names, value=None):
    """Expanded uncertainty (absolute) in force in the MOU register for a parameter: (U_abs, label, study id).
    Prefers a study of sample kind SAMPLE, then any; when the register gives only a relative U it is applied to the value."""
    from QC.models import MouStudy
    qs = MouStudy.objects.filter(location=location, status='approved')
    best = None
    for s in qs.order_by('-approved_at'):
        p = (s.parameter or '').strip().lower()
        if any(name_matches(p.split('(')[0], n) for n in names):
            if best is None or (s.sample_kind == 'SAMPLE' and best.sample_kind != 'SAMPLE'):
                best = s
    if best is None:
        return None, '', None
    u = best.u_abs
    if (u is None or u == 0) and best.u_exp and value is not None:
        u = best.u_exp * value
    label = 'MOU register: %s v%d (approved %s)' % (' '.join(x for x in (best.parameter, best.level or '') if x), best.version, best.approved_at.strftime('%d-%m-%Y') if best.approved_at else '-')
    return (round(u, 4) if u is not None else None), label, best.pk


def requisition_flags(sample_id):
    """The customer's additional requirements on the sample requisition: (MOU required, SOC required, requisition)."""
    from EnviTechAlApp.models import Sample_registration
    s = Sample_registration.objects.filter(sample_id=sample_id).order_by('-id').first()
    if not s:
        return False, False, None
    return bool(s.checkinp107), bool(s.checkinp110), s


def eligible_samples(location):
    """Sample IDs whose requisition asks for MOU / statement of conformity, newest first, with the reports found."""
    from EnviTechAlApp.models import Sample_registration, DrinkingWaterForm, WasteWaterForm2
    qs = Sample_registration.objects.filter(checkinp110=True) | Sample_registration.objects.filter(checkinp107=True)
    if location:
        qs = qs.filter(city_location__iexact=location) | qs.filter(city_location__isnull=True) | qs.filter(city_location='')
    out, seen = [], set()
    for s in qs.order_by('-id')[:400]:
        sid = (s.sample_id or '').strip()
        if not sid or sid in seen:
            continue
        seen.add(sid)
        dw = DrinkingWaterForm.objects.filter(sample_id=sid).order_by('-id').first()
        ww = WasteWaterForm2.objects.filter(sample_id=sid).order_by('-id').first()
        out.append({'sample_id': sid, 'mou': bool(s.checkinp107), 'soc': bool(s.checkinp110), 'reg': s,
                    'report': ('dw' if dw else 'ww2' if ww else ''), 'report_pk': (dw or ww).pk if (dw or ww) else None,
                    'customer': (dw or ww).report_to if (dw or ww) else '', 'date': s.inp7 or s.inp3 or ''})
    return out


def report_for(sample_id, report_type='', report_pk=None):
    """The test report of a sample: (type, object) - the newest DW or WW report with that sample ID (or the one given)."""
    from EnviTechAlApp.models import DrinkingWaterForm, WasteWaterForm2
    if report_pk and report_type == 'dw':
        r = DrinkingWaterForm.objects.filter(pk=report_pk).first()
        if r:
            return 'dw', r
    if report_pk and report_type == 'ww2':
        r = WasteWaterForm2.objects.filter(pk=report_pk).first()
        if r:
            return 'ww2', r
    if report_type in ('', 'dw'):
        r = DrinkingWaterForm.objects.filter(sample_id=sample_id).order_by('-id').first()
        if r:
            return 'dw', r
    if report_type in ('', 'ww2'):
        r = WasteWaterForm2.objects.filter(sample_id=sample_id).order_by('-id').first()
        if r:
            return 'ww2', r
    return '', None


def report_header(kind, r):
    if kind == 'dw':
        return {'customer': r.report_to or '', 'address': r.address or '', 'attention': r.attention or '', 'lab_report_no': r.lab_report_no or '',
                'collection_date': r.sample_collection_date or '', 'analysis': '%s to %s' % (r.date_of_analysis_from or '', r.date_of_analysis_to or ''),
                'description': r.sample_description or '', 'standard': STANDARD.get((r.select or 'SEQS').upper(), r.select or ''), 'location': r.city_location or ''}
    return {'customer': r.report_to or '', 'address': r.address or '', 'attention': r.attention or '', 'lab_report_no': r.lab_report_no or '',
            'collection_date': r.sample_Col_date or '', 'analysis': '%s to %s' % (r.date_of_analysis_from or '', r.date_of_analysis_to or ''),
            'description': r.sample_desc or '', 'standard': STANDARD.get((r.select or 'SEQS').upper(), r.select or ''), 'location': r.city_location or ''}


def report_parameters(kind, r, location):
    """Every parameter of the report with a result: name, result text / number, method, unit, limit, accredited, U from the MOU register."""
    rows = []
    table = DW_PARAMS if kind == 'dw' else WW_PARAMS
    acc_set = ACCREDITED.get((location, kind))
    for field, name, unit, limit, acc, names in table:
        if acc_set is not None:
            acc = is_accredited(name, acc_set)
        res = getattr(r, field, None)
        if res in (None, '') or str(res).strip() in ('-', 'N/A', 'NA'):
            continue
        n = re.search(r'(\d+)', field).group(1)
        method = getattr(r, 'method_%s' % n, '') or ''
        val, vtxt = parse_result(res)
        u, ulabel, sid = mou_u(location, names, val) if names else (None, '', None)
        lo, hi = parse_limit(limit)
        rows.append({'field': field, 'parameter': name, 'result': str(res).strip(), 'value': val, 'value_text': vtxt, 'method': method.strip(), 'unit': unit,
                     'limit': limit, 'lower': lo, 'upper': hi, 'accredited': acc, 'u': u, 'u_label': ulabel, 'mou_study': sid})
    for x in extra_parameters(kind, r):                     # parameters added to the report beyond the printed list (Alkalinity, Calcium ...)
        name = (x.get('parameters') or x.get('parameter') or '').strip()
        res = x.get('result') or x.get('outlet') or x.get('outlet_result') or ''
        if not name or str(res).strip() in ('', '-', 'N/A'):
            continue
        short = name.split('(')[0].strip()
        val, vtxt = parse_result(res)
        u, ulabel, sid = mou_u(location, [short.lower()], val)
        lim = str(x.get('limit') or x.get('custom_limit') or '').strip()
        lo, hi = parse_limit(lim)
        rows.append({'field': 'extra', 'parameter': name[:80], 'result': str(res).strip(), 'value': val, 'value_text': vtxt, 'method': str(x.get('methods') or x.get('method') or '').strip(),
                     'unit': str(x.get('unit') or 'mg/L').strip(), 'limit': lim, 'lower': lo, 'upper': hi,
                     'accredited': is_accredited(name, acc_set) if acc_set is not None else False, 'u': u, 'u_label': ulabel, 'mou_study': sid})
    return rows


def extra_parameters(kind, r):
    import ast, json
    try:
        if kind == 'dw':
            raw = (r.extra_field or '').strip()
            if not raw:
                return []
            try:
                data = json.loads(raw)
            except ValueError:
                data = ast.literal_eval(raw)
            return [x for x in data if isinstance(x, dict)] if isinstance(data, list) else []
        from QC.ww_live import extra_rows                      # R8: the report's current extra rows (structured_data is never updated)
        rows = extra_rows(r)
        if rows:
            return rows
        raw = (r.structured_data or '').strip()
        if not raw:
            return []
        data = json.loads(raw)
        return [x for x in (data.get('extra_parameters') or []) if isinstance(x, dict)]
    except Exception:
        return []
