"""Induct the laboratory's decision-rule record (customer request forms FF-17 and statement-of-conformity records FF-20).

    manage.py import_soc_spec QC/fixtures/soc_karachi_spec.json             # dry run (rolled back)
    manage.py import_soc_spec QC/fixtures/soc_karachi_spec.json --apply

Records are approved (as on the signed paper record) with the printed role names; idempotent per (location, sample, parameter).
"""
import json
from datetime import date

from django.core.management.base import BaseCommand
from django.db import transaction

from QC.models import SocRequest, SocRecord


def _d(s):
    return date.fromisoformat(s) if s else None


class Command(BaseCommand):
    def add_arguments(self, p):
        p.add_argument('spec')
        p.add_argument('--apply', action='store_true')

    def handle(self, *a, **o):
        spec = json.load(open(o['spec'], encoding='utf8'))
        loc, built = spec['location'], spec.get('built', '')
        n = {'requests': 0, 'records': 0, 'skipped': 0}
        with transaction.atomic():
            for q in spec['requests']:
                if SocRequest.objects.filter(location=loc, sample_id=q['sample_id']).exists():
                    n['skipped'] += 1; continue
                SocRequest.objects.create(location=loc, sample_id=q['sample_id'], date=_d(q['date']), reason=q['reason'], organization=q['organization'][:200],
                                          customer_name=q['customer_name'][:150], contact=q['contact'][:120], address=q['address'][:300], analysis=q['analysis'],
                                          parameters=q['parameters'], req_mou=q['req_mou'], req_soc=q['req_soc'], req_opinion=q['req_opinion'], req_limits=q['req_limits'],
                                          req_other=q['req_other'][:300], reporting=q['reporting'], decision=q['decision'], decision_comment=q['decision_comment'],
                                          decision_date=_d(q['decision_date']), customer_sign_name=q['customer_sign_name'][:150],
                                          legacy={'inducted': built, 'file': q['file'], 'notes': q.get('notes', []), 'source': spec.get('source', '')})
                n['requests'] += 1
                self.stdout.write('  request %s' % q['sample_id'])
            for r in spec['records']:
                if SocRecord.objects.filter(location=loc, sample_id=r['sample_id'], parameter__iexact=r['parameter']).exists():
                    n['skipped'] += 1; continue
                req = SocRequest.objects.filter(location=loc, sample_id=r['sample_id']).first()
                SocRecord.objects.create(location=loc, request=req, report_type=r['report_type'], sample_id=r['sample_id'], customer=r['customer'][:200],
                                         parameter=r['parameter'], method=r['method'][:120], unit=r['unit'], standard=r['standard'], limit_text=r['limit_text'],
                                         lower=r['lower'], upper=r['upper'], uncertainty=r['uncertainty'], u_source=r['u_source'], results=r['results'],
                                         decision_rule=r['decision_rule'], status='approved', performed_name=r['performed_name'], reviewed_name=r['reviewed_name'],
                                         approved_name=r['approved_name'],
                                         legacy={'inducted': built, 'file': r['file'], 'notes': r.get('notes', []), 'report_result': r.get('report_result', ''), 'source': spec.get('source', '')})
                n['records'] += 1
                self.stdout.write('  record  %s %s' % (r['sample_id'], r['parameter']))
            if not o['apply']:
                transaction.set_rollback(True)
        self.stdout.write('%s: requests %d, records %d, skipped %d' % ('APPLIED' if o['apply'] else 'DRY RUN (rolled back)', n['requests'], n['records'], n['skipped']))
