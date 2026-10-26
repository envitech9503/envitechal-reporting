"""Audit-trailed corrections to statement-of-conformity records (QC Decision Rule module).

    python manage.py correct_soc_spec QC/fixtures/soc_karachi_corrections.json            # dry run
    python manage.py correct_soc_spec QC/fixtures/soc_karachi_corrections.json --apply

Each change is written to the record's remarks as "Correction dd-mm-yyyy: field old -> new (reason)" and to
legacy['corrections']; the history table keeps the previous version. The status (approved) and signatures stay;
the laboratory re-signs the corrected paper copy. Records the paper record lacks are added from the issued report.
A correction id already applied to a record is skipped, so the command can be run again safely.
"""
import json

from django.core.management.base import BaseCommand
from django.db import transaction

from QC.models import SocRecord, SocRequest
from QC.soc_rules import parse_result

_LABEL = {'uncertainty': 'Expanded uncertainty U', 'u_source': 'U source', 'method': 'Method', 'results': 'Results',
          'lower': 'Lower specification', 'upper': 'Upper specification', 'limit_text': 'Limit'}


def _show(field, v):
    if field == 'results':
        return ', '.join(SocRecord.result_text(r) for r in (v or [])) or '-'
    return '-' if v in (None, '') else str(v)


class Command(BaseCommand):
    help = 'Apply audit-trailed corrections to statement-of-conformity records'

    def add_arguments(self, p):
        p.add_argument('spec')
        p.add_argument('--apply', action='store_true')

    def handle(self, *a, **o):
        spec = json.load(open(o['spec'], encoding='utf8'))
        loc, cid, when, why = spec['location'], spec['id'], spec['date'], spec['authority']
        n = {'corrected': 0, 'added': 0, 'skipped': 0}
        with transaction.atomic():
            for c in spec.get('corrections', []):
                rec = SocRecord.objects.get(location=loc, sample_id=c['sample_id'], parameter__iexact=c['parameter'])
                lg = dict(rec.legacy or {})
                done = lg.get('corrections', [])
                if any(x.get('id') == cid for x in done):
                    n['skipped'] += 1; self.stdout.write('  skip    %s %s (already corrected)' % (rec.sample_id, rec.parameter)); continue
                changes = []
                for field, new in (c.get('set') or {}).items():
                    old = getattr(rec, field, None)
                    if field == 'results_text':                       # every result written as on the report, e.g. '<0.0080'
                        v, t = parse_result(new)
                        newres = [dict(r, value=v, **({'text': t} if t else {})) for r in (rec.results or [])]
                        old, field, new = rec.results, 'results', newres
                    if old != new:
                        changes.append('%s %s -> %s' % (_LABEL.get(field, field), _show(field, old), _show(field, new)))
                        setattr(rec, field, new)
                line = 'Correction %s: %s. %s' % (when, '; '.join(changes) if changes else 'no value changed', c['note'])
                rec.remarks = (rec.remarks + '\n' if rec.remarks else '') + line
                lg['corrections'] = done + [{'id': cid, 'date': when, 'authority': why, 'changes': changes, 'note': c['note']}]
                rec.legacy = lg
                rec._change_reason = ('%s: %s' % (cid, why))[:100]
                rec.save()
                n['corrected'] += 1
                self.stdout.write('  correct %s %s: %s' % (rec.sample_id, rec.parameter, '; '.join(changes) or 'note only'))
            for r in spec.get('add', []):
                if SocRecord.objects.filter(location=loc, sample_id=r['sample_id'], parameter__iexact=r['parameter']).exists():
                    n['skipped'] += 1; self.stdout.write('  skip    %s %s (exists)' % (r['sample_id'], r['parameter'])); continue
                req = SocRequest.objects.filter(location=loc, sample_id=r['sample_id']).first()
                sib = SocRecord.objects.filter(location=loc, sample_id=r['sample_id']).first()
                rec = SocRecord(location=loc, request=req, report_type=r['report_type'], sample_id=r['sample_id'],
                                customer=r.get('customer') or (sib.customer if sib else ''), parameter=r['parameter'], method=r['method'],
                                unit=r['unit'], standard=r.get('standard') or (sib.standard if sib else ''), limit_text=r['limit_text'],
                                lower=r.get('lower'), upper=r.get('upper'), uncertainty=r['uncertainty'], u_source=r['u_source'],
                                results=r['results'], decision_rule=r.get('decision_rule') or SocRecord.RULE, status='approved',
                                report_pk=sib.report_pk if sib else None, remarks=r['remarks'],
                                legacy={'inducted': when, 'file': r['file'], 'report_result': r.get('report_result', ''), 'sign_note': r.get('sign_note', ''),
                                        'corrections': [{'id': cid, 'date': when, 'authority': why, 'changes': ['record added'], 'note': r['remarks']}]})
                rec._change_reason = ('%s: added' % cid)[:100]
                rec.save()
                n['added'] += 1
                self.stdout.write('  add     %s %s' % (r['sample_id'], r['parameter']))
            if not o['apply']:
                transaction.set_rollback(True)
        self.stdout.write('%s: corrected %d, added %d, skipped %d' % ('APPLIED' if o['apply'] else 'DRY RUN (rolled back)', n['corrected'], n['added'], n['skipped']))
