"""Management Records / Reports module (owner decision 24-10-2026): the home of the laboratory's management-system
records, organised by ISO/IEC 17025:2017 (Clause 8, Option A, and the related clauses 4, 6.2, 6.6, 7.9, 7.10).
Internal Audit and the Document Control register live here; every future management-related section is added as a
card of the clause map below and as an entry of the Management branch of the sidebar (_qc_sidebar.html, mgmt=1).
The addresses of the existing pages are unchanged (/qc/ia/..., /qc/document-control/), so links and bookmarks keep
working; /management/ia/ and /management/document-control/ are short links to them."""
from .shared import *  # noqa: F401,F403
import datetime as _dt

from django.shortcuts import redirect as _redirect

_LABS = ['Karachi', 'Lahore']


def _clause_map(loc):
    """[(group, [card])] - card: clause, title, scope, status ('live' / 'partial' / 'planned'), links, stats."""
    from QC.models import IaAudit, Ncca, NccaRca, IaPlan
    labs = _LABS if loc == 'All' else [loc]
    q = '?location=%s' % (labs[0] if len(labs) == 1 else 'Karachi')
    today = _dt.date.today()
    # same definitions as the Internal Audit dashboard (open = not closed) and the RCA register (pending RCA)
    open_q = Ncca.objects.filter(location__in=labs).exclude(status='closed')
    open_nc = open_q.count()
    overdue = open_q.filter(target_date__lt=today).count() + open_q.filter(target_date__isnull=True, proposed_date__lt=today).count()
    rca_pending = Ncca.objects.filter(location__in=labs, rca__isnull=True, log_only=False).exclude(status__in=('closed', 'draft')).count()
    audits_y = IaAudit.objects.filter(location__in=labs, year=today.year).count()
    plan_y = IaPlan.objects.filter(location__in=labs, year=today.year).count()
    from QC.views.doc_register import _build
    reg_rows = [r for g in _build(loc, today) for r in g['rows']]          # exactly what the register shows for this filter
    revs = sum(r['n'] for r in reg_rows)
    sched = sum(len(r['future']) for r in reg_rows)
    reg = '/qc/document-control/' + ('' if loc == 'All' else '?loc=%s' % loc)
    return [
        ('Management system (Clause 8)', [
            {'clause': '8.2', 'title': 'Management system documentation', 'status': 'planned',
             'scope': 'Quality policy, objectives, quality manual and their communication; evidence of commitment of top management.'},
            {'clause': '8.3', 'title': 'Control of management system documents', 'status': 'live',
             'scope': 'Document Control register: every controlled form with its revision history, effective dates, approval reason; PDF / Excel register by laboratory.',
             'links': [('Document Control register', reg, True), ('Download PDF', reg + ('&' if '?' in reg else '?') + 'export=pdf', False),
                       ('Download Excel', reg + ('&' if '?' in reg else '?') + 'export=xlsx', False)],
             'stats': [('revisions on record', revs), ('scheduled revisions', sched)]},
            {'clause': '8.4', 'title': 'Control of records', 'status': 'partial',
             'scope': 'Technical records are kept with audit history in each module (reports, certificates, QC, control charts, MOU); a records-retention register is planned.'},
            {'clause': '8.5', 'title': 'Actions to address risks and opportunities', 'status': 'planned',
             'scope': 'Risk & opportunity register: identification, evaluation, actions, effectiveness review.'},
            {'clause': '8.6', 'title': 'Improvement', 'status': 'planned',
             'scope': 'Improvement opportunities from audits, reviews, customer feedback, data analysis and staff suggestions.'},
            {'clause': '8.7', 'title': 'Corrective actions', 'status': 'live',
             'scope': 'NC & Corrective Action forms (710-FF-01), Root Cause Analysis (710-FF-01A) and the NC&CA Log (710-FF-02), with follow-up and closure.',
             'links': [('Open NC&CAs', '/qc/ia/ncs/%s&show=open' % q, True), ('Raise NC', '/qc/ia/ncs/new/%s' % q, False),
                       ('RCA register', '/qc/ia/rca/%s' % q, False), ('NC&CA Log', '/qc/ia/ncs/%s&show=all' % q, False)],
             'stats': [('open', open_nc), ('overdue', overdue), ('awaiting RCA', rca_pending)]},
            {'clause': '8.8', 'title': 'Internal audits', 'status': 'live',
             'scope': 'Annual audit plan (808-FF-01), circulars & attendance (808-FF-03), clause-by-clause audit reports with witnessing (808-FF-02), sign-off.',
             'links': [('IA dashboard', '/qc/ia/%s' % q, True), ('Audit plan', '/qc/ia/plans/%s' % q, False), ('Audit reports', '/qc/ia/audits/%s' % q, False),
                       ('Witnessing', '/qc/ia/witnessing/%s' % q, False), ('Sign-off', '/qc/ia/signing/%s' % q, False)],
             'stats': [('audits %d' % today.year, audits_y), ('plans %d' % today.year, plan_y)]},
            {'clause': '8.9', 'title': 'Management reviews', 'status': 'planned',
             'scope': 'Management review meetings: inputs (8.9.2), outputs, decisions and actions with follow-up.'},
        ]),
        ('Related requirements', [
            {'clause': '4.1 / 4.2', 'title': 'Impartiality and confidentiality', 'status': 'planned',
             'scope': 'Impartiality risk register, declarations and confidentiality undertakings of personnel.'},
            {'clause': '6.2', 'title': 'Personnel - competence, training, authorisation', 'status': 'planned',
             'scope': 'Competence requirements, training records, supervision, monitoring and authorisations per method.'},
            {'clause': '6.6', 'title': 'Externally provided products and services', 'status': 'planned',
             'scope': 'Approved suppliers and subcontractors, evaluation and re-evaluation records.'},
            {'clause': '7.9', 'title': 'Complaints', 'status': 'planned',
             'scope': 'Complaint receipt, investigation, response and closure with the NC&CA link.'},
            {'clause': '7.10', 'title': 'Nonconforming work', 'status': 'partial',
             'scope': 'Raised as NC&CA (source "Testing") in the corrective-action records; a dedicated nonconforming-work log is planned.',
             'links': [('Raise NC', '/qc/ia/ncs/new/%s' % q, False)]},
        ]),
    ]


def mgmt_home(request):
    if not request.user.is_authenticated:
        from urllib.parse import quote
        return _redirect('/login/?next=' + quote(request.get_full_path()))
    loc = request.GET.get('loc') if request.GET.get('loc') in _LABS else 'All'
    groups = _clause_map(loc)
    n = {'live': 0, 'partial': 0, 'planned': 0}
    for _g, cards in groups:
        for c in cards:
            n[c['status']] += 1
    return render(request, 'mgmt_home.html', {'groups': groups, 'loc': loc, 'labs': ['All'] + _LABS, 'n': n, 'mgmt': 1})


def mgmt_ia(request):
    q = request.META.get('QUERY_STRING', '')
    return _redirect('/qc/ia/' + ('?' + q if q else ''))


def mgmt_doc_register(request):
    q = request.META.get('QUERY_STRING', '')
    return _redirect('/qc/document-control/' + ('?' + q if q else ''))
