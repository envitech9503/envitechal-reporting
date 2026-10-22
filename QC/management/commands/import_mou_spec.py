"""Induct a laboratory's Measurement-of-Uncertainty record from a spec file. 21-10-2026.

    manage.py import_mou_spec QC/fixtures/mou_karachi_spec.json            # dry run
    manage.py import_mou_spec QC/fixtures/mou_karachi_spec.json --apply    # create

The spec (built from the laboratory's Excel workbooks, form ETAL-LAB-706-FF-01) holds the
source library and, per study, the replicates verbatim, the effective budget rows, the figures
the workbook printed (legacy) and the discrepancy notes. Owner decision 21-10-2026: studies
are recomputed correctly, the printed figures are kept beside them, complete studies are
inducted as 'submitted for review' for the Lab Manager's re-approval and incomplete ones as
drafts. Idempotent: a study already inducted from the same workbook file is skipped.
"""
import datetime as _dt
import json
import os

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from QC.models import MouSource, MouStudy, MouOperator, MouComponent
from QC import mou_calc


class Command(BaseCommand):
    help = 'Induct MOU studies and the source library from a spec JSON (dry run unless --apply).'

    def add_arguments(self, p):
        p.add_argument('spec')
        p.add_argument('--apply', action='store_true')
        p.add_argument('--user', default='', help='username recorded as creator (optional)')

    def handle(self, *a, **o):
        if not os.path.exists(o['spec']):
            raise CommandError('spec not found: %s' % o['spec'])
        with open(o['spec'], encoding='utf-8') as fh:
            spec = json.load(fh)
        loc = spec['location']
        user = None
        if o['user']:
            from django.contrib.auth.models import User
            user = User.objects.filter(username=o['user']).first()
        inducted = spec.get('built', '')
        n_src = n_new = n_skip = 0
        src_map = {}
        with transaction.atomic():
            for s in spec['sources']:
                obj = MouSource.objects.filter(location=loc, name=s['name'], unit=s['unit'] or '', range_value=float(s['range']), magnitude=s['magnitude']).first()
                if obj is None:
                    obj = MouSource(location=loc, category=s['category'], name=s['name'], unit=s['unit'] or '', range_value=float(s['range']),
                                    magnitude=s['magnitude'], dist=s['dist'], ci=float(s.get('ci') or 1), created_by=user,
                                    note='Seeded from the laboratory workbooks (%s)' % inducted)
                    obj.save()
                    n_src += 1
                src_map[s['key']] = obj
            for st in sorted(spec['studies'], key=lambda x: int(x.get('version') or 1)):
                if MouStudy.objects.filter(location=loc, legacy__file=st['file']).exists():
                    n_skip += 1
                    continue
                legacy = dict(st['legacy'])
                legacy['notes'] = st['notes']
                legacy['inducted'] = inducted
                legacy['unit_printed'] = st.get('unit_printed', '')
                obj = MouStudy(location=loc, parameter=st['parameter'], level=st['level'], unit=st['unit'], sample_kind=st['sample_kind'],
                               sample_ref=st['sample_ref'][:200], method=st['method'], instrument=st['instrument'], range_value=st['range'],
                               env_temp=st.get('env_temp'), study_date=(_dt.date.fromisoformat(st['study_date']) if st.get('study_date') else None), k=2.0, decimals=3, status='review' if st['complete'] else 'draft', version=int(st.get('version') or 1),
                               legacy=legacy, created_by=user, submitted_by=user if st['complete'] else None,
                               remarks='Inducted from the laboratory workbook %s on %s.' % (st['file'].split('/')[-1], inducted))
                if st['complete']:
                    from django.utils import timezone
                    obj.submitted_at = timezone.now()
                if obj.version > 1:
                    obj.supersedes = MouStudy.objects.filter(location=loc, parameter__iexact=obj.parameter, level__iexact=obj.level, sample_kind=obj.sample_kind,
                                                            version__lt=obj.version).order_by('-version').first()
                obj.save()
                for i, op in enumerate(st['operators']):
                    MouOperator.objects.create(study=obj, order=i, label=op['label'], values=op['values'])
                for i, c in enumerate(st['components']):
                    MouComponent.objects.create(study=obj, order=i, kind=c['kind'], source=src_map.get(c.get('source_key')), name=c['name'],
                                                unit=c['unit'] if c['kind'] == 'b' else st['unit'], range_value=c['range'] if c['kind'] == 'b' else None,
                                                magnitude=c.get('magnitude') or '', dist=c['dist'], ci=float(c.get('ci') or 1),
                                                included=True, note=c.get('note') or '')
                r = obj.recompute()
                n_new += 1
                self.stdout.write('%s %s [%s] -> uc %s U %s Uabs %s U%% %s | printed U %s | notes %d%s' % (
                    st['parameter'], st['level'], st['sample_kind'], mou_calc.fmt_sig(r['uc']), mou_calc.fmt_sig(r['U']), mou_calc.fmt_sig(r['U_abs']),
                    mou_calc.fmt_sig(r['U_pct']), mou_calc.fmt_sig(legacy.get('U')), len(st['notes']), ('  ERRORS: ' + ' '.join(r['errors'])) if r['errors'] else ''))
            if not o['apply']:
                transaction.set_rollback(True)
        self.stdout.write('%s: %d library entries added, %d studies inducted, %d already present.' % (
            'APPLIED' if o['apply'] else 'DRY RUN', n_src, n_new, n_skip))
