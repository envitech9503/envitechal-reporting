"""Management Review (ISO/IEC 17025 8.9) - tests (23-10-2026).

    manage.py test QC.tests_mrm

Induction of the Karachi and Lahore record from the spec (counts, verbatim rows, idempotence, actions closed by a
later meeting); plan, circular, checklist, minutes and action workflows with roles; PDFs; document control.
"""
import io
import os
import datetime as _dt

from django.core.management import call_command
from django.test import TestCase

from QC.models import MrmPlan, MrmMeeting, MrmItem, ControlChartDeletion
from QC.tests_ia import mk_users, C
from QC.views.mrm import parse_target

SPEC = os.path.join(os.path.dirname(__file__), 'fixtures', 'mrm_spec.json')
D = _dt.date


class ParseTests(TestCase):
    def test_targets(self):
        self.assertEqual(parse_target('12.03.2026'), D(2026, 3, 12))
        self.assertEqual(parse_target('06-01-2026'), D(2026, 1, 6))
        self.assertEqual(parse_target('31-Dec-2026'), D(2026, 12, 31))
        self.assertEqual(parse_target('July, 2025'), D(2025, 7, 31))
        self.assertEqual(parse_target('December, 2026'), D(2026, 12, 31))
        for t in ('N.A', 'N. A', 'Not Applicable', 'Continuous', '', '-'):
            self.assertIsNone(parse_target(t), t)


class InductionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        mk_users(cls)
        call_command('import_mrm_spec', SPEC, '--apply', stdout=io.StringIO())

    def test_counts_and_idempotence(self):
        self.assertEqual(MrmPlan.objects.count(), 4)
        self.assertEqual(MrmMeeting.objects.filter(location='Lahore').count(), 4)
        self.assertEqual(MrmMeeting.objects.filter(location='Karachi').count(), 2)
        self.assertEqual(MrmItem.objects.count(), 89)
        out = io.StringIO(); call_command('import_mrm_spec', SPEC, '--apply', stdout=out)
        self.assertIn('skipped 10', out.getvalue()); self.assertEqual(MrmItem.objects.count(), 89)

    def test_record_verbatim(self):
        m = MrmMeeting.objects.get(location='Lahore', meeting_no='01/2026')
        self.assertEqual((m.meeting_date, m.status, m.circular_status, m.mr_name, m.ceo_name), (D(2026, 3, 9), 'approved', 'issued', 'Saba Qadeer', 'Syed Imran Ali Kazmi'))
        self.assertEqual(len(m.participants), 9); self.assertEqual(m.items.filter(part='minutes').count(), 18)
        self.assertTrue(m.checklist_complete())
        first = m.items.order_by('order').first()
        self.assertEqual(first.inputs, 'Total 09 Non-Conformance were found.')
        f25 = MrmMeeting.objects.get(location='Lahore', meeting_no='01/2025')
        self.assertEqual(f25.items.filter(part='addendum').count(), 10); self.assertEqual(f25.addendum_date, D(2025, 4, 25))
        k = MrmMeeting.objects.get(location='Karachi', meeting_no='02/2025')
        self.assertIn('02/2025', k.legacy['note']); self.assertEqual(k.meeting_date, D(2025, 12, 31))
        p = MrmPlan.objects.get(location='Karachi', year=2026)
        self.assertEqual((p.status, len(p.rows)), ('draft', 4))
        self.assertTrue(p.rows[0]['months']['12']['due'])

    def test_actions_closed_by_a_later_meeting(self):
        old = MrmMeeting.objects.get(location='Lahore', meeting_no='01/2025')
        self.assertFalse(old.items.filter(action_status='open').exists())
        self.assertTrue(old.items.filter(action_status='done', done_note__contains='02/2025').exists())
        latest = MrmMeeting.objects.get(location='Lahore', meeting_no='01/2026')
        self.assertTrue(latest.items.filter(action_status='open').exists())

    def test_pages_and_pdfs(self):
        c = C(self.chem)
        for m in MrmMeeting.objects.all():
            for u in ('/qc/mrm/meetings/%d/' % m.pk, '/qc/mrm/meetings/%d/minutes.pdf' % m.pk, '/qc/mrm/meetings/%d/circular.pdf' % m.pk,
                      '/qc/mrm/meetings/%d/checklist.pdf' % m.pk):
                r = c.get(u)
                self.assertEqual(r.status_code, 200, u)
                if u.endswith('.pdf'):
                    self.assertTrue(r.content.startswith(b'%PDF'), u)
        for p in MrmPlan.objects.all():
            self.assertTrue(c.get('/qc/mrm/plans/%d/pdf/' % p.pk).content.startswith(b'%PDF'))
        for u in ('/qc/mrm/?location=Lahore', '/qc/mrm/actions/?location=Lahore&show=all', '/qc/mrm/signing/?location=Karachi', '/management/'):
            self.assertEqual(c.get(u).status_code, 200, u)


class WorkflowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        mk_users(cls)

    def _new_meeting(self, client, **extra):
        data = {'meeting_no': '01/2027', 'meeting_date': '15-01-2027', 'time_text': '10:00 am to 02:00 pm', 'venue': 'Conference room', 'review_type': 'Regular',
                'subject': 'Management Review Meeting', 'circular_date': '10-01-2027', 'circular_intro': 'MRM notice', 'ag0': 'Review of Internal Audit Reports',
                'ag1': 'Complaints', 'dist0': 'CEO', 'att0_name': 'ia_chem', 'att0_designation': 'Chemist', 'par0_name': 'ia_mgr', 'par0_designation': 'MR',
                'chair': 'CEO', 'm0_sno': 'a)', 'm0_clause': '8.9.2 e)', 'm0_agenda': 'Review of Internal Audit Reports', 'm0_inputs': '2 NCs found',
                'm0_outputs': 'Close the NCs', 'm0_resources': 'No', 'm0_responsibility': 'MR', 'm0_target': '30-01-2027',
                'm1_sno': 'b)', 'm1_agenda': 'Complaints', 'm1_inputs': 'No complaints', 'm1_outputs': 'Noted', 'm1_responsibility': 'N.A', 'm1_target': 'N.A'}
        data.update(extra)
        return client.post('/qc/mrm/meetings/new/?location=Karachi', data)

    def test_roles_and_full_cycle(self):
        # a chemist cannot create; the MR can
        self.assertEqual(self._new_meeting(C(self.chem)).status_code, 403)
        r = self._new_meeting(C(self.mgr))
        self.assertEqual(r.status_code, 302)
        m = MrmMeeting.objects.get(location='Karachi', meeting_no='01/2027')
        self.assertEqual(m.items.count(), 2)
        act = m.items.get(sno='a)'); info = m.items.get(sno='b)')
        self.assertEqual((act.action_status, act.target_date), ('open', D(2027, 1, 30)))
        self.assertEqual(info.action_status, '')
        # the circular is issued by the CEO, not the MR
        self.assertEqual(C(self.mgr).post('/qc/mrm/meetings/%d/action/' % m.pk, {'action': 'issue'}).status_code, 403)
        C(self.ceo).post('/qc/mrm/meetings/%d/action/' % m.pk, {'action': 'issue'})
        m.refresh_from_db(); self.assertEqual(m.circular_status, 'issued')
        # the listed chemist signs receipt; the Lahore chemist cannot
        self.assertEqual(C(self.lchem).post('/qc/mrm/meetings/%d/action/' % m.pk, {'action': 'sign'}).status_code, 403)
        C(self.chem).post('/qc/mrm/meetings/%d/action/' % m.pk, {'action': 'sign'})
        m.refresh_from_db(); self.assertTrue(m.attendance[0]['signed_at'])
        # checklist: incomplete then complete
        post = {'checklist_date': '15-01-2027'}
        for i in range(15):
            post['d%d' % i] = 'yes'
        post['d9'] = 'no'
        C(self.mgr).post('/qc/mrm/meetings/%d/checklist/' % m.pk, post)
        m.refresh_from_db(); self.assertFalse(m.checklist_complete())
        post['j9'] = 'No complaints received in the period'
        C(self.mgr).post('/qc/mrm/meetings/%d/checklist/' % m.pk, post)
        m.refresh_from_db(); self.assertTrue(m.checklist_complete())
        # plan with January planned is marked done when the minutes are approved
        p = MrmPlan.objects.create(location='Karachi', year=2027, rows=[{'department': 'Laboratory', 'months': {'1': {'due': True, 'done': False}}}])
        C(self.mgr).post('/qc/mrm/meetings/%d/action/' % m.pk, {'action': 'prepare'})
        m.refresh_from_db(); self.assertEqual(m.status, 'prepared')
        self.assertEqual(C(self.mgr).post('/qc/mrm/meetings/%d/action/' % m.pk, {'action': 'approve'}).status_code, 403)
        C(self.ceo).post('/qc/mrm/meetings/%d/action/' % m.pk, {'action': 'approve'})
        m.refresh_from_db(); p.refresh_from_db()
        self.assertEqual(m.status, 'approved'); self.assertTrue(p.rows[0]['months']['1']['done'])
        # approved minutes are locked
        self.assertEqual(C(self.mgr).get('/qc/mrm/meetings/%d/edit/' % m.pk).status_code, 302)
        # action follow-up: note required
        C(self.mgr).post('/qc/mrm/actions/%d/' % act.pk, {'action': 'done', 'note': 'x'})
        act.refresh_from_db(); self.assertEqual(act.action_status, 'open')
        C(self.mgr).post('/qc/mrm/actions/%d/' % act.pk, {'action': 'done', 'note': 'Both NCs closed and verified'})
        act.refresh_from_db(); self.assertEqual(act.action_status, 'done')
        self.assertEqual(C(self.chem).post('/qc/mrm/actions/%d/' % act.pk, {'action': 'reopen'}).status_code, 403)
        # PDFs carry the e-signatures without errors
        for k in ('circular', 'minutes', 'checklist'):
            self.assertTrue(C(self.chem).get('/qc/mrm/meetings/%d/%s.pdf' % (m.pk, k)).content.startswith(b'%PDF'))

    def test_edit_keeps_follow_up_and_delete_logs(self):
        self._new_meeting(C(self.mgr))
        m = MrmMeeting.objects.get(meeting_no='01/2027')
        act = m.items.get(sno='a)')
        act.action_status, act.done_note = 'done', 'closed'; act.save()
        r = self._new_meeting(C(self.mgr), m0_id=str(act.pk), m0_inputs='2 NCs found (edited)')
        # same number again from the new form is refused; edit through the edit page instead
        self.assertEqual(r.status_code, 200)
        data = {'meeting_no': '01/2027', 'meeting_date': '15-01-2027', 'ag0': 'Agenda', 'm0_id': str(act.pk), 'm0_sno': 'a)', 'm0_agenda': 'Review', 'm0_inputs': 'edited',
                'm0_responsibility': 'MR', 'm0_target': '30-01-2027'}
        C(self.mgr).post('/qc/mrm/meetings/%d/edit/' % m.pk, data)
        act.refresh_from_db()
        self.assertEqual((act.inputs, act.action_status), ('edited', 'done'))
        self.assertEqual(m.items.count(), 1)
        C(self.mgr).post('/qc/mrm/meetings/%d/action/' % m.pk, {'action': 'delete', 'reason': 'created by mistake'})
        self.assertFalse(MrmMeeting.objects.filter(pk=m.pk).exists())
        self.assertTrue(ControlChartDeletion.objects.filter(kind='mrm_meet').exists())

    def test_plan_cycle(self):
        r = C(self.mgr).post('/qc/mrm/plans/new/?location=Lahore', {'year': '2027', 'dept0': 'Environmental Laboratory', 'r0_m3_due': '1'})
        self.assertEqual(r.status_code, 403)                       # the Karachi MR cannot plan for Lahore
        C(self.lmgr).post('/qc/mrm/plans/new/?location=Lahore', {'year': '2027', 'dept0': 'Environmental Laboratory', 'r0_m3_due': '1'})
        p = MrmPlan.objects.get(location='Lahore', year=2027)
        C(self.lmgr).post('/qc/mrm/plans/%d/action/' % p.pk, {'action': 'sign_mr'})
        C(self.ceo).post('/qc/mrm/plans/%d/action/' % p.pk, {'action': 'approve'})
        p.refresh_from_db(); self.assertEqual(p.status, 'approved')

    def test_doc_control_defaults(self):
        from QC.views.mrm import mrm_docctrl
        self.assertEqual(mrm_docctrl('minutes', 'Karachi', D(2025, 1, 1))['issue_no'], '02')
        self.assertEqual(mrm_docctrl('checklist', 'Lahore', D(2025, 6, 1))['issue_date'], '25-04-2025')
        self.assertEqual(mrm_docctrl('checklist', 'Karachi', D(2025, 6, 1))['doc_no'], 'ETAL-QMS-809-FF-04')


class NamedSignatureTests(TestCase):
    """24-10-2026: inducted (paper) records print the e-signature of the named signatory when one is on file."""

    @classmethod
    def setUpTestData(cls):
        import tempfile
        from PIL import Image
        from django.contrib.auth.models import User
        from django.core.files import File
        from EnviTechAlApp.models import Signatures
        mk_users(cls)
        cls.tmp = tempfile.mkdtemp()
        def sig(username, first, last, active=True):
            u = User.objects.create_user(username, password='x', first_name=first, last_name=last, is_active=active)
            p = os.path.join(cls.tmp, username + '.png'); Image.new('RGBA', (120, 40), (20, 40, 160, 255)).save(p)
            s = Signatures(user=u)
            with open(p, 'rb') as fh:
                s.signature.save(username + '.png', File(fh), save=True)
            return u
        cls.kazmi = sig('ImranKazmiT', 'Syed Imran Ali', 'Kazmi')
        cls.mr = sig('HinaT', 'Hina', 'Abidi')
        cls.mod = sig('ModabirT', 'M. Modabir', 'Raza')
        cls.lab = sig('Lahorelab', 'Maryam', 'Fatima')
        cls.mar = sig('Maryam', 'Maryam', 'Fatima')
        call_command('import_mrm_spec', SPEC, '--apply', stdout=io.StringIO())

    def test_name_matching(self):
        from QC.views.mrm_pdf import _named_sig
        from EnviTechAlApp.models import Signatures
        c = {}
        path = lambda u: Signatures.objects.get(user=u).signature.path
        self.assertEqual(_named_sig('Syed Imran Ali Kazmi', c), path(self.kazmi))
        self.assertEqual(_named_sig('  hina abidi ', c), path(self.mr))
        self.assertEqual(_named_sig('Muhammad Modabir Raza', c), path(self.mod))       # Muhammad / M. alike
        self.assertEqual(_named_sig('Maryam Fatima', c), path(self.mar))              # personal account before the lab account
        self.assertIsNone(_named_sig('Abdul Samad', c))
        self.assertIsNone(_named_sig('', c)); self.assertIsNone(_named_sig('Hina', c))

    def test_pdfs_draw_the_signatures(self):
        from EnviTechAlApp.models import Signatures
        cl = C(self.chem)
        m = MrmMeeting.objects.get(location='Karachi', meeting_no='02/2025')
        self.assertEqual((m.mr_name, m.ceo_name), ('Hina Abidi', 'Syed Imran Ali Kazmi'))
        p = MrmPlan.objects.filter(status='approved').first()
        lk = MrmMeeting.objects.get(location='Lahore', meeting_no='01/2026')             # checklist on the record
        self.assertTrue(lk.checklist)
        urls = ['/qc/mrm/meetings/%d/minutes.pdf' % m.pk, '/qc/mrm/meetings/%d/checklist.pdf' % lk.pk, '/qc/mrm/meetings/%d/circular.pdf' % m.pk,
                '/qc/mrm/plans/%d/pdf/' % p.pk]
        def images():
            out = []
            for u in urls:
                r = cl.get(u); self.assertEqual(r.status_code, 200, u); self.assertTrue(r.content.startswith(b'%PDF'), u)
                out.append(r.content.count(b'/Subtype /Image'))
            return out
        with_sig = images()
        Signatures.objects.filter(user__in=[self.kazmi, self.mr, self.mod, self.lab, self.mar]).delete()
        without = images()
        for u, a, b in zip(urls, with_sig, without):
            self.assertGreater(a, b, u)

    def test_blank_checklist_is_not_signed(self):
        m = MrmMeeting.objects.get(location='Karachi', meeting_no='02/2025')
        self.assertFalse(m.checklist)
        lk = MrmMeeting.objects.get(location='Lahore', meeting_no='01/2026')
        cl = C(self.chem)
        blank_n = cl.get('/qc/mrm/meetings/%d/checklist.pdf' % m.pk).content.count(b'/Subtype /Image')
        min_n = cl.get('/qc/mrm/meetings/%d/minutes.pdf' % m.pk).content.count(b'/Subtype /Image')
        self.assertLess(blank_n, min_n)                       # minutes carry Hina + CEO, the blank checklist only the logo

    def test_system_record_never_borrows_a_signature(self):
        from QC.views.mrm_pdf import _paper_sig
        c = {}
        self.assertEqual(_paper_sig(None, None, 'Hina Abidi', c, False), (None, 'paper'))   # not inducted: no named signature
        img, mode = _paper_sig(None, None, 'Hina Abidi', c, True)
        self.assertTrue(img and mode == '' and c.get('_used'))
        new = MrmMeeting.objects.create(location='Karachi', meeting_no='09/2026', year=2026, seq=9, mr_name='Hina Abidi', ceo_name='Syed Imran Ali Kazmi')
        self.assertFalse(new.inducted)
        r = C(self.chem).get('/qc/mrm/meetings/%d/minutes.pdf' % new.pk)
        self.assertEqual(r.status_code, 200)
        old = MrmMeeting.objects.get(location='Karachi', meeting_no='02/2025')            # same two names, inducted
        self.assertLess(r.content.count(b'/Subtype /Image'), C(self.chem).get('/qc/mrm/meetings/%d/minutes.pdf' % old.pk).content.count(b'/Subtype /Image'))
