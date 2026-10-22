"""Internal Audit - PDF forms (22-10-2026): ETAL-QMS-808-FF-01 Annual Plan, FF-02 Audit Report (with the
witnessing record), FF-03 Circular, ETAL-QMS-710-FF-01 NC & Corrective Action form, 710-FF-01A Root Cause
Analysis, 710-FF-02 NC&CA Log. Same frame as the control-chart / MOU PDFs (Calibri, document-control box,
laboratory footer); every signature panel prints the name and e-signature of the user who signed in the system.
"""
from .shared import *  # noqa: F401,F403
import os as _os
import re as _re
from datetime import date as _date
from django.conf import settings as _settings

from QC.models import IaPlan, IaAudit, IaCircular, IaWitness, Ncca, NccaRca
from QC.views.control_chart import _CC_OFFICE, _uname, _sig_image, _is_admin, _user_labs, _user_office
from QC.views.ia import _ia_docctrl, _d, MONTHS, _RESULT_LABEL, _CAT_LABEL, _loc_of, _CC_LOCS

GREEN, GREY_FILL, LINE, AMBER, GREEN_DONE = (15, 81, 50), (242, 245, 243), (120, 120, 120), (255, 229, 153), (112, 173, 71)


def _paths():
    base = str(getattr(_settings, 'BASE_DIR', '') or '')
    return [_os.path.join(base, p) if base else p for p in ('static/assets/EnviTechAL LOGO.png', 'static/fonts/calibri.ttf', 'static/fonts/calibrib.ttf')]


def _pdf(title, sub, ctrl, location, orientation='P', wm=''):
    """FPDF subclass with the Envi Tech AL header (logo, document-control box, title) and footer."""
    _LOGO, _CAL, _CALB = _paths()
    office = _CC_OFFICE.get(location, _CC_OFFICE['Karachi'])

    class PDF(FPDF):
        def __init__(self):
            super().__init__(orientation, 'mm', 'A4')
            self.fam = 'Helvetica'
            try:
                if _os.path.exists(_CAL):
                    self.add_font('Calibri', '', _CAL); self.add_font('Calibri', 'B', _CALB if _os.path.exists(_CALB) else _CAL)
                    self.fam = 'Calibri'
            except Exception:
                pass
            self.W = self.w - 20.0

        def header(self):
            if wm:
                self.set_font(self.fam, 'B', 54); self.set_text_color(238, 238, 238)
                try:
                    with self.rotation(45 if orientation == 'P' else 30, self.w / 2, self.h / 2):
                        self.text(self.w / 2 - self.get_string_width(wm) / 2, self.h / 2 + 10, wm)
                except Exception:
                    pass
                self.set_text_color(0, 0, 0)
            if _os.path.exists(_LOGO):
                try:
                    self.image(_LOGO, 10, 8, 20, 22)
                except Exception:
                    pass
            lines = ['Doc. No: %s' % ctrl['doc_no'], 'Issue Date: %s' % ctrl['issue_date'],
                     'Issue No. %s    Rev. No. %s' % (ctrl['issue_no'], ctrl['rev_no']), 'Page No: %d of {nb}' % self.page_no()]
            self.set_font(self.fam, '', 7)
            bw = max(self.get_string_width(l.replace('{nb}', '99')) for l in lines) + 5.0
            bx, by, lh = self.w - 10.0 - bw, 8.0, 4.4
            self.set_draw_color(*LINE); self.set_fill_color(*GREY_FILL)
            self.rect(bx, by, bw, lh * len(lines) + 1.6, 'DF')
            for i, l in enumerate(lines):
                self.set_xy(bx + 2.0, by + 0.8 + i * lh); self.cell(bw - 4.0, lh, l, 0, 0, 'L')
            self.set_text_color(*GREEN)
            self.set_xy(10, 8.5); self.set_font(self.fam, 'B', 15); self.cell(self.W, 7, 'ENVI TECH AL', align='C', ln=1)
            self.set_x(10); self.set_font(self.fam, '', 8); self.set_text_color(70, 70, 70)
            self.cell(self.W, 4.5, 'Analytical Laboratory - Environmental & Water Testing', align='C', ln=1)
            self.set_x(10); self.set_font(self.fam, 'B', 10.5); self.set_text_color(0, 0, 0)
            self.cell(self.W, 5.5, title, align='C', ln=1)
            self.set_x(10); self.set_font(self.fam, 'B', 8.5); self.set_text_color(*GREEN)
            self.cell(self.W, 4.5, sub, align='C', ln=1)
            self.set_text_color(0, 0, 0)
            self.set_draw_color(*GREEN); self.set_line_width(0.5); self.line(10, 33, self.w - 10, 33)
            self.set_line_width(0.2); self.set_draw_color(0, 0, 0); self.set_y(36.5)

        def footer(self):
            self.set_y(-20); self.set_font(self.fam, '', 6.5); self.set_text_color(90, 90, 90)
            self.cell(0, 4, 'ENVI TECH AL  -  Controlled document.  Uncontrolled when printed.', align='C', ln=1)
            self.set_text_color(0, 0, 0); self.set_draw_color(*GREEN); self.set_line_width(0.4)
            yb = self.get_y() + 0.6; self.line(10, yb, self.w - 10, yb); self.set_line_width(0.2); self.set_draw_color(0, 0, 0)
            self.set_xy(10, yb + 1.2); self.cell(self.W / 2, 3.6, office['tel'], align='L')
            self.set_xy(10 + self.W / 2, yb + 1.2); self.cell(self.W / 2, 3.6, 'info@envitechal.com   -   www.envitechal.com', align='R')
            self.set_xy(10, yb + 4.8)
            self.cell(0, 3.6, office['address'], align='C')

        # -- helpers
        def kv(self, items, h=5.4):
            """Row of (label, value, wl, wv) cells."""
            for lbl, val, wl, wv in items:
                self.set_font(self.fam, 'B', 7.8); self.set_fill_color(*GREY_FILL)
                self.cell(wl, h, lbl, 1, 0, 'L', fill=True)
                txt = str(val) if val not in (None, '') else '-'
                fs = 8.0
                self.set_font(self.fam, '', fs)
                while self.get_string_width(txt) > wv - 1.6 and fs > 6.0:
                    fs -= 0.25; self.set_font(self.fam, '', fs)
                if self.get_string_width(txt) > wv - 1.6:
                    while self.get_string_width(txt + '...') > wv - 1.6 and len(txt) > 4:
                        txt = txt[:-1]
                    txt += '...'
                self.cell(wv, h, txt, 1, 0, 'L')
            self.ln(h)

        def box(self, label, text, w=None, min_h=12.0, fs=7.6, lh=3.5):
            """Labelled multi-line box (label on a grey strip, text below), full width by default."""
            w = w or self.W
            x = self.get_x(); y = self.get_y()
            self.set_font(self.fam, 'B', 7.6); self.set_fill_color(*GREY_FILL)
            self.cell(w, 4.6, label, 1, 1, 'L', fill=True)
            self.set_x(x); self.set_font(self.fam, '', fs)
            lines = self.multi_cell(w - 2.0, lh, text or '-', 0, 'L', split_only=True)
            h = max(min_h, len(lines) * lh + 2.0)
            if self.get_y() + h > self.h - 30 and self.page_no() > 0:
                self.add_page(); self.set_x(x); self.set_font(self.fam, 'B', 7.6); self.set_fill_color(*GREY_FILL)
                self.cell(w, 4.6, label + ' (contd.)', 1, 1, 'L', fill=True); self.set_x(x); self.set_font(self.fam, '', fs)
            y2 = self.get_y()
            self.rect(x, y2, w, h)
            self.set_xy(x + 1.0, y2 + 1.0); self.multi_cell(w - 2.0, lh, text or '-', 0, 'L')
            self.set_xy(x, y2 + h)

        def tick(self, x, y, on, size=2.8):
            self.set_draw_color(0, 0, 0); self.rect(x, y, size, size)
            if on:
                self.set_line_width(0.45); self.line(x + 0.5, y + size / 2, x + size * 0.42, y + size - 0.5); self.line(x + size * 0.42, y + size - 0.5, x + size - 0.4, y + 0.5); self.set_line_width(0.2)

        def ticklabel(self, x, y, on, label, fs=7.0):
            self.tick(x, y + 0.5, on)
            self.set_xy(x + 3.6, y); self.set_font(self.fam, '', fs); self.cell(self.get_string_width(label) + 1, 3.8, label, 0, 0, 'L')
            return x + 3.6 + self.get_string_width(label) + 3.0

        def sig_panels(self, panels, top, h, lbl_role=True):
            """panels: list of (label, role, name, sig_path, date_text). Even widths across the page."""
            n = max(1, len(panels)); gap = 2.0
            w = (self.W - gap * (n - 1)) / n
            self.set_draw_color(*LINE)
            for i, panel in enumerate(panels):
                lbl, role, who, sig, dtxt = panel[:5]
                paper = len(panel) > 5 and panel[5] == 'paper'
                x = 10 + i * (w + gap)
                if not lbl and not who:               # spacer between panels, as on the paper form
                    continue
                self.rect(x, top, w, h)
                self.set_fill_color(*GREY_FILL); self.rect(x, top, w, 5.0, 'F')
                self.set_xy(x, top); self.set_font(self.fam, 'B', 8); self.cell(w, 5.0, lbl, 0, 0, 'C')
                img_h = h - 5.0 - 4.6 - 4.0 - 2.0
                iy = top + 6.0
                if sig:
                    try:
                        from PIL import Image as _Im
                        with _Im.open(sig) as im:
                            iw, ih = im.size
                        ww = w - 8; hh = ww * ih / iw
                        if hh > img_h:
                            hh = img_h; ww = hh * iw / ih
                        self.image(sig, x + (w - ww) / 2, iy + (img_h - hh) / 2, ww, hh)
                    except Exception:
                        sig = None
                if not sig and who:
                    self.set_xy(x, iy + img_h / 2 - 2); self.set_font(self.fam, '', 6.5); self.set_text_color(110, 110, 110)
                    self.cell(w, 4, 'Signed on the paper record' if paper else 'Electronically signed', 0, 0, 'C'); self.set_text_color(0, 0, 0)
                ny = top + 6.0 + img_h + 0.5
                self.line(x + 4, ny, x + w - 4, ny)
                self.set_xy(x, ny); self.set_font(self.fam, 'B', 7.8)
                nm = who or ''
                while self.get_string_width(nm) > w - 4 and len(nm) > 3:
                    nm = nm[:-2]
                self.cell(w, 4.6, nm, 0, 0, 'C')
                self.set_xy(x, ny + 4.6); self.set_font(self.fam, '', 6.8); self.set_text_color(90, 90, 90)
                self.cell(w, 4.0, ('%s%s' % (role, ('   Date: ' + dtxt) if dtxt else '')) if lbl_role else (dtxt or ''), 0, 0, 'C')
                self.set_text_color(0, 0, 0)
            self.set_draw_color(0, 0, 0)
            self.set_y(top + h)

    p = PDF(); p.alias_nb_pages(); p.set_auto_page_break(True, 30); p.add_page()
    return p


def _resp(pdf, name):
    out = pdf.output(dest='S')
    data = bytes(out) if not isinstance(out, str) else out.encode('latin-1')
    resp = HttpResponse(data, content_type='application/pdf')
    resp['Content-Disposition'] = 'inline; filename="%s.pdf"' % _re.sub(r'[^A-Za-z0-9._-]+', '_', name).strip('_')
    return resp


def _sig_block_space(pdf, need):
    if pdf.get_y() + need > pdf.h - 30:
        pdf.add_page()


# ---------------------------------------------------------------- FF-01 annual plan (landscape)
def ia_plan_pdf(request, pk):
    plan = get_object_or_404(IaPlan.objects.select_related('mr_by', 'ceo_by'), pk=pk)
    ctrl = _ia_docctrl('plan', plan.location)
    pdf = _pdf('ANNUAL INTERNAL AUDIT PLAN - %d' % plan.year, '%s LABORATORY' % plan.location.upper(), ctrl, plan.location, 'L',
               '' if plan.status == 'approved' else 'NOT APPROVED')
    f = pdf.fam
    pdf.set_y(40)
    dept_w = 40.0; mw = (pdf.W - dept_w) / 12.0; cw = mw / 2.0
    x0 = 10.0; y = pdf.get_y()
    pdf.set_draw_color(*LINE); pdf.set_fill_color(217, 225, 242)
    pdf.set_font(f, 'B', 8)
    pdf.rect(x0, y, dept_w, 21, 'DF'); pdf.set_xy(x0, y + 8); pdf.cell(dept_w, 5, 'Department', 0, 0, 'C')
    pdf.rect(x0 + dept_w, y, pdf.W - dept_w, 7, 'DF'); pdf.set_xy(x0 + dept_w, y); pdf.cell(pdf.W - dept_w, 7, 'Schedule Month', 0, 0, 'C')
    for i, m in enumerate(MONTHS):
        x = x0 + dept_w + i * mw
        pdf.rect(x, y + 7, mw, 7, 'DF'); pdf.set_xy(x, y + 7); pdf.set_font(f, 'B', 7.5); pdf.cell(mw, 7, m, 0, 0, 'C')
        for j, lab in enumerate(('Due', 'Done')):
            pdf.rect(x + j * cw, y + 14, cw, 7, 'DF'); pdf.set_xy(x + j * cw, y + 14); pdf.set_font(f, '', 6.2); pdf.cell(cw, 7, lab, 0, 0, 'C')
    y += 21
    rows = plan.rows or []
    rh = 9.0
    for row in rows:
        pdf.rect(x0, y, dept_w, rh); pdf.set_xy(x0 + 1, y); pdf.set_font(f, '', 7.5); pdf.cell(dept_w - 2, rh, row.get('department', ''), 0, 0, 'L')
        for i in range(12):
            cell = (row.get('months') or {}).get(str(i + 1), {})
            x = x0 + dept_w + i * mw
            for j, k in enumerate(('due', 'done')):
                if cell.get(k):
                    pdf.set_fill_color(*(AMBER if k == 'due' else GREEN_DONE)); pdf.rect(x + j * cw, y, cw, rh, 'DF')
                else:
                    pdf.rect(x + j * cw, y, cw, rh)
        y += rh
    for _ in range(max(0, 6 - len(rows))):
        pdf.rect(x0, y, dept_w, rh)
        for i in range(24):
            pdf.rect(x0 + dept_w + i * cw, y, cw, rh)
        y += rh
    pdf.set_y(y + 6)
    # legend
    lx = 10; ly = pdf.get_y()
    pdf.set_fill_color(*AMBER); pdf.rect(lx, ly, 30, 5, 'DF'); pdf.set_fill_color(*GREEN_DONE); pdf.rect(lx + 30, ly, 30, 5, 'DF')
    pdf.set_font(f, '', 7.5); pdf.set_xy(lx, ly + 5); pdf.cell(30, 4.5, 'Audit Planned', 1, 0, 'C'); pdf.cell(30, 4.5, 'Audit Completed', 1, 0, 'C')
    if plan.remarks:
        pdf.set_xy(10, ly + 12); pdf.set_font(f, '', 7.2); pdf.multi_cell(pdf.W, 3.4, 'Remarks: ' + plan.remarks.replace('\n', '  |  '))
    top = max(pdf.get_y() + 4, 135)
    mr_sig = _sig_image(plan.mr_by) if plan.mr_at else None
    ceo_sig = _sig_image(plan.ceo_by) if plan.ceo_at else None
    panels = [('Management Representative', 'Prepared by', plan.mr_name or (_uname(plan.mr_by) if plan.mr_by else ''), mr_sig, _d(plan.mr_date), '' if plan.mr_at else 'paper'),
              ('CEO', 'Approved by', plan.ceo_name or (_uname(plan.ceo_by) if plan.ceo_by else ''), ceo_sig, _d(plan.ceo_date), '' if plan.ceo_at else 'paper')]
    # two panels with a gap in the middle like the paper form
    gap_panels = [panels[0], ('', '', '', None, ''), panels[1]]
    pdf.sig_panels(gap_panels, top, 26)
    pdf.set_y(top + 30); pdf.set_font(f, 'B', 7.5); pdf.cell(pdf.W, 5, '---END OF THE DOCUMENT---', 0, 0, 'C')
    return _resp(pdf, 'IA_Plan_%s_%d' % (plan.location, plan.year))


# ---------------------------------------------------------------- FF-03 circular (portrait)
def ia_circular_pdf(request, pk):
    c = get_object_or_404(IaCircular.objects.select_related('issued_by'), pk=pk)
    ctrl = _ia_docctrl('circular', c.location)
    pdf = _pdf('INTERNAL AUDIT CIRCULAR' + (' - WITNESSING' if c.kind == 'witness' else ''), '%s LABORATORY  -  AUDIT NO. %s' % (c.location.upper(), c.audit_no), ctrl, c.location, 'P',
               '' if c.status == 'issued' else 'DRAFT')
    f = pdf.fam
    pdf.set_y(39)
    pdf.kv([('To:', c.to_text, 28, 92), ('Circular Issue Date:', _d(c.issue_date), 34, 36)])
    pdf.kv([('From:', c.from_text, 28, 92), ('Audit Date:', c.audit_date_text, 34, 36)])
    pdf.kv([('Audit No. / Year:', c.audit_no, 28, 92), ('Issued by:', (_uname(c.issued_by) if c.issued_by else '-'), 34, 36)])
    pdf.ln(2)
    cols = [('Sr.', 9), ('Day', 27), ('Time', 28), ('Scope', 50), ('Criteria / (Cross Audit)', 36), ('Auditors', 20), ('Auditee', 20)]
    pdf.set_font(f, 'B', 7.4); pdf.set_fill_color(*GREY_FILL); pdf.set_draw_color(*LINE)
    for lbl, w in cols:
        pdf.cell(w, 6, lbl, 1, 0, 'C', fill=True)
    pdf.ln(6)
    pdf.set_font(f, '', 7.0)
    for s in c.sessions or []:
        vals = [s.get('sr', ''), s.get('day', ''), '%s to %s' % (s.get('time_from', ''), s.get('time_to', '')), s.get('scope', ''), s.get('criteria', ''), s.get('auditors', ''), s.get('auditee', '')]
        heights = [len(pdf.multi_cell(w - 1.5, 3.4, v or '-', 0, 'L', split_only=True)) for (lbl, w), v in zip(cols, vals)]
        h = max(heights) * 3.4 + 1.5
        if pdf.get_y() + h > pdf.h - 32:
            pdf.add_page()
        x = pdf.get_x(); y = pdf.get_y()
        for (lbl, w), v in zip(cols, vals):
            pdf.rect(x, y, w, h); pdf.set_xy(x + 0.75, y + 0.75); pdf.multi_cell(w - 1.5, 3.4, v or '-', 0, 'L'); x += w
        pdf.set_xy(10, y + h)
    pdf.ln(3)
    if c.ceo_name:
        pdf.set_font(f, 'B', 8); pdf.cell(pdf.W, 5, c.ceo_name, 0, 1, 'R'); pdf.set_font(f, '', 7.5); pdf.cell(pdf.W, 4, 'C.E.O', 0, 1, 'R')
    pdf.ln(2)
    pdf.set_font(f, 'B', 8.5); pdf.cell(pdf.W, 6, 'Internal Audit Schedule / Notice Receiving Attendance', 0, 1, 'C')
    acols = [('S. No.', 14), ('Name of Employee', 70), ('Designation', 56), ('Signature', 50)]
    pdf.set_font(f, 'B', 7.4); pdf.set_fill_color(*GREY_FILL)
    for lbl, w in acols:
        pdf.cell(w, 6, lbl, 1, 0, 'C', fill=True)
    pdf.ln(6)
    from django.contrib.auth.models import User as _User
    for i, a in enumerate(c.attendance or []):
        h = 9.0
        if pdf.get_y() + h > pdf.h - 32:
            pdf.add_page()
        x = 10; y = pdf.get_y()
        pdf.set_font(f, '', 7.4)
        pdf.rect(x, y, 14, h); pdf.set_xy(x, y); pdf.cell(14, h, '%02d' % (i + 1), 0, 0, 'C'); x += 14
        pdf.rect(x, y, 70, h); pdf.set_xy(x + 1, y); pdf.cell(68, h, a.get('name', ''), 0, 0, 'L'); x += 70
        pdf.rect(x, y, 56, h); pdf.set_xy(x + 1, y); pdf.cell(54, h, a.get('designation', ''), 0, 0, 'L'); x += 56
        pdf.rect(x, y, 50, h)
        if a.get('signed_at') and a.get('user_id'):
            u = _User.objects.filter(pk=a['user_id']).first()
            sig = _sig_image(u) if u else None
            if sig:
                try:
                    pdf.image(sig, x + 12, y + 0.8, 26, 7.4)
                except Exception:
                    sig = None
            if not sig:
                pdf.set_xy(x, y); pdf.set_font(f, '', 6.4); pdf.cell(50, h, 'Electronically signed', 0, 0, 'C')
            pdf.set_xy(x + 1, y + h - 3.2); pdf.set_font(f, '', 5.6); pdf.set_text_color(110, 110, 110)
            pdf.cell(48, 3, '-'.join(reversed((a['signed_at'] or '')[:10].split('-'))), 0, 0, 'R'); pdf.set_text_color(0, 0, 0)
        pdf.set_xy(10, y + h)
    return _resp(pdf, 'IA_Circular_%s_%s' % (c.location, c.audit_no))


# ---------------------------------------------------------------- FF-02 audit report (portrait, multi-page)
def ia_audit_pdf(request, pk):
    a = get_object_or_404(IaAudit.objects.select_related('auditor_signed_by', 'auditee_signed_by'), pk=pk)
    ctrl = _ia_docctrl('report', a.location)
    wm = {'closed': '', 'auditor': 'AWAITING AUDITEE'}.get(a.status, 'DRAFT')
    pdf = _pdf('INTERNAL AUDIT REPORT', '%s LABORATORY  -  AUDIT NO. %s  -  ISO/IEC 17025:2017' % (a.location.upper(), a.audit_no), ctrl, a.location, 'P', wm)
    f = pdf.fam
    pdf.set_y(39)
    dates = '%s - %s (%02d day%s audit)' % (_d(a.date_start), _d(a.date_end), a.days, '' if a.days == 1 else 's') if a.date_start else '-'
    pdf.kv([('Name of the Lab:', 'Envi Tech AL', 30, 65), ('Audit No. / Year:', a.audit_no, 30, 65)])
    pdf.kv([('Audit Date:', dates, 30, 65), ('Auditor:', '%s%s' % (a.auditor, (' - ' + a.auditor_title) if a.auditor_title else ''), 30, 65)])
    pdf.kv([('Location:', '%s Laboratory Facility' % a.location, 30, 65), ('Auditee:', '%s%s' % (a.auditee, (' - ' + a.auditee_title) if a.auditee_title else ''), 30, 65)])
    pdf.kv([('Address:', a.address, 30, 160)])
    pdf.ln(2)
    cols = [('Clause', 18), ('Requirement', 58), ("Lab's Reference to its QMS", 32), ('Auditor Findings', 68), ('Result', 14)]
    def head():
        pdf.set_font(f, 'B', 7.2); pdf.set_fill_color(*GREY_FILL); pdf.set_draw_color(*LINE)
        for lbl, w in cols:
            pdf.cell(w, 6, lbl, 1, 0, 'C', fill=True)
        pdf.ln(6)
    head()
    for fd in a.findings.select_related('clause'):
        heading = (fd.clause and fd.clause.is_heading) or (fd.label and fd.label.count('.') == 0) or (not fd.finding and not fd.ref and len(fd.requirement) < 70)
        vals = [fd.label, fd.requirement, fd.ref.replace('\n', ' / '), fd.finding, _RESULT_LABEL.get(fd.result, '') if fd.result else '']
        pdf.set_font(f, 'B' if heading else '', 6.8)
        heights = [len(pdf.multi_cell(w - 1.5, 3.1, v or '', 0, 'L', split_only=True)) if v else 1 for (lbl, w), v in zip(cols, vals)]
        h = max(heights) * 3.1 + 1.4
        if pdf.get_y() + min(h, 60) > pdf.h - 32:
            pdf.add_page(); head()
        x = 10; y = pdf.get_y()
        if h > pdf.h - 32 - 45:          # a very long finding: let multi_cell paginate the finding column alone
            pass
        for (lbl, w), v in zip(cols, vals):
            if heading:
                pdf.set_fill_color(248, 250, 252); pdf.rect(x, y, w, h, 'DF')
            else:
                pdf.rect(x, y, w, h)
            if v:
                pdf.set_xy(x + 0.75, y + 0.7)
                if lbl == 'Result' and fd.result in ('minor', 'major'):
                    pdf.set_text_color(185, 28, 28)
                elif lbl == 'Result' and fd.result == 'obs':
                    pdf.set_text_color(180, 83, 9)
                pdf.multi_cell(w - 1.5, 3.1, v, 0, 'L'); pdf.set_text_color(0, 0, 0)
            x += w
        pdf.set_xy(10, y + h)
    # summary
    _sig_block_space(pdf, 60)
    pdf.ln(3); pdf.set_font(f, 'B', 8.5); pdf.cell(pdf.W, 5, 'Summary of Findings in Internal Audit', 0, 1, 'C')
    pdf.set_font(f, '', 7.8); pdf.set_draw_color(*LINE)
    lg = a.legacy or {}
    rows = [('Observations', a.n_obs), ('Minor NCs', a.n_minor), ('Major NCs', a.n_major), ('Total Number of NCs', a.n_total)]
    x0 = 10 + (pdf.W - 90) / 2
    for lbl, v in rows:
        pdf.set_x(x0); pdf.set_fill_color(*GREY_FILL); pdf.set_font(f, 'B', 7.8); pdf.cell(60, 5, lbl, 1, 0, 'L', fill=True); pdf.set_font(f, '', 7.8); pdf.cell(30, 5, '%02d' % v, 1, 1, 'C')
    if lg.get('summary') and (lg['summary'].get('obs'), lg['summary'].get('minor'), lg['summary'].get('major')) != (a.n_obs, a.n_minor, a.n_major):
        pdf.set_x(x0); pdf.set_font(f, '', 6.4); pdf.set_text_color(90, 90, 90)
        pdf.cell(90, 4, 'Workbook printed: %s observation(s), %s minor, %s major (%s total).' % (lg['summary'].get('obs'), lg['summary'].get('minor'), lg['summary'].get('major'), lg['summary'].get('total')), 0, 1, 'L')
        pdf.set_text_color(0, 0, 0)
    pdf.ln(1.5)
    pdf.kv([('Time frame agreed to close the NCs:', a.timeframe, 55, 135)])
    if a.conclusion:
        pdf.ln(1.5); pdf.box('Conclusion Statement', a.conclusion, min_h=10)
    if a.remarks:
        pdf.ln(1.5); pdf.box('Remarks', a.remarks, min_h=8, fs=6.8)
    _sig_block_space(pdf, 34)
    pdf.ln(3)
    top = pdf.get_y()
    lgs = (a.legacy or {}).get('sign') or {}
    panels = [('Signature of Internal Auditor', 'Name of Internal Auditor', _uname(a.auditor_signed_by) if a.auditor_signed_at else (lgs.get('auditor', '') if a.legacy else ''), _sig_image(a.auditor_signed_by) if a.auditor_signed_at else None, _d(a.auditor_sign_date), '' if a.auditor_signed_at else 'paper'),
              ('', '', '', None, ''),
              ('Signature of Internal Auditee', 'Name of Internal Auditee', _uname(a.auditee_signed_by) if a.auditee_signed_at else (lgs.get('auditee', '') if a.legacy else ''), _sig_image(a.auditee_signed_by) if a.auditee_signed_at else None, _d(a.auditee_sign_date), '' if a.auditee_signed_at else 'paper')]
    pdf.sig_panels(panels, top, 28)
    pdf.ln(3); pdf.set_font(f, 'B', 7.5); pdf.cell(pdf.W, 5, '---END OF THE DOCUMENT---', 0, 1, 'C')
    # witnessing records
    for w in a.witnessings.all():
        pdf.add_page()
        pdf.set_font(f, 'B', 9); pdf.cell(pdf.W, 6, 'Witnessing Report', 0, 1, 'L')
        pdf.set_font(f, '', 8); pdf.cell(pdf.W, 5, 'Date of Witnessing: %s' % _d(w.date), 0, 1, 'L')
        wcols = [('Parameter / test', 24), ('Performed by', 26), ('Range / values covered', 26), ('Assigned value (blind sample)', 22), ('Obtained value', 20), ('Remarks', 72)]
        pdf.set_font(f, 'B', 6.8); pdf.set_fill_color(*GREY_FILL)
        xh = 10; yh = pdf.get_y()
        for lbl, ww in wcols:
            pdf.rect(xh, yh, ww, 8, 'DF'); pdf.set_xy(xh, yh + 0.6); pdf.multi_cell(ww, 3.2, lbl, 0, 'C'); xh += ww
        pdf.set_xy(10, yh + 8)
        for r in w.rows or []:
            vals = [r.get('parameter', ''), r.get('performed_by', ''), r.get('range', ''), r.get('assigned', ''), r.get('obtained', ''), r.get('remarks', '')]
            pdf.set_font(f, '', 6.8)
            heights = [len(pdf.multi_cell(ww - 1.5, 3.1, v or '-', 0, 'L', split_only=True)) for (lbl, ww), v in zip(wcols, vals)]
            h = max(heights) * 3.1 + 1.4
            if pdf.get_y() + h > pdf.h - 32:
                pdf.add_page()
            x = 10; y = pdf.get_y()
            for (lbl, ww), v in zip(wcols, vals):
                pdf.rect(x, y, ww, h); pdf.set_xy(x + 0.75, y + 0.7); pdf.multi_cell(ww - 1.5, 3.1, v or '-', 0, 'L'); x += ww
            pdf.set_xy(10, y + h)
        _sig_block_space(pdf, 34)
        pdf.ln(4)
        from django.contrib.auth.models import User as _User
        panels = [('Signature of Internal Auditor', 'Name of Internal Auditor', _uname(w.auditor_signed_by) if w.auditor_signed_at else (w.auditor if w.legacy else ''), _sig_image(w.auditor_signed_by) if w.auditor_signed_at else None, _d(w.sign_date), '' if w.auditor_signed_at else 'paper')]
        for x in (w.auditees or [])[:3]:
            u = _User.objects.filter(pk=x.get('user_id')).first() if x.get('user_id') else None
            panels.append(('Signature of Internal Auditee', 'Name of Internal Auditee', (_uname(u) if (u and x.get('signed_at')) else (x.get('name', '') if w.legacy else '')), _sig_image(u) if (u and x.get('signed_at')) else None, _d(w.sign_date), '' if x.get('signed_at') else 'paper'))
        pdf.sig_panels(panels, pdf.get_y(), 28)
    return _resp(pdf, 'IA_Report_%s_%s' % (a.location, a.audit_no))


# ---------------------------------------------------------------- 710-FF-01 NC & corrective action form (portrait)
def ia_nc_pdf(request, pk):
    n = get_object_or_404(Ncca.objects.select_related('mr_signed_by', 'hod_signed_by', 'closed_by', 'evaluated_by'), pk=pk)
    ctrl = _ia_docctrl('nc', n.location)
    wm = {'closed': '', 'draft': 'DRAFT'}.get(n.status, 'OPEN')
    pdf = _pdf('NON-CONFORMANCE & CORRECTIVE ACTION FORM', '%s LABORATORY  -  %s' % (n.location.upper(), n.nc_no), ctrl, n.location, 'P', wm)
    f = pdf.fam
    pdf.set_y(39)
    pdf.kv([('Department:', n.department, 26, 60), ('NC&CA No.:', n.nc_no, 24, 46), ('Date:', _d(n.date), 14, 20)])
    pdf.kv([('NC&CA Raised by:', n.raised_by, 30, 56), ('Standard & Clause:', n.clause, 32, 72)])
    pdf.set_draw_color(*LINE)
    # Raised due to
    y = pdf.get_y(); L = 30.0; cw = (pdf.W - L) / 5.0
    def rowlabel(lbl, h):
        pdf.set_fill_color(*GREY_FILL); pdf.rect(10, y, L, h, 'DF'); pdf.set_xy(10, y); pdf.set_font(f, 'B', 7.4); pdf.multi_cell(L, h / 2 if lbl.count('\n') else h, lbl, 0, 'C')
    h = 12.0
    rowlabel('Raised Due to:', h)
    cells = [('Audit', [('Internal', n.due_audit_internal), ('External', n.due_audit_external)]), ('Testing', [('', n.due_testing)]),
             ('Calibration', [('Internal', n.due_cal_internal), ('External', n.due_cal_external)]), ('Customer Complaint', [('', n.due_complaint)]),
             ('Others', None)]
    for i, (lbl, ticks) in enumerate(cells):
        x = 10 + L + i * cw
        pdf.rect(x, y, cw, h); pdf.set_xy(x, y + 0.6); pdf.set_font(f, 'B', 7.2); pdf.cell(cw, 3.8, lbl, 0, 0, 'C')
        if ticks is None:
            pdf.set_xy(x + 1, y + 4.6); pdf.set_font(f, '', 6.6); pdf.multi_cell(cw - 2, 3.2, 'Specify: ' + (n.due_other or '-'), 0, 'L')
        else:
            tw = sum(pdf.get_string_width(t) + 7.0 for t, _ in ticks)
            tx = x + (cw - tw) / 2
            for t, on in ticks:
                tx = pdf.ticklabel(tx, y + 5.6, on, t, 6.8) if t else (pdf.tick(x + cw / 2 - 1.4, y + 6.0, on) or tx)
    y += h
    h = 12.0
    rowlabel('Nonconformance\nCategory', h)
    cats = [('Point for Improvement', 'pfi'), ('Observation', 'obs'), ('Minor Nonconformance', 'minor'), ('Major Nonconformance', 'major'), ('Critical Nonconformance', 'critical')]
    for i, (lbl, key) in enumerate(cats):
        x = 10 + L + i * cw
        pdf.rect(x, y, cw, h); pdf.set_xy(x, y + 0.6); pdf.set_font(f, '', 7.0); pdf.multi_cell(cw, 3.3, lbl, 0, 'C')
        pdf.tick(x + cw / 2 - 1.4, y + 8.0, n.category == key or (key == 'critical' and n.category_also_critical))
    y += h
    h = 14.0
    rowlabel('Significance\nEvaluation', h)
    sig = [('Legal Compliance', n.sig_legal), ('Poses Any Risk', n.sig_risk), ('Requires Halt work.', n.sig_halt), ('Require Preventive Action', n.sig_preventive)]
    for i, (lbl, on) in enumerate(sig):
        x = 10 + L + i * cw
        pdf.rect(x, y, cw, h); pdf.set_xy(x, y + 0.6); pdf.set_font(f, 'B', 7.0); pdf.multi_cell(cw, 3.3, lbl, 0, 'C')
        tx = x + cw / 2 - 11
        tx = pdf.ticklabel(tx, y + 9.2, bool(on), 'Yes', 6.8); pdf.ticklabel(tx, y + 9.2, not on, 'No', 6.8)
    x = 10 + L + 4 * cw
    pdf.rect(x, y, cw, h); pdf.set_xy(x, y + 2.0); pdf.set_font(f, '', 7.0); pdf.cell(cw, 3.8, 'Non-Significant', 0, 0, 'C'); pdf.tick(x + cw / 2 - 1.4, y + 8.0, n.sig_non_significant)
    y += h
    h = 14.0
    rowlabel('Nature of\nNonconformance', h)
    lv = [('Priority', n.priority, ['High', 'Medium', 'Low']), ('Risk Type', n.risk_type, ['High', 'Medium', 'Low/No']), ('Severity', n.severity, ['High', 'Medium', 'Low/No'])]
    for i, (lbl, val, opts) in enumerate(lv):
        x = 10 + L + i * cw
        pdf.rect(x, y, cw, h); pdf.set_xy(x, y + 0.6); pdf.set_font(f, 'B', 7.0); pdf.cell(cw, 3.8, lbl, 0, 0, 'C')
        pdf.set_xy(x, y + 4.4); pdf.set_font(f, '', 6.4); pdf.cell(cw, 3.4, '   '.join(opts), 0, 0, 'C')
        sw = cw / 3.0
        for j, o in enumerate(('high', 'medium', 'low')):
            pdf.tick(x + j * sw + sw / 2 - 1.4, y + 9.2, val == o)
    x = 10 + L + 3 * cw
    pdf.rect(x, y, cw, h); pdf.set_xy(x, y + 0.6); pdf.set_font(f, 'B', 7.0); pdf.cell(cw, 3.8, 'Impact Analysis', 0, 0, 'C')
    pdf.set_xy(x, y + 4.4); pdf.set_font(f, '', 6.4); pdf.cell(cw, 3.4, 'Affects Past Result', 0, 0, 'C')
    tx = pdf.ticklabel(x + cw / 2 - 11, y + 9.2, n.impact_past, 'Yes', 6.8); pdf.ticklabel(tx, y + 9.2, not n.impact_past, 'No', 6.8)
    x = 10 + L + 4 * cw
    pdf.rect(x, y, cw, h); pdf.set_xy(x + 0.5, y + 0.6); pdf.set_font(f, '', 5.4); pdf.multi_cell(cw - 1, 2.6, 'Category, Significance & Nature', 0, 'C')
    pdf.set_xy(x, y + 5.0); pdf.set_font(f, 'B', 6.8); pdf.cell(cw, 3.6, 'Evaluated By M.R', 0, 0, 'C')
    pdf.set_xy(x, y + 8.8); pdf.set_font(f, 'B', 6.8); pdf.cell(cw, 3.6, 'Date: %s' % (_d(n.evaluated_date) or '-'), 0, 0, 'C')
    y += h
    pdf.set_xy(10, y)
    pdf.box('Non-Conformity / Observation Details:', n.details, min_h=22)
    # proposed completion + MR sign
    y = pdf.get_y()
    pdf.set_font(f, 'B', 7.4); pdf.set_fill_color(*GREY_FILL)
    pdf.cell(44, 9, 'Proposed completion date:', 1, 0, 'L', fill=True); pdf.set_font(f, '', 7.8); pdf.cell(51, 9, _d(n.proposed_date) or '-', 1, 0, 'L')
    pdf.set_font(f, 'B', 7.4); pdf.cell(34, 9, 'MR / Designee Sign:', 1, 0, 'L', fill=True)
    x = pdf.get_x(); pdf.rect(x, y, pdf.W - 129, 9)
    _sig_cell(pdf, x, y, pdf.W - 129, 9, n.mr_signed_by if n.mr_signed_at else None, n.mr_signed_at)
    pdf.set_xy(10, y + 9)
    pdf.set_font(f, 'B', 7.6); pdf.set_fill_color(230, 236, 232); pdf.cell(pdf.W, 4.6, 'Concern Department Section', 1, 1, 'L', fill=True)
    pdf.box('Root Cause:', n.root_cause, min_h=18)
    pdf.box('Corrective Action (to eliminate the root cause):', n.corrective, min_h=18)
    y = pdf.get_y()
    pdf.set_font(f, 'B', 7.4); pdf.set_fill_color(*GREY_FILL)
    pdf.cell(30, 9, 'Completion date:', 1, 0, 'L', fill=True); pdf.set_font(f, '', 7.8); pdf.cell(50, 9, _d(n.completion_date) or '-', 1, 0, 'L')
    pdf.set_font(f, 'B', 7.4); pdf.cell(54, 9, 'Concerned Head of Department Sign:', 1, 0, 'L', fill=True)
    x = pdf.get_x(); pdf.rect(x, y, pdf.W - 134, 9)
    _sig_cell(pdf, x, y, pdf.W - 134, 9, n.hod_signed_by if n.hod_signed_at else None, n.hod_signed_at)
    pdf.set_xy(10, y + 9)
    _sig_block_space(pdf, 48)
    pdf.set_font(f, 'B', 7.6); pdf.set_fill_color(230, 236, 232); pdf.cell(pdf.W, 4.6, 'MR Section', 1, 1, 'L', fill=True)
    sat = '' if n.satisfactory is None else ('Yes' if n.satisfactory else 'No')
    y = pdf.get_y()
    pdf.set_font(f, 'B', 7.4); pdf.set_fill_color(*GREY_FILL); pdf.cell(44, 6, 'Follow-Up & Close Out with:', 1, 0, 'L', fill=True)
    pdf.set_font(f, '', 7.8); pdf.cell(66, 6, n.followup_with or '-', 1, 0, 'L')
    pdf.set_font(f, 'B', 7.4); pdf.cell(24, 6, 'Satisfactory:', 1, 0, 'L', fill=True)
    x = pdf.get_x(); pdf.rect(x, y, pdf.W - 134, 6)
    tx = pdf.ticklabel(x + 8, y + 1.1, n.satisfactory is True, 'Yes', 7.0); pdf.ticklabel(tx + 6, y + 1.1, n.satisfactory is False, 'No', 7.0)
    pdf.set_xy(10, y + 6)
    pdf.kv([('Follow-Up & Close-Out Date:', _d(n.followup_date), 44, 66), ('If not satisfactory, Next Follow up Date', _d(n.next_followup_date), 48, 32)], h=6)
    pdf.box('Description of Follow-up / 2nd Follow-Up:', n.followup_desc, min_h=14)
    y = pdf.get_y()
    pdf.set_font(f, 'B', 7.4); pdf.set_fill_color(*GREY_FILL); pdf.cell(30, 10, 'NC&CA Closed by:', 1, 0, 'L', fill=True)
    x = pdf.get_x(); pdf.rect(x, y, 60, 10)
    _sig_cell(pdf, x, y, 60, 10, n.closed_by if n.closed_at else None, n.closed_at, n.closed_by_name)
    pdf.set_xy(x + 60, y); pdf.set_font(f, 'B', 7.4); pdf.cell(20, 10, 'Remarks:', 1, 0, 'L', fill=True); pdf.set_font(f, '', 7.6); pdf.cell(pdf.W - 110, 10, (n.remarks or '-')[:90], 1, 0, 'L')
    pdf.set_xy(10, y + 11)
    pdf.set_font(f, 'B', 6.4); pdf.multi_cell(pdf.W, 3.2, 'Note: All Observations raised during the internal audits will be reviewed, and verified in the next plan audit by the Internal Auditor(s).', 0, 'L')
    return _resp(pdf, 'NCCA_%s_%s' % (n.location, n.nc_no))


def _sig_cell(pdf, x, y, w, h, user, when, name=''):
    """Small inline signature cell: e-signature image (if any) with the name under it."""
    f = pdf.fam
    who = _uname(user) if user else name
    sig = _sig_image(user) if user else None
    if sig:
        try:
            pdf.image(sig, x + 2, y + 0.6, min(w - 30, 22), h - 1.2)
        except Exception:
            sig = None
    pdf.set_xy(x + (26 if sig else 1.5), y)
    pdf.set_font(f, 'B' if who else '', 7.0)
    pdf.cell(w - (27 if sig else 3), h, (who + (('  ' + _d(when.date())) if when else '')) if who else '', 0, 0, 'L')


# ---------------------------------------------------------------- 710-FF-01A root cause analysis (landscape)
def ia_rca_pdf(request, pk):
    n = get_object_or_404(Ncca, pk=pk)
    r = get_object_or_404(NccaRca.objects.select_related('performed_by', 'reviewed_by'), nc=n)
    ctrl = _ia_docctrl('rca', n.location)
    wm = {'reviewed': '', 'draft': 'DRAFT'}.get(r.status, 'AWAITING CEO REVIEW')
    pdf = _pdf('ROOT CAUSE ANALYSIS FORM', '%s LABORATORY  -  %s' % (n.location.upper(), n.nc_no), ctrl, n.location, 'L', wm)
    f = pdf.fam
    pdf.set_y(38)
    pdf.kv([('NCR #', n.nc_no, 16, 44), ('Clause #', r.clause, 16, 30), ('RCA #', r.rca_no, 14, 40), ('Person Deputed For RCA', r.deputed, 40, 42), ('Date', _d(r.date), 14, 29)], h=5.6)
    pdf.ln(1)
    pdf.set_font(f, 'B', 7.6); pdf.cell(pdf.W, 4.5, 'Selection of Potential Causes:', 0, 1, 'L')
    pdf.set_fill_color(*GREY_FILL); pdf.set_draw_color(*LINE)
    pdf.cell(44, 5, 'Possible Main Causes', 1, 0, 'C', fill=True); pdf.cell(pdf.W - 44, 5, 'Possible Sub Causes:', 1, 1, 'C', fill=True)
    causes = r.causes or {}
    for main, subs in NccaRca.MAIN_CAUSES:
        y = pdf.get_y(); h = 5.4
        pdf.rect(10, y, 44, h); pdf.tick(12, y + 1.6, main in causes); pdf.set_xy(16.5, y); pdf.set_font(f, '', 7.2); pdf.cell(37, h, main, 0, 0, 'L')
        pdf.rect(54, y, pdf.W - 44, h)
        picked = causes.get(main) or []
        tx = 56
        for s in subs:
            tx = pdf.ticklabel(tx, y + 1.1, s in picked, s, 6.6)
        other = causes.get(main + ':other', '')
        pdf.ticklabel(tx, y + 1.1, bool(other), 'Other: ' + other if other else 'Other:', 6.6)
        pdf.set_xy(10, y + h)
    y = pdf.get_y(); h = 5.4
    pdf.rect(10, y, 44, h); pdf.tick(12, y + 1.3, bool(r.other)); pdf.set_xy(16.5, y); pdf.set_font(f, '', 7.2); pdf.cell(37, h, 'Other:', 0, 0, 'L')
    pdf.rect(54, y, pdf.W - 44, h); pdf.set_xy(56, y); pdf.set_font(f, '', 6.8); pdf.cell(pdf.W - 48, h, r.other or '', 0, 0, 'L')
    pdf.set_xy(10, y + h + 1)
    y = pdf.get_y()
    pdf.set_font(f, 'B', 7.4); pdf.cell(44, 5.5, '6 Why Analysis Technique', 1, 0, 'L', fill=True)
    x = pdf.get_x(); pdf.rect(x, y, pdf.W - 44, 5.5)
    tx = pdf.ticklabel(x + 3, y + 0.9, r.six_why, 'Required for further in-depth analysis', 6.8)
    pdf.ticklabel(tx + 20, y + 0.9, not r.six_why, 'Not Required as above analysis have given conclusion', 6.8)
    pdf.set_xy(10, y + 6.5)
    y = pdf.get_y()
    pdf.set_font(f, 'B', 7.2); pdf.cell(58, 4, 'Statement of Problem as identified in above analysis', 0, 0, 'L')
    pdf.set_xy(70, y); pdf.set_font(f, '', 6.4); pdf.multi_cell(pdf.W - 60, 2.8, (r.statement or '-')[:700], 0, 'L')
    pdf.set_line_width(0.3); pdf.line(70, pdf.get_y() + 0.5, 10 + pdf.W, pdf.get_y() + 0.5); pdf.set_line_width(0.2)
    pdf.set_xy(10, pdf.get_y() + 1.5)
    pdf.set_font(f, '', 6.2); pdf.set_text_color(90, 90, 90); pdf.cell(pdf.W, 3.4, 'Why?  -  stop at the Why where no further answer is possible', 0, 1, 'R'); pdf.set_text_color(0, 0, 0)
    # Why chain: six boxes in a 3 x 2 zig-zag as on the form
    whys = list(r.whys or []) + [''] * 6
    y0 = pdf.get_y(); bw = 82.0; bh = 12.5; gx = 10.0
    pos = [(10, y0), (10 + bw + gx, y0), (10 + 2 * (bw + gx), y0), (10 + 2 * (bw + gx), y0 + bh + 5), (10 + bw + gx, y0 + bh + 5), (10, y0 + bh + 5)]
    for i, (x, y) in enumerate(pos):
        pdf.rect(x, y, bw, bh)
        pdf.set_fill_color(*GREY_FILL); pdf.rect(x, y, 16, bh, 'F'); pdf.set_xy(x, y + bh / 2 - 2); pdf.set_font(f, 'B', 7.4); pdf.cell(16, 4, '%d. Why?' % (i + 1), 0, 0, 'C')
        pdf.set_xy(x + 17, y + 0.8); pdf.set_font(f, '', 6.0); pdf.multi_cell(bw - 18, 2.6, (whys[i] or '---')[:300], 0, 'L')
        if i < 5:
            pdf.set_font(f, 'B', 6.2); pdf.set_text_color(90, 90, 90)
            nx, ny = pos[i + 1]
            if ny == y:
                pdf.set_xy(x + bw, y + bh / 2 - 2); pdf.cell(gx, 4, 'Therefore', 0, 0, 'C')
            else:
                pdf.set_xy(x + bw - 20, y + bh); pdf.cell(20, 5, 'Therefore', 0, 0, 'C')
            pdf.set_text_color(0, 0, 0)
    yb = y0 + 2 * bh + 8
    pdf.set_xy(10, yb)
    pdf.set_auto_page_break(False)
    pdf.box('Conclusion:', (r.conclusion or '')[:600], w=pdf.W - 100, min_h=14, fs=6.8, lh=3.0)
    pdf.set_draw_color(*LINE)
    pn = r.performed_name or (_uname(r.performed_by) if r.performed_by else '')
    rn = r.reviewed_name or (_uname(r.reviewed_by) if r.reviewed_by else '')
    pdf.set_xy(10 + pdf.W - 96, yb)
    pdf.set_font(f, 'B', 7.2); pdf.cell(22, 6, 'Performed By:', 0, 0, 'L'); x = pdf.get_x(); pdf.rect(x, yb, 24, 9)
    _sig_cell(pdf, x, yb, 24, 9, r.performed_by if r.performed_at else None, None, pn)
    pdf.set_xy(x + 26, yb); pdf.cell(20, 6, 'Reviewed by:', 0, 0, 'L'); x2 = pdf.get_x(); pdf.rect(x2, yb, 24, 9)
    _sig_cell(pdf, x2, yb, 24, 9, r.reviewed_by if r.reviewed_at else None, None, rn)
    pdf.set_xy(10 + pdf.W - 96, yb + 10); pdf.set_font(f, 'B', 7.2); pdf.cell(22, 5, 'Date:', 0, 0, 'L'); pdf.set_font(f, '', 7.2); pdf.cell(24, 5, _d(r.performed_date) or '-', 'B', 0, 'C')
    pdf.set_x(pdf.get_x() + 2); pdf.set_font(f, 'B', 7.2); pdf.cell(20, 5, 'Date:', 0, 0, 'L'); pdf.set_font(f, '', 7.2); pdf.cell(24, 5, _d(r.reviewed_date) or '-', 'B', 0, 'C')
    pdf.set_xy(10, min(max(pdf.get_y(), yb + 20) + 3, pdf.h - 28))
    pdf.set_font(f, 'B', 7.5); pdf.cell(pdf.W, 5, 'End of Document', 'T', 0, 'C')
    return _resp(pdf, 'RCA_%s_%s' % (n.location, r.rca_no or n.nc_no))


# ---------------------------------------------------------------- 710-FF-02 NC&CA log (landscape)
def ia_log_pdf(request):
    loc = _loc_of(request)
    year = request.GET.get('year')
    qs = Ncca.objects.filter(location=loc).select_related('closed_by')
    if (year or '').isdigit():
        qs = qs.filter(date__year=int(year))
    rows = list(qs.order_by('log_sno', 'date', 'id'))
    ctrl = _ia_docctrl('log', loc)
    pdf = _pdf('NON-CONFORMANCE & CORRECTIVE ACTION LOG', '%s LABORATORY%s' % (loc.upper(), ('  -  ' + year) if (year or '').isdigit() else ''), ctrl, loc, 'L')
    f = pdf.fam
    pdf.set_y(38)
    cols = [('S. No.', 11), ('NC & CA #', 34), ('Standard & Clause Reference', 30), ('Category (if NC)', 20), ('Reported By (Name and Designation)', 34), ('Date', 18),
            ('Assigned To (Name and Designation)', 32), ('Date', 18), ('Target Date', 18), ('Follow up Date', 18), ('Closing Date', 18), ('Close By (Name and Designation)', 32), ('Closed By Sign', 20)]
    def head():
        pdf.set_font(f, 'B', 6.6); pdf.set_fill_color(*GREY_FILL); pdf.set_draw_color(*LINE)
        x = 10; y = pdf.get_y()
        for lbl, w in cols:
            pdf.rect(x, y, w, 10, 'DF'); pdf.set_xy(x, y + 0.5); pdf.multi_cell(w, 3.0, lbl, 0, 'C'); x += w
        pdf.set_xy(10, y + 10)
    head()
    for i, n in enumerate(rows):
        vals = [str(n.log_sno or i + 1), n.nc_no, '%s (ISO/IEC 17025:2017)' % n.clause.split(' (')[0] if n.clause else '', _CAT_LABEL.get(n.category, '').replace(' nonconformance', ''),
                n.raised_by, _d(n.date), n.assigned_to, _d(n.assigned_date), _d(n.target_date), _d(n.followup_date), _d(n.closing_date),
                n.closed_by_name or (_uname(n.closed_by) if n.closed_by else ''), '']
        pdf.set_font(f, '', 6.4)
        heights = [len(pdf.multi_cell(w - 1.2, 2.9, v or '-', 0, 'C', split_only=True)) for (lbl, w), v in zip(cols, vals)]
        h = max(max(heights) * 2.9 + 1.4, 7.5)
        if pdf.get_y() + h > pdf.h - 32:
            pdf.add_page(); head()
        x = 10; y = pdf.get_y()
        for (lbl, w), v in zip(cols, vals):
            pdf.rect(x, y, w, h)
            if lbl == 'Closed By Sign':
                if n.closed_at and n.closed_by:
                    sig = _sig_image(n.closed_by)
                    if sig:
                        try:
                            pdf.image(sig, x + 2, y + 0.6, w - 4, min(h - 1.2, 6.5))
                        except Exception:
                            pass
                    else:
                        pdf.set_xy(x, y); pdf.set_font(f, '', 5.4); pdf.cell(w, h, 'e-signed', 0, 0, 'C')
            else:
                pdf.set_xy(x + 0.6, y + 0.7); pdf.multi_cell(w - 1.2, 2.9, v or '-', 0, 'C')
            x += w
        pdf.set_xy(10, y + h)
    if not rows:
        pdf.set_font(f, '', 8); pdf.cell(pdf.W, 8, 'No NC&CA records.', 0, 1, 'C')
    return _resp(pdf, 'NCCA_Log_%s%s' % (loc, ('_' + year) if (year or '').isdigit() else ''))
