"""NC&CA forms 'empty inside' (complaint of both Lab Managers, 26-10-2026) and several RCAs per NC&CA.

    manage.py test QC.tests_ia_record

The inducted record held only the NC&CA log rows (Karachi, 18) and the audit-report findings (Lahore, 19 drafts), so
those forms have blank sections. The software now says which parts are missing (page, list, PDF) and lets the
location's manager complete an inducted form from the signed paper form without touching its status or paper
signatures (record trail). An NC&CA may carry one RCA per root cause (a, b, c ...).
"""
import io

from django.core.management import call_command
from django.test import TestCase

from QC.models import Ncca, NccaRca
from QC.tests_ia import SPEC, mk_users, C


class FormGapTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        mk_users(cls)
        call_command('import_ia_spec', SPEC, '--apply', stdout=io.StringIO())

    def test_gaps_identified(self):
        full = Ncca.objects.filter(location='Karachi', log_only=False)
        self.assertEqual([n.nc_no for n in full if n.form_gaps], [])
        self.assertTrue(all(n.form_gaps for n in Ncca.objects.filter(log_only=True)))
        self.assertTrue(all('root cause' in n.form_gaps for n in Ncca.objects.filter(location='Lahore')))
        n = Ncca(location='Karachi', nc_no='X', details='live NC')          # a live (not inducted) NC&CA is never flagged
        self.assertEqual(n.form_gaps, [])

    def test_list_page_and_pdf_say_what_is_missing(self):
        mgr, chem = C(self.mgr), C(self.chem)
        r = mgr.get('/qc/ia/ncs/?location=Karachi&show=incomplete')
        self.assertContains(r, 'Form incomplete'); self.assertContains(r, 'NC-01-LA-01/PNAC/2025'); self.assertNotContains(r, 'NC-01/IA-1/025<')
        n = Ncca.objects.get(nc_no='NC-01-LA-01/PNAC/2025')
        r = mgr.get('/qc/ia/ncs/%d/' % n.pk)
        self.assertContains(r, 'Parts of this form are not in the system'); self.assertContains(r, 'Complete from paper record')
        r = chem.get('/qc/ia/ncs/%d/' % n.pk)
        self.assertContains(r, 'Parts of this form are not in the system'); self.assertNotContains(r, 'Complete from paper record')
        self.assertNotContains(mgr.get('/qc/ia/ncs/%d/' % Ncca.objects.get(nc_no='NC-01/IA-1/025').pk), 'Parts of this form are not in the system')
        self.assertEqual(chem.get('/qc/ia/ncs/%d/pdf/' % n.pk).status_code, 200)

    def _form(self, n, **kw):
        d = {'record': '1', 'nc_no': n.nc_no, 'date': n.date.strftime('%d-%m-%Y') if n.date else '', 'department': 'Lab', 'raised_by': n.raised_by, 'clause': n.clause,
             'source': n.source, 'category': n.category, 'priority': 'high', 'risk_type': 'low', 'severity': 'low', 'details': n.details,
             'proposed_date': '', 'assigned_to': n.assigned_to, 'target_date': n.target_date.strftime('%d-%m-%Y') if n.target_date else '',
             'root_cause': '', 'corrective': '', 'completion_date': '', 'followup_with': '', 'satisfactory': '', 'followup_date': n.followup_date.strftime('%d-%m-%Y') if n.followup_date else '',
             'next_followup_date': '', 'followup_desc': '', 'remarks': '', 'closed_by_name': n.closed_by_name, 'closing_date': n.closing_date.strftime('%d-%m-%Y') if n.closing_date else ''}
        for b in ('due_audit_internal', 'due_audit_external', 'due_complaint'):
            if getattr(n, b):
                d[b] = '1'
        d.update(kw)
        return d

    def test_complete_closed_log_row_from_record(self):
        mgr, lmgr, chem = C(self.mgr), C(self.lmgr), C(self.chem)
        n = Ncca.objects.get(nc_no='NC-01-LA-01/PNAC/2025')
        closed = (n.status, n.closed_by_name, n.closing_date)
        self.assertEqual(mgr.get('/qc/ia/ncs/%d/edit/' % n.pk).status_code, 302)              # still locked for normal editing
        self.assertContains(mgr.get('/qc/ia/ncs/%d/edit/?record=1' % n.pk), 'Completing the form from the paper record')
        self.assertEqual(chem.get('/qc/ia/ncs/%d/edit/?record=1' % n.pk).status_code, 302)    # a member: record mode not granted, form locked
        self.assertEqual(lmgr.get('/qc/ia/ncs/%d/edit/?record=1' % n.pk).status_code, 302)    # the other laboratory's manager: no record mode, form locked
        r = mgr.post('/qc/ia/ncs/%d/edit/' % n.pk, self._form(n, details='Calibration certificate of the balance did not show the uncertainty.',
                                                               root_cause='Certificate not reviewed on receipt.', corrective='Certificate review checklist introduced.',
                                                               completion_date='28-04-2025', followup_with='Lab Manager', satisfactory='1', followup_desc='Verified.'))
        self.assertEqual(r.status_code, 302); n.refresh_from_db()
        self.assertEqual((n.status, n.closed_by_name, n.closing_date), closed)                 # status and paper closure kept
        self.assertEqual((n.log_only, n.root_cause, n.satisfactory), (False, 'Certificate not reviewed on receipt.', True))
        self.assertEqual(n.form_gaps, [])
        t = n.legacy['completed'][-1]
        self.assertEqual((t['by'], t['from_status'], t['to_status']), ('ia_mgr', 'closed', 'closed'))
        self.assertIn('root_cause', t['fields']); self.assertIn('details', t['fields'])
        self.assertIsNone(n.hod_signed_by_id); self.assertIsNone(n.closed_by_id)                # no e-signature applied
        self.assertContains(mgr.get('/qc/ia/ncs/%d/' % n.pk), 'Record trail')
        self.assertEqual(n.history.count() >= 2, True)

    def test_lahore_draft_closed_as_per_record(self):
        lmgr = C(self.lmgr)
        n = Ncca.objects.get(location='Lahore', nc_no='NC-05/01-2026')
        r = lmgr.post('/qc/ia/ncs/%d/edit/' % n.pk, self._form(n, close_record='1'), follow=True)
        self.assertContains(r, 'enter the root cause, the corrective action, the closing date and who closed it')
        n.refresh_from_db(); self.assertEqual(n.status, 'draft')
        lmgr.post('/qc/ia/ncs/%d/edit/' % n.pk, self._form(n, close_record='1', root_cause='Balance range not verified.', corrective='Range verified and recorded.',
                                                           completion_date='20-03-2026', satisfactory='1', followup_with='Lab Manager', closed_by_name='Saba Qadeer Manager Lab',
                                                           closing_date='25-03-2026'))
        n.refresh_from_db()
        self.assertEqual((n.status, n.closed_by_name, n.closing_date.isoformat(), n.closed_by_id), ('closed', 'Saba Qadeer Manager Lab', '2026-03-25', None))
        self.assertEqual(n.legacy['completed'][-1]['to_status'], 'closed'); self.assertIn('status', n.legacy['completed'][-1]['fields'])

    def test_record_mode_only_for_inducted(self):
        mgr = C(self.mgr)
        n = Ncca.objects.create(location='Karachi', nc_no='NC-09/IA/026', details='live', status='open')
        r = mgr.get('/qc/ia/ncs/%d/edit/?record=1' % n.pk)
        self.assertNotContains(r, 'Completing the form from the paper record')
        self.assertNotContains(mgr.get('/qc/ia/ncs/%d/' % n.pk), 'Complete from paper record')


class MultiRcaTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        mk_users(cls)
        call_command('import_ia_spec', SPEC, '--apply', stdout=io.StringIO())

    def _rca(self, **kw):
        d = {'rca_no': '', 'clause': '6.4', 'deputed': 'MR', 'date': '03-01-2026', 'c_personnel': '1', 'c_personnel_2': '1', 'six_why': '1',
             'statement': 'second root cause', 'why1': 'w1', 'conclusion': 'c', 'performed_name': 'MR', 'reviewed_name': 'CEO'}
        d.update(kw); return d

    def test_parts_a_b_and_pages(self):
        mgr, chem = C(self.mgr), C(self.chem)
        n = Ncca.objects.create(location='Karachi', nc_no='NC-07/IA/026', details='three causes', status='open', clause='6.4 (ISO/IEC 17025:2017)')
        mgr.post('/qc/ia/ncs/%d/rca/' % n.pk, self._rca(statement='first cause'))
        first = NccaRca.objects.get(nc=n); self.assertEqual((first.part, first.rca_no), ('', ''))
        r = mgr.get('/qc/ia/ncs/%d/rca/?new=1' % n.pk); self.assertEqual(r.status_code, 200)
        first.refresh_from_db(); self.assertEqual(first.part, '')                                # a GET changes nothing
        mgr.post('/qc/ia/ncs/%d/rca/' % n.pk, self._rca(new='1', rca_no='R07/IA/026(b)'))
        rows = list(NccaRca.objects.filter(nc=n).order_by('part'))
        self.assertEqual([x.part for x in rows], ['a', 'b'])
        mgr.post('/qc/ia/ncs/%d/rca/' % n.pk, self._rca(new='1', rca_no='R07/IA/026(c)', statement='third'))
        self.assertEqual(sorted(NccaRca.objects.filter(nc=n).values_list('part', flat=True)), ['a', 'b', 'c'])
        b = NccaRca.objects.get(nc=n, part='b')
        mgr.post('/qc/ia/ncs/%d/rca/' % n.pk, self._rca(rca_pk=str(b.pk), rca_no=b.rca_no, statement='second cause edited'))
        b.refresh_from_db(); self.assertEqual(b.statement, 'second cause edited')
        self.assertEqual(NccaRca.objects.get(nc=n, part='a').statement, 'first cause')
        r = chem.get('/qc/ia/ncs/%d/' % n.pk)
        self.assertContains(r, 'second cause edited'); self.assertContains(r, 'third'); self.assertContains(r, 'RCA PDF (3)')
        self.assertEqual(chem.get('/qc/ia/ncs/%d/rca/pdf/' % n.pk).status_code, 200)
        self.assertEqual(chem.get('/qc/ia/ncs/%d/rca/pdf/?rca=%d' % (n.pk, b.pk)).status_code, 200)
        self.assertEqual(chem.get('/qc/ia/ncs/%d/rca/pdf/?rca=999999' % n.pk).status_code, 404)
        self.assertEqual(Ncca.objects.get(pk=n.pk).rca.part, 'a')
        self.assertEqual(mgr.get('/qc/ia/rca/?location=Karachi').status_code, 200)
        self.assertEqual(mgr.get('/qc/ia/ncs/?location=Karachi&show=all').status_code, 200)


class EaImportTests(TestCase):
    """Lahore PNAC external-assessment NC&CAs (2025 final assessment, 2026) with their RCAs (a, b, c ...)."""
    EA = __import__('os').path.join(__import__('os').path.dirname(__file__), 'fixtures', 'ea_lahore_spec.json')

    @classmethod
    def setUpTestData(cls):
        mk_users(cls)
        call_command('import_ea_spec', cls.EA, '--apply', stdout=io.StringIO())

    def test_counts_values_and_idempotence(self):
        q = Ncca.objects.filter(location='Lahore', source='EA')
        self.assertEqual(q.count(), 11); self.assertEqual(NccaRca.objects.filter(nc__in=q).count(), 19)
        self.assertTrue(all(n.status == 'closed' and n.inducted and set(n.form_gaps) <= {'MR follow-up'} for n in q))
        n = q.get(nc_no='NC-02/PNAC/2026')
        self.assertEqual([r.part for r in n.rca_list], ['a', 'b', 'c'])
        self.assertEqual((n.category, n.priority, n.risk_type, n.satisfactory, n.completion_date.isoformat()), ('major', 'high', 'medium', True, '2026-08-18'))
        self.assertEqual(q.get(nc_no='NC-01/PNAC-FA/2025').rca.causes, {'Personnel': ['Training Needed']})
        self.assertEqual(q.get(nc_no='NC-03/PNAC/2026').rcas.get(part='c').other[:22], 'Incorrect evaluation o')
        self.assertIn('Both "Minor" and "Major"', q.get(nc_no='NC-05/PNAC/2026').legacy['notes'][0])
        out = io.StringIO(); call_command('import_ea_spec', self.EA, '--apply', stdout=out)
        self.assertIn('skipped 11', out.getvalue()); self.assertEqual(q.count(), 11)

    def test_pages_and_pdfs(self):
        lmgr = C(self.lmgr)
        n = Ncca.objects.get(nc_no='NC-06/PNAC/2026')
        r = lmgr.get('/qc/ia/ncs/%d/' % n.pk); self.assertContains(r, 'RCA PDF (3)'); self.assertContains(r, 'Record notes')
        for u in ('/qc/ia/ncs/%d/pdf/', '/qc/ia/ncs/%d/rca/pdf/'):
            self.assertEqual(lmgr.get(u % n.pk).status_code, 200)
        self.assertContains(lmgr.get('/qc/ia/ncs/?location=Lahore&show=all&source=EA'), 'NC-09/PNAC/2026')


class VerifyAgainstPaperTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        mk_users(cls)
        call_command('import_ia_spec', SPEC, '--apply', stdout=io.StringIO())

    def test_verify_sign_list_and_cleared_on_change(self):
        mgr, chem, lmgr = C(self.mgr), C(self.chem), C(self.lmgr)
        n = Ncca.objects.get(nc_no='NC-01/IA-1/025')
        self.assertContains(mgr.get('/qc/ia/ncs/?location=Karachi&show=unverified'), 'NC-01/IA-1/025')
        self.assertContains(mgr.get('/qc/ia/ncs/%d/' % n.pk), 'Verify against paper form')
        self.assertNotContains(chem.get('/qc/ia/ncs/%d/' % n.pk), 'Verify against paper form')
        self.assertEqual(chem.post('/qc/ia/ncs/%d/action/' % n.pk, {'action': 'verify_record'}).status_code, 403)
        self.assertEqual(lmgr.post('/qc/ia/ncs/%d/action/' % n.pk, {'action': 'verify_record'}).status_code, 403)
        mgr.post('/qc/ia/ncs/%d/action/' % n.pk, {'action': 'verify_record'}); n.refresh_from_db()
        self.assertEqual(n.verified['by'], 'ia_mgr')
        self.assertContains(mgr.get('/qc/ia/ncs/%d/' % n.pk), 'verified against paper form')
        self.assertNotContains(mgr.get('/qc/ia/ncs/?location=Karachi&show=unverified'), 'NC-01/IA-1/025<')
        self.assertContains(mgr.post('/qc/ia/ncs/%d/action/' % n.pk, {'action': 'verify_record'}, follow=True), 'already verified')
        self.assertEqual(mgr.get('/qc/ia/ncs/%d/pdf/' % n.pk).status_code, 200)
        # completing from the record after the sign-off clears it
        d = {'record': '1', 'nc_no': n.nc_no, 'date': n.date.strftime('%d-%m-%Y'), 'department': n.department, 'raised_by': n.raised_by, 'clause': n.clause, 'source': n.source,
             'audit': str(n.audit_id or ''), 'category': n.category, 'priority': n.priority, 'risk_type': n.risk_type, 'severity': n.severity, 'details': n.details,
             'root_cause': n.root_cause + ' (paper)', 'corrective': n.corrective, 'completion_date': n.completion_date.strftime('%d-%m-%Y') if n.completion_date else ''}
        mgr.post('/qc/ia/ncs/%d/edit/' % n.pk, d); n.refresh_from_db()
        self.assertIsNone(n.verified); self.assertEqual(len(n.legacy['verified_cleared']), 1)
        live = Ncca.objects.create(location='Karachi', nc_no='NC-08/IA/026', details='live', status='open')
        self.assertEqual(mgr.post('/qc/ia/ncs/%d/action/' % live.pk, {'action': 'verify_record'}).status_code, 403)
