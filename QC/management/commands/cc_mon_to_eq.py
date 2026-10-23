"""Re-file a monitoring chart (MON) as a monthly equipment chart (EQ) - 23-10-2026.

    manage.py cc_mon_to_eq <chart id>            # dry run: report what would change
    manage.py cc_mon_to_eq <chart id> --apply

Background: the Lahore analytical-balance record (Weight 200 g, Mar-Sep 2026) was inducted on
10-10-2026 as a baseline-mode monitoring chart, three days before the "Monthly equipment chart
(IC baseline)" activity existed. Lahore (Sana Ashraf, 23-10-2026) asked for it under Monthly
Equipment Charts. The chart keeps its results, sign-offs and baseline versions; each result keeps
the baseline it was judged against; statuses are re-judged by the EQ rule (baseline +/- 2/3 SD);
baseline versions whose values match a run of the matching intermediate-check chart receive that
run's dates and a note naming the run, as a chart created from the IC run would have.
"""
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import Count

from QC.models import ControlChart, ControlChartBaseline


class Command(BaseCommand):
    help = 'Re-file a baseline-mode monitoring chart as a monthly equipment chart (dry run unless --apply).'

    def add_arguments(self, p):
        p.add_argument('chart', type=int)
        p.add_argument('--apply', action='store_true')

    def handle(self, *a, **o):
        from QC.views.control_chart import _ic_runs, _restatus_chart
        chart = ControlChart.objects.filter(pk=o['chart']).first()
        if chart is None:
            raise CommandError('chart %d not found' % o['chart'])
        if chart.activity != 'MON':
            raise CommandError('chart #%d is a %s chart, not a monitoring chart' % (chart.pk, chart.activity))
        if chart.mon_mode != 'baseline':
            raise CommandError('chart #%d is judged against %s; only baseline-mode monitoring charts can become equipment charts' % (
                chart.pk, 'fixed limits' if chart.mon_mode == 'fixed' else "the month's own readings"))
        ics = list(chart.ic_sources())
        if not ics:
            raise CommandError('no intermediate-check chart of %s / %s / %s %s exists - the equipment chart needs one for its baseline' % (
                chart.location, chart.equipment_id, chart.parameter, chart.level))
        if ControlChart.objects.filter(activity='EQ', location=chart.location, equipment_id__iexact=chart.equipment_id,
                                       parameter__iexact=chart.parameter, level__iexact=chart.level).exists():
            raise CommandError('a monthly equipment chart for this equipment / parameter / level already exists')
        runs = _ic_runs(chart)
        lines = ['Chart #%d %s - %s %s (%s %s): MON/baseline -> EQ' % (chart.pk, chart.location, chart.parameter, chart.level, chart.equipment, chart.equipment_id),
                 '  results %d, baseline versions %d, matching IC chart(s) %s' % (chart.results.count(), chart.baselines.count(), ', '.join('#%d' % c.pk for c in ics))]
        matched = {}
        for b in chart.baselines.order_by('version'):
            vals = [round(float(v), 10) for v in (b.values or [])]
            run = next((r for r in runs if [round(float(v), 10) for v in r['values']] == vals), None)
            if run is not None:
                matched[b.pk] = run
                lines.append('  baseline v%d (n=%d, est. %s) = IC run %s of #%d -> dates filled, note "Intermediate check %s ..."' % (
                    b.version, b.n, b.established_on, run['label'], run['ic'].pk, run['label']))
            else:
                lines.append('  baseline v%d (n=%d, est. %s): no matching IC run - kept as it is' % (b.version, b.n, b.established_on))
        unlinked = chart.results.filter(baseline__isnull=True).count()
        if unlinked:
            lines.append('  %d result(s) carry no baseline link - they will be judged against the current baseline' % unlinked)
        before = dict(chart.results.values_list('status').annotate(n=Count('id')))
        with transaction.atomic():
            chart.activity = 'EQ'
            chart.limit_mode = ''
            chart.save()
            for b in chart.baselines.all():
                run = matched.get(b.pk)
                if run is None:
                    continue
                if not b.dates:
                    b.dates = run['dates']
                extra = 'Intermediate check %s of the %s %s (%s %s; IC chart #%d) - ETAL-LAB-P-604' % (
                    run['label'], chart.equipment or 'equipment', chart.equipment_id or '', chart.parameter, chart.level, run['ic'].pk)
                old = (b.note or '').strip()
                b.note = (extra if not old else (old if old.startswith('Intermediate check') else '%s; %s' % (old, extra)))[:300].replace('  ', ' ')
                b.save()
            _restatus_chart(chart)
            after = dict(chart.results.values_list('status').annotate(n=Count('id')))
            lines.append('  statuses before %s, after %s' % (before, after))
            if not o['apply']:
                transaction.set_rollback(True)
        self.stdout.write('\n'.join(lines))
        self.stdout.write('APPLIED' if o['apply'] else 'DRY RUN (nothing changed)')
