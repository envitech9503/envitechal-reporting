"""RDS PDF - the cards of the RDS formula library (static/js/rds_formula_lib.js), owner request 27-10-2026.

Each card saved its working as JSON in the field lib_print_<nnn>; it is printed under the page's own calculations:
parameter (side), formula, method, the lines of the working, result and the check note (validity of the working).
"""
import json


def print_lib_cards(pdf, data, page_break=255, top=35):
    keys = sorted(k for k in (data or {}) if k.startswith('lib_print_') and str(data.get(k) or '').strip())
    cards = []
    for k in keys:
        try:
            c = json.loads(data[k])
        except Exception:
            continue
        if isinstance(c, dict) and c.get('parameter'):
            cards.append(c)
    if not cards:
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
    for c in cards:
        lines = [str(x) for x in (c.get('lines') or [])]
        room(18 + 4.2 * len(lines))
        pdf.ln(2); font('B', 10); pdf.set_x(pdf.l_margin)
        head = str(c.get('parameter')) + (' (%s)' % c['side'] if c.get('side') else '')
        meth = ' - '.join(x for x in (c.get('calc'), c.get('method')) if x)
        pdf.multi_cell(0, 5, head + ('   [' + meth + ']' if meth else ''))
        font('', 8.5); pdf.set_text_color(70, 70, 70); pdf.set_x(pdf.l_margin)
        pdf.multi_cell(0, 4, 'Formula: ' + str(c.get('formula') or ''))
        pdf.set_text_color(0, 0, 0); font('', 9.5)
        for ln in lines:
            pdf.set_x(pdf.l_margin + 4); pdf.multi_cell(0, 4.2, ln)
        font('B', 9.5); pdf.set_x(pdf.l_margin + 4)
        res = 'Result: %s %s' % (c.get('result') or '-', c.get('unit') or '')
        pdf.multi_cell(0, 4.6, res)                        # the test report's value is not printed on the raw data (analyst 30-10-2026)
        from QC.rds_pdf_extras import method_checks
        chk = method_checks(c.get('check'))
        if chk:
            font('', 8.5); pdf.set_x(pdf.l_margin + 4); pdf.multi_cell(0, 4, 'Check: ' + chk)
