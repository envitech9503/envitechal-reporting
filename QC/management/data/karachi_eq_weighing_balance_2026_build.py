"""Build the Karachi weighing-balance (AB-02) monthly equipment chart spec (13-10-2026)."""
import json, statistics as st, sys
wb = json.load(open('/home/claude/wb/wb.json'))
LV = {'1 g': ('(1 gm)', '1 gm'), '10 g': ('(10 gm)', '10 gm'), '100 g': ('(100gm)', '100 gm')}
charts = []
for lvl, (ick, mk) in LV.items():
    ic = [v for k, v in wb.items() if k.endswith(ick)][0]['rows']
    bd = [d for d, x, _ in ic]; bv = [x for d, x, _ in ic]
    mean, sd = st.mean(bv), st.stdev(bv)
    res = []
    for k, v in sorted(wb.items()):
        if k.endswith('|' + mk):
            for d, x, base in v['rows']:
                if d is None and x is None:
                    continue
                assert d and x is not None, (k, d, x)
                res.append(dict(date=d, value=x, remark=''))
            # the form's baseline column must be the February run (same values, any order)
            col = sorted(b for _, _, b in v['rows'] if b is not None)
            assert col == sorted(bv), (k, col, sorted(bv))
    ds = [r['date'] for r in res]
    assert len(ds) == len(set(ds)), lvl
    flag = []
    for r in res:
        z = (r['value'] - mean) / sd
        if abs(z) > 2 + 1e-9:
            flag.append((r['date'], r['value'], round(z, 2)))
    print(lvl, 'baseline n=%d mean %.7f SD %.7f' % (len(bv), mean, sd), 'results', len(res), 'per month',
          {m: sum(1 for d in ds if d[5:7] == m) for m in ('05', '06', '07', '08')}, 'beyond 2SD:', flag)
    charts.append(dict(
        key='EQ AB-02 ' + lvl, activity='EQ', target_id=None,
        match=dict(activity='EQ', parameter='Weight', level=lvl, equipment_id='AB-02'),
        master=dict(parameter='Weight', level=lvl, unit='g', equipment='Analytical Balance', equipment_id='AB-02',
                    method='Not Applicable', crm_detail='', crm_value='', crm_range_low='', crm_range_high='', decimals=4,
                    description='Monthly control charts for analytical balance performance', start_month=1),
        baselines=[dict(key='feb', established_on=bd[-1], values=bv, dates=bd,
                        note='Intermediate check Feb-2026 of the Analytical Balance AB-02 (%s) - ETAL-LAB-P-604' % lvl)],
        results=[dict(r, baseline='feb') for r in res], coverage_months=['2026-05', '2026-06', '2026-07', '2026-08']))
spec = dict(location='Karachi', created='2026-10-13', charts=charts)
json.dump(spec, open(sys.argv[1], 'w'), separators=(',', ':'))
print('charts', len(charts), 'results', sum(len(c['results']) for c in charts))
