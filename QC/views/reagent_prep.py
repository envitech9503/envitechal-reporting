"""
Reagent & Standards Preparation — QC views (additive, 23-07-2026; QA-hardened).
Mirrors the QC form + list + controlled-PDF pattern (see dw.py). Registered by
QC/views/__init__.py via `from .reagent_prep import *` + _FAMILY_MODULES.
"""
from .shared import *  # noqa: F401,F403  (FPDF, models, render, JsonResponse, csrf_exempt, get_object_or_404, os, json, datetime...)

import os as _os
import re as _re
import json as _json
from datetime import datetime as _dt, date as _date
from django.db.models import Q as _Q
from django.db import transaction as _tx
from django.utils.safestring import mark_safe as _mark_safe
from django.views.decorators.clickjacking import xframe_options_sameorigin as _xframe_sameorigin

_LOGO = "static/assets/EnviTechAL LOGO.png"
_CALIBRI = "static/fonts/calibri.ttf"
_CALIBRIB = "static/fonts/calibrib.ttf"
_LOCS = ['Karachi', 'Lahore']


def _safe_json(obj):
    """JSON for inline <script> injection — escape chars that could break out of
    the script element (prevents stored XSS from user-entered names/descriptions)."""
    s = _json.dumps(obj)
    s = (s.replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
          .replace(' ', '\\u2028').replace(' ', '\\u2029'))
    return _mark_safe(s)


def _parse_date(v):
    v = (v or '').strip()
    if not v:
        return None
    for fmt in ('%Y-%m-%d', '%d-%m-%Y'):
        try:
            return _dt.strptime(v, fmt).date()
        except Exception:
            pass
    return None


def _f(v):
    try:
        return float(str(v).replace(',', '').strip())
    except Exception:
        return None


def _docctrl(location):
    """Per-lab control document row for this module (office-editable in admin)."""
    obj, _created = InventoryDocControl.objects.get_or_create(
        module='reagent_prep', location=location,
        defaults={'doc_no': '', 'issue_no': '01', 'rev_no': '00'})
    return obj


def _split_cat_lot(raw):
    """Inventory has no dedicated CAT field — the lab records both in one lot_no
    string, e.g. 'CAT NO. C532.1000  LOT NO: E1078375'. Split into (cat, lot)."""
    raw = (raw or '').strip()
    if not raw:
        return '', ''
    up = raw.upper()
    ci, li = up.find('CAT'), up.find('LOT')

    def _clean(x):
        return _re.sub(r'^\s*(NO\.?|NUMBER)?\s*[:.\-]?\s*', '', x, flags=_re.I).strip()

    if ci != -1 and li != -1:
        if ci < li:
            return _clean(raw[ci + 3:li]), _clean(raw[li + 3:])
        return _clean(raw[ci + 3:]), _clean(raw[li + 3:ci])
    if li != -1:
        return '', _clean(raw[li + 3:])
    if ci != -1:
        return _clean(raw[ci + 3:]), ''
    return '', raw


def _inventory_for_autocomplete():
    rows = []
    try:
        for lot in (ChemicalLot.objects
                    .exclude(status='Discarded')
                    .select_related('item')
                    .order_by('item__name', 'id')[:800]):
            it = lot.item
            cat, lotno = _split_cat_lot(lot.lot_no)
            rows.append({
                'id': lot.id,
                'name': it.name if it else '',
                'cat': cat,
                'lot': lotno,
                'make': lot.supplier or '',
                'expiry': lot.expiry.strftime('%d-%m-%Y') if lot.expiry else '',
            })
    except Exception:
        rows = []
    return rows


def _docctrl_data(location):
    c = _docctrl(location)
    return {
        'doc_no': c.doc_no or '',
        'issue_date': getattr(c, 'issue_date', '') or '',
        'issue_no': c.issue_no or '01',
        'rev_no': c.rev_no or '00',
    }


def _record_json(obj):
    chems = [{
        's_no': c.s_no, 'chemical_name': c.chemical_name, 'cat_no': c.cat_no,
        'lot_no': c.lot_no, 'quantity': c.quantity, 'make': c.make, 'expiry': c.expiry,
        'chemical_lot': c.chemical_lot_id,
    } for c in obj.chemicals.all()]
    std = None
    try:
        s = obj.standardisation
        std = {
            'location': s.location, 'primary_std': s.primary_std, 'ps_mass': s.ps_mass,
            'ps_purity': s.ps_purity, 'ps_eqwt': s.ps_eqwt, 'titrant_ml': s.titrant_ml,
            'nominal_N': s.nominal_N, 'true_N': s.true_N, 'factor': s.factor, 'unit': s.unit,
            'std_date': s.std_date.strftime('%Y-%m-%d') if s.std_date else '',
            'next_due': s.next_due.strftime('%Y-%m-%d') if s.next_due else '',
        }
    except ReagentStandardisation.DoesNotExist:
        std = None
    return {
        'id': obj.id, 'location': obj.location, 'month': obj.month,
        'reagent_name': obj.reagent_name, 'reagent_no': obj.reagent_no, 'rtype': obj.rtype,
        'description': obj.description, 'final_volume': obj.final_volume,
        'conc_value': obj.conc_value, 'conc_unit': obj.conc_unit,
        'prepared_by': obj.prepared_by, 'verified_by': obj.verified_by,
        'dop': obj.dop.strftime('%Y-%m-%d') if obj.dop else '',
        'doe': obj.doe.strftime('%Y-%m-%d') if obj.doe else '',
        'remarks': obj.remarks, 'chemicals': chems, 'standardisation': std,
    }


def reagent_prep(request):
    """Create / edit / clone form page."""
    edit_id = request.GET.get('id')
    clone_id = request.GET.get('clone')
    record = None
    if edit_id:
        obj = get_object_or_404(ReagentPrep, id=edit_id)
        record = _record_json(obj)
    elif clone_id:
        obj = get_object_or_404(ReagentPrep, id=clone_id)
        record = _record_json(obj)
        record['id'] = None
        record['reagent_no'] = ''
    docctrl = {loc: _docctrl_data(loc) for loc in _LOCS}
    is_admin = bool(getattr(request, 'user', None) and request.user.is_superuser)
    context = {
        'record_json': _safe_json(record),
        'inventory_json': _safe_json(_inventory_for_autocomplete()),
        'docctrl_json': _safe_json(docctrl),
        'is_admin_json': _safe_json(is_admin),
        'locations': _safe_json(_LOCS),
    }
    return render(request, 'reagent_prep_form.html', context)


@csrf_exempt
def reagent_prep_doc_save(request):
    """Save the per-lab control document number (superuser only), mirroring the
    Chemicals module's doc-control edit."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    if not (getattr(request, 'user', None) and request.user.is_superuser):
        return JsonResponse({'error': 'Only an administrator can edit the control number.'}, status=403)
    g = request.POST
    location = g.get('location') if g.get('location') in _LOCS else 'Karachi'
    c = _docctrl(location)
    c.doc_no = (g.get('doc_no') or '').strip()[:60]
    c.issue_date = (g.get('issue_date') or '').strip()[:30]
    c.issue_no = (g.get('issue_no') or '').strip()[:10] or '01'
    c.rev_no = (g.get('rev_no') or '').strip()[:10] or '00'
    if getattr(request, 'user', None) and request.user.is_authenticated:
        try:
            c.updated_by = request.user
        except Exception:
            pass
    c.save()
    return JsonResponse({'ok': True, 'location': location, 'doc': _docctrl_data(location)})


@csrf_exempt
def reagent_prep_save(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    try:
        data = _json.loads(request.body.decode('utf-8') or '{}')
    except Exception:
        return JsonResponse({'error': 'Invalid JSON payload'}, status=400)

    name = (data.get('reagent_name') or '').strip()
    if not name:
        return JsonResponse({'error': 'Reagent name is required'}, status=400)
    location = data.get('location') if data.get('location') in _LOCS else 'Karachi'

    rid = data.get('id')
    if rid:
        try:
            obj = ReagentPrep.objects.get(id=int(rid))
        except Exception:
            return JsonResponse({'error': 'Record not found'}, status=404)
    else:
        obj = ReagentPrep()
        if getattr(request, 'user', None) and request.user.is_authenticated:
            obj.created_by = request.user

    # All mutations atomic — an edit never leaves the record with its old child
    # rows deleted but new ones un-written.
    with _tx.atomic():
        obj.location = location
        obj.month = (data.get('month') or '').strip()[:30]
        obj.reagent_name = name[:200]
        obj.reagent_no = (data.get('reagent_no') or '').strip()[:40]
        obj.rtype = (data.get('rtype') or 'Reagent').strip()[:30]
        obj.description = (data.get('description') or '').strip()
        obj.final_volume = (data.get('final_volume') or '').strip()[:40]
        obj.conc_value = (data.get('conc_value') or '').strip()[:40]
        obj.conc_unit = (data.get('conc_unit') or '').strip()[:20]
        obj.prepared_by = (data.get('prepared_by') or '').strip()[:120]
        obj.verified_by = (data.get('verified_by') or '').strip()[:120]
        obj.dop = _parse_date(data.get('dop'))
        obj.doe = _parse_date(data.get('doe'))
        obj.remarks = (data.get('remarks') or '').strip()[:300]
        obj.save()

        # replace child chemical rows
        obj.chemicals.all().delete()
        for i, row in enumerate(data.get('chemicals') or [], start=1):
            cname = (row.get('chemical_name') or '').strip()
            if not cname:
                continue
            lot_id = row.get('chemical_lot')
            lot_obj = None
            if lot_id:
                try:
                    lot_obj = ChemicalLot.objects.get(id=int(lot_id))
                except Exception:
                    lot_obj = None
            ReagentPrepChemical.objects.create(
                prep=obj, s_no=row.get('s_no') or i, chemical_name=cname[:200],
                cat_no=(row.get('cat_no') or '').strip()[:80],
                lot_no=(row.get('lot_no') or '').strip()[:80],
                quantity=(row.get('quantity') or '').strip()[:60],
                make=(row.get('make') or '').strip()[:120],
                expiry=(row.get('expiry') or '').strip()[:40],
                chemical_lot=lot_obj)

        # standardisation (only for standardised titrants that carry a payload)
        std = data.get('standardisation')
        if std and (std.get('factor') not in (None, '') or std.get('true_N') not in (None, '')):
            s, _c = ReagentStandardisation.objects.get_or_create(prep=obj)
            s.location = location
            s.primary_std = (std.get('primary_std') or '').strip()[:120]
            s.ps_mass = _f(std.get('ps_mass'))
            s.ps_purity = _f(std.get('ps_purity'))
            s.ps_eqwt = _f(std.get('ps_eqwt'))
            s.titrant_ml = _f(std.get('titrant_ml'))
            s.nominal_N = _f(std.get('nominal_N'))
            s.true_N = _f(std.get('true_N'))
            s.factor = _f(std.get('factor'))
            s.unit = (std.get('unit') or 'N').strip()[:10]
            s.std_date = _parse_date(std.get('std_date'))
            s.next_due = _parse_date(std.get('next_due'))
            s.save()
        else:
            ReagentStandardisation.objects.filter(prep=obj).delete()

    return JsonResponse({'ok': True, 'id': obj.id})


def reagent_prep_list(request):
    loc = request.GET.get('location') or 'All'
    q = (request.GET.get('q') or '').strip()
    qs = ReagentPrep.objects.all()
    if loc in _LOCS:
        qs = qs.filter(location=loc)
    if q:
        qs = qs.filter(
            _Q(reagent_name__icontains=q) |
            _Q(reagent_no__icontains=q) |
            _Q(chemicals__chemical_name__icontains=q)).distinct()
    qs = qs.order_by('-created_at')
    today = _date.today()
    rows = []
    for o in qs[:1000]:
        expired = bool(o.doe and o.doe < today)
        rows.append({'o': o, 'expired': expired})
    return render(request, 'reagent_prep_list.html',
                  {'list': rows, 'location': loc, 'q': q, 'locations': _LOCS})


@_xframe_sameorigin
def reagent_prep_calculator(request):
    """Standalone fully-loaded calculator, embedded in the form via iframe.
    Served raw (not through the template engine) so the calculator's own JS
    braces are never parsed as Django template tags. xframe_sameorigin lets the
    same-origin iframe render it (site default is X-Frame-Options: DENY)."""
    for p in ('templates/reagent_calc_tool.html',
              _os.path.join(_os.path.dirname(__file__), '..', '..', 'templates', 'reagent_calc_tool.html')):
        try:
            with open(p, encoding='utf-8') as fh:
                return HttpResponse(fh.read())
        except Exception:
            continue
    return HttpResponse('<p>Calculator asset not found.</p>', status=404)


# ---------------------------------------------------------------- controlled PDF
def generate_pdf_for_reagent_prep(obj):
    ctrl = _docctrl(obj.location)
    today = _date.today()

    class CustomPDF(FPDF):
        def __init__(self, *a, **k):
            super().__init__(*a, **k)
            # House brand font is Calibri (unicode TTF) — supports subscripts (H2SO4),
            # micro sign, etc. Fall back to Helvetica (+ latin-1 sanitising) only if
            # the TTF is unavailable, so the report can never crash on chemistry text.
            self.fam = 'Helvetica'
            try:
                if _os.path.exists(_CALIBRI):
                    self.add_font('Calibri', '', _CALIBRI, uni=True)
                    self.add_font('Calibri', 'B',
                                  _CALIBRIB if _os.path.exists(_CALIBRIB) else _CALIBRI, uni=True)
                    self.fam = 'Calibri'
            except Exception:
                self.fam = 'Helvetica'

        def t(self, s):
            s = '' if s is None else str(s)
            if self.fam == 'Calibri':
                return s
            return s.encode('latin-1', 'replace').decode('latin-1')

        def header(self):
            if _os.path.exists(_LOGO):
                try:
                    self.image(_LOGO, 10, 8, 20, 22)
                except Exception:
                    pass
            self.set_xy(32, 9)
            self.set_font(self.fam, 'B', 15)
            self.cell(120, 7, 'ENVI TECH AL', ln=1)
            self.set_xy(32, 16)
            self.set_font(self.fam, '', 8)
            self.cell(120, 5, self.t('Analytical Laboratory - Environmental & Water Testing'), ln=1)
            self.set_xy(32, 21)
            self.set_font(self.fam, 'B', 11)
            self.cell(120, 6, 'REAGENT PREPARATION RECORD', ln=1)
            # control box (top-right)
            bx, by, bw = 150, 8, 52
            self.set_font(self.fam, '', 7)
            self.set_xy(bx, by)
            rows = [
                ('Doc No.', ctrl.doc_no or '-'),
                ('Issue Date', getattr(ctrl, 'issue_date', '') or '-'),
                ('Issue No.', ctrl.issue_no or '-'),
                ('Rev No.', ctrl.rev_no or '-'),
                ('Location', obj.location),
            ]
            y = by
            for k, v in rows:
                self.set_xy(bx, y)
                self.set_font(self.fam, 'B', 7)
                self.cell(22, 5, k, border=1)
                self.set_font(self.fam, '', 7)
                self.cell(bw - 22, 5, self.t(' ' + str(v)), border=1, ln=1)
                y += 5
            self.set_draw_color(0, 0, 0)
            self.line(10, 33, 202, 33)
            self.set_y(37)

        def footer(self):
            self.set_y(-14)
            self.set_font(self.fam, 'I' if self.fam == 'Helvetica' else '', 7)
            self.cell(0, 4,
                      'ENVI TECH AL  -  Controlled document.  Uncontrolled when printed.',
                      align='C', ln=1)
            self.set_font(self.fam, '', 7)
            self.cell(0, 4, 'Page %s of {nb}' % self.page_no(), align='R')

    pdf = CustomPDF(orientation='P', unit='mm', format='A4')
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()

    def kv(label, value, w1=32, w2=64):
        pdf.set_font(pdf.fam, 'B', 9)
        pdf.cell(w1, 6, label, border=0)
        pdf.set_font(pdf.fam, '', 9)
        pdf.cell(w2, 6, pdf.t(value or '-'), border=0)

    kv('Month:', obj.month)
    kv('Type:', obj.rtype, 24, 60)
    pdf.ln(6)
    kv('Reagent Name:', obj.reagent_name, 32, 92)
    kv('Reagent No.:', obj.reagent_no, 26, 34)
    pdf.ln(6)
    conc = ((obj.conc_value + ' ' + obj.conc_unit).strip()) if (obj.conc_value or obj.conc_unit) else '-'
    kv('Concentration:', conc, 32, 60)
    kv('Final Volume:', obj.final_volume, 26, 40)
    pdf.ln(9)

    # chemicals table
    headers = [('S.#', 12), ('Chemical Name', 52), ('CAT No.', 26), ('LOT No.', 26),
               ('Quantity', 24), ('Make', 28), ('Expiry', 24)]
    pdf.set_font(pdf.fam, 'B', 8)
    pdf.set_fill_color(225, 232, 237)
    for h, w in headers:
        pdf.cell(w, 7, h, border=1, align='C', fill=True)
    pdf.ln(7)
    pdf.set_font(pdf.fam, '', 8)

    def _fit(txt, w):
        # Trim to the column width so a long value never overflows the cell.
        txt = pdf.t(txt)
        while txt and pdf.get_string_width(txt) > (w - 2):
            txt = txt[:-1]
        return txt

    for c in obj.chemicals.all():
        exp_dt = _parse_date(c.expiry)
        cells = [(str(c.s_no), 12, 'C'), (c.chemical_name, 52, 'L'), (c.cat_no or '-', 26, 'C'),
                 (c.lot_no or '-', 26, 'C'), (c.quantity or '-', 24, 'C'),
                 (c.make or '-', 28, 'C'), (c.expiry or '-', 24, 'C')]
        for i, (txt, w, al) in enumerate(cells):
            if i == 6 and exp_dt and exp_dt < today:
                pdf.set_text_color(200, 0, 0)
            pdf.cell(w, 6, _fit(txt, w), border=1, align=al)
            pdf.set_text_color(0, 0, 0)
        pdf.ln(6)
    if not obj.chemicals.exists():
        pdf.cell(sum(w for _h, w in headers), 6, 'No chemicals recorded', border=1, align='C')
        pdf.ln(6)
    pdf.ln(4)

    # description
    pdf.set_font(pdf.fam, 'B', 9)
    pdf.cell(0, 6, 'Description / Method of Preparation:', ln=1)
    pdf.set_font(pdf.fam, '', 9)
    pdf.multi_cell(0, 5, pdf.t(obj.description or '-'))
    pdf.ln(2)

    # standardisation
    try:
        s = obj.standardisation
        pdf.set_font(pdf.fam, 'B', 9)
        pdf.cell(0, 6, pdf.t('Standardisation (%s):' % (s.location or obj.location)), ln=1)
        pdf.set_font(pdf.fam, '', 9)
        u = s.unit or 'N'
        line = ('Primary std: %s  |  nominal %s %s -> true %s %s  |  factor %s  |  date %s  |  next due %s' % (
            s.primary_std or '-',
            ('%.4f' % s.nominal_N) if s.nominal_N is not None else '-', u,
            ('%.4f' % s.true_N) if s.true_N is not None else '-', u,
            ('%.4f' % s.factor) if s.factor is not None else '-',
            s.std_date.strftime('%d-%m-%Y') if s.std_date else '-',
            s.next_due.strftime('%d-%m-%Y') if s.next_due else '-'))
        pdf.multi_cell(0, 5, pdf.t(line))
        pdf.ln(2)
    except ReagentStandardisation.DoesNotExist:
        pass

    pdf.ln(4)
    pdf.set_font(pdf.fam, 'B', 9)
    dop = obj.dop.strftime('%d-%m-%Y') if obj.dop else '-'
    doe = obj.doe.strftime('%d-%m-%Y') if obj.doe else '-'
    pdf.cell(48, 6, pdf.t('Prepared By: ' + (obj.prepared_by or '-')))
    pdf.cell(48, 6, pdf.t('Verified By: ' + (obj.verified_by or '-')))
    pdf.ln(6)
    pdf.cell(48, 6, 'D.O.P.: ' + dop)
    if obj.doe and obj.doe < today:
        pdf.set_text_color(200, 0, 0)
    pdf.cell(48, 6, 'D.O.E.: ' + doe)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(8)

    out = pdf.output(dest='S')
    if isinstance(out, str):
        out = out.encode('latin-1')
    resp = HttpResponse(bytes(out), content_type='application/pdf')
    safe_no = ''.join(ch for ch in str(obj.reagent_no or obj.id) if ch.isalnum() or ch in '-_') or str(obj.id)
    fname = 'ReagentPrep_%s_%s.pdf' % (safe_no, obj.location)
    resp['Content-Disposition'] = 'inline; filename="%s"' % fname
    return resp


def reagent_prep_pdf_from_list(request, pk=None):
    if pk:
        obj = get_object_or_404(ReagentPrep, id=pk)
        return generate_pdf_for_reagent_prep(obj)
    # No pk: fall back to the list view (full context) rather than a bare render.
    return reagent_prep_list(request)


__all__ = [
    'reagent_prep', 'reagent_prep_save', 'reagent_prep_doc_save', 'reagent_prep_list',
    'reagent_prep_calculator', 'reagent_prep_pdf_from_list',
    'generate_pdf_for_reagent_prep',
]
