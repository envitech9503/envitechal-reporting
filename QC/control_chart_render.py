"""Control-chart rendering (web SVG + PDF PNG) and shared helpers.
07-10-2026 - QC Control Charts module (form ETAL-LAB-604-FF-11).
08-10-2026 - generalised to three cadences: CRM (12 month rows per year),
             RM (sequential weekly results per year) and IC (one run of daily
             readings per calendar month; limits from the run itself).

One matplotlib figure serves both outputs so the screen and the printed form
always agree. Styling follows the laboratory's Excel chart: results as a blue
line with diamonds, action limits (+/-3 SD) red, warning limits (+/-2 SD)
amber, mean green; out-of-limit points are filled red / amber.
"""
import io
import datetime

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import FormatStrFormatter  # noqa: E402

MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
C_RESULT, C_UL, C_UWL, C_MEAN, C_OK, C_WARN, C_OOC = '#1d4ed8', '#dc2626', '#f59e0b', '#15803d', '#1d4ed8', '#f59e0b', '#dc2626'


def fmt(v, dec):
    if v is None or v == '':
        return ''
    try:
        return ('%.' + str(int(dec)) + 'f') % float(v)
    except Exception:
        return str(v)


def period_label(chart, year, month=0):
    if chart.period_is_month and month:
        return '%s-%d' % (MONTHS[month - 1], year)
    return chart.cycle_label(year)


def _slots(chart, results, year):
    """x positions of the results: position of the month within the chart's
    cycle for monthly charts, 1..n in date order otherwise; plus the number of
    x slots to draw."""
    if chart.cadence == 'monthly':
        pos = {ym: i + 1 for i, ym in enumerate(chart.cycle_months(year))}
        return [(pos.get((r.date.year, r.date.month), ((r.date.month - chart.sm) % 12) + 1), r) for r in results], 12
    rs = sorted(results, key=lambda r: (r.date, r.id))
    return [(i + 1, r) for i, r in enumerate(rs)], max(12, len(rs))


def render_chart(chart, lim, results, year, month=0, fmt_out='svg', width_in=7.6, height_in=3.4):
    """Return bytes (SVG or PNG) of the control chart for one record period.
    `lim` is the limits dict (baseline or run), `results` already filtered."""
    dec = chart.decimals
    fig, ax = plt.subplots(figsize=(width_in, height_in), dpi=150)
    slots, nx = _slots(chart, results, year)
    xs = list(range(1, nx + 1))
    ax.set_xlim(0.5, nx + 0.5)
    ax.set_xticks(xs)
    if chart.cadence == 'monthly':
        labels = ['%s-%s' % (MONTHS[m - 1], str(y)[2:]) for y, m in chart.cycle_months(year)]
    else:
        by_x = {x: r for x, r in slots}
        labels = [by_x[x].date.strftime('%d-%m') if x in by_x else '' for x in xs]
    ax.set_xticklabels(labels, fontsize=7 if nx <= 16 else 5.5, rotation=0 if nx <= 16 else 60)
    if lim:
        mean_lbl = 'Run mean' if chart.self_limited else 'Baseline mean'
        lines = [('ul', C_UL, 'UL (+3 SD)', '-'), ('uwl', C_UWL, 'UWL (+2 SD)', '--'), ('mean', C_MEAN, mean_lbl, '-')]
        if not chart.upper_only:      # duplicates: one-sided chart, no lower limits
            lines += [('lwl', C_UWL, 'LWL (-2 SD)', '--'), ('ll', C_UL, 'LL (-3 SD)', '-')]
        for key, col, lbl, ls in lines:
            ax.plot([0.5, nx + 0.5], [lim[key], lim[key]], color=col, lw=1.1, ls=ls, label=lbl, zorder=2)
            ax.annotate(fmt(lim[key], dec), xy=(nx + 0.5, lim[key]), xytext=(3, 0), textcoords='offset points',
                        fontsize=6.5, color=col, va='center', ha='left', annotation_clip=False)
    pts = sorted((x, r.value, r.status) for x, r in slots)
    if pts:
        ax.plot([p[0] for p in pts], [p[1] for p in pts], color=C_RESULT, lw=1.3, marker='D', ms=5,
                mfc='white', mec=C_RESULT, label=chart.result_label, zorder=4)
        for x, v, st in pts:
            if st != 'ok':
                ax.plot([x], [v], marker='D', ms=6.5, color=(C_OOC if st == 'ooc' else C_WARN), zorder=5)
            ax.annotate(fmt(v, dec), xy=(x, v), xytext=(0, 6), textcoords='offset points',
                        fontsize=6.5 if nx <= 16 else 5.5, ha='center', color='#1f2937')
    # y-range: limits +/- 1 SD padding, widened by any result outside
    ys = [p[1] for p in pts]
    if lim:
        lo, hi = (max(0.0, lim['mean'] - 2 * lim['sd']) if chart.upper_only else lim['ll'] - lim['sd']), lim['ul'] + lim['sd']
        if ys:
            lo, hi = min(lo, min(ys) - lim['sd']), max(hi, max(ys) + lim['sd'])
        if hi > lo:
            ax.set_ylim(lo, hi)
    elif ys:
        pad = (max(ys) - min(ys) or abs(ys[0]) * 0.05 or 1) * 0.5
        ax.set_ylim(min(ys) - pad, max(ys) + pad)
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.' + str(dec) + 'f'))
    ax.tick_params(axis='y', labelsize=7)
    ax.set_xlabel('Testing date', fontsize=8)
    ax.set_ylabel(('Test result (%s)' % chart.unit) if chart.unit else 'Test result', fontsize=8)
    what = chart.profile['what']
    ax.set_title('CONTROL CHART OF %s %s  -  %s' % (chart.title.upper(), what, period_label(chart, year, month)),
                 fontsize=9.5, fontweight='bold', color='#0f5132')
    ax.grid(True, color='#e5e7eb', lw=0.6)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.22 if nx <= 16 else -0.34), ncol=6, fontsize=6.5, frameon=False)
    fig.tight_layout()
    fig.subplots_adjust(right=0.9)
    buf = io.BytesIO()
    fig.savefig(buf, format=fmt_out, bbox_inches='tight')
    plt.close(fig)
    return buf.getvalue()


def period_rows(chart, lim, base_values, results, year, month=0):
    """Rows of the printed form for one record period.
    monthly: 12 rows (one per month); weekly / run: one row per result in date
    order, padded to 12. Baseline values fill the baseline column row by row."""
    lim = lim or {}
    vals = list(base_values or [])
    dec = chart.decimals
    sd_dec = dec + 1 if dec < 4 else dec
    common = {'ul': fmt(lim.get('ul'), dec), 'uwl': fmt(lim.get('uwl'), dec), 'lwl': fmt(lim.get('lwl'), dec),
              'll': fmt(lim.get('ll'), dec), 'mean': fmt(lim.get('mean'), dec), 'sd': fmt(lim.get('sd'), sd_dec)}
    if chart.upper_only and lim:
        common['lwl'] = common['ll'] = '-'
    rows = []
    if chart.cadence == 'monthly':
        by_month = {}
        for r in results:
            by_month.setdefault((r.date.year, r.date.month), r)   # first result of the month
        seq = [(i + 1, '%s-%s' % (MONTHS[m - 1], str(y)[2:]), by_month.get((y, m))) for i, (y, m) in enumerate(chart.cycle_months(year))]
    else:
        rs = sorted(results, key=lambda r: (r.date, r.id))
        seq = []
        for i in range(max(12, len(rs))):
            r = rs[i] if i < len(rs) else None
            if chart.cadence == 'weekly':
                lbl = ('Wk %02d' % r.date.isocalendar()[1]) if r else ''
            else:
                lbl = str(i + 1) if r else ''
            seq.append((i + 1, lbl, r))
    for sno, lbl, r in seq:
        row = {'sno': sno, 'month': lbl, 'result': r,
               'date': r.date.strftime('%d-%m-%Y') if r else '', 'value': fmt(r.value, dec) if r else '',
               'status': r.status if r else '', 'remark': r.remark if r else '',
               'base': fmt(vals[sno - 1], dec) if sno - 1 < len(vals) else ''}
        row.update(common)
        rows.append(row)
    extra = [fmt(v, dec) for v in vals[len(rows):]]   # baseline values beyond the rows, if any
    return rows, extra


def month_rows(chart, baseline, results, year):
    """Backward-compatible wrapper (CRM form)."""
    return period_rows(chart, baseline.limits() if baseline else None, baseline.values if baseline else [], results, year)
