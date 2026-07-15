"""The full-absorption cost engine. Pure Decimal arithmetic; returns a JSON-safe
breakdown so the same function serves the page and the live-recompute API.

Reagent cost is resolved in three layers:
  1) receipt-derived weighted average (from priced lots captured at Receive),
  2) the costing ReagentRate table (finance override / fallback),
  3) otherwise flagged missing ('⚠ set rate')."""
from decimal import Decimal, ROUND_HALF_UP


def D(x):
    return Decimal(str(x if x is not None else 0))


def q2(x):
    return float(D(x).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))


def receipt_rate(chemical, location=None):
    """Weighted-average unit cost from priced lots (the new Receive 'unit_cost').
    Uses in-stock lots if any, else the latest priced lot. Returns None if no priced lots."""
    lots = getattr(chemical, 'lots', None)
    if lots is None:
        return None
    try:
        lots = list(lots.all())
    except Exception:
        return None
    if location:
        lots = [l for l in lots if getattr(l, 'location', '') in ('', location)]
    priced = [l for l in lots if D(getattr(l, 'unit_cost', getattr(l, 'cost', 0))) > 0]
    if not priced:
        return None
    in_stock = [l for l in priced if D(getattr(l, 'quantity', 0)) > 0]
    pool = in_stock or None
    if pool:
        qty = sum((D(l.quantity) for l in pool), Decimal('0'))
        if qty > 0:
            return sum((D(l.quantity) * D(getattr(l, 'unit_cost', getattr(l, 'cost', 0))) for l in pool), Decimal('0')) / qty
    latest = max(priced, key=lambda l: getattr(l, 'id', 0))
    return D(getattr(latest, 'unit_cost', getattr(latest, 'cost', 0)))


def resolve_rate(chemical, location=None):
    """Return (rate, source) where source is 'receipt' | 'table' | 'missing'."""
    r = receipt_rate(chemical, location)
    if r is not None and r > 0:
        return D(r), 'receipt'
    from .models import ReagentRate
    qs = ReagentRate.objects.filter(chemical=chemical)
    rate = None
    if location:
        rate = qs.filter(location=location).order_by('-effective_from', '-id').first()
    if rate is None:
        rate = qs.filter(location='').order_by('-effective_from', '-id').first()
    if rate is None:
        rate = qs.order_by('-effective_from', '-id').first()
    if rate:
        return D(rate.unit_cost), 'table'
    return Decimal('0'), 'missing'


def chemical_rate(chemical, location=None):
    return resolve_rate(chemical, location)[0]


def compute_cost(parameter, batch_size=None, config=None):
    from .models import CostingConfig
    config = config or CostingConfig.current()
    B = D(batch_size or parameter.batch_size or 1)
    if B <= 0:
        B = Decimal('1')
    V = D(parameter.annual_volume or 1)
    if V <= 0:
        V = Decimal('1')

    reag_sample = Decimal('0'); reag_batch = Decimal('0'); chem_lines = []; missing = 0
    for rc in parameter.chemicals.select_related('chemical').all():
        rate, source = resolve_rate(rc.chemical, parameter.location)
        cs = rate * rc.qty_sample
        cb = rate * rc.qty_batch
        reag_sample += cs; reag_batch += cb
        no_rate = (source == 'missing')
        if no_rate:
            missing += 1
        chem_lines.append({'name': str(rc.chemical), 'rate': q2(rate), 'missing': no_rate, 'source': source,
                           'qty_sample': float(rc.qty_sample), 'qty_batch': float(rc.qty_batch),
                           'cost_sample': q2(cs), 'cost_batch': q2(cb)})

    lab_sample = Decimal('0'); lab_lines = []
    for rl in parameter.labour.select_related('grade').all():
        rate = rl.grade.loaded_hourly(config)
        c = rate * rl.minutes_sample / Decimal('60')
        lab_sample += c
        lab_lines.append({'grade': str(rl.grade), 'rate': q2(rate),
                          'minutes': float(rl.minutes_sample), 'cost_sample': q2(c)})

    elec = parameter.electricity_kwh * config.electricity_tariff
    water = parameter.di_water_ml * config.di_water_cost
    util_sample = elec + water
    instrument = D(parameter.instrument_cost)
    waste = D(parameter.waste_cost)

    per_sample = reag_sample + lab_sample + util_sample + instrument + waste
    batch_shared = (reag_batch + D(parameter.qc_batch_cost)) / B
    vol_alloc = D(parameter.annual_pool) / V
    pre = per_sample + batch_shared + vol_alloc
    rework = pre * config.rework_factor
    overhead = (pre + rework) * (config.lab_overhead + config.ga_overhead)
    cost = pre + rework + overhead
    margin = cost * config.target_margin
    rounding = config.price_rounding or Decimal('1')
    raw_price = cost + margin
    if rounding and rounding > 0:
        price = (raw_price / rounding).quantize(Decimal('1'), rounding=ROUND_HALF_UP) * rounding
    else:
        price = raw_price

    return {
        'batch_size': int(B), 'annual_volume': int(V), 'missing_rates': missing,
        'reagents_sample': q2(reag_sample), 'reagents_batch': q2(reag_batch),
        'labour_sample': q2(lab_sample), 'electricity': q2(elec), 'water': q2(water),
        'utilities_sample': q2(util_sample), 'instrument': q2(instrument), 'waste': q2(waste),
        'per_sample': q2(per_sample), 'batch_shared': q2(batch_shared), 'vol_alloc': q2(vol_alloc),
        'pre_overhead': q2(pre), 'rework': q2(rework), 'overhead': q2(overhead),
        'cost': q2(cost), 'margin': q2(margin), 'price': q2(price),
        'chem_lines': chem_lines, 'lab_lines': lab_lines,
        'composition': [
            ['Reagents & standards', q2(reag_sample)],
            ['Labour', q2(lab_sample)],
            ['Utilities', q2(util_sample)],
            ['Instrument', q2(instrument)],
            ['Waste', q2(waste)],
            ['Batch-shared / test', q2(batch_shared)],
            ['Volume-allocated', q2(vol_alloc)],
            ['Repeat-rework', q2(rework)],
            ['Overhead & G&A', q2(overhead)],
        ],
    }
