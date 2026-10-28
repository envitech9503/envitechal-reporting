"""Lab test report with decision rule, printed in the laboratory's normal test-report format (26-10-2026).

The normal drinking-water (generatePDF_report) and waste-water 2 (wasteWater2Pdf1) report generators are run with
`soc=soc_context(...)`. Their PDF class is then replaced by a subclass that
  * adds the column "Uncertainty ±U" after the (last) result column of the analytical table - the expanded
    uncertainty of each parameter that has a statement-of-conformity record, "N.A" for the others - and marks those
    parameters *** (accreditation scope), as on ETAL-LAB-708-FF-18 / FF-19;
  * prints NOT APPROVED across the page while any record of the sample is not approved;
and the generator prints the Statement of Conformity block (Result = Pass / Fail and the paragraph) above the
signatures. Everything else - header, customer block, table, notes, legends, signatures, footer, QR - is the
report's own, unchanged.
"""
import re
from contextlib import contextmanager

from QC.soc_rules import DW_PARAMS, WW_PARAMS

_ALIASES = {}
for _t in (DW_PARAMS, WW_PARAMS):
    for _f, _name, _u, _l, _acc, _names in _t:
        _ALIASES.setdefault(_name.lower(), set()).update([_name.lower()] + list(_names))


def _norm(s):
    s = str(s or '').lower().replace('***', '').replace('₃', '3')
    return re.sub(r'\s+', ' ', s).strip()


def _matches(desc, param):
    d = _norm(desc)
    for a in _ALIASES.get(param.lower(), {param.lower()}) | {param.lower()}:
        if a and re.search(r'(^|[^a-z])%s($|[^a-z])' % re.escape(a), d):
            return True
    return False


def _fmt_u(v):
    if v is None:
        return 'N.A'
    return ('%.4f' % v).rstrip('0').rstrip('.') if v != int(v) else '%d' % v


def result_column(kind, report):
    """Index of the result column the statement is made on: drinking water 4; waste water 4, or 5 (outlet) when the
    report prints inlet and outlet results."""
    if kind == 'ww2' and (getattr(report, 'in_out', '') or '') not in ('in', 'out', 'outlet_customLimits', 'inlet_customlimits'):
        return 5
    return 4


def _acc(rec):
    from QC.soc_rules import ACCREDITED, is_accredited
    return is_accredited(rec.parameter, ACCREDITED.get((rec.location, rec.report_type)))


def soc_context(recs):
    """What the report needs from the statement-of-conformity records of one sample (accredited parameters only:
    the statement of conformity applies to the accreditation scope)."""
    recs = [r for r in recs if _acc(r)]
    passes = [r.parameter for r in recs if r.overall == 'Pass']
    fails = [r.parameter for r in recs if r.overall == 'Fail']
    band_out = [r.parameter for r in recs if r.overall == 'Pass' and not r.band_within]
    na = [r.parameter for r in recs if r.no_limit]
    req = next((r.request for r in recs if r.request_id), None)
    soc_asked = True if req is None else bool(req.req_soc)                  # MOU only: the uncertainty column, no statement (QA 28-10-2026)
    return {'recs': recs, 'draft': any(r.status != 'approved' for r in recs), 'passes': passes, 'fails': fails, 'band_out': band_out, 'na': na,
            'result': 'Fail' if fails else ('Pass' if passes else '-'), 'rule': recs[0].decision_rule if recs else '',
            'no_statement': not soc_asked or not (passes or fails)}


def _join(names):
    names = list(names)
    return names[0] if len(names) == 1 else ', '.join(names[:-1]) + ' & ' + names[-1]


def statement_text(soc):
    t = ('Statement of conformity only applicable on accredited parameters. The statement of compliance is based on a '
         '95% coverage probability for the expanded uncertainty. ')
    within = [p for p in soc['passes'] if p not in soc.get('band_out', [])]
    if within:
        t += ('The measured value of %s along with %s uncertainty band%s %s within the acceptance limit, '
              'therefore %s considered as Pass (accepted based on guard band). '
              % (_join(within), 'its' if len(within) == 1 else 'their respective', '' if len(within) == 1 else 's',
                 'was' if len(within) == 1 else 'were', 'this parameter is' if len(within) == 1 else 'these parameters are'))
    if soc.get('band_out'):
        b = soc['band_out']
        t += ('The measured value of %s %s within the acceptance limit while %s uncertainty band%s extend%s beyond it; under the '
              'simple acceptance rule (guard band = 0) %s considered as Pass. '
              % (_join(b), 'was' if len(b) == 1 else 'were', 'its' if len(b) == 1 else 'their', '' if len(b) == 1 else 's',
                 's' if len(b) == 1 else '', 'this parameter is' if len(b) == 1 else 'these parameters are'))
    if soc['fails']:
        f = soc['fails']
        t += ('The measured value of %s %s outside the acceptance limit, therefore %s considered as Fail (rejected based on guard band). '
              % (_join(f), 'was' if len(f) == 1 else 'were', 'this parameter is' if len(f) == 1 else 'these parameters are'))
    if soc.get('na'):
        n = soc['na']
        t += ('The standard gives no specification limit for %s; %s reported and no statement of conformity is made for %s. '
              % (_join(n), 'its expanded uncertainty is' if len(n) == 1 else 'their expanded uncertainties are', 'it' if len(n) == 1 else 'them'))
    if soc['rule']:
        t += 'Decision rule: %s.' % soc['rule'].rstrip('.')
    return t


def draw_statement(pdf, soc, sign_top=229):
    """The Statement of Conformity block, above the signatures (a new page when it does not fit)."""
    txt = statement_text(soc)
    pdf.set_font('Calibri', '', 8)
    lines = len(pdf.multi_cell(186, 3.8, txt, dry_run=True, output='LINES'))
    need = 10 + lines * 3.8
    if pdf.get_y() + need > sign_top - 2:
        ab = pdf.auto_page_break
        pdf.add_page()
        pdf.set_auto_page_break(ab, margin=pdf.b_margin)
    pdf.ln(1)
    pdf.set_x(10); pdf.set_font('Calibri', 'B', 9); pdf.cell(190, 5, 'Statement of Conformity:', border=0, new_x='LMARGIN', new_y='NEXT')
    pdf.set_x(14); pdf.set_font('Calibri', 'B', 8.5)
    if soc['result'] == 'Fail':
        pdf.set_text_color(185, 28, 28)
    pdf.cell(186, 4.5, '•  Result = %s' % soc['result'], border=0, new_x='LMARGIN', new_y='NEXT')
    pdf.set_text_color(0, 0, 0)
    pdf.set_x(14); pdf.set_font('Calibri', '', 8)
    pdf.multi_cell(186, 3.8, '•  ' + txt, border=0, align='J', new_x='LMARGIN', new_y='NEXT')


class _Row:
    def __init__(self):
        self.cells = []

    def cell(self, *a, **k):
        self.cells.append((a, k))


class _Table:
    """Collects the rows the report generator writes; they are laid out with the extra column afterwards."""
    def __init__(self):
        self.rows, self.closed = [], False

    def row(self, *a, **k):
        r = _Row()
        if not self.closed:
            self.rows.append((r, a, k))
        return r


def _text(cell):
    a, k = cell
    return str(a[0] if a else k.get('text', '') or '')


def soc_pdf_class(base, soc):
    class SocReportPDF(base):
        _soc = soc

        def header(self):
            later = self.page_no() > 1
            if later:                                     # customer & sample block on the first page only (27-10-2026)
                self.show_full_header = False
            super().header()
            self._soc_footer()
            if later:
                self.set_y(60)
            if self._soc.get('draft'):
                with self.local_context():
                    self.set_font('Calibri', 'B', 46); self.set_text_color(222, 172, 172)
                    with self.rotation(35, self.w / 2, self.h / 2):
                        self.text(self.w / 2 - self.get_string_width('NOT APPROVED') / 2, self.h / 2, 'NOT APPROVED')

        def _soc_footer(self):
            """The shared report footer (centred office lines), drawn over the class's own (owner review 27-10-2026)."""
            from EnviTechAlApp.pdf_common import etal_footer
            with self.local_context():
                etal_footer(self)

        @contextmanager
        def table(self, *args, **kw):
            proxy = _Table()
            yield proxy
            proxy.closed = True
            rows = proxy.rows
            hdr = [_text(c) for c in rows[0][0].cells] if rows else []
            analytic = len(hdr) >= 6 and hdr[0].strip().lower().startswith('sr')
            if not rows or not analytic:
                with super().table(*args, **kw) as t:              # not an analytical table: unchanged
                    for r, ra, rk in rows:
                        real = t.row(*ra, **rk)
                        for a, k in r.cells:
                            real.cell(*a, **k)
                return
            pos = self._soc.get('result_col', 4)                  # the U column follows the (outlet) result column
            cw = list(kw.get('col_widths') or ())
            if cw and len(cw) > pos:                              # room for U: taken from the description and method columns
                T = float(sum(cw))
                cw[1] -= 0.04 * T; cw[2] -= 0.02 * T; cw[pos] -= 0.02 * T
                cw.insert(pos + 1, 0.10 * T)
                kw['col_widths'] = tuple(cw)
            ta = kw.get('text_align')
            if isinstance(ta, (tuple, list)) and len(ta) > pos:
                ta = list(ta); ta.insert(pos + 1, 'CENTER'); kw['text_align'] = tuple(ta)
            used = set()
            with super().table(*args, **kw) as t:
                for n, (r, ra, rk) in enumerate(rows):
                    real = t.row(*ra, **rk)
                    col, inserted = 0, False
                    rec = None
                    if n:
                        desc = _text(r.cells[1]) if len(r.cells) > 1 else ''
                        rec = next((x for x in self._soc['recs'] if x.pk not in used and _matches(desc, x.parameter)), None)
                        if rec:
                            used.add(rec.pk)
                    if n and isinstance(self._soc.get('capture'), list):
                        cells = [_text(c) for c in r.cells]
                        if len(cells) > pos + 1:
                            self._soc['capture'].append({'desc': cells[1], 'result': cells[pos], 'limit': cells[pos + 1]})
                    for i, (a, k) in enumerate(r.cells):
                        span = int(k.get('colspan', 1) or 1)
                        if n == 0 and self._soc.get('kind') == 'ww2' and col == i and i in (4, 5) and i <= pos:
                            # the result column's heading, not the free-text label typed on the report (27-10-2026)
                            lab = 'Results' if pos == 4 else ('Inlet Results' if i == 4 else 'Outlet Results')
                            a, k = ((lab,) + tuple(a[1:]), k) if a else (a, dict(k, text=lab))
                        if n and rec and i == pos + 1 and col == i:     # the limit judged must be the limit printed
                            from QC.soc_rules import parse_limit
                            if parse_limit(_text((a, k))) != (rec.lower, rec.upper):
                                if a:
                                    a = (rec.spec_text,) + tuple(a[1:])
                                else:
                                    k = dict(k, text=rec.spec_text)
                        if not inserted and col <= pos < col + span - 1:          # a cell spanning past the result column
                            k = dict(k, colspan=span + 1); inserted = True
                        if i == 1 and rec and n:
                            a = (str(a[0]).rstrip('*').rstrip() + '***',) + tuple(a[1:]) if a else a
                            if not a:
                                k = dict(k, text=str(k.get('text', '')).rstrip('*').rstrip() + '***')
                        real.cell(*a, **k)
                        col += span
                        if not inserted and col == pos + 1:
                            if n == 0:
                                real.cell('Uncertainty ±U', **{kk: vv for kk, vv in k.items() if kk not in ('colspan', 'text')})
                            else:
                                real.cell(_fmt_u(rec.uncertainty) if rec else 'N.A')
                            inserted = True
            self._soc['unmatched'] = [x.parameter for x in self._soc['recs'] if x.pk not in used]
    SocReportPDF.__name__ = base.__name__
    return SocReportPDF


def printed_rows(request, kind, report):
    """The analytical table exactly as the normal test report prints it: [{'desc', 'result', 'limit'}] (limit = the
    first limit column after the result, i.e. the standard's limit the statement is made against)."""
    soc = {'recs': [], 'draft': False, 'passes': [], 'fails': [], 'band_out': [], 'result': '-', 'rule': '',
           'capture': [], 'result_col': result_column(kind, report), 'no_statement': True}
    try:
        if kind == 'dw':
            from EnviTechAlApp.views.generate import generatePDF_report as gen
        else:
            from EnviTechAlApp.views.waste import wasteWater2Pdf1 as gen
        gen(request, report.pk, return_bytes=True, soc=soc)
    except Exception:
        return []
    return soc['capture']
