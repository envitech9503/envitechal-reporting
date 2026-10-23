"""Management Review - PDF forms (23-10-2026): ETAL-QMS-809-FF-03 Management Review Meeting Plan, FF-01 Circular of the
Management Review Meeting (with the receiving attendance), FF-02 Minutes (with the addendum) and FF-04 MRM Checklist.
Same frame as the Internal Audit forms (Calibri, document-control box, laboratory footer); every signature panel
prints the name and e-signature of the user who signed in the system. Inducted (paper) records print the e-signature of
the named signatory when one is on file (24-10-2026), otherwise "Signed on the paper record".
"""
from .shared import *  # noqa: F401,F403
import re
from django.contrib.auth.models import User as _User

from QC.models import MrmPlan, MrmMeeting
from QC.views.control_chart import _uname, _sig_image
from QC.views.ia import _d, MONTHS
from QC.views.ia_pdf import _pdf, _resp, _table_row, GREY_FILL, LINE, AMBER, GREEN_DONE
from QC.views.mrm import mrm_docctrl, _on


def _wm(ok):
    return '' if ok else 'DRAFT'


# ---------------------------------------------------------------- e-signature of a named signatory (24-10-2026)
_HON = {'muhammad': 'm', 'mohammad': 'm', 'mohammed': 'm', 'muhammed': 'm', 'mohd': 'm', 'md': 'm'}


def _ntok(name):
    toks = re.sub(r'[^a-z ]+', ' ', (name or '').lower()).split()
    return tuple(_HON.get(t, t) for t in toks if t not in ('mr', 'mrs', 'ms', 'miss', 'dr', 'engr'))


def _signers():
    """[(name tokens, username, active, user id, image path)] of every user with an e-signature image on file."""
    import os
    from EnviTechAlApp.models import Signatures
    out = []
    for s in Signatures.objects.select_related('user').order_by('user_id'):
        u = s.user
        try:
            if not (u and s.signature and os.path.exists(s.signature.path)):
                continue
        except Exception:
            continue
        tk = _ntok(_uname(u))
        if tk:
            out.append((tk, (u.username or '').lower(), u.is_active, u.pk, s.signature.path))
    return out


def _named_sig(name, cache):
    """E-signature image of the staff member printed by name on an inducted (paper) record: the name must match the
    user's full name (Muhammad / Mohammad / M. treated alike); with two accounts for one person the personal account
    (username within the name) is preferred, then an active one. None when nobody matches - the panel then keeps
    'Signed on the paper record'."""
    key = _ntok(name)
    if not key:
        return None
    if key in cache:
        return cache[key]
    if '_all' not in cache:
        cache['_all'] = _signers()
    core = set(key) - {'m'}
    hits = [r for r in cache['_all'] if r[0] == key]
    if not hits and len(core) >= 2:              # e.g. "M. Modabir Raza" against "Muhammad Modabir Raza", or a missing title
        hits = [r for r in cache['_all'] if core <= set(r[0]) or (set(r[0]) - {'m'}) and (set(r[0]) - {'m'}) <= core and len(set(r[0]) - {'m'}) >= 2]
    hits.sort(key=lambda r: (r[1] not in key, not r[2], r[3]))
    cache[key] = hits[0][4] if hits else None
    if cache[key]:
        cache['_used'] = True
    return cache[key]


def _paper_sig(signed_in_system, user, name, cache, inducted):
    """(image, mode) for a signature panel: the system signer's image; on an inducted (paper) record the named
    signatory's e-signature. A record created in the system is never given a signature it has not received."""
    if signed_in_system:
        return _sig_image(user), ''
    if not inducted:
        return None, 'paper'
    s = _named_sig(name, cache)
    return s, ('' if s else 'paper')


_INDUCT_NOTE = 'Record inducted from the signed paper original held by the laboratory; signatures shown are the e-signatures on file of the named signatories.'


def _induct_note(pdf, cache):
    if cache.get('_used'):
        pdf.set_font(pdf.fam, '', 6.4); pdf.set_text_color(110, 110, 110)
        pdf.multi_cell(pdf.W, 3.2, _INDUCT_NOTE, 0, 'C'); pdf.set_text_color(0, 0, 0)


def _head(pdf, cols, fs=7.4, fill=GREY_FILL):
    pdf.set_font(pdf.fam, 'B', fs); pdf.set_fill_color(*fill); pdf.set_draw_color(*LINE)
    for lbl, w in cols:
        pdf.cell(w, 6, lbl, 1, 0, 'C', fill=True)
    pdf.ln(6)


# ---------------------------------------------------------------- FF-03 plan (landscape)
def mrm_plan_pdf(request, pk):
    plan = get_object_or_404(MrmPlan.objects.select_related('mr_by', 'ceo_by'), pk=pk)
    ctrl = mrm_docctrl('plan', plan.location, _on(plan))
    pdf = _pdf('MANAGEMENT REVIEW MEETING PLAN - %d' % plan.year, '%s LABORATORY' % plan.location.upper(), ctrl, plan.location, 'L',
               '' if plan.status == 'approved' else 'NOT APPROVED')
    f = pdf.fam
    pdf.set_y(40)
    dept_w = 48.0; mw = (pdf.W - dept_w) / 12.0; cw = mw / 2.0
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
    rh = max(5.0, min(9.0, 60.0 / max(1, len(rows))))          # many departments: rows shrink so the signatures stay on the page
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
    for _ in range(max(0, 4 - len(rows))):
        pdf.rect(x0, y, dept_w, rh)
        for i in range(24):
            pdf.rect(x0 + dept_w + i * cw, y, cw, rh)
        y += rh
    pdf.set_y(y + 6)
    lx = 10; ly = pdf.get_y()
    pdf.set_fill_color(*AMBER); pdf.rect(lx, ly, 34, 5, 'DF'); pdf.set_fill_color(*GREEN_DONE); pdf.rect(lx + 34, ly, 34, 5, 'DF')
    pdf.set_font(f, '', 7.5); pdf.set_xy(lx, ly + 5); pdf.cell(34, 4.5, 'MRM Planned', 1, 0, 'C'); pdf.cell(34, 4.5, 'MRM Completed', 1, 0, 'C')
    if plan.remarks:
        pdf.set_xy(10, ly + 12); pdf.set_font(f, '', 7.2); pdf.multi_cell(pdf.W, 3.4, 'Remarks: ' + plan.remarks.replace('\n', '  |  '))
    top = max(pdf.get_y() + 4, 130)
    if top + 30 > pdf.h - 28:
        pdf.add_page(); top = pdf.get_y() + 4
    sc = {}
    mr_nm = plan.mr_name or (_uname(plan.mr_by) if plan.mr_by else '')
    ceo_nm = plan.ceo_name or (_uname(plan.ceo_by) if plan.ceo_by else '')
    mr_sig, mr_mode = _paper_sig(plan.mr_at, plan.mr_by, mr_nm, sc, plan.inducted)
    ceo_sig, ceo_mode = _paper_sig(plan.ceo_at, plan.ceo_by, ceo_nm, sc, plan.inducted)
    panels = [('Management Representative', 'Prepared by', mr_nm, mr_sig, _d(plan.mr_date), mr_mode),
              ('', '', '', None, ''),
              ('CEO', 'Approved by', ceo_nm, ceo_sig, _d(plan.ceo_date), ceo_mode)]
    pdf.sig_panels(panels, top, 26)
    pdf.set_y(top + 27); _induct_note(pdf, sc)
    pdf.set_y(max(pdf.get_y() + 1, top + 30)); pdf.set_font(f, 'B', 7.5); pdf.cell(pdf.W, 5, '---END OF THE DOCUMENT---', 0, 0, 'C')
    return _resp(pdf, 'MRM_Plan_%s_%d' % (plan.location, plan.year))


# ---------------------------------------------------------------- FF-01 circular (portrait)
def mrm_circular_pdf(request, pk):
    m = get_object_or_404(MrmMeeting.objects.select_related('circular_by'), pk=pk)
    ctrl = mrm_docctrl('circular', m.location, _on(m, 'circular'))
    pdf = _pdf('CIRCULAR OF MANAGEMENT REVIEW MEETING', '%s LABORATORY  -  MEETING # %s' % (m.location.upper(), m.meeting_no), ctrl, m.location, 'P',
               _wm(m.circular_status == 'issued'))
    f = pdf.fam
    snap = (m.legacy or {}).get('circ_snap') or {} if m.circular_status == 'issued' else {}
    import datetime as _dt
    try:
        cdate = _dt.date.fromisoformat(snap['meeting_date']) if snap.get('meeting_date') else m.meeting_date
    except ValueError:
        cdate = m.meeting_date
    pdf.set_y(39)
    pdf.kv([('Dated:', _d(m.circular_date), 32, 63), ('Meeting #:', snap.get('meeting_no') or m.meeting_no, 32, 63)])
    pdf.kv([('Meeting date:', _d(cdate), 32, 63), ('Time:', snap.get('time', m.time_text) if snap else m.time_text, 32, 63)])
    pdf.kv([('Venue:', snap.get('venue', m.venue) if snap else m.venue, 32, 158)])
    pdf.kv([('Subject:', snap.get('subject') or m.subject, 32, 158)])
    pdf.ln(3)
    pdf.set_font(f, '', 8.4)
    if m.circular_intro:
        pdf.multi_cell(pdf.W, 4.4, 'AOA,\n\n' + m.circular_intro)
        pdf.ln(2)
    pdf.set_font(f, 'B', 8.8); pdf.cell(pdf.W, 5.5, 'Meeting Agenda', 0, 1, 'L')
    pdf.set_font(f, '', 8.2)
    for i, a in enumerate(m.agenda or []):
        pdf.set_x(14); pdf.multi_cell(pdf.W - 4, 4.2, '%s)  %s' % (chr(97 + i) if i < 26 else str(i + 1), a))
    pdf.ln(2)
    pdf.set_font(f, 'B', 8.4); pdf.cell(pdf.W, 5, 'Distribute to:', 0, 1, 'L'); pdf.set_font(f, '', 8.2)
    for i, d in enumerate(m.distribute_to or []):
        pdf.set_x(14); pdf.cell(pdf.W - 4, 4.4, '%d. %s' % (i + 1, d), 0, 1, 'L')
    # CEO signature (right)
    y = pdf.get_y() + 2
    if y + 22 > pdf.h - 32:
        pdf.add_page(); y = pdf.get_y()
    sc = {}
    if m.circular_at and m.circular_by:
        sig = _sig_image(m.circular_by)
    else:
        sig = _named_sig(m.circular_signer, sc) if (m.circular_status == 'issued' and m.inducted) else None
    x = 10 + pdf.W - 62
    if sig:
        try:
            pdf.image(sig, x + 8, y, 46, 12)
        except Exception:
            sig = None
    if not sig and m.circular_status == 'issued':
        pdf.set_xy(x, y + 4); pdf.set_font(f, '', 6.4); pdf.set_text_color(110, 110, 110)
        pdf.cell(62, 4, 'Electronically signed' if m.circular_at else 'Signed on the paper record', 0, 0, 'C'); pdf.set_text_color(0, 0, 0)
    pdf.set_xy(x, y + 13); pdf.set_font(f, 'B', 8.2); pdf.cell(62, 4.4, m.circular_signer or '', 0, 1, 'C')
    from django.utils import timezone as _tz
    pdf.set_x(x); pdf.set_font(f, '', 7.6); pdf.cell(62, 4, 'C.E.O' + ('   %s' % _d(_tz.localtime(m.circular_at).date()) if m.circular_at else ''), 0, 1, 'C')
    pdf.ln(4)
    pdf.set_font(f, 'B', 8.6); pdf.cell(pdf.W, 6, 'Circular Receiving Attendance', 0, 1, 'C')
    acols = [('S. No.', 14), ('Name of Employee', 70), ('Designation', 56), ('Signature', 50)]
    _head(pdf, acols)
    for i, a in enumerate(m.attendance or []):
        h = 9.0
        if pdf.get_y() + h > pdf.h - 32:
            pdf.add_page(); _head(pdf, acols)
        x = 10; y = pdf.get_y()
        pdf.set_font(f, '', 7.4)
        pdf.rect(x, y, 14, h); pdf.set_xy(x, y); pdf.cell(14, h, '%d.' % (i + 1), 0, 0, 'C'); x += 14
        pdf.rect(x, y, 70, h); pdf.set_xy(x + 1, y); pdf.cell(68, h, a.get('name', ''), 0, 0, 'L'); x += 70
        pdf.rect(x, y, 56, h); pdf.set_xy(x + 1, y); pdf.cell(54, h, a.get('designation', ''), 0, 0, 'L'); x += 56
        pdf.rect(x, y, 50, h)
        if a.get('signed_at') and a.get('user_id'):
            u = _User.objects.filter(pk=a['user_id']).first()
            s = _sig_image(u) if u else None
            if s:
                try:
                    pdf.image(s, x + 12, y + 0.8, 26, 7.4)
                except Exception:
                    s = None
            if not s:
                pdf.set_xy(x, y); pdf.set_font(f, '', 6.4); pdf.cell(50, h, 'Electronically signed', 0, 0, 'C')
            pdf.set_xy(x + 1, y + h - 3.2); pdf.set_font(f, '', 5.6); pdf.set_text_color(110, 110, 110)
            pdf.cell(48, 3, '-'.join(reversed((a['signed_at'] or '')[:10].split('-'))), 0, 0, 'R'); pdf.set_text_color(0, 0, 0)
        elif m.inducted:
            s = _named_sig(a.get('name', ''), sc)
            if s:
                try:
                    pdf.image(s, x + 12, y + 0.8, 26, 7.4)
                except Exception:
                    s = None
            if not s:
                pdf.set_xy(x, y); pdf.set_font(f, '', 6.0); pdf.set_text_color(110, 110, 110); pdf.cell(50, h, 'on the paper record', 0, 0, 'C'); pdf.set_text_color(0, 0, 0)
        pdf.set_xy(10, y + h)
    pdf.ln(2); _induct_note(pdf, sc)
    return _resp(pdf, 'MRM_Circular_%s_%s' % (m.location, m.meeting_no))


# ---------------------------------------------------------------- FF-02 minutes (landscape, multi-page)
def mrm_minutes_pdf(request, pk):
    m = get_object_or_404(MrmMeeting.objects.select_related('mr_by', 'ceo_by'), pk=pk)
    ctrl = mrm_docctrl('minutes', m.location, _on(m))
    pdf = _pdf('MINUTES OF MANAGEMENT REVIEW MEETING', '%s LABORATORY  -  MEETING # %s' % (m.location.upper(), m.meeting_no), ctrl, m.location, 'L',
               _wm(m.status == 'approved'))
    f = pdf.fam
    pdf.set_y(39)
    half = pdf.W / 2
    pdf.kv([('Meeting #.', m.meeting_no, 32, half - 32), ('Meeting Date', _d(m.meeting_date), 32, half - 32)])
    pdf.kv([('Time', m.time_text, 32, half - 32), ('Type of Review', m.review_type, 32, half - 32)])
    pdf.kv([('Venue', m.venue, 32, pdf.W - 32)])
    pdf.ln(2)
    pdf.set_font(f, 'B', 8.6); pdf.cell(pdf.W, 5.5, 'Participants:', 0, 1, 'L')
    pc = [('Sr. No', 14), ('Name of Participant', (pdf.W / 2) - 14 - 50), ('Designation', 50)]
    cols = pc + pc
    _head(pdf, cols, fs=7.2)
    ps = m.participants or []
    half_n = (len(ps) + 1) // 2
    for i in range(half_n):
        a = ps[i]; b = ps[i + half_n] if i + half_n < len(ps) else None
        vals = [str(i + 1), a.get('name', ''), a.get('designation', ''), str(i + half_n + 1) if b else '', b.get('name', '') if b else '', b.get('designation', '') if b else '']
        _table_row(pdf, cols, vals, lh=3.6, fs=7.2)
    pdf.ln(2)
    pdf.set_font(f, 'B', 8.6); pdf.cell(pdf.W, 5.5, 'Roles:', 0, 1, 'L')
    rc = [('Chair', pdf.W / 4), ('Facilitator', pdf.W / 4), ('Minutes Taker', pdf.W / 4), ('Documenter', pdf.W / 4)]
    _head(pdf, rc, fs=7.2)
    _table_row(pdf, rc, [m.chair, m.facilitator, m.minutes_taker, m.documenter], lh=3.6, fs=7.4)
    pdf.ln(2)

    mcols = [('S. #', 12), ('Agenda', 40), ('Inputs / Details of Discussions', 70), ('Outputs / Decision & Direction', 75), ('Resources Needed', 28), ('Responsibility', 25), ('Target Date', 27)]
    scale = pdf.W / sum(w for _l, w in mcols)
    mcols = [(l, w * scale) for l, w in mcols]

    def minutes_table(title, items):
        if pdf.get_y() + 20 > pdf.h - 32:
            pdf.add_page()
        pdf.set_font(f, 'B', 8.6); pdf.cell(pdf.W, 5.5, title, 0, 1, 'L')
        head = lambda: _head(pdf, mcols, fs=7.0)
        head()
        for it in items:
            agenda = ('%s\n%s' % (it.clause, it.agenda)).strip() if it.clause else it.agenda
            _table_row(pdf, mcols, [it.sno, agenda, it.inputs, it.outputs, it.resources, it.responsibility, it.target_text], lh=3.3, fs=6.9, head=head)
        pdf.ln(2)

    items = list(m.items.all())
    minutes_table('Minutes:', [i for i in items if i.part == 'minutes'])
    nc = [('Next MRM Date', 50), ('', pdf.W - 50)]
    _table_row(pdf, nc, ['Next MRM Date', m.next_mrm or '-'], lh=3.8, fs=7.6)
    _table_row(pdf, nc, ['Distributed to', m.distributed_to or '-'], lh=3.8, fs=7.6)
    pdf.ln(3)

    def sigs():
        if pdf.get_y() + 34 > pdf.h - 30:
            pdf.add_page()
        top = pdf.get_y()
        sc = {}
        mr_sig, mr_mode = _paper_sig(m.mr_at, m.mr_by, m.mr_name, sc, m.inducted)
        ceo_sig, ceo_mode = _paper_sig(m.ceo_at, m.ceo_by, m.ceo_name, sc, m.inducted)
        panels = [('Prepared By (M.R)', 'Management Representative', m.mr_name, mr_sig, _d(m.mr_date), mr_mode),
                  ('', '', '', None, ''),
                  ('Approved By (CEO)', 'CEO', m.ceo_name, ceo_sig, _d(m.ceo_date), ceo_mode)]
        pdf.sig_panels(panels, top, 28)
        pdf.ln(1); _induct_note(pdf, sc); pdf.ln(2)

    sigs()
    add = [i for i in items if i.part == 'addendum']
    if add:
        pdf.add_page()
        if m.addendum_date:
            pdf.set_font(f, 'B', 8.4); pdf.cell(pdf.W, 5, 'Dated: %s' % _d(m.addendum_date), 0, 1, 'L')
        minutes_table('Addendum:', add)
    pdf.set_font(f, 'B', 7.5); pdf.cell(pdf.W, 5, '---END OF THE DOCUMENT---', 0, 0, 'C')
    return _resp(pdf, 'MRM_Minutes_%s_%s' % (m.location, m.meeting_no))


# ---------------------------------------------------------------- FF-04 checklist (portrait)
def mrm_checklist_pdf(request, pk):
    m = get_object_or_404(MrmMeeting.objects.select_related('mr_by', 'ceo_by'), pk=pk)
    ctrl = mrm_docctrl('checklist', m.location, _on(m, 'checklist'))
    pdf = _pdf('MANAGEMENT REVIEW MEETING (MRM) CHECKLIST', '%s LABORATORY  -  MEETING # %s' % (m.location.upper(), m.meeting_no), ctrl, m.location, 'P',
               _wm(bool(m.checklist) and m.status == 'approved'))
    f = pdf.fam
    pdf.set_y(39)
    pdf.set_font(f, 'B', 8.4)
    pdf.cell(pdf.W / 2, 5.5, 'Based on ISO/IEC 17025:2017 Clause 8.9.2', 0, 0, 'L')
    pdf.cell(pdf.W / 2, 5.5, 'Date: %s' % _d(m.checklist_date or m.meeting_date), 0, 1, 'R')
    cols = [('S. No.', 11), ('Clause', 17), ('Agenda Item', 52), ('Discussed (Y/N)', 18), ('Reference / Remarks', 50), ('Justification (if not discussed)', 42)]
    head = lambda: _head(pdf, cols, fs=6.9)
    head()
    for i, r in enumerate(m.checklist_rows()):
        mark = {'yes': 'Yes', 'no': 'No'}.get(r.get('discussed'), '-')
        _table_row(pdf, cols, [str(i + 1), r['code'], r['item'], mark, r.get('remarks') or '-', r.get('justification') or '-'], lh=3.4, fs=7.0, head=head,
                   align={'S. No.': 'C', 'Discussed (Y/N)': 'C'})
    pdf.ln(2)
    pdf.set_font(f, '', 7.2)
    pdf.multi_cell(pdf.W, 3.6, 'Note: Each item should be either discussed, referenced, or have documented justification if not discussed.')
    pdf.ln(4)
    if pdf.get_y() + 32 > pdf.h - 30:
        pdf.add_page()
    top = pdf.get_y()
    sc = {}
    filled = bool(m.checklist)                     # no checklist on the record: blank panels, nobody signs an empty form
    mr_nm, ceo_nm = (m.mr_name, m.ceo_name) if filled else ('', '')
    mr_sig, mr_mode = _paper_sig(m.mr_at, m.mr_by, mr_nm, sc, m.inducted) if filled else (None, '')
    ceo_sig, ceo_mode = _paper_sig(m.ceo_at, m.ceo_by, ceo_nm, sc, m.inducted) if filled else (None, '')
    panels = [('Prepared by', 'MR', mr_nm, mr_sig, _d(m.checklist_date or m.mr_date) if mr_nm else '', mr_mode),
              ('', '', '', None, ''),
              ('Approved by', 'CEO', ceo_nm, ceo_sig, _d(m.checklist_date or m.ceo_date) if ceo_nm else '', ceo_mode)]
    pdf.sig_panels(panels, top, 26)
    pdf.ln(1); _induct_note(pdf, sc)
    pdf.ln(3); pdf.set_font(f, 'B', 7.5); pdf.cell(pdf.W, 5, '---END OF THE DOCUMENT---', 0, 0, 'C')
    return _resp(pdf, 'MRM_Checklist_%s_%s' % (m.location, m.meeting_no))
