"""Retire users who have left the company (24-10-2026) - see EnviTechAlApp/user_retire.py.

    manage.py retire_users Tabish Samia --reason "left the company"            # dry run: shows what is kept
    manage.py retire_users Tabish Samia --reason "left the company" --apply
"""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from EnviTechAlApp.user_retire import retire, protected, linked_counts


class Command(BaseCommand):
    help = 'Retire user accounts (keep every record, signature and log; no sign-in, no rights). Dry run unless --apply.'

    def add_arguments(self, p):
        p.add_argument('usernames', nargs='+')
        p.add_argument('--reason', default='left the company')
        p.add_argument('--apply', action='store_true')

    def handle(self, *a, **o):
        U = get_user_model()
        users = []
        for n in o['usernames']:
            u = U.objects.filter(username__iexact=n).first()
            if not u:
                raise CommandError('no such user: %s' % n)
            if protected(u):
                raise CommandError('%s is an exempt (CEO) account and is not retired' % u.username)
            users.append(u)
        with transaction.atomic():
            for u in users:
                kept = linked_counts(u)
                ch = retire(u, reason=o['reason'])
                self.stdout.write('RETIRE %s (%s, id %d): %s | keeps %d linked rows in %d tables'
                                  % (u.username, u.get_full_name() or '-', u.pk, ', '.join(ch) or 'already retired',
                                     sum(kept.values()), len(kept)))
            if not o['apply']:
                transaction.set_rollback(True)
                self.stdout.write('dry run - nothing saved (use --apply)')
