"""Document Control register (owner decision 23-10-2026): one page holding every controlled form of the reporting
software with its revision history. Every logged-in user can view it, filter it by laboratory and by current / history,
and download it as PDF or Excel (24-10-2026); issuing and correcting revisions is reserved to the administrator. A new revision applies from its effective date to
documents dated on or after that date; documents dated earlier keep the revision they were issued with."""
from .shared import *  # noqa: F401,F403
import datetime as _dt

from django.contrib import messages as _msg
from django.shortcuts import redirect as _redirect

from EnviTechAlApp.models import DocControlRevision, InventoryDocControl
from EnviTechAlApp import doccontrol as DC
from QC.models import ControlChart

_LABS = ['Karachi', 'Lahore']
_CC_KEYS = [('control_chart', 'CRM'), ('control_chart_rm', 'RM'), ('control_chart_ic', 'IC'), ('control_chart_eq', 'EQ'),
            ('control_chart_dup', 'DUP'), ('control_chart_spk', 'SPK'), ('control_chart_mon', 'MON'), ('control_chart_ws', 'WS')]


def _groups():
    """(group, [(module, label, where printed)]) for every controlled form of the software."""
    acts = dict(ControlChart.ACTIVITIES)
    cc = [(k, 'Control chart - %s' % acts.get(a, a), 'chart pages and PDFs of the period') for k, a in _CC_KEYS]
    own = []
    mods = set(InventoryDocControl.objects.filter(module__startswith='cc_chart_').values_list('module', flat=True))
    mods |= set(DocControlRevision.objects.filter(module__startswith='cc_chart_').values_list('module', flat=True))
    for m in sorted(mods, key=lambda x: int(x.split('_')[-1]) if x.split('_')[-1].isdigit() else 0):
        pk = m.split('_')[-1]
        c = ControlChart.objects.filter(pk=int(pk)).first() if pk.isdigit() else None
        if c is not None:
            own.append((m, 'Chart #%d - %s%s (%s, %s)' % (c.pk, c.parameter, (' ' + c.level) if c.level else '', c.location, c.activity),
                        'own form of this chart (periods it was in force)', ['*'], c.location))
    return [
        ('Laboratory records', [('logging_sheet', 'Sample logging sheet (Issue Date)', 'logging sheet PDF; the form number and issue no. are stored on each sheet'),
                                ('job_completion', 'Job completion form', 'job completion PDF')]),
        ('Registers', [('chemicals', 'Chemicals register', 'chemicals register and stock reports (current)'),
                       ('equipment', 'Equipment register', 'equipment register report (current)')]),
        ('QC sheets', [('qc_rds', 'QC raw-data sheet (RDS DW / WW)', 'RDS PDFs (both laboratories)', ['*']),
                       ('qc_test_results', 'Testing results of DW / WW samples', 'testing-results PDFs; "Both / other" = record without a laboratory', _LABS + ['*']),
                       ('reagent_prep', 'Reagent & standard preparation', 'preparation records and calculator')]),
        ('Control charts', cc + own),
        ('Measurement of Uncertainty', [('mou', 'MOU study (ETAL-LAB-706-FF-01)', 'study pages and PDFs')]),
        ('Internal Audit', [('ia_plan', 'Annual audit plan', 'plan PDF (plan year)'), ('ia_circular', 'Audit circular & attendance', 'circular PDF (issue date)'),
                            ('ia_report', 'Internal audit report & witnessing', 'audit report PDF (audit date)'),
                            ('ia_nc', 'NC & corrective action form', 'NC&CA PDF (NC date)'), ('ia_rca', 'Root cause analysis', 'RCA PDF (RCA date)'),
                            ('ia_log', 'NC&CA log', 'log PDF (current)')]),
    ]


def _locs(module, f):
    return f[3] if len(f) > 3 else sorted(set(_LABS) | set(DocControlRevision.objects.filter(module=module).exclude(location='*').values_list('location', flat=True)),
                                          key=lambda x: (x == '*', x))


def _allowed():
    """(module, location) pairs a document of the software reads - the only ones the register may change."""
    return {(f[0], loc) for _g, forms in _groups() for f in forms for loc in _locs(f[0], f)}


def _row(module, location, label, where, today):
    revs = list(DC.revisions(module, location))
    cur = DC.revision_on(module, location, today) if revs else None
    mirror = InventoryDocControl.objects.filter(module=module, location=location).first() if not revs else None
    return {'module': module, 'location': location, 'label': label, 'where': where, 'revs': revs, 'cur': cur, 'n': len(revs),
            'future': [r for r in revs if r.effective_from > today],
            'mirror': mirror, 'key': '%s|%s' % (module, location), 'key2': '%s__%s' % (module, location),
            'cv': DC._vals(cur) if cur is not None else {f: '' for f in DC.FIELDS},
            'seed_doc': (cur.doc_no if cur is not None else '') or ((mirror.doc_no or '') if mirror is not None else '')}


_SHOWS = {'both': 'Current revisions and history', 'current': 'Current revisions', 'history': 'Revision history'}


def _applies(row_loc, chart_loc, loc):
    """Does a register row belong to the laboratory filter `loc` ('All', 'Karachi', 'Lahore')?"""
    if loc == 'All':
        return True
    if row_loc == loc:
        return True
    return row_loc == '*' and (chart_loc is None or chart_loc == loc)


def _build(loc, today):
    groups = []
    for g, forms in _groups():
        rows = []
        for f in forms:
            module, label, where = f[:3]
            chart_loc = f[4] if len(f) > 4 else None
            for l in _locs(module, f):
                if _applies(l, chart_loc, loc):
                    rows.append(_row(module, l, label, where, today))
        if rows:
            groups.append({'name': g, 'rows': rows})
    return groups


def _lab_label(r):
    if r['location'] != '*':
        return r['location']
    return 'This chart' if r['module'].startswith('cc_chart_') else 'Both / other'


def _status(v, r, today):
    if r['cur'] is not None and v.pk == r['cur'].pk:
        return 'In force'
    return 'Scheduled' if v.effective_from > today else 'Superseded'


def _eff(d):
    return 'From the start' if d is None or d.year == 2000 else d.strftime('%d-%m-%Y')


def _who(u):
    if u is None:
        return 'system'
    return (u.get_full_name() or u.get_username()).strip()


def _export_name(loc, show, today, ext):
    return 'EnviTechAL_Document_Control_Register_%s_%s_%s.%s' % (loc, show, today.strftime('%d-%m-%Y'), ext)


def _xlsx(groups, loc, show, today, user):
    from QC.xlsx_lite import Workbook
    wb = Workbook()
    head_lines = ['ENVI TECH AL - DOCUMENT CONTROL REGISTER',
                  'Laboratory: %s   |   Report: %s   |   Generated %s by %s' % (loc if loc != 'All' else 'All laboratories', _SHOWS[show],
                                                                             _dt.datetime.now().strftime('%d-%m-%Y %H:%M'), _who(user))]
    if show in ('both', 'current'):
        ws = wb.sheet('Current revisions')
        cols = ['S. No.', 'Group', 'Form', 'Laboratory', 'Document No.', 'Issue date', 'Issue No.', 'Rev. No.', 'In force since', 'Revisions on record', 'Scheduled revisions', 'Where printed']
        ws.widths([7, 22, 44, 14, 26, 13, 10, 9, 15, 11, 12, 48])
        ws.row([head_lines[0]], style='title', merge=len(cols), height=24)
        ws.row([head_lines[1]], style='sub', merge=len(cols))
        ws.row([''], style='text')
        ws.row(cols, style='head', header=True, height=30)
        n = 0
        for g in groups:
            for r in g['rows']:
                n += 1
                cv = r['cv']
                ws.row([n, g['name'], r['label'], _lab_label(r), (cv['doc_no'] or 'TBA'), cv['issue_date'] or '-', cv['issue_no'] or '-', cv['rev_no'] or '-',
                        _eff(r['cur'].effective_from) if r['cur'] is not None else '-', r['n'],
                        ', '.join('%s from %s' % (v.doc_no, v.effective_from.strftime('%d-%m-%Y')) for v in r['future']) or '-', r['where']],
                       styles=[None, None, None, None, None, None, None, None, None, None, 'cell_info' if r['future'] else None, 'cell_muted'])
    if show in ('both', 'history'):
        ws = wb.sheet('Revision history')
        cols = ['S. No.', 'Group', 'Form', 'Laboratory', 'Effective from', 'Status', 'Document No.', 'Issue date', 'Issue No.', 'Rev. No.', 'Reason / note', 'Recorded on', 'Recorded by']
        ws.widths([7, 22, 44, 14, 15, 12, 26, 13, 10, 9, 60, 17, 20])
        ws.row([head_lines[0]], style='title', merge=len(cols), height=24)
        ws.row([head_lines[1]], style='sub', merge=len(cols))
        ws.row([''], style='text')
        ws.row(cols, style='head', header=True, height=30)
        n = 0
        for g in groups:
            for r in g['rows']:
                for v in sorted(r['revs'], key=lambda x: (x.effective_from, x.id)):
                    n += 1
                    st = _status(v, r, today)
                    ws.row([n, g['name'], r['label'], _lab_label(r), _eff(v.effective_from), st, v.doc_no or '-', v.issue_date or '-', v.issue_no or '-', v.rev_no or '-',
                            v.note, v.created_at.strftime('%d-%m-%Y %H:%M') if v.created_at else '-', _who(v.created_by)],
                           styles=[None, None, None, None, None, {'In force': 'cell_ok', 'Scheduled': 'cell_info'}.get(st, 'cell_muted')])
        if not n:
            ws.row(['No revision on record for this selection.'], style='note', merge=len(cols))
    ws = wb.sheets[-1]
    ws.row([''], style='text')
    ws.row(['Documents dated on or after the effective date of a revision print that revision; documents dated earlier keep the revision they were issued with. '
            'Analysis reports store their form number on each report and are not listed here.'], style='note', merge=10, height=30)
    resp = HttpResponse(wb.save(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    resp['Content-Disposition'] = 'attachment; filename="%s"' % _export_name(loc, show, today, 'xlsx')
    return resp


def _pdf_report(groups, loc, show, today, user):
    from QC.views.ia_pdf import _pdf, _resp
    ctrl = {'doc_no': 'Document Control Register', 'issue_date': today.strftime('%d-%m-%Y'), 'issue_no': '-', 'rev_no': '-'}
    sub = '%s  -  %s' % ((loc.upper() + ' LABORATORY') if loc != 'All' else 'ALL LABORATORIES', _SHOWS[show].upper())
    pdf = _pdf('DOCUMENT CONTROL REGISTER', sub, ctrl, loc if loc in _LABS else 'Karachi', 'L')
    pdf.alias_nb_pages(); pdf.set_auto_page_break(True, 26)
    if pdf.page == 0:
        pdf.add_page()
    f = pdf.fam
    GREEN, GREY = (15, 81, 50), (242, 245, 243)
    pdf.set_font(f, '', 7.5); pdf.set_text_color(80, 80, 80)
    pdf.cell(pdf.W, 4.5, 'Generated %s by %s  -  documents dated on or after a revision\'s effective date print it; documents dated earlier keep the revision they were issued with.'
             % (_dt.datetime.now().strftime('%d-%m-%Y %H:%M'), _who(user)), ln=1)
    pdf.set_text_color(0, 0, 0); pdf.ln(1)

    def lines(txt, w):
        try:
            return max(1, len(pdf.multi_cell(w - 1.6, 3.6, txt, dry_run=True, output='LINES')))
        except Exception:
            return 1

    def table(title, cols, rowsets):
        """cols: [(name, width, align)]; rowsets: [(group, [(values, fills)])]."""
        def head():
            pdf.set_font(f, 'B', 7.4); pdf.set_fill_color(*GREEN); pdf.set_text_color(255, 255, 255); pdf.set_draw_color(160, 170, 165)
            for name, w, _a in cols:
                pdf.cell(w, 6, name, 1, 0, 'C', fill=True)
            pdf.ln(6); pdf.set_text_color(0, 0, 0)
        pdf.set_font(f, 'B', 10); pdf.set_text_color(*GREEN); pdf.cell(pdf.W, 6, title, ln=1); pdf.set_text_color(0, 0, 0)
        head()
        for g, rows in rowsets:
            if pdf.get_y() + 12 > pdf.h - 26:
                pdf.add_page(); head()
            pdf.set_font(f, 'B', 7.6); pdf.set_fill_color(232, 243, 236); pdf.set_text_color(*GREEN)
            pdf.cell(pdf.W, 5, g, 1, 1, 'L', fill=True); pdf.set_text_color(0, 0, 0)
            for vals, fills in rows:
                pdf.set_font(f, '', 7.2)
                h = max(lines(str(v), w) for v, (_n, w, _a) in zip(vals, cols)) * 3.6 + 1.4
                if pdf.get_y() + h > pdf.h - 26:
                    pdf.add_page(); head()
                x0, y0 = pdf.get_x(), pdf.get_y()
                x = x0
                for i, (v, (_n, w, a)) in enumerate(zip(vals, cols)):
                    fill = fills.get(i) if fills else None
                    if fill:
                        pdf.set_fill_color(*fill); pdf.rect(x, y0, w, h, 'F')
                    pdf.rect(x, y0, w, h)
                    pdf.set_xy(x + 0.8, y0 + 0.7)
                    pdf.multi_cell(w - 1.6, 3.6, str(v), 0, a)
                    x += w
                pdf.set_xy(x0, y0 + h)
        pdf.ln(3)

    if show in ('both', 'current'):
        cols = [('S.No.', 10, 'C'), ('Form', 70, 'L'), ('Laboratory', 22, 'C'), ('Document No.', 46, 'L'), ('Issue date', 22, 'C'),
                ('Issue', 13, 'C'), ('Rev.', 13, 'C'), ('In force since', 24, 'C'), ('Revisions', 15, 'C'), ('Scheduled', 42, 'L')]
        rowsets, n = [], 0
        for g in groups:
            rs = []
            for r in g['rows']:
                n += 1
                cv = r['cv']
                sched = ', '.join('%s from %s' % (v.doc_no, v.effective_from.strftime('%d-%m-%Y')) for v in r['future']) or '-'
                rs.append(([n, r['label'], _lab_label(r), cv['doc_no'] or 'TBA', cv['issue_date'] or '-', cv['issue_no'] or '-', cv['rev_no'] or '-',
                            _eff(r['cur'].effective_from) if r['cur'] is not None else '-', r['n'], sched],
                           {9: (224, 242, 254)} if r['future'] else ({3: (254, 243, 199)} if not cv['doc_no'] else None)))
            rowsets.append((g['name'], rs))
        table('1.  Revisions in force on %s' % today.strftime('%d-%m-%Y'), cols, rowsets)
    if show in ('both', 'history'):
        if show == 'both':
            pdf.add_page()
        cols = [('S.No.', 10, 'C'), ('Form', 52, 'L'), ('Laboratory', 19, 'C'), ('Effective from', 21, 'C'), ('Status', 17, 'C'), ('Document No.', 40, 'L'),
                ('Issue date', 19, 'C'), ('Issue', 10, 'C'), ('Rev.', 10, 'C'), ('Reason / note', 52, 'L'), ('Recorded', 27, 'C')]
        rowsets, n = [], 0
        for g in groups:
            rs = []
            for r in g['rows']:
                for v in sorted(r['revs'], key=lambda x: (x.effective_from, x.id)):
                    n += 1
                    st = _status(v, r, today)
                    rs.append(([n, r['label'], _lab_label(r), _eff(v.effective_from), st, v.doc_no or '-', v.issue_date or '-', v.issue_no or '-', v.rev_no or '-',
                                v.note or '-', '%s\n%s' % (v.created_at.strftime('%d-%m-%Y') if v.created_at else '-', _who(v.created_by))],
                               {4: {'In force': (220, 252, 231), 'Scheduled': (224, 242, 254)}.get(st, (242, 245, 243))}))
            if rs:
                rowsets.append((g['name'], rs))
        table('%s.  Revision history' % ('2' if show == 'both' else '1'), cols, rowsets)
    pdf.set_font(f, '', 7); pdf.set_text_color(90, 90, 90)
    pdf.multi_cell(pdf.W, 3.6, 'Analysis reports (drinking water, waste water, ambient air, gaseous, noise, lux, ...) store their form number on each report and are '
                               'not listed in this register. A revision marked "From the start" is the revision in force before revision history was introduced (23-10-2026).')
    resp = _resp(pdf, _export_name(loc, show, today, 'pdf')[:-4])
    return resp


def doc_register(request):
    user = request.user
    if not user.is_authenticated:
        return _redirect('/login/?next=/qc/document-control/')
    today = _dt.date.today()
    if request.method == 'POST' and not user.is_superuser:
        return HttpResponse('Document-control numbers are maintained by an administrator.', status=403)
    if request.method == 'POST':
        P = request.POST
        act = P.get('action')
        module, location = (P.get('module') or '').strip()[:40], (P.get('location') or '').strip()[:20]
        vals = {f: (P.get(f) or '').strip() for f in DC.FIELDS}
        note = (P.get('note') or '').strip()
        back = _redirect('/qc/document-control/?focus=%s__%s#%s__%s' % (module, location, module, location))
        if (module, location) not in _allowed():
            return HttpResponse('bad request', status=400)
        if len(note) < 5:
            _msg.error(request, 'Nothing was changed: give the reason (at least 5 characters), e.g. "Form revised after management review MR-03/2026".')
            return back
        if act == 'issue':
            if not vals['doc_no']:
                _msg.error(request, 'Nothing was changed: the document number is required.')
                return back
            try:
                eff = _dt.datetime.strptime(P.get('effective_from') or '', '%Y-%m-%d').date()
            except ValueError:
                _msg.error(request, 'Nothing was changed: the effective date is required (the date from which documents carry the new revision).')
                return back
            cur = DC.revision_on(module, location, eff)
            if cur is not None and all(DC._vals(cur)[f] == vals[f] for f in DC.FIELDS):
                _msg.error(request, 'Nothing was changed: the values are the same as the revision in force on %s.' % eff.strftime('%d-%m-%Y'))
                return back
            DC.issue_revision(module, location, vals, eff, note, user)
            _msg.success(request, 'New revision of %s (%s) issued: %s, issue date %s, issue %s rev. %s - applies to documents dated from %s; '
                                  'documents dated earlier keep their revision.' % (module, location, vals['doc_no'], vals['issue_date'] or '-',
                                                                                    vals['issue_no'] or '01', vals['rev_no'] or '00', eff.strftime('%d-%m-%Y')))
        elif act == 'correct':
            rid = (P.get('rev') or '').strip()
            rev = DocControlRevision.objects.filter(pk=int(rid), module=module, location=location).first() if rid.isdigit() else None
            if rev is None:
                return HttpResponse('unknown revision', status=404)
            DC.correct_revision(rev, vals, note, user)
            _msg.success(request, 'Revision of %s (%s) effective %s corrected. Every document dated in its period prints the corrected values; '
                                  'the previous values are kept in the audit history.' % (module, location, rev.effective_from.strftime('%d-%m-%Y')))
        else:
            return HttpResponse('unknown action', status=400)
        return back
    loc = request.GET.get('loc') if request.GET.get('loc') in _LABS else 'All'
    show = request.GET.get('show') if request.GET.get('show') in _SHOWS else 'both'
    groups = _build(loc, today)
    fmt = request.GET.get('export')
    if fmt == 'xlsx':
        return _xlsx(groups, loc, show, today, user)
    if fmt == 'pdf':
        return _pdf_report(groups, loc, show, today, user)
    focus = request.GET.get('focus') or ''
    n_rev = sum(r['n'] for g in groups for r in g['rows'])
    return render(request, 'doc_register.html', {'groups': groups, 'today': today, 'focus': focus, 'n_rev': n_rev, 'loc': loc, 'show': show,
                                                 'shows': list(_SHOWS.items()), 'labs': ['All'] + _LABS, 'can_admin': user.is_superuser,
                                                 'n_forms': sum(len(g['rows']) for g in groups)})
