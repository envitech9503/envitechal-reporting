"""Induct the laboratories' internal-audit record from a spec file (22-10-2026).

    manage.py import_ia_spec QC/fixtures/ia_spec.json            # dry run
    manage.py import_ia_spec QC/fixtures/ia_spec.json --apply    # create

The spec (built from the Word / Excel record: audit reports, plans, circulars, witnessing, NC&CA forms,
RCAs, the NC&CA log) holds every clause finding verbatim. Owner decisions 22-10-2026: audits inducted as
signed records (the printed names and dates kept; no e-signature, since nobody signed in the system);
Karachi NC&CA forms and RCAs inducted closed / reviewed as on paper; Lahore NC entries derived from the
findings as drafts for the laboratory to complete; log-only rows kept as closed log entries. Idempotent:
a record already inducted from the same source is skipped (legacy.key).
"""
import datetime as _dt
import json
import os

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from QC.models import IaClause, IaPlan, IaAudit, IaFinding, IaCircular, IaWitness, Ncca, NccaRca


def _date(s):
    return _dt.date.fromisoformat(s) if s else None


class Command(BaseCommand):
    help = 'Induct the internal-audit record from a spec JSON (dry run unless --apply).'

    def add_arguments(self, p):
        p.add_argument('spec')
        p.add_argument('--apply', action='store_true')

    def handle(self, *a, **o):
        if not os.path.exists(o['spec']):
            raise CommandError('spec not found: %s' % o['spec'])
        with open(o['spec'], encoding='utf-8') as fh:
            spec = json.load(fh)
        built = spec.get('built', '')
        n = {'clauses': 0, 'plans': 0, 'circulars': 0, 'audits': 0, 'findings': 0, 'witness': 0, 'ncs': 0, 'rcas': 0, 'log': 0, 'lahore': 0, 'skipped': 0}
        with transaction.atomic():
            clause_by_code = {}
            for c in spec['clauses']:
                obj = IaClause.objects.filter(code=c['code'], standard='17025').first()
                if obj is None:
                    obj = IaClause.objects.create(code=c['code'], title=c['title'], requirement=c['requirement'], level=c['level'], order=c['order'])
                    n['clauses'] += 1
                clause_by_code[c['code']] = obj
            # plans
            for p in spec['plans']:
                key = 'plan:%s:%d' % (p['location'], p['year'])
                if IaPlan.objects.filter(legacy__key=key).exists() or IaPlan.objects.filter(location=p['location'], year=p['year']).exists():
                    n['skipped'] += 1; continue
                IaPlan.objects.create(location=p['location'], year=p['year'], rows=p['rows'], status='approved', mr_name=p['mr_name'], mr_date=_date(p['mr_date']),
                                      ceo_name=p['ceo_name'], ceo_date=_date(p['ceo_date']), legacy={'key': key, 'file': p['file'], 'notes': p['notes'], 'inducted': built})
                n['plans'] += 1
            # audits (+ findings, witnessing)
            audits = {}
            for a in spec['audits']:
                key = 'audit:%s:%s' % (a['location'], a['audit_no'])
                ex = IaAudit.objects.filter(location=a['location'], audit_no=a['audit_no']).first()
                if ex is not None:
                    audits['%s %s' % (a['location'], a['audit_no'])] = ex
                    n['skipped'] += 1; continue
                s = a['summary']
                obj = IaAudit.objects.create(location=a['location'], audit_no=a['audit_no'], year=a['year'], seq=a['seq'], date_start=_date(a['date_start']), date_end=_date(a['date_end']),
                                             days=a['days'], auditor=a['auditor'], auditor_title=a['auditor_title'], auditee=a['auditee'], auditee_title=a['auditee_title'], address=a['address'],
                                             n_obs=s['obs'], n_minor=s['minor'], n_major=s['major'], timeframe=a['timeframe'], conclusion=a['conclusion'], status='closed',
                                             auditor_sign_date=_date(a['sign']['auditor_date']), auditee_sign_date=_date(a['sign']['auditee_date']),
                                             legacy={'key': key, 'file': a['file'], 'notes': a['notes'], 'inducted': built, 'summary': s, 'sign': a['sign']},
                                             remarks='Inducted from the laboratory record (%s) on %s; signed on paper by %s (auditor) and %s (auditee).' % (a['file'][:80], built, a['sign']['auditor'], a['sign']['auditee']))
                rows = []
                for i, f in enumerate(a['findings']):
                    rows.append(IaFinding(audit=obj, order=(i + 1) * 10, clause=clause_by_code.get(f['clause']) if f['clause'] else None, label=f['label'], requirement=f['requirement'],
                                          ref=f['ref'], finding=f['finding'], result=f['result'], tag=', '.join(f['tags'])[:40]))
                IaFinding.objects.bulk_create(rows)
                n['findings'] += len(rows)          # the summary counts stay as the laboratory printed and signed them (legacy.summary)
                audits['%s %s' % (a['location'], a['audit_no'])] = obj
                n['audits'] += 1
                if a.get('witness'):
                    w = a['witness']
                    IaWitness.objects.create(audit=obj, date=_date(w['date']), rows=w['rows'], auditor=w['auditor'], auditees=[{'name': x} for x in w['auditees']],
                                             sign_date=_date(w['sign_date']), status='closed', legacy={'key': key + ':witness', 'circular': w.get('circular', ''), 'inducted': built})
                    n['witness'] += 1
            # circulars
            for c in spec['circulars']:
                key = 'circ:%s' % c['key']
                if IaCircular.objects.filter(legacy__key=key).exists():
                    n['skipped'] += 1; continue
                audit = audits.get('%s %s' % (c['location'], c['audit_no']))
                if audit is None and c['kind'] == 'witness':            # the 2025 witnessing circular is numbered 02/2025 but belongs to audit 01/2025
                    audit = audits.get('%s 01/%s' % (c['location'], c['audit_no'].split('/')[-1]))
                obj = IaCircular.objects.create(location=c['location'], kind=c['kind'], audit=audit, audit_no=c['audit_no'], issue_date=_date(c['issue_date']), audit_date_text=c['audit_date_text'],
                                                to_text=c['to'], from_text=c['from'], sessions=c['sessions'], attendance=[{'name': x['name'], 'designation': x['designation'], 'user_id': None, 'signed_at': None} for x in c['attendance']],
                                                ceo_name=c['ceo_name'], status='issued', legacy={'key': key, 'file': c['file'], 'notes': c['notes'], 'inducted': built})
                n['circulars'] += 1
                if c['kind'] == 'witness' and audit is not None:
                    IaWitness.objects.filter(audit=audit, circular__isnull=True).update(circular=obj)
            # Karachi NC&CA forms + RCAs
            for x in spec['ncs']:
                if Ncca.objects.filter(location=x['location'], nc_no=x['nc_no']).exists():
                    n['skipped'] += 1; continue
                audit = audits.get(x['audit'])
                finding = None
                if audit is not None:
                    finding = audit.findings.filter(label=x['finding_clause']).first()
                lg = x['log']
                obj = Ncca.objects.create(
                    location=x['location'], nc_no=x['nc_no'], date=_date(x['date']), department=x['department'], raised_by=x['raised_by'], clause='%s (ISO/IEC 17025:2017)' % x['clause'],
                    source=x['source'], audit=audit, finding=finding,
                    due_audit_internal=x['due_audit_internal'], due_audit_external=x['due_audit_external'], due_testing=x['due_testing'], due_cal_internal=x['due_cal_internal'],
                    due_cal_external=x['due_cal_external'], due_complaint=x['due_complaint'], due_other=x['due_other'],
                    category=x['category'], category_also_critical=x['category_also_critical'], sig_legal=x['sig_legal'], sig_risk=x['sig_risk'], sig_halt=x['sig_halt'],
                    sig_preventive=x['sig_preventive'], sig_non_significant=x['sig_non_significant'], priority=x['priority'], risk_type=x['risk_type'], severity=x['severity'],
                    impact_past=x['impact_past'], evaluated_date=_date(x['evaluated_date']), details=x['details'], proposed_date=_date(x['proposed_date']),
                    root_cause=x['root_cause'], corrective=x['corrective'], completion_date=_date(x['completion_date']),
                    followup_with=x['followup_with'], satisfactory=x['satisfactory'], followup_date=_date(x['followup_date']) if x['followup_date'] else _date(lg['followup_date']),
                    next_followup_date=_date(x['next_followup_date']), followup_desc=x['followup_desc'], closed_by_name=lg['closed_by'], closing_date=_date(lg['closing_date']), remarks=x['remarks'],
                    log_sno=lg['s_no'], assigned_to=lg['assigned_to'], assigned_date=_date(lg['assigned_date']), target_date=_date(lg['target_date']), status='closed',
                    legacy={'key': 'nc:%s:%s' % (x['location'], x['nc_no']), 'form_no': x['form_no'], 'log_clause': lg['clause'], 'form_closed_by': x['closed_by'], 'notes': x['notes'], 'inducted': built})
                n['ncs'] += 1
                r = x['rca']
                NccaRca.objects.create(nc=obj, rca_no=r['rca_no'], clause=r['clause'], deputed=r['deputed'], date=_date(r['date']), causes=r['causes'], other=r['other'], six_why=r['six_why'],
                                       statement=r['statement'], whys=r['whys'], conclusion=r['conclusion'], performed_name=r['performed_by'], performed_date=_date(r['performed_date']),
                                       reviewed_name=r['reviewed_by'], reviewed_date=_date(r['reviewed_date']), status='reviewed', legacy={'inducted': built})
                n['rcas'] += 1
            # log-only rows
            for x in spec['log_only']:
                if Ncca.objects.filter(location=x['location'], nc_no=x['nc_no']).exists():
                    n['skipped'] += 1; continue
                Ncca.objects.create(location=x['location'], nc_no=x['nc_no'], date=_date(x['date']), raised_by=x['reported_by'], clause='%s (ISO/IEC 17025:2017)' % x['clause'], source=x['source'],
                                    due_audit_internal=x['source'] == 'IA', due_audit_external=x['source'] == 'EA', due_complaint=x['source'] == 'CC', category=x['category'],
                                    assigned_to=x['assigned_to'], assigned_date=_date(x['assigned_date']), target_date=_date(x['target_date']), followup_date=_date(x['followup_date']),
                                    closing_date=_date(x['closing_date']), closed_by_name=x['closed_by'], log_sno=x['s_no'], log_only=True, status='closed',
                                    details='Entry of the NC&CA log (ETAL-QMS-710-FF-02); the NC&CA form is not in the inducted record.',
                                    legacy={'key': 'log:%s:%s' % (x['location'], x['nc_no']), 'notes': x['notes'], 'inducted': built})
                n['log'] += 1
            # Lahore NC drafts derived from the findings
            for x in spec['lahore_ncs']:
                nc_no = '%s/%s' % (x['nc_no'], x['audit'].split()[-1].replace('/', '-')) if not x['nc_no'].startswith('Obs/') else 'Obs/%s' % x['audit'].split()[-1].replace('/', '-')
                if Ncca.objects.filter(location=x['location'], nc_no=nc_no).exists():
                    n['skipped'] += 1; continue
                audit = audits.get(x['audit'])
                finding = audit.findings.filter(label=x['clause'].split(',')[0].strip()).first() if audit else None
                Ncca.objects.create(location=x['location'], nc_no=nc_no, date=_date(x['date']), raised_by=x['raised_by'], clause='%s (ISO/IEC 17025:2017)' % x['clause'], source='IA',
                                    audit=audit, finding=finding, due_audit_internal=True, category=x['category'], details=x['details'], status='draft',
                                    legacy={'key': 'lnc:%s:%s' % (x['location'], nc_no), 'notes': x['notes'], 'inducted': built})
                n['lahore'] += 1
            if not o['apply']:
                transaction.set_rollback(True)
        self.stdout.write('%s: %s' % ('APPLIED' if o['apply'] else 'DRY RUN', ', '.join('%s %d' % (k, v) for k, v in n.items())))
