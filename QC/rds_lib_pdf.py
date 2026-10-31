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
            for ln in inputs:
                pdf.set_x(pdf.l_margin); pdf.multi_cell(0, 6, ln)
        # R12 (owner 31-10-2026, point 4): the working in the sheet's own style - "Reading 01", "Formula:", the figures as a
        # fraction over the divisor, "= result"; the one-line symbolic formula is not printed
        print_lines(pdf, lines, str(c.get('parameter') or ''), font)
        font('B', 10); pdf.set_x(pdf.l_margin)
        pdf.multi_cell(0, 6, 'Result: %s' % result_text(c))  # the test report's value is not printed on the raw data (analyst 30-10-2026)
        from QC.rds_pdf_extras import method_checks
        chk = method_checks(c.get('check'))
        if chk:
            font('', 10); pdf.set_x(pdf.l_margin); pdf.multi_cell(0, 6, 'Check: ' + chk)


LINE_RX = re.compile(r'^(?:Replicate (\d+): )?(.+?) = ([^=]+)$')


def split_fraction(expr):
    """'num / den' -> (num, den) at the last top-level ' / '; (expr, None) when there is no division."""
    depth, pos = 0, -1
    for i, ch in enumerate(expr):
        if ch in '([':
            depth += 1
        elif ch in ')]':
            depth -= 1
        elif depth == 0 and expr.startswith(' / ', i):
            pos = i
    if pos < 0:
        return expr, None
    return expr[:pos], expr[pos + 3:]


def print_lines(pdf, lines, param, font):
    """Each working line as the native sections print it: a heading line ("Reading 01" / "Average of <parameter>"),
    "Formula:" in bold, then the figures as a fraction with the result (QC/rds_pdf_extras._fraction)."""
    from QC.rds_pdf_extras import _fraction
    for ln in lines:
        m = LINE_RX.match(ln.strip())
        if not m:
            font('', 10); pdf.set_x(pdf.l_margin + 4); pdf.multi_cell(0, 6, ln); continue
        rep, expr, res = m.group(1), m.group(2).strip(), m.group(3).strip()
        label = None
        if rep:
            label = 'Reading %02d' % int(rep)
        elif expr.startswith('Average'):
            label = 'Average of ' + param; expr = expr[len('Average'):].lstrip(' =').strip()
        elif expr.startswith('Result x DF'):
            label = 'Dilution factor'; expr = expr[len('Result x DF'):].lstrip(' =').strip()
        elif expr.startswith('Check standard'):
            font('', 10); pdf.set_x(pdf.l_margin + 4); pdf.multi_cell(0, 6, ln); continue
        if label:
            font('', 10); pdf.set_x(pdf.l_margin); pdf.cell(0, 6, label, ln=True)
        font('B', 10); pdf.set_x(pdf.l_margin); pdf.cell(0, 6, 'Formula:', ln=True)
        font('', 10)
        num, den = split_fraction(expr)
        _fraction(pdf, num.replace(' x ', ' X '), res, den.strip('()') if den and den.count('(') == 1 and den.startswith('(') and den.endswith(')') else den, pdf.l_margin + 20)
