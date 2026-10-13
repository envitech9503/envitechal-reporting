"""Reconcile a laboratory's control-chart records with its Excel workbooks.

    python manage.py import_cc_spec spec.json            # dry run: prints every change, rolls back
    python manage.py import_cc_spec spec.json --apply    # applies in one transaction

The specification (built from the workbooks) lists, per chart: how to find it (target id and/or
match fields), the master data, the baseline(s) and the results. Rules (owner decision 10-10-2026,
"workbooks win"):
  * master fields are set to the workbook values;
  * a workbook baseline equal to an existing version is reused, otherwise a new version is added;
  * a result already in the system for the same month (CRM) / date (IC, monitoring) is corrected to
    the workbook value with a traceable note; a missing result is added (unsigned: the analyst signs
    it with "Sign as performer");
  * results inside the periods the workbook covers that the workbook does not contain are removed
    (history keeps them); results outside those periods are kept unchanged;
  * statuses are recomputed; a review / approval of a period whose results changed is cleared;
  * listed duplicates are retired, empty duplicates deleted, unused seeded placeholders retired.
"""
import json
from collections import defaultdict
from datetime import date

from django.core.management.base import BaseCommand
from django.db import transaction

from QC.models import ControlChart, ControlChartBaseline, ControlChartResult, ControlChartSignoff


class _DryRun(Exception):
    pass


def _f(v, dec=6):
    return ('%.' + str(dec) + 'f') % v if isinstance(v, (int, float)) else str(v)


class Command(BaseCommand):
    help = 'Reconcile control charts with a workbook import specification (dry run unless --apply).'

    def add_arguments(self, parser):
        parser.add_argument('spec')
        parser.add_argument('--apply', action='store_true')
        parser.add_argument('--ignore-ids', action='store_true', help='find charts by match fields only (rehearsal copies)')
        parser.add_argument('--id-offset', type=int, default=0, help='rehearsal: target ids are shifted by this offset')

    def handle(self, *args, **o):
        spec = json.load(open(o['spec']))
        self.loc = spec['location']
        self.ignore_ids = o['ignore_ids']
        self.id_offset = o['id_offset']
        self.today = date.today().strftime('%d-%m-%Y')
        self.lines = []
        self.stats = defaultdict(int)
        try:
            with transaction.atomic():
                self.run(spec)
                if not o['apply']:
                    raise _DryRun()
        except _DryRun:
            self.lines.append('DRY RUN - nothing was saved.')
        for line in self.lines:
            self.stdout.write(line)
        self.stdout.write('SUMMARY ' + ', '.join('%s=%d' % kv for kv in sorted(self.stats.items())))

    # ------------------------------------------------------------------ helpers
    def log(self, *a):
        self.lines.append(' '.join(str(x) for x in a))

    def find(self, item, required=False):
        qs = ControlChart.objects.filter(location=self.loc)
        tid = item.get('target_id', item.get('id'))
        if tid and self.id_offset:
            tid += self.id_offset
        m = dict(item.get('match') or {})
        if tid and not self.ignore_ids:
            c = qs.filter(pk=tid).first()
            if c is None:
                raise ValueError('chart #%s not found' % tid)
            for k, v in m.items():
                if str(getattr(c, k)).strip().lower() != str(v).strip().lower():
                    raise ValueError('chart #%s: %s is %r, expected %r - stopping' % (tid, k, getattr(c, k), v))
            return c
        if not m:
            return None
        flt = {}
        for k, v in m.items():
            flt[k + '__iexact' if isinstance(v, str) else k] = v
        cands = list(qs.filter(**flt).order_by('id'))
        if tid is not None and len(cands) > 1:
            cands = [c for c in cands if c.created_by_id] or cands
        if len(cands) > 1:
            raise ValueError('%s: %d charts match %s - stopping' % (item.get('key', tid), len(cands), m))
        return cands[0] if cands else None

    @staticmethod
    def same_values(a, b):
        return len(a) == len(b) and all(abs(float(x) - float(y)) < 1e-9 for x, y in zip(a, b))

    # ------------------------------------------------------------------ main
    def run(self, spec):
        targeted = set()
        charts = []
        for item in spec['charts']:
            c = self.find(item)
            charts.append((item, c))
            if c:
                targeted.add(c.pk)
        # duplicates first, so the matching of the kept chart is unambiguous afterwards
        for item in spec.get('retire', []):
            c = self.find(item)
            if c and c.active:
                c.active = False
                c.save()
                self.stats['charts_retired'] += 1
                self.log('RETIRE #%d %s %s [%s] (%d results kept in archive) - %s' % (c.pk, c.activity, c.title, c.equipment_id, c.results.count(), item.get('reason', '')))
        for item in spec.get('delete_empty', []):
            c = self.find(item)
            if c:
                if c.results.exists():
                    self.log('KEEP #%d %s %s - not empty, retired instead' % (c.pk, c.activity, c.title))
                    c.active = False
                    c.save()
                    self.stats['charts_retired'] += 1
                else:
                    self.log('DELETE #%d %s %s [%s] (no results) - %s' % (c.pk, c.activity, c.title, c.equipment_id, item.get('reason', '')))
                    c.delete()
                    self.stats['charts_deleted'] += 1
        if spec.get('retire_placeholders'):
            n = 0
            for c in ControlChart.objects.filter(location=self.loc, created_by=None, active=True).exclude(pk__in=targeted):
                if not c.results.exists():
                    c.active = False
                    c.save()
                    n += 1
            self.stats['placeholders_retired'] = n
            self.log('RETIRE %d unused seeded placeholder charts (no results) of %s' % (n, self.loc))
        for item, c in charts:
            self.chart(item, c)
        for d in spec.get('doc_control', []):
            from EnviTechAlApp.models import InventoryDocControl
            obj, _ = InventoryDocControl.objects.get_or_create(module=d['module'], location=d['location'])
            if not (obj.doc_no or '').strip():
                obj.doc_no = d['doc_no']
                obj.save()
                self.log('DOC-CONTROL %s %s set to %s' % (d['location'], d['module'], d['doc_no']))
            else:
                self.log('DOC-CONTROL %s %s already %s - unchanged' % (d['location'], d['module'], obj.doc_no))

    def chart(self, item, c):
        from QC.views.control_chart import _restatus_run, _restatus_chart, _qs_period, _plabel
        m = item['master']
        created = False
        if c is None:
            c = ControlChart(location=self.loc, activity=item['activity'], created_by=None)
            created = True
        changes = []
        for k, v in m.items():
            old = getattr(c, k)
            if str(old if old is not None else '') != str(v):
                changes.append('%s: %r -> %r' % (k, old, v))
                setattr(c, k, v)
        if not c.active:
            c.active = True
            changes.append('active: False -> True')
        c.save()
        self.stats['charts_created' if created else 'charts_updated' if changes else 'charts_unchanged'] += 1
        self.log('\n== %s #%d %s %s [%s]%s' % ('NEW' if created else 'CHART', c.pk, c.activity, c.title, c.equipment_id, ' (%s)' % item['key']))
        for ch in ([] if created else changes):
            self.log('   master ' + ch)

        # ---- baselines
        bmap = {}
        existing = list(c.baselines.all().order_by('version'))
        for b in sorted(item.get('baselines', []), key=lambda x: x['established_on']):
            if b.get('stats_only'):
                hit = next((x for x in existing if x.stats_only and x.mean is not None and abs(x.mean - b['mean']) < 1e-9
                            and abs((x.sd or 0) - b['sd']) < 1e-9), None)
            else:
                hit = next((x for x in existing if self.same_values(x.values, b['values'])), None)
            est = date.fromisoformat(b['established_on'])
            if b.get('replace_version'):
                # owner decision 13-10-2026 ("correct in place"): the version is the same baseline period, its values
                # are corrected to the laboratory's baseline-study record; the previous values stay in the history
                tgt = next((x for x in existing if x.version == b['replace_version']), None)
                if tgt is None:
                    raise ValueError('%s: baseline v%s not found' % (item.get('key'), b['replace_version']))
                newv = [float(v) for v in b['values']]
                upd = []
                if not self.same_values(tgt.values or [], newv):
                    upd.append('values (was n=%d mean %s SD %s)' % (len(tgt.values or []), _f(tgt.mean, c.decimals + 2), _f(tgt.sd, c.decimals + 3)))
                    old_note = 'Corrected %s to the baseline-study record (was mean %s, SD %s).' % (
                        self.today, _f(tgt.mean, c.decimals + 2), _f(tgt.sd, c.decimals + 3))
                    tgt.values = newv
                    tgt.note = ((b.get('note') or tgt.note or '') + ' ' + old_note).strip()[:300]
                elif b.get('note') and tgt.note != b['note'][:300]:
                    tgt.note = b['note'][:300]
                    upd.append('note')
                if list(tgt.dates or []) != list(b.get('dates') or []):
                    tgt.dates = b.get('dates') or []
                    upd.append('dates')
                if tgt.established_on != est:
                    upd.append('established_on %s -> %s' % (tgt.established_on, est))
                    tgt.established_on = est
                for fk in ('range_low', 'range_high'):
                    if fk in b and (getattr(tgt, fk) or '') != (b[fk] or ''):
                        upd.append('%s %r -> %r' % (fk, getattr(tgt, fk), b[fk]))
                        setattr(tgt, fk, b[fk] or '')
                tgt.stats_only = False
                tgt.compute()
                tgt.save()
                bmap[b['key']] = tgt
                self.stats['baselines_corrected' if upd else 'baselines_unchanged'] += 1
                self.log('   baseline v%d %s%s -> n=%d mean %s SD %s' % (tgt.version, 'CORRECTED ' if upd else 'unchanged',
                         ', '.join(upd), tgt.n, _f(tgt.mean, c.decimals + 2), _f(tgt.sd, c.decimals + 3)))
                continue
            if hit:
                upd = []
                if b.get('dates') and list(hit.dates or []) != b['dates']:
                    hit.dates = b['dates']
                    upd.append('dates')
                for fk in ('range_low', 'range_high'):
                    if fk in b and (getattr(hit, fk) or '') != (b[fk] or ''):
                        upd.append('%s %r -> %r' % (fk, getattr(hit, fk), b[fk]))
                        setattr(hit, fk, b[fk] or '')
                if (c.mon_mode == 'baseline' or b.get('set_established')) and hit.established_on != est:
                    upd.append('established_on %s -> %s' % (hit.established_on, est))
                    hit.established_on = est
                if b.get('note') and not hit.note:
                    hit.note = b['note'][:300]
                    upd.append('note')
                if upd:
                    hit.save()
                bmap[b['key']] = hit
                self.log('   baseline v%d reused (values identical)%s' % (hit.version, (' - ' + ', '.join(upd)) if upd else ''))
            else:
                ver = (max([x.version for x in existing]) if existing else 0) + 1
                nb = ControlChartBaseline(chart=c, version=ver, established_on=est, note=b.get('note', '')[:300],
                                          values=[float(v) for v in b.get('values', [])], dates=b.get('dates', []),
                                          range_low=b.get('range_low', ''), range_high=b.get('range_high', ''),
                                          stats_only=bool(b.get('stats_only')), n_points=b.get('n'),
                                          mean=b.get('mean'), sd=b.get('sd'), is_current=False, created_by=None)
                nb.compute()
                nb.save()
                existing.append(nb)
                bmap[b['key']] = nb
                self.stats['baselines_added'] += 1
                self.log('   baseline v%d ADDED (%s, n=%d, mean %s, SD %s)' % (ver, b['established_on'], nb.n, _f(nb.mean, c.decimals + 1), _f(nb.sd, c.decimals + 2)))
        if existing and not item.get('keep_current'):
            latest = max(existing, key=lambda x: (x.established_on or date.min, x.version)) if c.mon_mode == 'baseline' else \
                (bmap[item['baselines'][-1]['key']] if item.get('baselines') else max(existing, key=lambda x: x.version))
            for x in existing:
                want = x.pk == latest.pk
                if x.is_current != want:
                    ControlChartBaseline.objects.filter(pk=x.pk).update(is_current=want)

        # ---- results
        monthly = c.cadence == 'monthly'
        sys_res = list(c.results.all().order_by('date', 'time', 'id'))
        used = set()
        touched = set()
        for r in item['results']:
            d = date.fromisoformat(r['date'])
            if monthly:
                hit = next((x for x in sys_res if x.pk not in used and (x.date.year, x.date.month) == (d.year, d.month)), None)
            else:
                hit = next((x for x in sys_res if x.pk not in used and x.date == d), None)
            if c.no_baseline:
                base = None
            elif r.get('baseline'):
                base = bmap[r['baseline']]
            elif c.mon_mode == 'baseline':
                base = c.baseline_for(d)          # None before the first baseline: acceptance range only
            else:
                base = c.current_baseline()
            val = float(r['value'])
            if hit:
                used.add(hit.pk)
                diffs = []
                if hit.date != d:
                    diffs.append('date')
                if abs(hit.value - val) > 1e-9:
                    diffs.append('value')
                if (hit.time or '') and c.spec_limited:
                    diffs.append('time')
                if diffs:
                    note = '[Corrected %s from the laboratory workbook: was %s on %s%s]' % (
                        self.today, _f(hit.value, max(c.decimals, 0) + 2).rstrip('0').rstrip('.'), hit.date.strftime('%d-%m-%Y'),
                        (' ' + hit.time) if hit.time else '')
                    self.log('   CORRECT %s %s -> %s %s (%s)' % (hit.date, _f(hit.value, 6).rstrip('0').rstrip('.'), d, _f(val, 6).rstrip('0').rstrip('.'), '/'.join(diffs)))
                    touched.update({_qs_period(c, hit.date), _qs_period(c, d)})
                    hit.date, hit.value = d, val
                    hit.time = ''
                    hit.remark = (((hit.remark or '').strip() + ' ') + note).strip()
                    self.stats['results_corrected'] += 1
                else:
                    self.stats['results_identical'] += 1
                if r.get('r1') is not None and hit.reading_1 is None:
                    hit.reading_1, hit.reading_2 = r['r1'], r['r2']
                hit.baseline = base
                hit.save()
            else:
                ControlChartResult.objects.create(chart=c, baseline=base, date=d, time='', value=val, status='ok',
                                                  reading_1=r.get('r1'), reading_2=r.get('r2'), remark='', performed_by=None)
                touched.add(_qs_period(c, d))
                self.stats['results_added'] += 1
        added = sum(1 for r in item['results']) - len(used)
        if added:
            self.log('   ADD %d result(s) from the workbook (unsigned - to be signed with "Sign as performer")' % added)
        # results inside the covered periods that the workbook does not contain
        cover = set()
        if item.get('coverage'):
            a, b = date.fromisoformat(item['coverage'][0]), date.fromisoformat(item['coverage'][1])
            y, mth = a.year, a.month
            while (y, mth) <= (b.year, b.month):
                cover.add('%04d-%02d' % (y, mth))
                y, mth = (y + 1, 1) if mth == 12 else (y, mth + 1)
        cover |= set(item.get('coverage_months') or [])
        for x in sys_res:
            if x.pk in used:
                continue
            if x.date.strftime('%Y-%m') in cover:
                self.log('   REMOVE %s%s %s (not in the workbook for a period it covers; entered by %s)' % (
                    x.date, (' ' + x.time) if x.time else '', _f(x.value, 6).rstrip('0').rstrip('.'), getattr(x.performed_by, 'username', 'import')))
                touched.add(_qs_period(c, x.date))
                x.delete()
                self.stats['results_removed'] += 1
            else:
                self.stats['results_kept_outside_workbook'] += 1
                self.log('   keep %s %s (after the workbook period)' % (x.date, _f(x.value, 6).rstrip('0').rstrip('.')))

        # ---- statuses
        if c.self_limited:
            for y, mth in {(r.date.year, r.date.month) for r in c.results.all()}:
                _restatus_run(c, y, mth)
        elif c.spec_limited:
            _restatus_chart(c)
        else:
            for r in c.results.select_related('baseline'):
                b = r.baseline or c.current_baseline()
                st = c.classify(b.limits() if b else None, r.value)
                if st != r.status:
                    ControlChartResult.objects.filter(pk=r.pk).update(status=st)
        n_bad = c.results.exclude(status='ok').count()
        n_norem = c.results.exclude(status='ok').filter(remark='').count()
        if n_bad:
            self.log('   status: %d result(s) warning / out of control, %d without remark' % (n_bad, n_norem))
            self.stats['results_need_remark'] += n_norem

        # ---- sign-offs of changed periods
        for (y, mth) in touched:
            so = ControlChartSignoff.objects.filter(chart=c, year=y, month=mth).first()
            if so and (so.reviewed_at or so.approved_at):
                self.log('   sign-off of %s cleared (results changed): reviewed by %s' % (_plabel(c, y, mth), getattr(so.reviewed_by, 'username', '-')))
                so.reviewed_by = so.approved_by = None
                so.reviewed_at = so.approved_at = None
                so.save()
                self.stats['signoffs_cleared'] += 1
        self.log('   now %d results' % c.results.count())
