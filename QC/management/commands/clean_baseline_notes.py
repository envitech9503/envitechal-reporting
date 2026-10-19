"""Remove the record-receipt date from baseline notes (Karachi Lab Manager, 19-10-2026, item 2).

    manage.py clean_baseline_notes            # dry run: lists every change
    manage.py clean_baseline_notes --apply    # saves (each change is kept in the baseline history)

"Baseline study - working standard exercise Feb-2026 (laboratory record received 13-10-2026)"
becomes "Baseline study - working standard exercise Feb-2026". Baseline drafts are cleaned too.
"""
import re

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q

from QC.models import ControlChartBaseline, ControlChartBaselineDraft

_RX = re.compile(r'\s*[(;,]?\s*(?:the\s+)?laboratory record received \d{2}-\d{2}-\d{4}\)?', re.I)


def clean(note):
    out = re.sub(r'\s{2,}', ' ', _RX.sub('', note or '')).strip()
    # "... Feb-2026 Corrected 13-10-2026 ..." -> "... Feb-2026. Corrected 13-10-2026 ..." (two sentences)
    return re.sub(r'(?<=[\w)])\s+(Corrected \d{2}-\d{2}-\d{4})', r'. \1', out)


class Command(BaseCommand):
    help = 'Remove "laboratory record received dd-mm-yyyy" from baseline notes (dry run unless --apply).'

    def add_arguments(self, p):
        p.add_argument('--apply', action='store_true')

    def handle(self, *a, **o):
        n = 0
        with transaction.atomic():
            for model in (ControlChartBaseline, ControlChartBaselineDraft):
                for b in model.objects.filter(Q(note__icontains='laboratory record received') | Q(note__contains=' Corrected ')).select_related('chart'):
                    new = clean(b.note)
                    if new == b.note:
                        continue
                    n += 1
                    self.stdout.write('%s #%d %s %s [%s] v%s:\n   - %s\n   + %s' % (
                        model.__name__, b.pk, b.chart.location, b.chart.title, b.chart.equipment_id or '-',
                        getattr(b, 'version', 'draft'), b.note, new))
                    if o['apply']:
                        b.note = new
                        b.save(update_fields=['note']) if model is ControlChartBaselineDraft else b.save()
            if not o['apply']:
                transaction.set_rollback(True)
        self.stdout.write('%s: %d note(s) %s.' % ('APPLIED' if o['apply'] else 'DRY RUN', n, 'cleaned' if o['apply'] else 'to clean'))
