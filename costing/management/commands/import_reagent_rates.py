"""Import reagent purchase rates into the costing ReagentRate table from a CSV.

CSV columns (header required): name, location, unit_cost   [optional: source]
- name       : chemical name (matched to the host Chemical by exact name, else contains)
- location   : Karachi / Lahore / blank (blank = all labs)
- unit_cost  : PKR per base unit
- source     : optional note (defaults to the CSV filename)

Usage:  python manage.py import_reagent_rates reagent_rates.csv
Re-running updates existing (chemical, location) rates rather than duplicating.
"""
import csv
import os
from decimal import Decimal, InvalidOperation
from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from costing.models import ReagentRate


class Command(BaseCommand):
    help = 'Import reagent purchase rates from a CSV into the costing rate table.'

    def add_arguments(self, parser):
        parser.add_argument('csv_path')
        parser.add_argument('--dry-run', action='store_true', help='Report matches without writing.')

    def handle(self, *args, **opts):
        path = opts['csv_path']
        if not os.path.exists(path):
            raise CommandError(f'CSV not found: {path}')
        Chemical = apps.get_model(getattr(settings, 'COSTING_CHEMICAL_MODEL', 'dashboard.Chemical'))
        by_name = {}
        for c in Chemical.objects.all():
            by_name.setdefault(c.name.strip().lower(), c)
        names_lower = list(by_name.keys())

        def match(name):
            key = (name or '').strip().lower()
            if key in by_name:
                return by_name[key]
            for k in names_lower:
                if key and key in k:
                    return by_name[k]
            return None

        created = updated = unmatched = skipped = 0
        default_source = os.path.basename(path)
        with open(path, newline='', encoding='utf-8-sig') as fh:
            for row in csv.DictReader(fh):
                name = row.get('name') or row.get('Name')
                raw = (row.get('unit_cost') or row.get('rate') or '').strip()
                if not name or not raw:
                    skipped += 1
                    continue
                try:
                    cost = Decimal(raw)
                except (InvalidOperation, ValueError):
                    skipped += 1
                    continue
                chem = match(name)
                if not chem:
                    unmatched += 1
                    self.stdout.write(self.style.WARNING(f'  no chemical match: {name}'))
                    continue
                location = (row.get('location') or '').strip()
                source = (row.get('source') or default_source).strip()
                if opts['dry_run']:
                    continue
                obj, was_created = ReagentRate.objects.update_or_create(
                    chemical=chem, location=location,
                    defaults={'unit_cost': cost, 'source': source})
                created += int(was_created)
                updated += int(not was_created)
        self.stdout.write(self.style.SUCCESS(
            f'Done. created={created} updated={updated} unmatched={unmatched} skipped={skipped}'))
