"""ETAL-LAB-708-FF-17 Customer Request Form for MOU & SOC, laid out as the laboratory's controlled Word form.

26-10-2026: content and order of the controlled form. Karachi prints its form (Issue 01 / Rev 01: "CUSTOMER REQUEST
FORM FOR MOU & SOC", four types of request, name and authorised signature on one line); Lahore prints its own (Issue
02 / Rev 01: "CUSTOMER REQUEST FORM", measurement of uncertainty and statement of conformity, name and signature on
separate lines, Lahore office in the footer).
27-10-2026 (owner review): premium layout - a clean header (logo, company name, document-control table aligned on one
band), a centred two-line footer above a slim brand bar, and the form frame filling the page between them: the vertical
spacing of the form is stretched so that its frame always ends just above the footer.
"""
import os

from django.conf import settings
from fpdf import FPDF

GREEN = (0, 150, 74)
BLUE = (13, 46, 145)
BAND = (226, 236, 246)
INK = (25, 25, 25)
GREY = (90, 90, 90)
RULE = (150, 150, 150)

HEAD_OFFICE = '345, First Floor, Street-15, Block-3, Bahadurabad, Karachi 75900, Pakistan'
_FOOT = {
    'Karachi': {'lines': ['Head Office: %s   |   Tel: +92 310 2288801' % HEAD_OFFICE]},
    'Lahore': {'lines': ['Lahore Office: Madina Heights, Office # A/30-31, 8th Floor, Shaukat Ali Road, Johar Town, Lahore, Pakistan   |   '
                         'Tel: +92 42 32296099',
                         'Head Office: %s' % HEAD_OFFICE]},
}
TAGLINE = 'We strive for Pragmatic approach to achieve quality Excellence'

TOP = 37.0          # form frame: from just under the header ...
BOTTOM_GAP = 25.0   # ... to just above the footer (page height - this)


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
        self.set_margins(12, 10, 12)

    def header(self):
        w = self.w
        self.set_fill_color(*GREEN); self.rect(0, 0, w, 2.4, 'F')                  # brand strip
        logo = _p('static/assets/etal_form_logo.png')
        if not os.path.exists(logo):
            logo = _p('static/assets/EnviTechAL LOGO.png')
        try:
            self.image(logo, 13, 6, 21, 23)
        except Exception:
            pass
        # company name and tagline, centred between the logo and the control table
        cx0, cx1 = 38, w - 70
        self.set_text_color(*BLUE); self.set_font(self.fam, 'B', 17)
        self.set_xy(cx0, 11); self.cell(cx1 - cx0, 8, 'ENVI TECH AL', 0, 0, 'C')
        self.set_text_color(*GREEN); self.set_font(self.fam, '', 8.5)
        self.set_xy(cx0, 19.5); self.cell(cx1 - cx0, 5, TAGLINE, 0, 0, 'C')
        # document-control table
        c = self.ctrl
        rows = [('Document No.', c['doc_no']), ('Issue Date', c['issue_date']),
                ('Issue / Rev. No.', '%s / %s' % (c['issue_no'], c['rev_no'])), ('Page No.', '01 of 01')]
        tx, ty, lw, vw, rh = w - 66, 7.5, 21, 33, 4.6
        self.set_draw_color(*RULE); self.set_line_width(0.2); self.set_text_color(*INK)
        for i, (k, v) in enumerate(rows):
            y = ty + i * rh
            self.set_fill_color(*BAND); self.rect(tx, y, lw, rh, 'DF')
            self.rect(tx + lw, y, vw, rh, 'D')
            self.set_font(self.fam, 'B', 7.2); self.set_xy(tx + 1.2, y); self.cell(lw - 1.5, rh, k, 0, 0, 'L')
            self.set_font(self.fam, '', 7.4); self.set_xy(tx + lw + 1.2, y); self.cell(vw - 1.5, rh, str(v or ''), 0, 0, 'L')
        self.set_draw_color(*GREEN); self.set_line_width(0.6); self.line(12, 32.5, w - 12, 32.5)
        self.set_line_width(0.2); self.set_draw_color(0, 0, 0)

    def footer(self):
        w, h = self.w, self.h
        self.set_draw_color(*GREEN); self.set_line_width(0.4); self.line(12, h - 21, w - 12, h - 21); self.set_line_width(0.2)
        lines = _FOOT[self.loc]['lines']
        self.set_text_color(*GREY); self.set_font(self.fam, '', 7.6)
        y = h - 18.2 if len(lines) > 1 else h - 16.2
        for t in lines:
            self.set_xy(0, y); self.cell(w, 4, t, 0, 0, 'C'); y += 4.2
        self.set_fill_color(*BLUE); self.rect(0, h - 8, w, 8, 'F')
        self.set_text_color(255, 255, 255); self.set_font(self.fam, 'B', 7.8)
        self.set_xy(0, h - 6.5); self.cell(w, 5, 'info@envitechal.com      |      www.envitechal.com', 0, 0, 'C')
        self.set_fill_color(*GREEN); self.rect(0, h - 1.4, w, 1.4, 'F')
        self.set_text_color(0, 0, 0); self.set_draw_color(0, 0, 0)


def _draw(pdf, q, signer_name, sign_img, k):
    """The form body with every vertical gap multiplied by k; returns the bottom of the frame."""
    loc = q.location if q.location in _FOOT else 'Karachi'
    lahore = loc == 'Lahore'
    f = pdf.fam
    X0, X1 = 12.0, pdf.w - 12.0
    W = X1 - X0
    FS = 9.0                       # text size
    LH = 4.9                       # line height of wrapped values

    def g(v):                      # a vertical gap, stretched to fill the page
        return v * k

    def lbl(x, y, t, size=FS):
        pdf.set_text_color(*INK); pdf.set_font(f, 'B', size); pdf.set_xy(x, y); pdf.cell(pdf.get_string_width(t) + 0.6, 5, t, 0, 0, 'L')
        return x + pdf.get_string_width(t) + 1.4

    def blank(x, y, x_end, val):
        """A value written on an underlined blank from x to x_end."""
        pdf.set_font(f, '', FS); pdf.set_text_color(*INK)
        s = str(val or '')
        tw = pdf.get_string_width(s)
        pdf.set_xy(x + 1, y); pdf.cell(tw, 5, s, 0, 0, 'L')
        pdf.set_draw_color(*RULE); pdf.set_line_width(0.2); pdf.line(x, y + 4.6, max(x_end, x + tw + 2), y + 4.6)
        pdf.set_draw_color(0, 0, 0)

    def para(x, y, x_end, label, val):
        """Label followed by a long underlined value that wraps onto following underlined lines."""
        xs = lbl(x, y, label) if label else x
        pdf.set_font(f, '', FS)
        words, line, lines, cur_x = str(val or '').split(), '', [], xs
        for wd in words:
            t = (line + ' ' + wd).strip()
            if pdf.get_string_width(t) > (x_end - cur_x - 2) and line:
                lines.append((cur_x, line)); line, cur_x = wd, x
            else:
                line = t
        lines.append((cur_x, line))
        pdf.set_draw_color(*RULE)
        for i, (lx, t) in enumerate(lines):
            yy = y + i * LH
            pdf.set_xy(lx + 1, yy); pdf.cell(pdf.get_string_width(t), 5, t, 0, 0, 'L')
            pdf.line(lx, yy + 4.6, x_end, yy + 4.6)
        pdf.set_draw_color(0, 0, 0)
        return y + len(lines) * LH

    def box(x, y, on):
        pdf.set_draw_color(0, 0, 0); pdf.set_line_width(0.25); pdf.rect(x, y + 0.7, 3.4, 3.4)
        if on:
            pdf.set_line_width(0.35)
            pdf.line(x + 0.5, y + 2.5, x + 1.4, y + 3.6); pdf.line(x + 1.4, y + 3.6, x + 3.0, y + 1.1)   # tick
            pdf.set_line_width(0.2)
        return x + 5

    def band(y, t):
        h = 7.0
        pdf.set_fill_color(*BAND); pdf.set_draw_color(0, 0, 0); pdf.rect(X0, y, W, h, 'DF')
        pdf.set_fill_color(*GREEN); pdf.rect(X0, y, 1.6, h, 'F')
        pdf.set_text_color(*BLUE); pdf.set_font(f, 'B', 9.5); pdf.set_xy(X0 + 4, y + 1); pdf.cell(100, 5, t, 0, 0, 'L')
        pdf.set_text_color(*INK)
        return y + h

    top = TOP
    # title
    pdf.set_draw_color(0, 0, 0); pdf.set_fill_color(*BLUE)
    pdf.rect(X0, top, W, 9.5, 'F')
    pdf.set_text_color(255, 255, 255); pdf.set_font(f, 'B', 12.5)
    pdf.set_xy(X0, top + 1.6); pdf.cell(W, 6.5, 'CUSTOMER REQUEST FORM' if lahore else 'CUSTOMER REQUEST FORM FOR MOU & SOC', 0, 0, 'C')
    pdf.set_text_color(*INK)
    y = top + 9.5 + g(3.2)
    # customer
    dt = q.date.strftime('%d-%m-%Y') if q.date else ''
    xe = lbl(X0 + 3, y, 'Date:'); blank(xe, y, xe + 28, dt)
    y = para(xe + 32, y, X1 - 3, 'Reason for Request:', q.reason) + g(2.2)
    xe = lbl(X0 + 3, y, 'Name of Organization:'); blank(xe, y, X1 - 3, q.organization); y += 5 + g(2.2)
    xe = lbl(X0 + 3, y, 'Name of Customer:'); blank(xe, y, xe + 58, q.customer_name)
    xe2 = lbl(xe + 63, y, 'Contact Details:'); blank(xe2, y, X1 - 3, q.contact); y += 5 + g(2.2)
    y = para(X0 + 3, y, X1 - 3, 'Address:', q.address) + g(3.0)
    # sample information
    y = band(y, 'Sample Information') + g(2.6)
    lbl(X0 + 3, y, 'Analysis Requested:'); y += 5 + g(1.8)
    x = box(X0 + 4, y, q.analysis == 'ww'); x = lbl(x, y, 'Wastewater')
    x = box(x + 6, y, q.analysis == 'dw'); x = lbl(x, y, 'Drinking Water')
    x = box(x + 6, y, q.analysis == 'other'); x = lbl(x, y, 'Others (Please Specify):')
    blank(x, y, X1 - 3, q.analysis_other if q.analysis == 'other' else '')
    y += 5 + g(2.4)
    y = para(X0 + 3, y, X1 - 3, 'Parameters:', q.parameters) + g(3.0)
    # type of request
    y = band(y, 'Type of Request') + g(2.8)
    opts = [(q.req_mou, 'Measurement of Uncertainty'), (q.req_soc, 'Statement of Conformity')]
    if not lahore:
        opts += [(q.req_opinion, 'Opinions & Interpretation'), (q.req_limits, 'Customer Specification Limit')]
    pdf.set_font(f, 'B', FS)
    need = sum(5 + pdf.get_string_width(t) + 1.4 for _, t in opts)
    gap = min(8.0, max(2.0, (W - 7 - need) / max(1, len(opts) - 1)))      # spread evenly across the frame
    x = X0 + 4
    for on, t in opts:
        x = box(x, y, on); x = lbl(x, y, t) + gap
    y += 5 + g(2.4)
    other = q.req_other if (q.req_other or '').strip() not in ('-',) else ''
    if lahore:
        extra = [t for t, on in (('Opinions & Interpretation', q.req_opinion), ('Customer Specification Limit', q.req_limits)) if on]
        other = ', '.join(extra + ([other] if other else []))
    xe = lbl(X0 + 3, y, 'Others (Please Specify):'); blank(xe, y, X1 - 3, other); y += 5 + g(3.0)
    # reporting of results
    y = band(y, 'Reporting of Results') + g(2.6)
    pdf.set_font(f, 'B', FS); pdf.set_xy(X0 + 3, y)
    pdf.cell(W - 6, 5, 'Please specify specification limit, select decision rules, and select decision rules statements of conformity wishes to use:', 0, 0, 'L')
    y += 5 + g(1.8)
    rep = (q.reporting or '').strip()
    rep = '' if rep == '-' else rep
    y = para(X0 + 3, y, X1 - 3, '', rep or ' ')
    if lahore:
        pdf.set_draw_color(*RULE); pdf.line(X0 + 3, y + 4.6, X1 - 3, y + 4.6); pdf.set_draw_color(0, 0, 0); y += LH
    y += g(3.0)
    # Envi Tech AL follow-up
    y = band(y, 'Envi Tech AL - Follow Up Action')
    fy = y
    mid = X0 + W * (0.5 if lahore else 0.55)
    y += g(2.6)
    x = box(X0 + 4, y, q.decision == 'approved'); lbl(x, y, 'Request Approved')
    x = box(mid + 4, y, q.decision == 'denied'); lbl(x, y, 'Request Denied')
    y += 5 + g(2.4)
    appr, deny = q.decision == 'approved', q.decision == 'denied'
    ya = para(X0 + 3, y, mid - 3, 'Comment:', q.decision_comment if appr else '')
    yd = para(mid + 4, y, X1 - 3, 'Comment:', q.decision_comment if deny else '')
    y = max(ya, yd) + g(2.4)
    ddt = q.decision_date.strftime('%d-%m-%Y') if q.decision_date else ''
    xe = lbl(X0 + 3, y, 'Date:'); blank(xe, y, xe + 40, ddt if appr else '')
    xe = lbl(mid + 4, y, 'Date:'); blank(xe, y, xe + 40, ddt if deny else '')
    y += 5 + g(3.0)
    pdf.set_draw_color(0, 0, 0); pdf.line(mid, fy, mid, y); pdf.line(X0, y, X1, y)
    # name and authorised signature
    y += g(5.0)
    signed = signer_name or ''
    if lahore:
        xe = lbl(X0 + 3, y, 'Name:'); blank(xe, y, xe + 60, q.customer_sign_name)
        y += 5 + g(6.0)
        xe = lbl(X0 + 3, y, 'Authorised Signature:'); blank(xe, y, xe + 60, signed)
        sx, sy = xe + 2, y - 11
    else:
        xe = lbl(X0 + 3, y, 'Name:'); blank(xe, y, xe + 60, q.customer_sign_name)
        xe2 = lbl(mid + 4, y, 'Authorised Signature:'); blank(xe2, y, X1 - 3, signed)
        sx, sy = xe2 + 6, y - 11
    if sign_img:
        try:
            pdf.image(sign_img, sx, sy, 28, 11)
        except Exception:
            pass
    y += 5 + g(4.0)
    pdf.set_draw_color(0, 0, 0); pdf.set_line_width(0.5); pdf.rect(X0, top, W, y - top); pdf.set_line_width(0.2)
    return y


def _height(q, ctrl, k):
    p = _Form(ctrl, q.location); p.add_page()
    return _draw(p, q, '', None, k)


def build_ff17(q, ctrl, signer_name='', sign_img=None, watermark=''):
    """The form for one SocRequest `q`; ctrl = document control of the request's laboratory. The form's vertical
    spacing is stretched (k) so that its frame ends just above the footer, using the full page."""
    pdf = _Form(ctrl, q.location)
    target = pdf.h - BOTTOM_GAP
    h1, h2 = _height(q, ctrl, 1.0), _height(q, ctrl, 2.0)
    k = 1.0
    if h2 > h1:
        k = max(0.6, min(3.0, 1.0 + (target - h1) / (h2 - h1)))
    pdf.add_page()
    if watermark:
        with pdf.local_context():
            pdf.set_font(pdf.fam, 'B', 54); pdf.set_text_color(236, 236, 236)
            with pdf.rotation(40, pdf.w / 2, pdf.h / 2):
                pdf.text(pdf.w / 2 - pdf.get_string_width(watermark) / 2, pdf.h / 2, watermark)
    _draw(pdf, q, signer_name, sign_img, k)
    return pdf
