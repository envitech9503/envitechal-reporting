"""Current results of a waste-water report (RDS R8, chemist feedback 28-10-2026, point 5).

`structured_data` of a WasteWaterForm2 is written once, when the report is created; editing the report changes the
result fields (result_N inlet, result_N_N outlet) and `extra_field`, but never `structured_data`. The RDS (and the SOC
extra parameters) read `structured_data`, so an edited report loaded its first-entry results. These helpers return
the structure with the report's current results, built the same way as on creation.
"""
import ast
import json


def _load(raw, default):
    if raw in (None, ''):
        return default
    if isinstance(raw, (list, dict)):
        return raw
    try:
        return json.loads(raw)
    except Exception:
        try:
            return ast.literal_eval(raw)
        except Exception:
            return default


def extra_rows(r):
    """The report's extra parameters (beyond the 32 printed rows) as they are now."""
    data = _load(r.extra_field, [])
    return [x for x in data if isinstance(x, dict)] if isinstance(data, list) else []


def live_structured(r):
    """`structured_data` of the report with its current results; None when the report has no structured_data."""
    sd = _load(r.structured_data, None)
    if not isinstance(sd, dict) or 'standard_parameters' not in sd:
        return None
    for p in sd.get('standard_parameters') or []:
        try:
            i = int(p.get('sr_no'))
        except (TypeError, ValueError):
            continue
        if not 1 <= i <= 32:
            continue
        p['inlet_result'] = str(getattr(r, 'result_%d' % i, '') or '')
        p['outlet_result'] = str(getattr(r, 'result_%d_%d' % (i, i), '') or '')
        if i < 32 and hasattr(r, 'cutomLimit%d' % (i + 1)):
            p['custom_limit'] = str(getattr(r, 'cutomLimit%d' % (i + 1)) or '')
    rt = r.in_out or sd.get('report_type') or 'in-out'
    rows = extra_rows(r)
    if not rows:                                                  # no extra rows on the report: keep those recorded at creation
        return sd
    extras, n = [], 33
    for item in rows:
        x = {'sr_no': n, 'parameter': item.get('parameters', 'Extra Parameter %d' % n), 'methods': item.get('methods', ''), 'unit': item.get('unit', '')}
        if rt == 'in':
            x['inlet_result'] = item.get('result', '')
        elif rt == 'out':
            x['outlet_result'] = item.get('outlet', item.get('result', ''))
        elif rt == 'inlet_customlimits':
            x['inlet_result'] = item.get('result', ''); x['custom_limit'] = item.get('customLimits', '')
        elif rt == 'outlet_customLimits':
            x['outlet_result'] = item.get('outlet', item.get('result', '')); x['custom_limit'] = item.get('customLimits', '')
        elif rt == 'in_out_customlimits':
            x['inlet_result'] = item.get('result', ''); x['outlet_result'] = item.get('outlet', ''); x['custom_limit'] = item.get('customLimits', '')
        else:
            x['inlet_result'] = item.get('result', ''); x['outlet_result'] = item.get('outlet', '')
        extras.append(x)
        n += 1
    sd['extra_parameters'] = extras
    return sd
