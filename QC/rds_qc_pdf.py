"""RDS PDF - quality-control checks (working standard, reference material, certified reference material), release R5
(owner request 27-10-2026). Each check on the page (static/js/rds_qc.js) saves its working as JSON in qc_print_<nnn>;
the checks are printed after the page's calculations: material, parameter (side), identification, true / certified
value, readings, mean, recovery (or difference for pH), acceptance and verdict."""
import json
import re


def _font(pdf, style='', size=10):
    try:
        pdf.set_font('Calibri', style, size)
    except Exception:
        pdf.set_font('Helvetica', style, size)


def checks(data, present=None):
    keys = sorted(k for k in (data or {}) if k.startswith('qc_print_') and str(data.get(k) or '').strip())
    out = []
    for k in keys:
        try:
            c = json.loads(data[k])
        except Exception:
            continue
        if isinstance(c, dict) and c.get('type') and any(str(x or '').strip() for x in (c.get('readings') or [])):
            if present is not None and not present(c.get('parameter')):
                continue                                   # its parameter is not in the results table (owner 30-10-2026)
            out.append(c)
    return out


def print_qc_checks(pdf, data, page_break=255, top=35):
    cs = checks(data)
    if not cs:
        return
    def room(h):
        if pdf.get_y() + h > page_break:
            pdf.add_page(); pdf.set_y(top)
    room(24)
    pdf.ln(4); _font(pdf, 'B', 11); pdf.set_x(pdf.l_margin)
    pdf.cell(0, 6, 'Quality control checks (working standard / reference material / certified reference material)', ln=True)
    for c in cs:
        room(30 + 6 * len(c.get('work') or []))
        pdf.ln(1.5); _font(pdf, 'B', 10); pdf.set_x(pdf.l_margin)
        head = '%s - %s%s' % (c.get('type_label') or c.get('type'), c.get('parameter') or '', ' (%s)' % c['side'] if c.get('side') else '')
        if str(c.get('ident') or '').strip():
            head += '   [%s]' % str(c['ident']).strip()
        pdf.multi_cell(0, 5, head)
        _font(pdf, '', 10); pdf.set_x(pdf.l_margin + 4)
        unit = str(c.get('unit') or '').strip()
        tv = str(c.get('true_value') or '').strip()
        line = '%s value: %s %s' % ('Certified' if c.get('type') == 'CRM' else 'True', tv or '-', unit)
        if str(c.get('u') or '').strip():
            line += ' (U = +/- %s %s)' % (str(c['u']).strip(), unit)
        reads = [str(x).strip() for x in (c.get('readings') or []) if str(x or '').strip()]
        mean = str(c.get('mean') or '-')
        mm = re.match(r'^\s*(\S+)\s*(\(n = \d+\))?\s*$', mean)
        mean = '%s %s%s' % (mm.group(1), unit, (' ' + mm.group(2)) if mm.group(2) else '') if mm else mean
        line += ';   readings: %s;   mean: %s' % (', '.join(reads), mean)
        pdf.multi_cell(0, 6, line)
        for w in [x for x in (c.get('work') or []) if str(x).strip()]:   # R8 point 10: the working, every line (was cut at 3, 30-10-2026)
            pdf.set_x(pdf.l_margin + 8); pdf.multi_cell(0, 6, str(w))
        pdf.set_x(pdf.l_margin + 4)
        if c.get('mode') == 'abs':
            acc = 'difference from the true value: %s (acceptance +/- %s)' % (c.get('result') or '-', c.get('abs') or '-')
        else:
            acc = 'recovery: %s %% (acceptance %s - %s %%)' % (c.get('result') or '-', c.get('lo') or '-', c.get('hi') or '-')
        _font(pdf, 'B', 10)
        pdf.multi_cell(0, 6, acc + ('   -   %s' % c['verdict'] if c.get('verdict') else ''))
