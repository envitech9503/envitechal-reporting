"""RDS PDF - the cards of the RDS formula library (static/js/rds_formula_lib.js), owner request 27-10-2026.

Each card saved its working as JSON in the field lib_print_<nnn>; it is printed under the page's own calculations:
parameter (side), formula, method, the lines of the working, result and the check note (validity of the working).
"""
import json
import re


_NUM = re.compile(r'^\s*[<>]?\s*=?\s*-?\d')


def result_text(c):
    """Result with its unit; a result in words (odourless, unobjectionable, clear) carries no unit (owner 30-10-2026)."""
    res = str(c.get('result') or '').strip() or '-'
    unit = str(c.get('unit') or '').strip()
    return res + (' ' + unit if unit and _NUM.match(res) else '')


def _obs(c):
    """An observation card saved before 30-10-2026: the reading as labelled input, the formula as the rule applied."""
    if not str(c.get('formula') or '').startswith('Recorded as observed'):
        return c
    c = dict(c)
    res = str(c.get('result') or '').strip()
    inst = ''
    for ln in c.get('lines') or []:
        m = re.search(r'\(([^)]*)\)\s*$', str(ln))
        if m:
            inst = m.group(1)
    c['formula'] = 'Result = value observed / read on the instrument (no calculation step)'
    c['inputs'] = ['Observed value = ' + (res or '-')] + (['Instrument / remarks = ' + inst] if inst else [])
    c['lines'] = ['Result = ' + result_text(c)]
    return c


def cards(data, present=None):
    """The library cards to print: a card with a result whose parameter is in the results table (present: a
    callable name -> bool, None = all)."""
    out = []
    for k in sorted(k for k in (data or {}) if k.startswith('lib_print_') and str(data.get(k) or '').strip()):
        try:
            c = json.loads(data[k])
        except Exception:
            continue
        if not (isinstance(c, dict) and c.get('parameter')):
            continue
        if not str(c.get('result') or '').strip():
            continue                                       # a card never calculated prints nothing (owner 30-10-2026)
        if present is not None and not present(c.get('parameter')):
            continue
        out.append(_obs(c))
    return out


def print_lib_cards(pdf, data, page_break=255, top=35):
    cs = cards(data)
    if not cs:
        return
    def font(style='', size=10):
        try:
            pdf.set_font('Calibri', style, size)
        except Exception:
            pdf.set_font('Helvetica', style, size)
    def room(h):
        if pdf.get_y() + h > page_break:
            pdf.add_page(); pdf.set_y(top)
    room(20)
    pdf.ln(4); font('B', 11)
    pdf.set_x(pdf.l_margin); pdf.cell(0, 6, 'Calculations - formula library', ln=True)
    for c in cs:
        lines = [str(x) for x in (c.get('lines') or []) if str(x).strip()]
        inputs = [str(x) for x in (c.get('inputs') or []) if str(x).strip()]
        room(30 + 9 * (len(lines) + len(inputs)))
        pdf.ln(2); font('B', 11); pdf.set_x(pdf.l_margin)
        head = str(c.get('parameter')) + (' (%s)' % c['side'] if c.get('side') else '')
        pdf.multi_cell(0, 6, head + ' Calculation:')
        meth = ' - '.join(x for x in (c.get('calc'), c.get('method')) if x)
        font('', 10)                                       # one size and colour for every line of a calculation (owner 30-10-2026)
        if meth:
            pdf.set_x(pdf.l_margin); pdf.multi_cell(0, 6, 'Method: ' + meth)
        if inputs:
            for ln in inputs:                             # R13: "Reading 01: ..." as the working below names it
                ln = re.sub(r'^Replicate (\d+):', lambda m: 'Reading %02d:' % int(m.group(1)), ln)
                pdf.set_x(pdf.l_margin); pdf.multi_cell(0, 6, re.sub(r'\s*;\s+', ';  ', ln))
        # R12 (owner 31-10-2026, point 4): the working in the sheet's own style - "Reading 01", "Formula:", the figures as a
        # fraction over the divisor, "= result"; the one-line symbolic formula is not printed
        print_lines(pdf, lines, str(c.get('parameter') or ''), font)
        font('B', 10); pdf.set_x(pdf.l_margin)
        pdf.multi_cell(0, 6, 'Result: %s' % result_text(c))  # the test report's value is not printed on the raw data (analyst 30-10-2026)
        # R13 (owner strict QA 02-11-2026, point 1): the card's check note ("Check: OK") is not printed


LINE_RX = re.compile(r'^(?:Replicate (\d+): )?(.+?) = ([^=]+)$')          # kept for callers of the R12 parser
_EXPR = re.compile(r'^[\d\s.,+\-*/()\[\]xX×]+$')


def _top_split(text, sep):
    """text split at sep outside brackets."""
    out, depth, cur, i = [], 0, '', 0
    while i < len(text):
        ch = text[i]
        if ch in '([{':
            depth += 1
        elif ch in ')]}':
            depth -= 1
        if depth == 0 and text.startswith(sep, i):
            out.append(cur); cur = ''; i += len(sep); continue
        cur += ch; i += 1
    out.append(cur)
    return [x.strip() for x in out]


def split_fraction(expr):
    """'num / den' -> (num, den) at the last top-level ' / '; (expr, None) when there is no division."""
    parts = _top_split(expr, ' / ')
    if len(parts) < 2:
        return expr, None
    return ' / '.join(parts[:-1]), parts[-1]


def _is_expr(t):
    """Figures and operators only ("1.4 x 1 x 1000 / 50", "(57 + 60 + 60) / 3"); the dilution factor "x DF 2" counts."""
    t = re.sub(r'\bDF\b', '', re.sub(r'\bsqrt\b', '', str(t)))
    return bool(re.search(r'\d', t)) and bool(_EXPR.match(t))


def _show(t):
    """The figures as the native sections print them: "X" for times, "X DF 2" as "X 2"."""
    t = re.sub(r'\s+x\s+DF\s+', ' X ', ' ' + str(t) + ' ').strip()
    return re.sub(r'(?<=[\d)\]])\s+[x×]\s+(?=[\d(\[])', ' X ', t)


def parse_line(ln, reps=None):
    """One saved working line -> printable steps [(heading, prefix, expr, result)] or [(None, None, text, None)] for
    a plain line; [] for a line that is not printed. Handles every format the formula library has saved:
    "Replicate 2: 20 x 100 x 2 / 100 = 40", "Average = (40 + 36) / 2 = 38", "Average of 3 = 59" (before 31-10-2026:
    rebuilt from the readings), "Hardness = a x b x 1000 / v = 28 mg/L as CaCO3", "(as calcium: ... = 11.2 mg/L Ca)",
    "Total = ...;  free = ...;  combined = ...", "Result x DF = 5 x 2 = 10", "Result = 7.2"."""
    s = str(ln or '').strip()
    if not s or re.match(r'^check standard\b', s, re.I):
        return []                                        # a check standard is a QC check: not printed (R12 point 1)
    m = re.match(r'^\((as \w[^:]*):\s*(.*)\)$', s)
    if m:                                                # "(as calcium: 1.4 x 1 x 400.8 / 50 = 11.22 mg/L Ca)"
        return parse_line(m.group(1)[0].upper() + m.group(1)[1:] + ' = ' + m.group(2), reps)
    out = []
    for st in _top_split(s, ';'):
        if not st:
            continue
        rm = re.match(r'^Replicate (\d+):\s*(.*)$', st)
        heading = 'Reading %02d' % int(rm.group(1)) if rm else None
        body = rm.group(2) if rm else st
        parts = _top_split(body, ' = ')
        prefix = None
        if len(parts) >= 2 and not _is_expr(parts[0]):
            name = parts[0]
            if re.match(r'^average\b', name, re.I):
                heading, parts = 'AVERAGE', parts[1:]
                if re.match(r'^average of \d+$', name, re.I) and reps and len(parts) == 1:   # "Average of 3 = 59"
                    parts = ['(' + ' + '.join(reps) + ') / ' + str(len(reps))] + parts
            elif re.match(r'^result x df$', name, re.I):
                heading, parts = 'Dilution factor', parts[1:]
            else:
                prefix, parts = name, parts[1:]
        if not parts:
            continue
        if len(parts) == 1:
            out.append((heading, None, ((prefix + ' = ') if prefix else '') + parts[0], None))
            continue
        out.append((heading, prefix, parts[0], ' = '.join(parts[1:])))
    return out


def _fraction_at(pdf, x, prefix, num, result, den):
    """[prefix = ] num = result, a division drawn as a fraction: the bar under the wider of numerator and divisor, both
    centred on it, "= result" after it (the native sections' layout; a divisor wider than its numerator, e.g. the SAR's
    square root, no longer hangs out of the bar)."""
    y = pdf.get_y()
    if prefix:
        pre = prefix + ' = '
        pdf.set_xy(x, y); pdf.cell(pdf.get_string_width(pre), 6, pre, 0, 0, 'L')
        x += pdf.get_string_width(pre)
    tw = pdf.get_string_width(num)
    if not den:
        pdf.set_xy(x, y); pdf.cell(0, 6, '%s = %s' % (num, result), 0, 1, 'L'); pdf.ln(2); return
    dw = pdf.get_string_width(str(den)); w = max(tw, dw)
    pdf.set_xy(x + (w - tw) / 2, y); pdf.cell(tw, 6, num, 0, 0, 'L')
    pdf.set_xy(x + w, y); pdf.cell(0, 6, ' = %s' % result, 0, 1, 'L')
    pdf.line(x, y + 5.5, x + w, y + 5.5)
    pdf.set_xy(x + (w - dw) / 2, y + 6); pdf.cell(dw, 4, str(den), 0, 1, 'C')
    pdf.ln(2)


def _unwrap(t):
    """'(a + b + c)' -> 'a + b + c' when the brackets enclose the whole term (a numerator or divisor needs none)."""
    t = str(t).strip()
    if (t.startswith('(') and t.endswith(')')) or (t.startswith('[') and t.endswith(']')):
        depth = 0
        for i, ch in enumerate(t):
            depth += ch in '(['
            depth -= ch in ')]'
            if depth == 0 and i < len(t) - 1:
                return t
        return t[1:-1].strip()
    return t


def print_lines(pdf, lines, param, font):
    """Each working line as the native sections print it: a heading ("Reading 01", "Average of <parameter>",
    "Dilution factor") where the line has one, "Formula:" in bold, then the figures, a division as a fraction with the
    divisor under the numerator and "= result" (R12 point 4; R13 every saved format, owner strict QA 02-11-2026)."""
    reps = []
    for ln in lines:
        for heading, prefix, expr, res in parse_line(ln, reps):
            if heading == 'AVERAGE':
                heading = 'Average of ' + param if param else 'Average'
            if heading:                                        # bold 10, as the native sections' "Reading 01"
                font('B', 10); pdf.set_x(pdf.l_margin); pdf.cell(0, 6, heading, ln=True)
            if res is None:                                    # a value or a note: one plain line
                if re.match(r'^Result = ', expr):              # an observation: its rule is its step (R11)
                    font('B', 10); pdf.set_x(pdf.l_margin); pdf.cell(0, 6, 'Formula:', ln=True)
                font('', 10); pdf.set_x(pdf.l_margin + 20); pdf.multi_cell(0, 6, _show(expr)); continue
            if heading and heading.startswith('Reading'):
                reps.append(re.sub(r'\s.*$', '', res.strip()))
            font('B', 10); pdf.set_x(pdf.l_margin); pdf.cell(0, 6, 'Formula:', ln=True)
            font('', 10)
            num, den = split_fraction(expr)
            if den:
                num, den = _unwrap(num), _unwrap(den)
            _fraction_at(pdf, pdf.l_margin + 20, prefix, _show(num), res, _show(den) if den else None)
