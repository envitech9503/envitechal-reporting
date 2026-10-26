"""ETAL-LAB-708-FF-17 Customer Request Form for MOU & SOC, laid out as the laboratory's controlled Word form (26-10-2026).

Karachi prints its form (Issue 01 / Rev 01: "CUSTOMER REQUEST FORM FOR MOU & SOC", four types of request, name and
authorised signature on one line); Lahore prints its own (Issue 02 / Rev 01: "CUSTOMER REQUEST FORM", measurement of
uncertainty and statement of conformity, name and signature on separate lines, Lahore office in the footer).
The values are written on the form's underlined blanks; the boxes are ticked as on the paper form.
"""
import os

from django.conf import settings
from fpdf import FPDF

GREEN = (0, 166, 81)
BAND = (218, 230, 242)
BLUE = (0, 32, 160)
INK = (0, 0, 0)

_FOOT = {
    'Karachi': {'tel': '+92 310 2288801', 'office': ('Head Office: ', '345, First Floor, Street-15, Block-3, Bahadurabad, Karachi. 75900, Pakistan.'), 'band': ''},
    'Lahore': {'tel': '+92 042-32296099', 'office': ('', 'Madina Heights, Office# A/30-31, 8th Floor, Shaukat Ali road, Johar Town, Lahore, Pakistan.'),
               'band': 'Head Office: 345, First Floor, Street-15, Block-3, Bahadurabad, Karachi. 75900, Pakistan.'},
}


def _p(rel):
    base = str(getattr(settings, 'BASE_DIR', '') or '')
    return os.path.join(base, rel) if base else rel


class _Form(FPDF):
    def __init__(self, ctrl, location):
        super().__init__('P', 'mm', 'A4')
        self.ctrl, self.loc = ctrl, location if location in _FOOT else 'Karachi'
        self.fam = 'Helvetica'
        cal, calb = _p('static/fonts/calibri.ttf'), _p('static/fonts/calibrib.ttf')
        if os.path.exists(cal):
            self.add_font('Calibri', '', cal); self.add_font('Calibri', 'B', calb if os.path.exists(calb) else cal)
            self.fam = 'Calibri'
        self.set_auto_page_break(False)
        self.set_margins(10, 10, 10)

    def header(self):
        w = self.w
        # green corner shape, grey rule and the logo, as on the Word form
        self.set_fill_color(*GREEN)
        self.polygon([(w - 66, 0), (w, 0), (w, 14), (w - 52, 14)], style='F')
        self.set_draw_color(200, 200, 200); self.set_line_width(0.6); self.line(0, 30, w, 30); self.set_line_width(0.2)
        logo = _p('static/assets/etal_form_logo.png')
        if not os.path.exists(logo):
            logo = _p('static/assets/EnviTechAL LOGO.png')
        try:
            self.image(logo, 7, 3, 21, 24)
        except Exception:
            pass
        self.set_text_color(*BLUE); self.set_font('Helvetica', '', 13)
        self.set_xy(0, 6); self.cell(w, 6, 'Envi Tech AL', 0, 0, 'C')
        c = self.ctrl
        rev = ('Issue No: %s Rev. No: %s' if self.loc == 'Lahore' else 'Issue No: %s  Rev.No %s') % (c['issue_no'], c['rev_no'])
        lines = [c['doc_no'], 'Issue Date: %s' % c['issue_date'], rev, 'Page No:  01 of 01']
        self.set_text_color(*INK); self.set_draw_color(0, 0, 0)
        self.set_fill_color(255, 255, 255); self.rect(w - 60, 13, 48, 18.5, 'DF')
        self.set_font(self.fam, 'B', 7)
        for i, l in enumerate(lines):
            self.set_xy(w - 58.5, 14 + i * 4.1); self.cell(45, 4.1, l, 0, 0, 'L')

    def footer(self):
        w, h = self.w, self.h
        f = _FOOT[self.loc]
        y = h - 20
        self.set_text_color(*INK); self.set_font(self.fam, '', 7.5)
        self.set_xy(14, y); self.cell(40, 5, f['tel'], 0, 0, 'L')
        self.set_xy(66, y - 2.2)
        lbl, txt = f['office']
        if lbl:
            self.set_font(self.fam, 'B', 7.5); self.write(3.6, lbl)
        self.set_font(self.fam, '', 7.5)
        self.set_left_margin(66); self.set_right_margin(w - 134)
        self.write(3.6, txt)
        self.set_left_margin(10); self.set_right_margin(10)
        self.set_fill_color(*BLUE)
        self.polygon([(w - 72, y - 4), (w, y - 4), (w, y + 8), (w - 66, y + 8)], style='F')
        self.set_text_color(255, 255, 255); self.set_font(self.fam, 'B', 7.5)
        self.set_xy(w - 54, y - 2.5); self.cell(50, 3.8, 'info@envitechal.com', 0, 2, 'L')
        self.set_x(w - 54); self.cell(50, 3.8, 'www.envitechal.com', 0, 0, 'L')
        self.set_fill_color(*GREEN); self.rect(0, h - 8, w, 8, 'F')
        if f['band']:
            self.set_xy(0, h - 7); self.set_font(self.fam, 'B', 7)
            self.cell(w, 6, f['band'], 0, 0, 'C')
        self.set_text_color(*INK)


def build_ff17(q, ctrl, signer_name='', sign_img=None, watermark=''):
    """The form for one SocRequest `q`; ctrl = document control of the request's laboratory."""
    loc = q.location if q.location in _FOOT else 'Karachi'
    lahore = loc == 'Lahore'
    pdf = _Form(ctrl, loc)
    pdf.add_page()
    f = pdf.fam
    X0, X1 = 13.0, 197.0          # the form frame
    W = X1 - X0
    if watermark:
        with pdf.local_context():
            pdf.set_font(f, 'B', 50); pdf.set_text_color(235, 235, 235)
            with pdf.rotation(40, pdf.w / 2, pdf.h / 2):
                pdf.text(pdf.w / 2 - pdf.get_string_width(watermark) / 2, pdf.h / 2, watermark)

    def lbl(x, y, t, size=8.2):
        pdf.set_font(f, 'B', size); pdf.set_xy(x, y); pdf.cell(pdf.get_string_width(t) + 0.6, 5, t, 0, 0, 'L')
        return x + pdf.get_string_width(t) + 1.2

    def blank(x, y, x_end, val, bold_val=True):
        """A value written on an underlined blank from x to x_end (the text may run past the end, as typed)."""
        pdf.set_font(f, 'B' if bold_val else '', 8.2)
        s = str(val or '')
        tw = pdf.get_string_width(s)
        pdf.set_xy(x + 1, y); pdf.cell(tw, 5, s, 0, 0, 'L')
        pdf.set_line_width(0.2); pdf.line(x, y + 4.3, max(x_end, x + tw + 2), y + 4.3)

    def para(x, y, x_end, label, val, lh=4.6):
        """Label followed by a long underlined value that wraps onto following underlined lines."""
        xs = lbl(x, y, label)
        pdf.set_font(f, 'B', 8.2)
        words, line, lines, cur_x = str(val or '').split(), '', [], xs
        for wd in words:
            t = (line + ' ' + wd).strip()
            if pdf.get_string_width(t) > (x_end - cur_x - 2) and line:
                lines.append((cur_x, line)); line, cur_x = wd, x
            else:
                line = t
        lines.append((cur_x, line))
        for i, (lx, t) in enumerate(lines):
            yy = y + i * lh
            pdf.set_xy(lx + 1, yy); pdf.cell(pdf.get_string_width(t), 5, t, 0, 0, 'L')
            end = lx + pdf.get_string_width(t) + 2
            if i == len(lines) - 1:                       # the last line's blank runs to the end, as on the form
                end = max(end, x_end)
            pdf.line(lx, yy + 4.3, end, yy + 4.3)
        return y + len(lines) * lh

    def box(x, y, on):
        pdf.set_line_width(0.25); pdf.rect(x, y + 0.8, 3.2, 3.2)
        if on:
            pdf.line(x, y + 0.8, x + 3.2, y + 4.0); pdf.line(x + 3.2, y + 0.8, x, y + 4.0)
        return x + 4.6

    def band(y, t, h=6.4):
        pdf.set_fill_color(*BAND); pdf.rect(X0, y, W, h, 'DF')
        pdf.set_font(f, 'B', 8.2); pdf.set_xy(X0 + 2, y + 0.7); pdf.cell(80, 5, t, 0, 0, 'L')
        return y + h

    pdf.set_draw_color(0, 0, 0)
    top = 41.0
    # title
    pdf.set_line_width(0.5)
    pdf.set_font(f, 'B', 11)
    pdf.set_xy(X0, top); pdf.cell(W, 8, 'CUSTOMER REQUEST FORM' if lahore else 'CUSTOMER REQUEST FORM FOR MOU & SOC', 0, 0, 'C')
    pdf.line(X0, top + 8, X1, top + 8)
    pdf.set_line_width(0.2)
    y = top + 10.5
    # date and reason
    dt = q.date.strftime('%d-%m-%Y') if q.date else ''
    xe = lbl(X0 + 2, y, 'Date:')
    blank(xe, y, xe + 32, dt)
    y = para(xe + 36, y, X1 - 2, 'Reason for Request ', q.reason) + 1.2
    xe = lbl(X0 + 2, y, 'Name of Organization:'); blank(xe, y, X1 - 2, q.organization); y += 6.4
    xe = lbl(X0 + 2, y, 'Name of Customer:'); blank(xe, y, xe + 50, q.customer_name)
    xe2 = lbl(xe + 54, y, 'Contact Details:'); blank(xe2, y, X1 - 2, q.contact); y += 6.4
    y = para(X0 + 2, y, X1 - 2, 'Address: ', q.address) + 1.6
    # sample information
    y = band(y, 'Sample Information:')
    y += 1.2
    lbl(X0 + 2, y, 'Analysis Requested:'); y += 6
    x = box(X0 + 3, y, q.analysis == 'ww'); x = lbl(x, y, 'Wastewater')
    x = box(x + 1, y, q.analysis == 'dw'); x = lbl(x, y, 'Drinking Water')
    x = lbl(x + 5, y, 'Others (Please Specify)')
    blank(x, y, x + 60, q.analysis_other if q.analysis == 'other' else '')
    y += 6.6
    y = para(X0 + 2, y, X1 - 2, 'Parameters: ', q.parameters) + 1.4
    sec_top = y
    # type of request
    y = band(y, 'Type of Request:')
    y += 7
    x = box(X0 + 3, y, q.req_mou); x = lbl(x, y, 'Measurement of Uncertainty')
    x = box(x + 1, y, q.req_soc); x = lbl(x, y, 'Statement of Conformity')
    if not lahore:
        x = box(x + 1, y, q.req_opinion); x = lbl(x, y, 'Opinions & Interpretation')
        x = box(x + 1, y, q.req_limits); x = lbl(x, y, 'Customer Specification')
        y += 4.6; lbl(X0 + 2, y, 'Limit')
    y += 7
    other = q.req_other if (q.req_other or '').strip() not in ('-',) else ''
    if lahore:
        extra = [t for t, on in (('Opinions & Interpretation', q.req_opinion), ('Customer Specification Limit', q.req_limits)) if on]
        other = ', '.join(extra + ([other] if other else []))
    xe = lbl(X0 + 2, y, 'Others (Please Specify)'); blank(xe, y, xe + 115, other); y += 7.4
    # reporting of results
    y = band(y, 'Reporting of Results:')
    y += (5.5 if lahore else 1.4)
    pdf.set_font(f, 'B', 8.2); pdf.set_xy(X0 + 2, y)
    pdf.cell(W - 4, 5, 'Please specify specification limit, select decision rules, and select decision rules statements of conformity wishes to use:', 0, 0, 'L')
    y += 7
    rep = (q.reporting or '').strip()
    rep = '' if rep == '-' else rep
    y = para(X0 + 2, y, X1 - 2, '', rep or ' ')
    if lahore:
        pdf.line(X0 + 2, y + 4.3 - 4.6 + 5, X1 - 2, y + 4.3 - 4.6 + 5); y += 5
    pdf.line(X0 + 2, y - 4.6 + 4.3, X1 - 2, y - 4.6 + 4.3)
    y += 3.4
    # Envi Tech AL follow up
    y = band(y, 'Envi Tech AL')
    fy = y
    mid = X0 + W * 0.56 if not lahore else X0 + W * 0.5
    y += 1.4
    lbl(X0 + 2, y, 'Follow Up Action:'); y += 6.6
    x = box(X0 + 3, y, q.decision == 'approved'); lbl(x, y, 'Request Approved')
    x = box(mid + 3, y, q.decision == 'denied'); lbl(x, y, 'Request Denied')
    y += 7.4
    appr, deny = q.decision == 'approved', q.decision == 'denied'
    ya = para(X0 + 3, y, mid - 3, 'Comment: ', q.decision_comment if appr else '')
    yd = para(mid + 3, y, X1 - 3, 'Comment: ', q.decision_comment if deny else '')
    y = max(ya, yd) + 2.6
    ddt = q.decision_date.strftime('%d-%m-%Y') if q.decision_date else ''
    xe = lbl(X0 + 3, y, 'Date:'); blank(xe, y, xe + 42, ddt if appr else '')
    xe = lbl(mid + 3, y, 'Date:'); blank(xe, y, xe + 30, ddt if deny else '')
    y += 8
    pdf.line(mid, fy, mid, y)
    pdf.line(X0, y, X1, y)
    # name and authorised signature
    y += 6
    signed = signer_name or ''
    if lahore:
        xe = lbl(X0 + 2, y, 'Name:'); blank(xe, y, xe + 40, q.customer_sign_name)
        y += 11
        xe = lbl(X0 + 2, y, 'Authorize signature:'); blank(xe, y, xe + 45, signed, bold_val=False)
        sx, sy = xe + 2, y - 11
    else:
        xe = lbl(X0 + 2, y, 'Name:'); blank(xe, y, xe + 45, q.customer_sign_name)
        xe2 = lbl(xe + 49, y, 'Authorize signature:'); blank(xe2, y, xe2 + 48, signed, bold_val=False)
        sx, sy = xe2 + 6, y - 11
    if sign_img:
        try:
            pdf.image(sign_img, sx, sy, 28, 11)
        except Exception:
            pass
    y += 9
    # frame
    pdf.set_line_width(0.5); pdf.rect(X0, top, W, y - top); pdf.set_line_width(0.2)
    return pdf
