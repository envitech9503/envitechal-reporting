"""Control-chart rendering (web SVG + PDF PNG) and shared helpers.
07-10-2026 - QC Control Charts module (form ETAL-LAB-604-FF-11).

One matplotlib figure serves both outputs so the screen and the printed form
always agree. Styling follows the laboratory's Excel chart: monthly results as
a blue line with diamonds, action limits (+/-3 SD) red, warning limits (+/-2 SD)
amber, baseline mean green; out-of-limit points are filled red / amber.
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


def render_chart(chart, baseline, results, year, fmt_out='svg', width_in=7.6, height_in=3.4):
    """Return bytes (SVG or PNG) of the control chart for one calendar year.
    `results` is an iterable of ControlChartResult already filtered to `year`."""
    lim = baseline.limits() if baseline else None
    dec = chart.decimals
    fig, ax = plt.subplots(figsize=(width_in, height_in), dpi=150)
    xs = list(range(1, 13))
    ax.set_xlim(0.5, 12.5)
    ax.set_xticks(xs)
    ax.set_xticklabels(['%s-%s' % (m, str(year)[2:]) for m in MONTHS], fontsize=7)
    if lim:
        for key, col, lbl, ls in (('ul', C_UL, 'UL (+3 SD)', '-'), ('uwl', C_UWL, 'UWL (+2 SD)', '--'),
                                  ('mean', C_MEAN, 'Baseline mean', '-'),
                                  ('lwl', C_UWL, 'LWL (-2 SD)', '--'), ('ll', C_UL, 'LL (-3 SD)', '-')):
            ax.plot([0.5, 12.5], [lim[key], lim[key]], color=col, lw=1.1, ls=ls, label=lbl, zorder=2)
            ax.annotate(fmt(lim[key], dec), xy=(12.5, lim[key]), xytext=(3, 0), textcoords='offset points',
                        fontsize=6.5, color=col, va='center', ha='left', annotation_clip=False)
    pts = [(r.date.month, r.value, r.status) for r in results]
    if pts:
        pts.sort()
        ax.plot([p[0] for p in pts], [p[1] for p in pts], color=C_RESULT, lw=1.3, marker='D', ms=5,
                mfc='white', mec=C_RESULT, label='Monthly CRM result', zorder=4)
        for m, v, st in pts:
            if st != 'ok':
                ax.plot([m], [v], marker='D', ms=6.5, color=(C_OOC if st == 'ooc' else C_WARN), zorder=5)
            ax.annotate(fmt(v, dec), xy=(m, v), xytext=(0, 6), textcoords='offset points',
                        fontsize=6.5, ha='center', color='#1f2937')
    # y-range: limits +/- 1 SD padding, widened by any result outside
    ys = [p[1] for p in pts]
    if lim:
        lo, hi = lim['ll'] - lim['sd'], lim['ul'] + lim['sd']
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
    ax.set_title('CONTROL CHART OF %s TESTING' % chart.title.upper(), fontsize=9.5, fontweight='bold', color='#0f5132')
    ax.grid(True, color='#e5e7eb', lw=0.6)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.22), ncol=6, fontsize=6.5, frameon=False)
    fig.tight_layout()
    fig.subplots_adjust(right=0.9)
    buf = io.BytesIO()
    fig.savefig(buf, format=fmt_out, bbox_inches='tight')
    plt.close(fig)
    return buf.getvalue()


def month_rows(chart, baseline, results, year):
    """12 rows (one per month) with the result (if any) and the baseline columns,
    exactly like the printed form."""
    lim = baseline.limits() if baseline else {}
    vals = list(baseline.values) if baseline else []
    by_month = {}
    for r in results:
        by_month.setdefault(r.date.month, r)   # first result of the month
    rows = []
    for i, m in enumerate(range(1, 13)):
        r = by_month.get(m)
        rows.append({
            'sno': i + 1, 'month': '%s-%s' % (MONTHS[i], str(year)[2:]), 'result': r,
            'date': r.date.strftime('%d-%m-%Y') if r else '', 'value': fmt(r.value, chart.decimals) if r else '',
            'status': r.status if r else '', 'remark': r.remark if r else '',
            'base': fmt(vals[i], chart.decimals) if i < len(vals) else '',
            'ul': fmt(lim.get('ul'), chart.decimals), 'uwl': fmt(lim.get('uwl'), chart.decimals),
            'lwl': fmt(lim.get('lwl'), chart.decimals), 'll': fmt(lim.get('ll'), chart.decimals),
            'mean': fmt(lim.get('mean'), chart.decimals), 'sd': fmt(lim.get('sd'), chart.decimals + 1 if chart.decimals < 4 else chart.decimals),
        })
    extra = [fmt(v, chart.decimals) for v in vals[12:]]   # 13th+ baseline values, if any
    return rows, extra
