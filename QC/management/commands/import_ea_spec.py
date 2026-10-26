"""Induct external-assessment (PNAC) NC&CA forms with their root cause analyses (26-10-2026).

    manage.py import_ea_spec QC/fixtures/ea_lahore_spec.json            # dry run (rolled back), prints what would be added
    manage.py import_ea_spec QC/fixtures/ea_lahore_spec.json --apply

The spec is built from the laboratory's signed Word / Excel forms (ETAL-QMS-710-FF-01 and -01A): one NC&CA per form,
with one RCA per root cause (parts a, b, c ... as on paper). Records are closed, the RCAs reviewed; paper signatures are
kept as printed names (no e-signature is applied). Idempotent: an NC&CA number already present for the location is skipped.
"""
import json
from datetime import date

from django.core.management.base import BaseCommand
from django.db import transaction

from QC.models import Ncca, NccaRca


def _date(s):
    return date.fromisoformat(s) if s else None


class Command(BaseCommand):
    help = 'Induct external-assessment NC&CA forms (with RCAs) from a spec.'

    def add_arguments(self, p):
        p.add_argument('spec')
        p.add_argument('--apply', action='store_true')

    def handle(self, *a, **o):
        spec = json.load(open(o['spec'], encoding='utf8'))
        built = spec.get('built', '')
        n = {'ncs': 0, 'rcas': 0, 'skipped': 0}
        with transaction.atomic():
            for x in spec['ncs']:
                if Ncca.objects.filter(location=x['location'], nc_no=x['nc_no']).exists():
                    n['skipped'] += 1
                    self.stdout.write('  skip (exists) %s' % x['nc_no'])
                    continue
                f = {k: x[k] for k in ('location', 'nc_no', 'department', 'raised_by', 'clause', 'source', 'details', 'root_cause', 'corrective', 'followup_with',
                                       'followup_desc', 'remarks', 'closed_by_name', 'assigned_to', 'category', 'category_also_critical', 'priority', 'risk_type',
                                       'severity', 'impact_past', 'satisfactory', 'due_audit_internal', 'due_audit_external', 'due_testing', 'due_cal_internal',
                                       'due_cal_external', 'due_complaint', 'sig_legal', 'sig_risk', 'sig_halt', 'sig_preventive', 'sig_non_significant')}
                for k in ('date', 'proposed_date', 'completion_date', 'followup_date', 'evaluated_date', 'closing_date', 'target_date'):
                    f[k] = _date(x.get(k))
                f['raised_by'] = f['raised_by'][:120]; f['closed_by_name'] = f['closed_by_name'][:120]
                f['assigned_date'] = f['date']
                obj = Ncca.objects.create(status='closed', legacy={'key': 'ea:%s:%s' % (x['location'], x['nc_no']), 'form_no': x.get('form_no', ''),
                                                                    'clause_text': x.get('clause_text', ''), 'file': x.get('file', ''), 'notes': x.get('notes', []),
                                                                    'source': spec.get('source', ''), 'inducted': built}, **f)
                n['ncs'] += 1
                for r in x['rcas']:
                    NccaRca.objects.create(nc=obj, part=r.get('part', ''), rca_no=r['rca_no'][:40], clause=r['clause'][:60], deputed=r['deputed'][:120],
                                           date=_date(r['date']), causes=r['causes'], other=(r.get('other') or '')[:300], six_why=r['six_why'], statement=r['statement'],
                                           whys=r['whys'], conclusion=r['conclusion'], performed_name=r['performed_by'][:120], performed_date=_date(r['performed_date']),
                                           reviewed_name=r['reviewed_by'][:120], reviewed_date=_date(r['reviewed_date']), status='reviewed', legacy={'inducted': built})
                    n['rcas'] += 1
                self.stdout.write('  add %s (%s, %d RCA%s)' % (x['nc_no'], x['category'], len(x['rcas']), '' if len(x['rcas']) == 1 else 's'))
            if not o['apply']:
                transaction.set_rollback(True)
        self.stdout.write('%s: NC&CA %d, RCA %d, skipped %d' % ('APPLIED' if o['apply'] else 'DRY RUN (rolled back)', n['ncs'], n['rcas'], n['skipped']))
