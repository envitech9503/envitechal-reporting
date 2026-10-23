"""Induct the laboratories' Management Review record from a spec file (23-10-2026).

    manage.py import_mrm_spec QC/fixtures/mrm_spec.json            # dry run
    manage.py import_mrm_spec QC/fixtures/mrm_spec.json --apply    # create

The spec is built from the Word record (Karachi: MRM 01/2025 and 02/2025 with the 2026 plan; Lahore: MRM 01/2024,
01/2025 with its addendum, 02/2025 and 01/2026 with the plans 2024-2026): circulars with agenda and receiving
attendance, minutes verbatim (every row, the addendum), the 8.9.2 checklists and the plans.
Records are inducted as on paper: circular issued, minutes prepared by the MR and approved by the CEO with the printed
names and dates (no e-signature, since nobody signed in the system). Actions of a meeting whose target date had passed
when a later meeting of the same laboratory was held are closed as reviewed at that meeting (input 8.9.2 d); all other
actions stay open for follow-up on the Action tracker. Idempotent: a record already inducted (legacy.key) or an existing meeting number is skipped.
"""
import datetime as _dt
import json
import os
import re

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from QC.models import MrmPlan, MrmMeeting, MrmItem, MRM_INPUTS
from QC.views.mrm import parse_target, _is_action


def _date(s):
    return _dt.date.fromisoformat(s) if s else None


def _intro_clean(s):
    return re.sub(r'\s+\n', '\n', s or '').strip()


class Command(BaseCommand):
    help = 'Induct the Management Review record from a spec JSON (dry run unless --apply).'

    def add_arguments(self, p):
        p.add_argument('spec')
        p.add_argument('--apply', action='store_true')

    def handle(self, *a, **o):
        if not os.path.exists(o['spec']):
            raise CommandError('spec not found: %s' % o['spec'])
        with open(o['spec'], encoding='utf-8') as fh:
            spec = json.load(fh)
        built = spec.get('built', '')
        n = {'plans': 0, 'meetings': 0, 'items': 0, 'actions_open': 0, 'actions_closed': 0, 'skipped': 0}
        with transaction.atomic():
            for p in spec['plans']:
                key = 'mrm_plan:%s:%d' % (p['location'], p['year'])
                if MrmPlan.objects.filter(legacy__key=key).exists() or MrmPlan.objects.filter(location=p['location'], year=p['year']).exists():
                    n['skipped'] += 1; continue
                signed = bool(p.get('signed'))
                MrmPlan.objects.create(location=p['location'], year=p['year'], rows=p['rows'], status='approved' if signed else 'draft',
                                       mr_name=p['mr_name'] if signed else '', mr_date=_date(p['mr_date']) if signed else None,
                                       ceo_name=p['ceo_name'] if signed else '', ceo_date=_date(p['ceo_date']) if signed else None,
                                       legacy={'key': key, 'file': p['file'], 'inducted': built,
                                               'notes': [] if signed else ['Unsigned on the record - to be signed by the MR and approved by the CEO in the system.']})
                n['plans'] += 1
            created = []
            for mt in spec['meetings']:
                loc, c, mi, k = mt['location'], mt.get('circular') or {}, mt['minutes'], mt.get('checklist')
                no = (c.get('meeting_no') or mi.get('meeting_no') or '').strip()
                mm = re.match(r'^(\d{1,2})/(\d{4})$', no)
                if not mm:
                    raise CommandError('bad meeting number %r' % no)
                no = '%02d/%s' % (int(mm.group(1)), mm.group(2))
                key = 'mrm:%s:%s' % (loc, no)
                if MrmMeeting.objects.filter(legacy__key=key).exists() or MrmMeeting.objects.filter(location=loc, meeting_no=no).exists():
                    n['skipped'] += 1; continue
                mdate = _date(mi.get('meeting_date') or c.get('meeting_date'))
                signed_on = _date(mi.get('dated')) or mdate
                roles = mi.get('roles') or {}
                checklist, chk_date = [], None
                if k:
                    by = {r['code'].replace(' ', ''): r for r in k['rows']}
                    for code, item in MRM_INPUTS:
                        r = by.get(code.replace(' ', ''), {})
                        checklist.append({'code': code, 'item': r.get('item') or item, 'discussed': r.get('discussed', ''), 'remarks': r.get('remarks', ''),
                                          'justification': r.get('justification', '')})
                    chk_date = _date(k.get('date'))
                files = [x['file'] for x in (c, mi, k) if x and x.get('file')]
                m = MrmMeeting.objects.create(
                    location=loc, meeting_no=no, year=int(mm.group(2)), seq=int(mm.group(1)), meeting_date=mdate,
                    time_text=mi.get('time') or c.get('time') or '', venue=mi.get('venue') or c.get('venue') or '', review_type=mi.get('review_type') or '',
                    subject=c.get('subject') or 'Management Review Meeting', circular_date=_date(c.get('dated')), circular_intro=_intro_clean(c.get('intro')),
                    agenda=c.get('agenda') or [], distribute_to=c.get('distribute') or [],
                    attendance=[{'name': x['name'], 'designation': x.get('designation', ''), 'user_id': None, 'signed_at': None} for x in (c.get('attendance') or [])],
                    circular_status='issued' if c else 'draft', circular_signer=c.get('ceo_name', '') if c else '',
                    participants=mi.get('participants') or [], chair=roles.get('chair', ''), facilitator=roles.get('facilitator', ''),
                    minutes_taker=roles.get('minutes_taker', ''), documenter=roles.get('documenter', ''), next_mrm=mi.get('next_mrm') or '',
                    distributed_to=mi.get('distributed_to') or '', addendum_date=_date(mi.get('addendum_dated')),
                    checklist=checklist, checklist_date=chk_date,
                    status='approved', mr_name=mi.get('prepared_by') or '', mr_date=signed_on, ceo_name=mi.get('approved_by') or '', ceo_date=signed_on,
                    legacy={'key': key, 'files': files, 'note': mt.get('note', ''), 'inducted': built,
                            'circ_snap': {'meeting_no': no, 'meeting_date': c.get('meeting_date') or '', 'time': c.get('time') or '', 'venue': c.get('venue') or '',
                                          'subject': c.get('subject') or ''} if c else {}})
                for part, rows in (('minutes', mi.get('items') or []), ('addendum', mi.get('addendum') or [])):
                    for order, r in enumerate(rows):
                        it = MrmItem(meeting=m, part=part, order=order, sno=r.get('sno', '')[:12], clause=(r.get('clause') or '')[:12], agenda=r.get('agenda', ''),
                                     inputs=r.get('inputs', ''), outputs=r.get('outputs', ''), resources=r.get('resources', ''),
                                     responsibility=(r.get('responsibility') or ''), target_text=(r.get('target') or '')[:60])
                        it.target_date = parse_target(it.target_text)
                        it.action_status = 'open' if _is_action(it) else ''
                        it.save()
                        n['items'] += 1
                created.append(m)
                n['meetings'] += 1
            # actions reviewed at a later meeting of the same laboratory are closed as on the record
            for m in created:
                later = MrmMeeting.objects.filter(location=m.location, meeting_date__gt=m.meeting_date).order_by('meeting_date').first() if m.meeting_date else None
                for it in m.items.filter(action_status='open'):
                    if later and it.target_date and it.target_date <= later.meeting_date:
                        it.action_status = 'done'
                        it.done_note = 'Paper record: status reviewed at MRM %s of %s (8.9.2 d).' % (later.meeting_no, later.meeting_date.strftime('%d-%m-%Y'))
                        it.save(update_fields=['action_status', 'done_note'])
                        n['actions_closed'] += 1
                    else:
                        n['actions_open'] += 1
            self.stdout.write('MRM induction: %s' % ', '.join('%s %d' % kv for kv in n.items()))
            if not o['apply']:
                transaction.set_rollback(True)
                self.stdout.write('dry run - nothing saved (use --apply)')
