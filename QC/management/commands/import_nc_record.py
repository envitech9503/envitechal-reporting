"""Complete inducted NC&CA records from the laboratory's signed forms and NC&CA logs (26-10-2026).

    manage.py import_nc_record QC/fixtures/nc_record_spec.json             # dry run (rolled back): prints every change
    manage.py import_nc_record QC/fixtures/nc_record_spec.json --apply

Follows the managers' complaint that inducted NC&CA forms were empty: the second batch of records holds the signed
NC&CA forms, RCAs and the Lahore NC&CA logs. For each form in the spec:
  * an inducted record with the same number (or the draft it was set up as, e.g. MNC-01/01-2025 -> NC-01/A1/2025) is
    completed from the form: every section of the form, the log fields, closure as per the record; it takes the form's
    number (the previous one is kept in legacy.previous_nc_no) and gets its RCAs if it has none;
  * otherwise a new inducted record is created.
Each change is listed in the record trail (legacy.completed, by "Record induction") and in the history. Records made
in the software (not inducted), records already completed or verified by a user, are never touched (reported).
Log rows without a form become log-only entries; log rows of existing records update only the log fields.
"""
import json
from datetime import date

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from QC.models import Ncca, NccaRca

FORM_FIELDS = ('date', 'department', 'raised_by', 'clause', 'source', 'due_audit_internal', 'due_audit_external', 'due_testing', 'due_cal_internal',
               'due_cal_external', 'due_complaint', 'due_other', 'category', 'category_also_critical', 'sig_legal', 'sig_risk', 'sig_halt', 'sig_preventive',
               'sig_non_significant', 'priority', 'risk_type', 'severity', 'impact_past', 'evaluated_date', 'details', 'proposed_date', 'root_cause', 'corrective',
               'completion_date', 'followup_with', 'satisfactory', 'followup_date', 'followup_desc', 'remarks', 'closed_by_name')
LOG_FIELDS = ('assigned_to', 'assigned_date', 'target_date', 'closing_date')
DATES = {'date', 'evaluated_date', 'proposed_date', 'completion_date', 'followup_date', 'assigned_date', 'target_date', 'closing_date'}
MAXLEN = {'department': 80, 'raised_by': 120, 'clause': 60, 'due_other': 120, 'followup_with': 120, 'remarks': 300, 'closed_by_name': 120, 'assigned_to': 120}


def _d(s):
    return date.fromisoformat(s) if s else None


def _v(k, v):
    if k in DATES:
        return _d(v)
    if isinstance(v, str):
        v = v.strip()
        return v[:MAXLEN[k]] if k in MAXLEN else v
    return v


class Command(BaseCommand):
    help = 'Complete / induct NC&CA records from the signed forms and NC&CA logs (spec).'

    def add_arguments(self, p):
        p.add_argument('spec')
        p.add_argument('--apply', action='store_true')

    def out(self, s):
        self.stdout.write(s)

    def _protected(self, n):
        lg = n.legacy or {}
        if not n.inducted:
            return 'made in the software (not inducted)'
        if lg.get('verified'):
            return 'already verified against the paper form'
        if any(t.get('by') != 'Record induction' for t in lg.get('completed', [])):
            return 'already completed by a user'
        return ''

    def _trail(self, n, changed, prev, src, built):
        n.legacy = dict(n.legacy or {})
        n.legacy.setdefault('completed', []).append({'by': 'Record induction', 'at': timezone.localtime().strftime('%d-%m-%Y %H:%M'), 'fields': changed,
                                                     'from_status': prev, 'to_status': n.status, 'source': src, 'spec': built})

    def _log_values(self, n, lf, notes):
        vals = {}
        for k in LOG_FIELDS:
            v = _v(k, lf.get(k))
            if v in (None, ''):
                continue
            if k in DATES and v and n.date and v < n.date:
                notes.append('NC&CA log %s %s is before the NC date and was not used (typing error on the log).' % (k.replace('_', ' '), v.strftime('%d-%m-%Y')))
                continue
            vals[k] = v
        return vals

    def handle(self, *a, **o):
        spec = json.load(open(o['spec'], encoding='utf8'))
        built = spec.get('built', '')
        c = {'completed': 0, 'created': 0, 'rcas': 0, 'log_only': 0, 'log_updated': 0, 'skipped': 0}
        with transaction.atomic():
            for x in spec['forms']:
                n = Ncca.objects.filter(location=x['location'], nc_no=x['nc_no']).first() or \
                    Ncca.objects.filter(location=x['location'], nc_no__in=x.get('match') or ['-']).first()
                notes = list(x.get('notes') or [])
                lf = x.get('log_fields') or {}
                if n:
                    why = self._protected(n)
                    if why:
                        c['skipped'] += 1; self.out('  SKIP %s (%s): %s' % (n.nc_no, x['nc_no'], why)); continue
                    prev, before = n.status, {f: getattr(n, f) for f in FORM_FIELDS + LOG_FIELDS + ('nc_no', 'log_only')}
                    before_legacy = json.loads(json.dumps(n.legacy or {}))
                    old_no = n.nc_no
                else:
                    n = Ncca(location=x['location'], nc_no=x['nc_no'], status='closed',
                             legacy={'key': 'rec:%s:%s' % (x['location'], x['nc_no']), 'inducted': built})
                    prev, before, old_no = None, None, None
                for f in FORM_FIELDS:
                    src = 'closed_by' if f == 'closed_by_name' else f
                    v = _v(f, x.get(src))
                    if f == 'closed_by_name' and not v:
                        v = (lf.get('log_closed_by') or '')[:120]
                    setattr(n, f, v if v is not None else ('' if f in ('details', 'root_cause', 'corrective', 'followup_desc', 'remarks', 'followup_with',
                                                                        'closed_by_name', 'due_other', 'department', 'raised_by', 'clause') else None))
                for k, v in self._log_values(n, lf, notes).items():
                    setattr(n, k, v)
                n.target_date = n.target_date or n.proposed_date
                n.assigned_date = n.assigned_date or n.evaluated_date
                n.closing_date = n.closing_date or n.followup_date or n.completion_date
                n.nc_no, n.log_only = x['nc_no'], False
                if n.closing_date and (n.closed_by_name or 'closed' in (n.remarks or '').lower()):
                    n.status = 'closed'
                lg = n.legacy = dict(n.legacy or {})
                if old_no and old_no != n.nc_no:
                    lg['previous_nc_no'] = old_no
                lg['form_file'] = x.get('file', '')
                lg['form_no'] = x.get('nc_no_form', '')
                if x.get('log'):
                    lg['log_row'] = x['log']
                kept = [s for s in (lg.get('notes') or []) if not s.startswith('Derived from the audit report findings')]   # superseded by the form
                lg['notes'] = kept + [s for s in notes if s not in kept]
                lg.pop('blank_on_form', None)
                blank = n.form_gaps                     # what is still empty now comes from the form itself
                if blank:
                    lg['blank_on_form'] = blank
                if before is None:
                    n.save(); c['created'] += 1
                    self.out('  NEW  %-18s %s %s, %s' % (n.nc_no, n.location, n.get_source_display(), n.get_status_display()))
                else:
                    changed = [f for f in before if getattr(n, f) != before[f]]
                    if n.status != prev:
                        changed.append('status')
                    if not changed and lg == before_legacy:
                        self.out('  SAME %-18s (already as on the form)' % n.nc_no)
                        continue
                    self._trail(n, changed, prev, 'signed NC&CA form' + (' and NC&CA log' if x.get('log') else ''), built)
                    n.save(); c['completed'] += 1
                    self.out('  FORM %-18s <- %-16s %s -> %s; %d fields' % (n.nc_no, old_no, prev, n.status, len(changed)))
                if not n.rcas.exists():
                    for r in x.get('rcas') or []:
                        NccaRca.objects.create(nc=n, part=r.get('part', ''), rca_no=r['rca_no'][:40], clause=(r['clause'] or n.clause.split(' (')[0])[:60],
                                               deputed=(r['deputed'] or '')[:120], date=_d(r['date']), causes=r['causes'], other=(r.get('other') or '')[:300],
                                               six_why=r['six_why'], statement=r['statement'], whys=r['whys'], conclusion=r['conclusion'],
                                               performed_name=(r['performed_by'] or '')[:120], performed_date=_d(r['performed_date']),
                                               reviewed_name=(r['reviewed_by'] or '')[:120], reviewed_date=_d(r['reviewed_date']), status='reviewed',
                                               legacy={'inducted': built})
                        c['rcas'] += 1
                elif x.get('rcas'):
                    self.out('       %s already has an RCA: the %d RCA form(s) of the record were not added' % (n.nc_no, len(x['rcas'])))
            for x in spec.get('log_only', []):
                if Ncca.objects.filter(location=x['location'], nc_no=x['nc_no']).exists():
                    c['skipped'] += 1; self.out('  SKIP log row %s (exists)' % x['nc_no']); continue
                lf = x['log_fields']
                n = Ncca(location=x['location'], nc_no=x['nc_no'], date=_d(x['date']), raised_by=(x['raised_by'] or '')[:120], clause=(x['clause'] or '')[:60],
                         source=x['source'], category=x['category'], log_only=True, status='closed', details=Ncca.LOG_ONLY_TEXT,
                         due_audit_external=x['source'] == 'EA', due_complaint=x['source'] == 'CC', due_testing=x['source'] == 'TEST',
                         closed_by_name=(lf.get('log_closed_by') or '')[:120],
                         legacy={'key': 'log:%s:%s' % (x['location'], x['nc_no']), 'log_row': x['log'], 'inducted': built,
                                 'notes': ['Category on the NC&CA log: "%s".' % x['log'].get('category', '')]})
                for k, v in self._log_values(n, lf, n.legacy['notes']).items():
                    setattr(n, k, v)
                if not n.closing_date:
                    n.status = 'open'
                n.save(); c['log_only'] += 1
                self.out('  LOG  %-18s %s (%s)' % (n.nc_no, n.get_category_display(), n.get_status_display()))
            for x in spec.get('log_updates', []):
                n = Ncca.objects.filter(location=x['location'], nc_no=x['nc_no']).first()
                if not n or self._protected(n):
                    self.out('  SKIP log update %s (%s)' % (x['nc_no'], 'missing' if not n else self._protected(n))); continue
                notes = []
                before_l = json.loads(json.dumps(n.legacy or {}))
                vals = self._log_values(n, x['log_fields'], notes)
                changed = [k for k, v in vals.items() if getattr(n, k) != v]
                for k, v in vals.items():
                    setattr(n, k, v)
                n.legacy = dict(n.legacy or {}); n.legacy['log_row'] = x['log']
                if not n.log_only and 'blank_on_form' not in n.legacy and n.form_gaps:
                    n.legacy['blank_on_form'] = n.form_gaps      # inducted from its signed form: what is empty was blank on the form
                n.legacy['notes'] = list(n.legacy.get('notes') or []) + [s for s in notes if s not in (n.legacy.get('notes') or [])]
                if changed:
                    self._trail(n, changed, n.status, 'NC&CA log', built)
                    n.save(); c['log_updated'] += 1
                elif n.legacy != before_l:
                    n.save()
                self.out('  LOGU %-18s %s' % (n.nc_no, ', '.join(changed) or 'no change'))
            if not o['apply']:
                transaction.set_rollback(True)
        self.out('%s: forms completed %d, created %d, RCAs %d, log-only rows %d, log updates %d, skipped %d'
                 % ('APPLIED' if o['apply'] else 'DRY RUN (rolled back)', c['completed'], c['created'], c['rcas'], c['log_only'], c['log_updated'], c['skipped']))
