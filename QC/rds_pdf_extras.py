"""RDS PDF completeness and presentation (QA audit 27-10-2026, release R3).

tidy()          every printed working: no "None" terms, an empty block is not printed, a "/ 3" under fewer readings
                shows the number of readings actually averaged (RDS-13, RDS-22, RDS-35)
particulars()   the sample block at the top of page 1: client, laboratory, report no., dates, matrix (RDS-32)
closing()       analysts, checkers and the end line after the working (RDS-32)
print_groups()  sections that were calculated and saved but had no printer (RDS-12)
fmt_date()      one date format on the RDS (dd-mm-yyyy) (RDS-16)
"""
import contextvars
import re
from datetime import datetime

SKIP_CALC = contextvars.ContextVar('rds_skip_calc', default=False)

NONE_RX = re.compile(r'\bNone\b')


def tidy(formula, result, divisor):
    f = '' if formula is None else str(formula)
    if not re.search(r'\d', NONE_RX.sub('', f)):
        return None                                       # no figures entered: nothing to print
    if re.search(r'[(\[]\s*-\s*[)\]]', NONE_RX.sub('', f)):
        return None                                       # a replicate with no readings ("( - ) X ...", R12 owner 31-10-2026)
    terms = [t.strip() for t in f.split(' + ')]
    empty = lambda t: re.sub(r'[\s()\[\]X×\-]|None', '', t) == '' or re.search(r'X\s*\)$|\(\s*X', t) is not None   # "(0 X )": a reading without its factor
    kept = [t for t in terms if not empty(t)]
    n_all, n = len(terms), len(kept)
    if 1 < n_all and n < n_all:
        f = ' + '.join(kept)
    f = NONE_RX.sub('', f)
    r = NONE_RX.sub('', '' if result is None else str(result)).strip()
    d = None if divisor in (None, '') else str(divisor)
    if d is not None and n_all == 3 and 0 < n < 3 and d.strip() == '3':
        d = str(n)                                        # averaged over the readings entered (R1 rule)
    return f, r, d


_FMTS = ('%d-%m-%Y', '%d-%b-%Y', '%d-%B-%Y', '%Y-%m-%d', '%d/%m/%Y', '%d-%m-%y', '%d %B %Y', '%d %b %Y', '%B %d, %Y')


def fmt_date(v):
    s = str(v or '').strip()
    if not s or s in ('None', 'undefined'):
        return ''
    for f in _FMTS:
        try:
            return datetime.strptime(s, f).strftime('%d-%m-%Y')
        except ValueError:
            pass
    return s


def row_order(row_key):
    return tuple(int(x) for x in re.findall(r'\d+', str(row_key))) or (10 ** 6,)


def method_checks(note):
    """A saved check note without its comparison with the test report's value ("differs from the reported ...",
    "... below the reported ..."): the RDS is the raw record the report is made from, so only the checks of the working
    itself are printed (analyst feedback 30-10-2026). '' when nothing is left."""
    parts = [p.strip() for p in str(note or '').split(';')]
    kept = [p for p in parts if p and not re.search(r'\breported\b', p, re.I)]
    return '; '.join(kept)


def _day(v):
    s = fmt_date(v)
    try:
        return datetime.strptime(s, '%d-%m-%Y').toordinal()
    except (TypeError, ValueError):
        return 10 ** 7                                   # no readable date: after the dated rows, in table order


def chrono_key(data):
    """Order of the RDS table on the PDF: by the date of analysis (oldest first), then the order on the page; a row's
    own sub-rows (WS / RM / CRM checks, N.k) stay right after it (analyst feedback 30-10-2026)."""
    def key(row_key):
        main = str(row_key).split('_')[0]
        return (_day(data.get('date_' + main) or data.get('date_' + str(row_key))), row_order(main), row_order(row_key))
    return key


def _report(kind, sample_id):
    from EnviTechAlApp.models import DrinkingWaterForm, WasteWaterForm2
    model = WasteWaterForm2 if kind == 'ww' else DrinkingWaterForm
    return model.objects.filter(sample_id=sample_id).order_by('-id').first()


def particulars(pdf, kind, sample_id, data, rec=None):
    """Sample block (two columns) printed where the bare "Sample ID" line used to be."""
    r = _report(kind, sample_id)
    g = lambda *names: next((str(getattr(r, n)) for n in names if r is not None and getattr(r, n, None) not in (None, '')), '')
    matrix = 'Drinking water' if kind == 'dw' else 'Waste water'
    io = {'in': 'inlet', 'out': 'outlet', 'in-out': 'inlet and outlet'}.get(str(data.get('report_type') or g('in_out')).strip(), '')
    if io and kind == 'ww':
        matrix += ' (%s)' % io
    a_from, a_to = fmt_date(g('date_of_analysis_from')), fmt_date(g('date_of_analysis_to'))
    rows = [('Sample ID', sample_id), ('Laboratory', g('city_location')),
            ('Client', g('report_to')), ('Lab report no.', g('lab_report_no')),
            ('Matrix', matrix), ('Sampling date', fmt_date(g('sample_Col_date', 'sample_collection_date'))),
            ('Analysis', (a_from + (' to ' + a_to if a_to and a_to != a_from else '')) if a_from else '')]
    # "RDS saved" (the date the record was stored in the software) is not printed: it is not a date of the analysis and
    # could be read by an assessor as one (analyst feedback 30-10-2026)
    x0, w = 12, 186
    vw = w / 2 - 30                                             # width of a value
    y = pdf.get_y()
    pdf.set_font('Calibri', '', 9)

    def wrap(v):                                                # R8 (chemist feedback, point 4): long names wrap, no overprint
        words, lines, cur = str(v).split(), [], ''
        for wd in words:
            t = (cur + ' ' + wd).strip()
            if pdf.get_string_width(t) <= vw - 1 or not cur:
                cur = t
            else:
                lines.append(cur); cur = wd
        if cur:
            lines.append(cur)
        return lines[:3] or ['']
    pairs = [rows[i:i + 2] for i in range(0, len(rows), 2)]
    heights = [max(len(wrap(v)) for _, v in pr) * 4.4 + 0.8 for pr in pairs]
    pdf.set_draw_color(150, 150, 150); pdf.set_line_width(0.2)
    pdf.rect(x0, y, w, sum(heights) + 2)
    yy = y + 1
    for pr, h in zip(pairs, heights):
        for col, (k, v) in enumerate(pr):
            x = x0 + 2 + col * (w / 2)
            pdf.set_xy(x, yy)
            pdf.set_font('Calibri', 'B', 9); pdf.cell(26, 5, k + ':', 0, 0, 'L')
            pdf.set_font('Calibri', '', 9)
            for j, ln in enumerate(wrap(v)):
                pdf.set_xy(x + 26, yy + j * 4.4); pdf.cell(vw, 5, ln, 0, 0, 'L')
        yy += h
    pdf.set_draw_color(0, 0, 0)
    pdf.set_xy(x0, y + sum(heights) + 4)


def micro_steps(pdf, ans, unit):
    """A microbiology section of the page that records the count only (E. coli, faecal coliform, coliform, total /
    heterotrophic bacteria): the rule, the count read and the result (owner 30-10-2026: every calculation with its
    steps), Calibri 10 like the working."""
    ans, unit = str(ans or '').strip(), str(unit or '').strip()
    per = '100 mL' if '100' in unit else ('mL' if re.search(r'/\s*m[lL]', unit) else '')
    pdf.set_font('Calibri', '', 10); pdf.set_x(pdf.l_margin)
    pdf.cell(0, 6, 'Colonies counted = %s (direct count on the membrane / plate)' % (ans or '-'), ln=True)
    pdf.set_font('Calibri', 'B', 10); pdf.set_x(pdf.l_margin); pdf.cell(0, 6, 'Formula:', ln=True)
    pdf.set_font('Calibri', '', 10)
    vol = '100' if per == '100 mL' else '1'
    _fraction(pdf, '%s X %s X 1' % (ans or '-', vol), ('%s %s' % (ans, unit)).strip(), vol, pdf.l_margin + 20)   # R12: the sheet's fraction style
    pdf.set_font('Calibri', 'B', 10); pdf.set_x(pdf.l_margin)
    pdf.cell(0, 6, ('Result: %s %s' % (ans, unit)).strip(), ln=True)
    pdf.set_font('Calibri', '', 10)


def calc_open(pdf, header):
    """The CALCULATION page and heading; on the second drawing of a sheet with no calculation, neither (owner
    30-10-2026: no blank calculation on the RDS). Marks where the calculations start."""
    if SKIP_CALC.get():
        pdf._etal_calc_mark = None
        return
    pdf.add_page()
    pdf.set_y(35)
    header()
    pdf._etal_calc_mark = (pdf.page, len(pdf.pages[pdf.page].contents))


def calc_empty(pdf):
    """True when nothing was drawn after the CALCULATION heading (checked before the closing block)."""
    m = getattr(pdf, '_etal_calc_mark', None)
    if not m or pdf.page != m[0]:
        return False
    drawn = bytes(pdf.pages[pdf.page].contents[m[1]:])            # a font switch or a cursor move draws nothing
    return not re.search(rb'T[jJ]\b|\bl S\b|\bre\b|\bDo\b|\bS\b|\bf\b', drawn)


def without_empty_calc(gen, report, pk):
    """Draw again without the CALCULATION page when it would stay empty."""
    tok = SKIP_CALC.set(True)
    try:
        return gen(report, pk)
    finally:
        SKIP_CALC.reset(tok)


DF_LINE = re.compile(r'^df_(\d+)$')


def df_records(data):
    """The dilution factors applied on the page (static/js/rds_df.js): [{n, df, base, result, sec, side, param}] for DF != 1."""
    out = []
    for k, v in (data or {}).items():
        m = DF_LINE.match(k)
        if not m:
            continue
        n = m.group(1)
        try:
            df = float(str(v).strip())
        except (TypeError, ValueError):
            continue
        base = str(data.get('df_base_' + n) or '').strip()
        if df == 1 or not base:
            continue
        out.append({'n': n, 'df': df, 'base': base, 'result': str(data.get('df_result_' + n) or '').strip(),
                    'sec': str(data.get('df_sec_' + n) or '').strip(), 'side': str(data.get('df_side_' + n) or '').strip(),
                    'param': str(data.get('df_param_' + n) or '').strip(), 'done': False})
    return out


def _words(s):
    return {w for w in re.split(r'[^a-z0-9]+', str(s or '').lower().replace('*', '')) if len(w) >= 3 and w not in ('calculation', 'calculations', 'the', 'and', 'inlet', 'outlet')}


def install_df(pdf, data):
    """Prints the dilution-factor step under the section it belongs to (R12, owner 31-10-2026). The generators print a
    section heading as a bold 11 pt cell ending in ":" or "Calculation(s)"; before the next heading, the closing block or
    the library cards, the step of the heading just printed is flushed: "Dilution factor (DF = x): result = base x DF = final"."""
    recs = df_records(data)
    pdf._etal_df = {'recs': recs, 'cur': None}
    if not recs:
        return
    orig_cell = pdf.cell

    def cell(w=0, h=0, txt='', *a, **kw):
        if 'text' in kw:
            txt = kw.pop('text')
        txt = '' if txt is None else txt
        t = str(txt)
        if (pdf.font_style == 'B' and abs(pdf.font_size_pt - 11) < 0.01 and len(t) < 90
                and re.search(r':\s*$|\bcalculations?\s*:?\s*$', t, re.I)
                and not re.match(r'\s*(average|reading|ws[-\s]|crm|rm[-\s]|sample|blank)', t, re.I)):   # sub-headings stay in their section
            flush_df(pdf)
            pdf._etal_df['cur'] = t
        return orig_cell(w, h, txt, *a, **kw)
    pdf.cell = cell


def flush_df(pdf):
    st = getattr(pdf, '_etal_df', None)
    if not st or not st['cur']:
        return
    hw = _words(st['cur']); side = 'Inlet' if re.search(r'\binlet\b', st['cur'], re.I) else ('Outlet' if re.search(r'\boutlet\b', st['cur'], re.I) else '')
    best, score = None, 0
    for r in st['recs']:
        if r['done'] or (r['side'] or side) and r['side'] != side:
            continue
        sc = len(hw & (_words(r['sec']) | _words(r['param'])))
        if sc > score:
            best, score = r, sc
    st['cur'] = None
    if not best:
        return
    best['done'] = True
    pdf.set_font('Calibri', 'B', 10); pdf.set_x(pdf.l_margin)
    pdf.cell(0, 6, 'Dilution factor (DF = %s):' % _num(best['df']), ln=True)
    pdf.set_font('Calibri', '', 10); pdf.set_x(pdf.l_margin + 4)
    try:
        fin = best['result'] or _num(float(best['base']) * best['df'])
    except (TypeError, ValueError):
        fin = best['result'] or '-'
    pdf.cell(0, 6, 'Result = calculated result X DF = %s X %s = %s' % (best['base'], _num(best['df']), fin), ln=True)
    pdf.ln(1)


def _num(v):
    try:
        return ('%.6f' % float(v)).rstrip('0').rstrip('.')
    except (TypeError, ValueError):
        return str(v)


def closing(pdf, data, page_break=255, top=35):
    """Analysed by / checked by with their e-signatures, then the end line."""
    flush_df(pdf)
    pdf._etal_calc_empty = calc_empty(pdf)
    from EnviTechAlApp.models import Signatures
    def ids(prefix):
        out = []
        for k, v in data.items():
            if k.startswith(prefix) and str(v).strip().isdigit() and int(v) not in out:
                out.append(int(v))
        return out
    groups = [('Analysed by', ids('performed_by_')), ('Checked by', ids('checked_by_'))]
    if not any(g[1] for g in groups):
        names_h = 0
    else:
        names_h = 30
    if pdf.get_y() + names_h + 14 > page_break:
        pdf.add_page(); pdf.set_y(top)
    pdf.ln(4)
    if names_h:
        y = pdf.get_y()
        for c, (label, sids) in enumerate(groups):
            x = 14 + c * 95
            pdf.set_xy(x, y); pdf.set_font('Calibri', 'B', 10); pdf.cell(90, 5, label, 0, 1, 'L')
            for i, sid in enumerate(sids[:3]):
                s = Signatures.objects.filter(id=sid).select_related('user').first()
                if s is None:
                    continue
                yy = y + 6 + i * 8
                try:
                    if s.signature:
                        pdf.image(s.signature.path, x, yy, w=22, h=7)
                except Exception:
                    pass
                pdf.set_xy(x + 24, yy + 1); pdf.set_font('Calibri', '', 9)
                pdf.cell(66, 5, (s.user.get_full_name() or s.user.username)[:40], 0, 0, 'L')
        pdf.set_y(y + 6 + 3 * 8)
    pdf.ln(2)
    pdf.set_font('Calibri', 'B', 10)
    pdf.cell(0, 6, '--- END OF THE DOCUMENT ---', 0, 1, 'C')


def _fraction(pdf, text, result, divisor, x=30):
    y = pdf.get_y()
    tw = pdf.get_string_width(text)
    pdf.set_x(x); pdf.cell(tw, 6, '%s = %s' % (text, result), 0, 1, 'L')
    if divisor:
        pdf.line(x, y + 5.5, x + tw, y + 5.5)
        dw = pdf.get_string_width(str(divisor))
        pdf.set_x(x + tw / 2 - dw / 2); pdf.cell(dw, 4, str(divisor), 0, 1, 'C')
    pdf.ln(2)


def _avg_group(pdf, data, title, head, reps, divi, ans, param, page_break, top):
    if not str(data.get(ans) or '').strip():
        return False
    terms = []
    for v, d in reps:
        val = str(data.get(v) or '').strip()
        if not val:
            continue
        df = str(data.get(d) or '').strip() if d else ''
        terms.append('(%s X %s)' % (val, df) if d and df else val)
    if not terms:
        return False
    if pdf.get_y() + 26 > page_break:
        pdf.add_page(); pdf.set_y(top)
    if title:
        pdf.set_font('Calibri', 'B', 11); pdf.cell(0, 7, title, 0, 1, 'L')
    if head and str(data.get(head) or '').strip():
        pdf.set_font('Calibri', 'B', 10); pdf.cell(0, 6, str(data.get(head)), 0, 1, 'L')
    pdf.set_font('Calibri', '', 10)
    div = str(data.get(divi) or '').strip() if divi else ''
    if len(terms) > 1:
        _fraction(pdf, ' + '.join(terms), '%s %s' % (data.get(ans), data.get(param) or ''), div or str(len(terms)))
    else:
        _fraction(pdf, terms[0], '%s %s' % (data.get(ans), data.get(param) or ''), None)
    return True


GROUPS = [
    ('Cobalt Calculations', 'cobalt_head', [('for_cobalt%d' % i, 'for_cobalt%d_df' % i) for i in (1, 2, 3)], 'cobalt_divi', 'cobalt_ans', 'cobalt_param'),
    ('Conductivity Calculations', 'conduct_head', [('for_conduct%d' % i, None) for i in (1, 2, 3)], 'conduct_divi', 'conduct_ans', 'conduct_param'),
    ('Dissolved Oxygen (DO) Calculations', 'desolve_oxygen_head', [('for_desolve_oxygen%d' % i, None) for i in (1, 2, 3)], 'desolve_oxygen_divi', 'desolve_oxygen_ans', 'desolve_oxygen_param'),
    ('Chromium (VI) Calculations', 'chromium_IV_head', [('for_chromium_IV%d' % i, None) for i in (1, 2, 3)], None, 'chromium_IV_ans', 'chromium_IV_param'),
    ('Chromium (VI) Calculations', 'chromium_IV_head_1', [('for_chromium_IV1_%d' % i, 'for_chromium_IV1_%d_df' % i) for i in (1, 2, 3)], 'chromium_IV_divi', 'chromium_IV_ans_1', 'chromium_IV_param_1'),
    ('Chromium (III) Calculations', 'chromium_III_head_1', [('for_chromium_III1_%d' % i, 'for_chromium_III1_%d_df' % i) for i in (1, 2, 3)], 'chromium_III_divi', 'chromium_III_ans_1', 'chromium_III_param_1'),
    ('Chromium (III) Calculations', 'chromium_III_head_2', [('for_chromium_III2_%d' % i, 'for_chromium_III2_%d_df' % i) for i in (1, 2, 3)], 'chromium_III_divi', 'chromium_III_ans_2', 'chromium_III_param_2'),
    ('Ferrous Iron Calculations', 'ferrous_head', [('for_ferrous%d' % i, None) for i in (1, 2, 3)], None, 'ferrous_ans', 'ferrous_param'),
    ('Ferrous Iron Calculations', 'ferrous_head_1', [('for_ferrous1_%d' % i, 'for_ferrous1_%d_df' % i) for i in (1, 2, 3)], 'ferrous_divi', 'ferrous_ans_1', 'ferrous_param_1'),
]
GROUPS_DW = [
    ('COD Calculations', 'cod_head', [('for_cod%d' % i, None) for i in (1, 2, 3)], None, 'cod_ans', 'cod_param'),
    ('COD Calculations', 'cod_head_1', [('for_cod1_%d' % i, 'for_cod1_%d_df' % i) for i in (1, 2, 3)], 'cod_divi', 'cod_ans_1', 'cod_param_1'),
]


def print_groups(pdf, data, kind, page_break=255, top=35):
    """Print the sections that are saved on the page but had no printer before (QA RDS-12)."""
    for g in GROUPS + (GROUPS_DW if kind == 'dw' else []):
        try:
            _avg_group(pdf, data, *g, page_break=page_break, top=top)
        except Exception:
            pass
    a, b = str(data.get('chromium_III_final_ans1') or '').strip(), str(data.get('chromium_III_final_ans2') or '').strip()
    if str(data.get('chromium_III_fnf_ans') or '').strip() and a and b:
        pdf.set_font('Calibri', '', 10); pdf.set_x(30)
        pdf.cell(0, 6, 'Chromium (III) = total chromium - chromium (VI) = %s - %s = %s %s' % (
            a, b, data.get('chromium_III_fnf_ans'), data.get('chromium_III_final_param') or ''), 0, 1, 'L')
    if kind == 'dw':
        for key, label in (('enterobacteria_ans', 'Enterobacteria'), ('fecalentero_ans', 'Faecal enterococci')):
            if str(data.get(key) or '').strip():
                pdf.set_font('Calibri', 'B', 11); pdf.cell(0, 7, label, 0, 1, 'L')
                pdf.set_font('Calibri', '', 10); pdf.set_x(30)
                pdf.cell(0, 6, 'Result: %s %s' % (data.get(key), data.get(key.replace('_ans', '_param')) or ''), 0, 1, 'L')


def fill_last_weights(data):
    """For printing only: the 5th / 10th / 15th / 20th weighing box carries the last weighing entered in its group of five,
    as the page calculates since R1 (constant weight is often reached before the fifth weighing) - QA RDS-05/13."""
    out = dict(data)
    for pre in ('AW', 'FW', 'oil_FW'):
        for last in (5, 10, 15, 20):
            for sfx in ('', '_inlet', '_outlet'):
                key = '%s%02d%s' % (pre, last, sfx)
                if str(out.get(key) or '').strip():
                    continue
                vals = [str(out.get('%s%02d%s' % (pre, i, sfx)) or '').strip() for i in range(last - 4, last + 1)]
                vals = [v for v in vals if v]
                if vals:
                    out[key] = vals[-1]
    return out


def edta_b(data, key):
    """' X <B>' for an EDTA titration reading saved with its factor B (QA RDS-23, release R5): the section and the
    inlet / outlet side follow from the reading's own key (hardness_2_1_inlet, cal_r1_final, ch_r2_final, r1_1_final).
    Records saved before R5 have no B and print as before."""
    k = str(key or '')
    sfx = '_inlet' if k.endswith('_inlet') else ('_outlet' if k.endswith('_outlet') else '')
    base = 'calcium' if k.startswith(('cal_', 'ch_')) else ('magnesium' if re.match(r'r\d', k) else 'hardness')
    b = str((data or {}).get(base + '_edta_b' + sfx) or '').strip()
    try:
        float(b)
    except ValueError:
        return ''
    return ' X ' + b


def fit_cell(pdf, w, h, txt, border=1, ln=0, align='L', min_size=6.0):
    """A table cell whose text is narrowed to its width (R8: "Biological Oxygen Demand(BOD)5 CRM" ran into the next column)."""
    txt = str(txt)
    size = pdf.font_size_pt
    cur = size
    while cur > min_size and pdf.get_string_width(txt) > w - 2:
        cur -= 0.5
        pdf.set_font_size(cur)
    pdf.cell(w, h, txt, border, ln, align)
    pdf.set_font_size(size)
