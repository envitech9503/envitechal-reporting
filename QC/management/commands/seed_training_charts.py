"""Training / reference control charts (owner instruction 11-10-2026).

    manage.py seed_training_charts <spec.json> [--analysts u1,u2] [--reviewer u] [--approver u] [--by u] [--dry-run]

Creates fully worked duplicate (RPD) and spike-recovery charts for one laboratory: a dated 20-point
baseline, per-batch results with sample IDs and raw working (Result A / B; unspiked / spiked / added),
a remark and corrective action on every warning / out-of-control point, the analyst on every result and
the review (Lab Manager) and approval (CEO) of the record period. The charts are flagged is_training:
every printed form is watermarked TRAINING RECORD and the Lab Manager / CEO may delete them although approved.

Earlier training charts named in "replace" are deleted first, with a copy in the deletion log.
The whole run is one transaction; every computed value and status is checked against the spec.
"""
import json
from datetime import date, datetime, time

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from QC.models import ControlChart, ControlChartBaseline, ControlChartResult, ControlChartSignoff, ControlChartReviewer


class _Rollback(Exception):
    pass


class Command(BaseCommand):
    help = 'Create the training / reference duplicate and spike-recovery charts of one laboratory.'

    def add_arguments(self, p):
        p.add_argument('spec')
        p.add_argument('--analysts', default='', help='comma-separated usernames (default: Analyst signatures of the laboratory)')
        p.add_argument('--reviewer', default='', help='Lab / QC Manager username (default: the laboratory reviewer)')
        p.add_argument('--approver', default='', help='CEO / administrator username (default: ImranKazmi)')
        p.add_argument('--by', default='', help='username recorded as having deleted replaced charts (default: approver)')
        p.add_argument('--dry-run', action='store_true')

    # ------------------------------------------------------------------ users
    def users(self, loc, o):
        from EnviTechAlApp.models import Signatures
        if o['analysts']:
            analysts = [User.objects.get(username=u.strip()) for u in o['analysts'].split(',') if u.strip()]
        else:
            sigs = Signatures.objects.select_related('user', 'role').filter(user__is_active=True)
            analysts = [s.user for s in sigs if (s.office or '').strip().title() == loc and s.role and 'analyst' in str(s.role).lower()
                        and s.signature]
            analysts.sort(key=lambda u: u.username.lower())
        if not analysts:
            raise CommandError('No analyst found for %s - pass --analysts.' % loc)
        if o['reviewer']:
            reviewer = User.objects.get(username=o['reviewer'])
        else:
            rv = ControlChartReviewer.objects.filter(location=loc).select_related('user').order_by('user__username').first()
            if not rv:
                raise CommandError('No reviewer assigned to %s - pass --reviewer.' % loc)
            reviewer = rv.user
        approver = User.objects.get(username=o['approver'] or 'ImranKazmi')
        by = User.objects.get(username=o['by']) if o['by'] else approver
        return analysts, reviewer, approver, by

    @staticmethod
    def _name(u):
        return '%s (%s)' % (u.username, (u.get_full_name() or '-').strip())

    @staticmethod
    def _aware(d, hh, mm):
        return timezone.make_aware(datetime.combine(d, time(hh, mm)))

    # ------------------------------------------------------------------ main
    def handle(self, *a, **o):
        spec = json.load(open(o['spec']))
        loc = spec['location']
        analysts, reviewer, approver, by = self.users(loc, o)
        self.stdout.write('%s: analysts %s; reviewer %s; approver %s' % (
            loc, ', '.join(self._name(u) for u in analysts), self._name(reviewer), self._name(approver)))
        try:
            with transaction.atomic():
                self.run(spec, loc, analysts, reviewer, approver, by)
                if o['dry_run']:
                    raise _Rollback()
        except _Rollback:
            self.stdout.write('DRY RUN - rolled back.')
            return
        self.stdout.write('Committed.')

    def run(self, spec, loc, analysts, reviewer, approver, by):
        from QC.views.control_chart import _log_deletion, _snap_chart, _snap_result, _snap_baseline, _plabel, _qs_period
        for rp in spec.get('replace', []):
            for c in ControlChart.objects.filter(location=loc, activity=rp['activity'], equipment_id=rp['equipment_id']):
                if not (c.is_training or c.parameter.upper().startswith('TRAINING')):
                    raise CommandError('Refusing to replace #%d: it is not a training chart.' % c.pk)
                n = c.results.count()
                _log_deletion(by, 'chart', c, '%s %s [%s] - %s %s' % (c.parameter, c.level, c.equipment_id or '-', c.location, c.activity),
                              rp.get('reason', 'Replaced by the revised training chart'),
                              {'chart': _snap_chart(c), 'results': [_snap_result(r) for r in c.results.select_related('baseline', 'performed_by')],
                               'baselines': [_snap_baseline(b) for b in c.baselines.all()], 'signoffs': []})
                self.stdout.write('REPLACE: deleted #%d %s (%d results; copy in the deletion log)' % (c.pk, c.title, n))
                c.delete()

        for ci, item in enumerate(spec['charts']):
            m = item['master']
            if ControlChart.objects.filter(location=loc, activity=item['activity'], parameter__iexact=m['parameter'],
                                           level__iexact=m.get('level', ''), equipment_id__iexact=m['equipment_id']).exists():
                raise CommandError('Chart already exists: %s [%s]' % (m['parameter'], m['equipment_id']))
            c = ControlChart(location=loc, activity=item['activity'], is_training=True, created_by=by, **m)
            c.save()
            bs = item['baseline']
            b = ControlChartBaseline(chart=c, version=1, established_on=date.fromisoformat(bs['established_on']),
                                     note=bs['note'][:300], values=[float(v) for v in bs['values']], dates=bs['dates'],
                                     is_current=True, created_by=analysts[ci % len(analysts)])   # the analyst who ran the baseline batches
            b.compute()
            b.save()
            lim = b.limits()
            self.stdout.write('\n== NEW #%d %s %s [%s]: baseline n=%d mean %.4f SD %.4f  UWL %.3f UL %.3f%s' % (
                c.pk, c.activity, c.title, c.equipment_id, b.n, b.mean, b.sd, lim['uwl'], lim['ul'],
                '' if c.upper_only else '  LWL %.3f LL %.3f' % (lim['lwl'], lim['ll'])))
            tally = {'ok': 0, 'warning': 0, 'ooc': 0}
            for i, r in enumerate(item['results']):
                d = date.fromisoformat(r['date'])
                cv = c.raw_value(r.get('a'), r.get('b'), r.get('c'))
                if cv is None:
                    raise CommandError('%s %s: incomplete raw working' % (c.title, r['date']))
                val = round(cv, c.decimals)
                if 'value' in r and abs(r['value'] - val) > 1e-9:
                    raise CommandError('%s %s: spec value %s but raw working gives %s' % (c.title, r['date'], r['value'], val))
                st = c.classify(lim, val, b)
                if r.get('expect') and r['expect'] != st:
                    raise CommandError('%s %s: expected %s, judged %s (value %s)' % (c.title, r['date'], r['expect'], st, val))
                if st != 'ok' and not r.get('remark'):
                    raise CommandError('%s %s: %s without a remark' % (c.title, r['date'], st))
                # one analyst per chart, so that the Performed-by panel carries that analyst's signature
                who = analysts[(r['analyst'] if 'analyst' in r else ci) % len(analysts)]
                x = ControlChartResult.objects.create(chart=c, baseline=b, date=d, time='', value=val, status=st,
                                                      sample_id=r['sample_id'], raw_a=r.get('a'), raw_b=r.get('b'), raw_c=r.get('c'),
                                                      remark=r.get('remark', ''), performed_by=who)
                ControlChartResult.objects.filter(pk=x.pk).update(performed_at=self._aware(d, 16, 30))
                tally[st] += 1
            self.stdout.write('   %d results: %d in control, %d warning, %d out of control - all flagged points carry a remark' % (
                len(item['results']), tally['ok'], tally['warning'], tally['ooc']))
            for so in item.get('signoffs', []):
                rv, ap = date.fromisoformat(so['reviewed_on']), date.fromisoformat(so['approved_on'])
                ControlChartSignoff.objects.create(chart=c, year=so['year'], month=so.get('month', 0),
                                                   reviewed_by=reviewer, reviewed_at=self._aware(rv, 11, 15),
                                                   approved_by=approver, approved_at=self._aware(ap, 12, 40))
                self.stdout.write('   %s: performed by %s; reviewed %s by %s; approved %s by %s' % (
                    _plabel(c, so['year'], so.get('month', 0)), ', '.join(sorted({x.performed_by.username for x in c.results.all()})),
                    rv.strftime('%d-%m-%Y'), reviewer.username, ap.strftime('%d-%m-%Y'), approver.username))
            # every result must fall into a signed period
            periods = {_qs_period(c, r.date) for r in c.results.all()}
            signed = {(s.year, s.month) for s in c.signoffs.all()}
            if periods - signed:
                raise CommandError('%s: periods without sign-off: %s' % (c.title, sorted(periods - signed)))
