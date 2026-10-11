"""Training charts v2 (11-10-2026): per-batch duplicates (Nitrate-N) and matrix spikes (Pb) with raw working,
20-point baselines, planned warning / out-of-control events with remarks and corrective actions."""
import json, random, datetime as dt, statistics as st

HOL = {dt.date(2026, 2, 5), dt.date(2026, 3, 20), dt.date(2026, 3, 21), dt.date(2026, 3, 23), dt.date(2026, 5, 1),
       dt.date(2026, 5, 27), dt.date(2026, 5, 28), dt.date(2026, 5, 29), dt.date(2026, 6, 25), dt.date(2026, 6, 26),
       dt.date(2026, 8, 14), dt.date(2026, 8, 26)}   # Pakistan public holidays 2026 (Eid dates approximate)


def batches(rnd, start, end):
    """2-3 analytical batches per working week."""
    out, d = [], start - dt.timedelta(days=start.weekday())
    while d <= end:
        days = [d + dt.timedelta(days=i) for i in range(5)]
        days = [x for x in days if start <= x <= end and x not in HOL]
        k = min(len(days), rnd.choice((2, 2, 3, 3, 3)))
        out += sorted(rnd.sample(days, k))
        d += dt.timedelta(days=7)
    return out


def r3(x):
    return round(x, 3)


def rpd(a, b):
    return abs(a - b) / ((a + b) / 2) * 100


def rec(u, s, c):
    return (s - u) / c * 100


def build(lab, seed, analysts_hint):
    rnd = random.Random(seed)
    L = 'KHI' if lab == 'Karachi' else 'LHR'
    sid_n = [rnd.randint(40, 90)]

    def sid(d):
        sid_n[0] += rnd.randint(2, 9)
        return 'TRN-%s-%s-%03d' % (L, d.strftime('%y%m'), sid_n[0] % 1000)

    # ---------------- duplicates: Nitrate-N
    def dup_pair(target=None):
        conc = min(32.0, max(1.6, rnd.lognormvariate(2.05, 0.55)))
        if target is None:
            a, b = conc * (1 + rnd.gauss(0, 0.0105)), conc * (1 + rnd.gauss(0, 0.0105))
        else:
            sgn = rnd.choice((1, -1))
            a, b = conc * (1 + sgn * target / 200), conc * (1 - sgn * target / 200)
        return r3(a), r3(b)

    bdates = batches(rnd, dt.date(2026, 1, 5), dt.date(2026, 2, 27))[:20]
    bvals = []
    for _ in bdates:
        while True:
            a, b = dup_pair()
            v = round(rpd(a, b), 2)
            if v <= 4.2:
                break
        bvals.append(v)
    m, s = st.mean(bvals), st.stdev(bvals)
    uwl, ul = m + 2 * s, m + 3 * s
    rdates = batches(rnd, dt.date(2026, 3, 2), dt.date(2026, 9, 30))
    n = len(rdates)
    ev = {round(n * .18): ('warning', (uwl + ul) / 2),
          round(n * .41): ('ooc', ul + 0.35 * s + 1.0),
          round(n * .66): ('ooc', 11.6),
          round(n * .86): ('warning', uwl + 0.3 * (ul - uwl))}
    res = []
    prev = None
    for i, d in enumerate(rdates):
        S = sid(d)
        if i in ev:
            kind, tgt = ev[i]
            a, b = dup_pair(tgt)
        else:
            while True:
                a, b = dup_pair()
                if round(rpd(a, b), 2) < uwl - 0.05:
                    break
        v = round(rpd(a, b), 2)
        r = dict(date=d.isoformat(), sample_id=S, a=a, b=b, value=v, expect='ok')
        if i in ev:
            r['expect'] = ev[i][0]
            if ev[i][0] == 'warning' and i == min(ev):
                r['remark'] = ('RPD %.2f %% exceeds the +2 SD warning limit (%.2f %%) but is within the <=10 %% acceptance criterion. '
                               'Replicate cuvettes re-checked for scratches and bubbles, both aliquots re-read: confirmed. '
                               'No bias found; batch results released. Next duplicate to be watched for a trend.') % (v, uwl)
            elif ev[i][0] == 'ooc' and tgt < 10:
                r['remark'] = ('RPD %.2f %% beyond the +3 SD action limit (%.2f %%), although within the <=10 %% acceptance. '
                               'Investigation: the second aliquot was filtered through a different 0.45 um membrane lot. Both aliquots '
                               're-filtered with the same membrane and re-analysed: RPD 1.9 %%. Batch re-run before reporting; analysts '
                               'reminded to use one membrane lot per duplicate pair (refresher training recorded).') % (v, ul)
            elif ev[i][0] == 'ooc':
                r['remark'] = ('RPD %.2f %% exceeds the <=10 %% acceptance criterion. Sample %s had heavy suspended solids; '
                               'aliquots were not representative. Batch results withheld. Sample re-homogenised (2 min shaking), '
                               're-filtered and re-analysed in duplicate on the next batch - see the following entry. '
                               'Corrective action: shake-and-split step added to the duplicate procedure.') % (v, S)
                prev = (S, d)
            else:
                r['remark'] = ('RPD %.2f %% beyond +2 SD (%.2f %%), within the <=10 %% acceptance. Lamp energy and '
                               'blank absorbance checked - normal. Isolated point, no trend in the preceding batches; results released.') % (v, uwl)
        elif prev:
            r['remark'] = ('Re-analysis of %s (out of control on %s) after re-homogenisation: RPD %.2f %% - in control. '
                           'Withheld batch results reported from this re-analysis.') % (prev[0], prev[1].strftime('%d-%m-%Y'), v)
            prev = None
        res.append(r)
    dup = dict(activity='DUP', master=dict(
        parameter='TRAINING - Nitrate-N duplicates', level='', unit='%', raw_unit='mg/L',
        equipment='UV-VIS Spectrophotometer', equipment_id='TRN-DUP-%s' % lab[:3].upper(),
        method='APHA 4500-NO3- B (UV)',
        crm_detail='Duplicate of a routine wastewater sample, one pair per batch',
        crm_value='', crm_range_low='', crm_range_high='10',
        description='TRAINING / REFERENCE CHART - RPD of duplicate Nitrate-N analyses (to be deleted by the Lab Manager after training)',
        decimals=2, start_month=1),
        baseline=dict(established_on='2026-03-02', values=bvals, dates=[d.isoformat() for d in bdates],
                      note='Training baseline: 20 duplicate pairs of routine wastewater samples, %s to %s' % (
                          bdates[0].strftime('%d-%m-%Y'), bdates[-1].strftime('%d-%m-%Y'))),
        results=res, signoffs=[dict(year=2026, month=0, reviewed_on='2026-10-05', approved_on='2026-10-07')])
    dinfo = (m, s, uwl, ul, n)

    # ---------------- matrix spikes: Lead (Pb)
    ADD = 0.500

    def spike(target=None):
        u = r3(max(0.012, rnd.lognormvariate(-3.3, 0.55)))
        R = target if target is not None else rnd.gauss(98.6, 2.9)
        sp = r3(u + ADD * R / 100)
        return u, sp

    bdates = batches(rnd, dt.date(2026, 1, 6), dt.date(2026, 2, 27))[:20]
    bvals = []
    for _ in bdates:
        while True:
            u, sp = spike()
            v = round(rec(u, sp, ADD), 1)
            if 92.5 <= v <= 104.5:
                break
        bvals.append(v)
    m2, s2 = st.mean(bvals), st.stdev(bvals)
    lim = dict(uwl=m2 + 2 * s2, ul=m2 + 3 * s2, lwl=m2 - 2 * s2, ll=m2 - 3 * s2)
    rdates = batches(rnd, dt.date(2026, 3, 3), dt.date(2026, 9, 30))
    n2 = len(rdates)
    ev = {round(n2 * .15): ('warning', (lim['lwl'] + lim['ll']) / 2),
          round(n2 * .37): ('warning', (lim['uwl'] + lim['ul']) / 2),
          round(n2 * .58): ('ooc', lim['ll'] - 0.4 * s2 - 0.6),
          round(n2 * .79): ('ooc', 77.4)}
    res = []
    prev = None
    for i, d in enumerate(rdates):
        S = sid(d)
        if i in ev:
            u, sp = spike(ev[i][1])
        else:
            while True:
                u, sp = spike()
                v = round(rec(u, sp, ADD), 1)
                if lim['lwl'] + 0.2 < v < lim['uwl'] - 0.2:
                    break
        v = round(rec(u, sp, ADD), 1)
        r = dict(date=d.isoformat(), sample_id=S, a=u, b=sp, c=ADD, value=v, expect='ok')
        if i in ev:
            kind = ev[i][0]
            r['expect'] = kind
            if kind == 'warning' and v < m2:
                r['remark'] = ('Recovery %.1f %% below the -2 SD limit (%.1f %%), within the 80-120 %% acceptance. '
                               'Burner head cleaned and nebuliser uptake re-checked; calibration verification standard read '
                               '0.497 mg/L (99.4 %%). Batch released; next spike monitored.') % (v, lim['lwl'])
            elif kind == 'warning':
                r['remark'] = ('Recovery %.1f %% above the +2 SD limit (%.1f %%), within 80-120 %%. Unspiked result close '
                               'to the detection limit; background correction (D2 lamp) confirmed ON. No trend; results released.') % (v, lim['uwl'])
            elif v >= 80:
                r['remark'] = ('Recovery %.1f %% below the -3 SD action limit (%.1f %%), within 80-120 %%. '
                               'Spiking pipette (100-1000 uL) checked gravimetrically: delivered 4 %% low - removed from use and sent '
                               'for calibration. Spike repeated with a verified pipette: 98.9 %%. Batch re-analysed before reporting.') % (v, lim['ll'])
            else:
                r['remark'] = ('Recovery %.1f %% is outside the 80-120 %% acceptance. Sample %s - high-TDS textile '
                               'effluent (matrix suppression). Batch results for this matrix withheld; sample re-analysed after 1:5 '
                               'dilution and by standard additions on the next batch - see the following entry.') % (v, S)
                prev = (S, d)
        elif prev:
            r['remark'] = ('Re-analysis of %s (outside acceptance on %s) after 1:5 dilution: recovery %.1f %% - in control. '
                           'Corrective action: high-TDS matrices to be diluted before spiking (procedure updated).') % (prev[0], prev[1].strftime('%d-%m-%Y'), v)
            prev = None
        res.append(r)
    spk = dict(activity='SPK', master=dict(
        parameter='TRAINING - Lead (Pb) spike recovery', level='', unit='%', raw_unit='mg/L',
        equipment='Atomic Absorption Spectrophotometer (flame)', equipment_id='TRN-SPK-%s' % lab[:3].upper(),
        method='APHA 3111 B (flame AAS)',
        crm_detail='0.500 mg/L Pb spiked into a routine wastewater sample, one per batch',
        crm_value='100', crm_range_low='80', crm_range_high='120',
        description='TRAINING / REFERENCE CHART - percent recovery of Pb matrix spikes (to be deleted by the Lab Manager after training)',
        decimals=1, start_month=1),
        baseline=dict(established_on='2026-03-02', values=bvals, dates=[d.isoformat() for d in bdates],
                      note='Training baseline: 20 matrix spikes (0.500 mg/L Pb) of routine wastewater samples, %s to %s' % (
                          bdates[0].strftime('%d-%m-%Y'), bdates[-1].strftime('%d-%m-%Y'))),
        results=res, signoffs=[dict(year=2026, month=0, reviewed_on='2026-10-05', approved_on='2026-10-07')])
    print('%s DUP: baseline mean %.3f SD %.3f UWL %.2f UL %.2f, %d results' % ((lab,) + dinfo))
    print('%s SPK: baseline mean %.2f SD %.2f, %d results' % (lab, m2, s2, n2))
    return dict(location=lab, created='2026-10-11', charts=[dup, spk],
                replace=[dict(activity='DUP', equipment_id='TRN-DUP-%s' % lab[:3].upper(), reason='Replaced by the revised training chart with raw working, remarks and sign-offs (owner instruction 11-10-2026)'),
                         dict(activity='SPK', equipment_id='TRN-SPK-%s' % lab[:3].upper(), reason='Replaced by the revised training chart with raw working, remarks and sign-offs (owner instruction 11-10-2026)')])


for lab, seed in (('Karachi', 1101), ('Lahore', 2202)):
    import os
    json.dump(build(lab, seed, None), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'training_dup_spk_%s.json' % lab.lower()), 'w'), indent=1)
