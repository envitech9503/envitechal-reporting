"""Document Control register (owner decision 23-10-2026): one page, for the administrator, holding every controlled
form of the reporting software with its revision history. A new revision applies from its effective date to
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
                        'own form of this chart (periods it was in force)', ['*']))
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


def doc_register(request):
    user = request.user
    if not (user.is_authenticated and user.is_superuser):
        return HttpResponse('Document-control numbers are maintained by an administrator.', status=403)
    today = _dt.date.today()
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
    groups = []
    for g, forms in _groups():
        rows = []
        for f in forms:
            module, label, where = f[:3]
            locs = _locs(module, f)
            for loc in locs:
                rows.append(_row(module, loc, label, where, today))
        groups.append({'name': g, 'rows': rows})
    focus = request.GET.get('focus') or ''
    return render(request, 'doc_register.html', {'groups': groups, 'today': today, 'focus': focus, 'n_rev': DocControlRevision.objects.count()})
