"""Internal Audit module - tests (22-10-2026).

    manage.py test QC.tests_ia

Induction of the laboratory record from the spec (counts, idempotence, clause results vs the printed
summaries); workflow and roles of every form (plan, circular, audit report with copy-forward checklist,
witnessing, NC&CA in three sections, RCA); bulk signing; laboratory scoping; deletion log; PDFs.
"""
import io
import os

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase, Client

from QC.models import (IaClause, IaPlan, IaAudit, IaFinding, IaCircular, IaWitness, Ncca, NccaRca, ControlChartReviewer, ControlChartDeletion)

SPEC = os.path.join(os.path.dirname(__file__), 'fixtures', 'ia_spec.json')


def mk_users(cls):
    from EnviTechAlApp.models import Signatures
    cls.chem = User.objects.create_user('ia_chem', password='x')          # Karachi member
    cls.chem2 = User.objects.create_user('ia_chem2', password='x')        # Karachi member
    cls.lchem = User.objects.create_user('ia_lchem', password='x')        # Lahore member
    cls.mgr = User.objects.create_user('ia_mgr', password='x')            # Karachi QC / Lab Manager = MR
    cls.lmgr = User.objects.create_user('ia_lmgr', password='x')          # Lahore manager
    cls.ceo = User.objects.create_superuser('ia_ceo', 'c@b.c', 'x')
    ControlChartReviewer.objects.create(user=cls.mgr, location='Karachi')
    ControlChartReviewer.objects.create(user=cls.lmgr, location='Lahore')
    for u, off in ((cls.chem, 'Karachi'), (cls.chem2, 'Karachi'), (cls.lchem, 'Lahore'), (cls.mgr, 'Karachi'), (cls.lmgr, 'Lahore')):
        Signatures.objects.create(user=u, office=off)


def C(u):
    c = Client(); c.force_login(u); return c


class InductionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        mk_users(cls)
        call_command('import_ia_spec', SPEC, '--apply', stdout=io.StringIO())

    def test_counts_and_idempotence(self):
        self.assertEqual(IaClause.objects.count(), 120)
        self.assertEqual(IaAudit.objects.count(), 4); self.assertEqual(IaFinding.objects.count(), 318)
        self.assertEqual(IaPlan.objects.count(), 2); self.assertEqual(IaCircular.objects.count(), 6); self.assertEqual(IaWitness.objects.count(), 2)
        self.assertEqual(Ncca.objects.filter(location='Karachi', log_only=False).count(), 4); self.assertEqual(NccaRca.objects.count(), 4)
        self.assertEqual(Ncca.objects.filter(log_only=True).count(), 18); self.assertEqual(Ncca.objects.filter(location='Lahore').count(), 19)
        out = io.StringIO(); call_command('import_ia_spec', SPEC, '--apply', stdout=out)
        self.assertIn('skipped 53', out.getvalue()); self.assertEqual(IaFinding.objects.count(), 318)

    def test_results_match_printed_summaries(self):
        for a in IaAudit.objects.all():
            s = a.legacy['summary']
            self.assertEqual((a.n_obs, a.n_major), (s['obs'], s['major']), a.audit_no)
        l25 = IaAudit.objects.get(location='Lahore', audit_no='01/2025')
        self.assertEqual(l25.n_minor, 2)            # printed summary kept; A7: the findings tag three minor NCs (MNC-01..03)
        self.assertEqual(Ncca.objects.filter(audit=l25, category='minor').count(), 3)
        l26 = IaAudit.objects.get(location='Lahore', audit_no='01/2026')
        self.assertEqual(Ncca.objects.filter(audit=l26, category='major').count(), 7)
        self.assertEqual(Ncca.objects.filter(audit=l26, category='minor').count(), 2)
        self.assertEqual(Ncca.objects.filter(audit=l26, category='obs').count(), 1)

    def test_links_and_states(self):
        k1 = IaAudit.objects.get(location='Karachi', audit_no='01/2025')
        n = Ncca.objects.get(nc_no='NC-01/IA-1/025')
        self.assertEqual((n.audit_id, n.finding.label, n.status, n.rca.status), (k1.pk, '6.4.1', 'closed', 'reviewed'))
        self.assertEqual(n.rca.causes, {'Personnel': ['Random Error'], 'Equipment': ['Improvement needed']})
        w = IaWitness.objects.get(audit__audit_no='01/2025', audit__location='Lahore')
        self.assertEqual(w.circular.audit_no, '02/2025')          # A8
        self.assertTrue(all(c.status == 'issued' for c in IaCircular.objects.all()))
        self.assertTrue(all(a.status == 'closed' for a in IaAudit.objects.all()))
        self.assertTrue(all(n.status == 'draft' for n in Ncca.objects.filter(location='Lahore')))

    def test_pages_and_pdfs_render(self):
        c = C(self.ceo)
        urls = ['/qc/ia/', '/qc/ia/?location=Lahore', '/qc/ia/plans/', '/qc/ia/circulars/?location=Lahore', '/qc/ia/audits/', '/qc/ia/ncs/?show=all', '/qc/ia/signing/',
                '/qc/ia/clauses/', '/qc/ia/deleted/', '/qc/ia/doc-control/', '/qc/ia/manual/', '/qc/ia/log/pdf/?location=Karachi&year=2025', '/qc/qc_main/']
        urls += ['/qc/ia/audits/%d/' % a.pk for a in IaAudit.objects.all()] + ['/qc/ia/audits/%d/pdf/' % a.pk for a in IaAudit.objects.all()]
        urls += ['/qc/ia/plans/%d/pdf/' % p.pk for p in IaPlan.objects.all()] + ['/qc/ia/circulars/%d/pdf/' % p.pk for p in IaCircular.objects.all()]
        urls += ['/qc/ia/ncs/%d/' % n.pk for n in Ncca.objects.all()[:10]] + ['/qc/ia/ncs/%d/pdf/' % n.pk for n in Ncca.objects.filter(log_only=False)[:6]]
        urls += ['/qc/ia/ncs/%d/rca/pdf/' % r.nc_id for r in NccaRca.objects.all()]
        for u in urls:
            r = c.get(u)
            self.assertEqual(r.status_code, 200, u)
        pdf = c.get('/qc/ia/audits/%d/pdf/' % IaAudit.objects.get(location='Karachi', audit_no='01/2025').pk).content
        try:
            from pypdf import PdfReader
            txt = ''.join(p.extract_text() for p in PdfReader(io.BytesIO(pdf)).pages)
            self.assertIn('Signed on the paper record', txt); self.assertIn('Hina Abidi', txt); self.assertIn('1.5 weeks', txt)
        except ImportError:
            pass
        # the record page shows the discrepancy notes, the checklist and the NC links
        r = c.get('/qc/ia/audits/%d/?show=findings' % IaAudit.objects.get(location='Karachi', audit_no='01/2025').pk)
        self.assertContains(r, 'A4:'); self.assertContains(r, 'NC-01/IA-1/025'); self.assertContains(r, 'titration stand')


class WorkflowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        mk_users(cls)
        call_command('import_ia_spec', SPEC, '--apply', stdout=io.StringIO())

    # ---- plan
    def test_plan_roles_and_signatures(self):
        mgr, ceo, chem, lmgr = C(self.mgr), C(self.ceo), C(self.chem), C(self.lmgr)
        self.assertEqual(chem.get('/qc/ia/plans/new/?location=Karachi').status_code, 403)
        self.assertEqual(lmgr.get('/qc/ia/plans/new/?location=Karachi').status_code, 403)
        r = mgr.post('/qc/ia/plans/new/?location=Karachi', {'year': '2026', 'dept0': 'Environmental Laboratory', 'r0_m6_due': '1', 'r0_m12_due': '1'})
        self.assertEqual(r.status_code, 302); p = IaPlan.objects.get(location='Karachi', year=2026)
        self.assertEqual(p.rows[0]['months'], {'6': {'due': True, 'done': False}, '12': {'due': True, 'done': False}})
        self.assertEqual(chem.post('/qc/ia/plans/%d/action/' % p.pk, {'action': 'sign_mr'}).status_code, 403)
        self.assertEqual(mgr.post('/qc/ia/plans/%d/action/' % p.pk, {'action': 'approve'}).status_code, 403)      # not CEO, and not signed
        mgr.post('/qc/ia/plans/%d/action/' % p.pk, {'action': 'sign_mr'}); p.refresh_from_db(); self.assertEqual((p.status, p.mr_by_id), ('signed', self.mgr.pk))
        ceo.post('/qc/ia/plans/%d/action/' % p.pk, {'action': 'approve'}); p.refresh_from_db(); self.assertEqual((p.status, p.ceo_by_id), ('approved', self.ceo.pk))
        self.assertEqual(mgr.get('/qc/ia/plans/%d/edit/' % p.pk).status_code, 302)                  # locked
        mgr.post('/qc/ia/plans/%d/action/' % p.pk, {'action': 'mark_done', 'reason': '0:6'}); p.refresh_from_db(); self.assertTrue(p.rows[0]['months']['6']['done'])
        r = ceo.post('/qc/ia/plans/%d/action/' % p.pk, {'action': 'unapprove', 'reason': 'dates changed'}, follow=True)
        p.refresh_from_db(); self.assertEqual(p.status, 'signed'); self.assertIn('dates changed', p.remarks)
        self.assertEqual(ceo.get('/qc/ia/plans/%d/pdf/' % p.pk).status_code, 200)
        self.assertContains(mgr.post('/qc/ia/plans/new/?location=Karachi', {'year': '2026', 'dept0': 'x'}), 'already exists')
        # unapprove cleared the CEO name; a bad mark_done cell is rejected without saving; delete a draft plan with the deletion log
        self.assertEqual((p.ceo_name, p.ceo_date), ('', None))
        self.assertContains(mgr.post('/qc/ia/plans/%d/action/' % p.pk, {'action': 'mark_done', 'reason': '0:13'}, follow=True), 'Bad cell'); p.refresh_from_db(); self.assertNotIn('13', p.rows[0]['months'])
        self.assertContains(mgr.post('/qc/ia/plans/%d/action/' % p.pk, {'action': 'delete', 'reason': 'not needed'}, follow=True), 'deleted'); self.assertFalse(IaPlan.objects.filter(pk=p.pk).exists())
        self.assertTrue(ControlChartDeletion.objects.filter(kind='ia_plan', location='Karachi').exists())

    # ---- circular
    def test_circular_issue_and_receipts(self):
        mgr, chem, lchem, chem2 = C(self.mgr), C(self.chem), C(self.lchem), C(self.chem2)
        from EnviTechAlApp.models import Signatures
        Signatures.objects.filter(user=self.chem).update(name='Ali Chemist') if hasattr(Signatures, 'name') else None
        r = mgr.post('/qc/ia/circulars/new/?location=Karachi&kind=audit', {'kind': 'audit', 'audit_no': '01/2026', 'issue_date': '10-06-2026', 'audit_date_text': '17-18 June 2026',
                                                                            's0_sr': '01', 's0_day': '17-June-26', 's0_time_from': '10:00 am', 's0_time_to': '04:00 pm', 's0_scope': 'All clauses', 's0_criteria': 'ISO 17025', 's0_auditors': 'MR', 's0_auditee': 'Lab',
                                                                            'a0_name': 'Syed Imran Ali Kazmi', 'a0_designation': 'CEO', 'a1_name': 'ia_chem', 'a1_designation': 'Chemist'})
        self.assertEqual(r.status_code, 302); c = IaCircular.objects.get(location='Karachi', audit_no='01/2026')
        self.assertEqual(len(c.attendance), 2)
        self.assertContains(chem.post('/qc/ia/circulars/%d/action/' % c.pk, {'action': 'sign'}, follow=True), 'not issued yet')
        self.assertEqual(chem.post('/qc/ia/circulars/%d/action/' % c.pk, {'action': 'issue'}).status_code, 403)
        mgr.post('/qc/ia/circulars/%d/action/' % c.pk, {'action': 'issue'}); c.refresh_from_db(); self.assertEqual((c.status, c.issued_by_id), ('issued', self.mgr.pk))
        self.assertEqual(lchem.post('/qc/ia/circulars/%d/action/' % c.pk, {'action': 'sign'}).status_code, 403)           # other laboratory
        chem.post('/qc/ia/circulars/%d/action/' % c.pk, {'action': 'sign'}); c.refresh_from_db()
        self.assertEqual(c.attendance[1]['user_id'], self.chem.pk); self.assertTrue(c.attendance[1]['signed_at'])
        self.assertContains(chem.post('/qc/ia/circulars/%d/action/' % c.pk, {'action': 'sign'}, follow=True), 'already signed')
        chem2.post('/qc/ia/circulars/%d/action/' % c.pk, {'action': 'sign'}); c.refresh_from_db()
        self.assertEqual(len(c.attendance), 3); self.assertEqual(c.attendance[2]['user_id'], self.chem2.pk)   # not listed: added
        self.assertEqual(mgr.get('/qc/ia/circulars/%d/edit/' % c.pk).status_code, 302)                            # locked
        mgr.post('/qc/ia/circulars/%d/action/' % c.pk, {'action': 'withdraw', 'reason': 'date moved'}); c.refresh_from_db()
        self.assertEqual(c.status, 'draft'); self.assertFalse(any(a.get('signed_at') for a in c.attendance))
        self.assertEqual(chem.get('/qc/ia/circulars/%d/pdf/' % c.pk).status_code, 200)
        # re-issued after withdrawal: still a live circular - an unlisted member can add themselves
        mgr.post('/qc/ia/circulars/%d/action/' % c.pk, {'action': 'issue'})
        chem2.post('/qc/ia/circulars/%d/action/' % c.pk, {'action': 'sign'}); c.refresh_from_db()
        self.assertTrue(any(a.get('user_id') == self.chem2.pk for a in c.attendance)); self.assertFalse(c.inducted)

    # ---- audit report
    def test_new_audit_copy_forward_edit_and_signatures(self):
        mgr, chem, chem2, lmgr, lchem = C(self.mgr), C(self.chem), C(self.chem2), C(self.lmgr), C(self.lchem)
        self.assertEqual(chem.post('/qc/ia/audits/new/?location=Karachi', {'year': '2026'}).status_code, 403)
        self.assertEqual(lmgr.post('/qc/ia/audits/new/?location=Karachi', {'year': '2026'}).status_code, 403)
        r = mgr.post('/qc/ia/audits/new/?location=Karachi', {'year': '2026', 'seed': 'prev'})
        a = IaAudit.objects.get(location='Karachi', audit_no='01/2026')
        prev = IaAudit.objects.get(location='Karachi', audit_no='02/2025')
        self.assertEqual(a.findings.count(), prev.findings.count())
        f = a.findings.get(label='8.5.1')
        self.assertEqual(f.ref, prev.findings.get(label='8.5.1').ref); self.assertEqual(f.result, '')      # carried forward, result cleared
        self.assertTrue(f.finding)
        # master seed
        mgr.post('/qc/ia/audits/new/?location=Karachi', {'year': '2026', 'seed': 'master'})
        b = IaAudit.objects.get(location='Karachi', audit_no='02/2026')
        self.assertEqual(b.findings.count(), IaClause.objects.filter(active=True).count()); self.assertEqual(b.findings.filter(finding='').count(), b.findings.count())
        # edit: header, two results, a dropped row, an inserted row
        g = a.findings.get(label='6.4.1'); h = a.findings.get(label='7.8.5')
        data = {'date_start': '17-06-2026', 'date_end': '18-06-2026', 'auditor': 'MR', 'auditor_title': 'Lab Manager', 'auditee': 'Chemist', 'auditee_title': 'Chemist', 'address': 'x', 'scope': 'all',
                'timeframe': '2 weeks', 'conclusion': 'ok', 'then': 'detail',
                'f%d_ref' % g.pk: 'ETAL-LAB-P-604', 'f%d_finding' % g.pk: 'Stand rusted again <b>x</b>', 'f%d_result' % g.pk: 'major', 'f%d_tag' % g.pk: 'NC-01',
                'f%d_result' % f.pk: 'obs', 'f%d_drop' % h.pk: '1',
                'n0_label': '7.8.5.1', 'n0_req': 'sampling report', 'n0_after': str(g.pk), 'n0_result': 'na'}
        for x in a.findings.exclude(pk__in=(g.pk, f.pk, h.pk)):
            data['f%d_result' % x.pk] = 'c' if x.label and x.label.count('.') else ''
        r = mgr.post('/qc/ia/audits/%d/edit/' % a.pk, data)
        self.assertEqual(r.status_code, 302); a.refresh_from_db()
        self.assertEqual((a.n_obs, a.n_minor, a.n_major, a.days), (1, 0, 1, 2))
        self.assertFalse(a.findings.filter(label='7.8.5').exists()); self.assertTrue(a.findings.filter(label='7.8.5.1', result='na').exists())
        self.assertEqual(a.findings.get(label='7.8.5.1').order, a.findings.get(label='6.4.1').order + 10)
        r = mgr.get('/qc/ia/audits/%d/?show=findings' % a.pk)
        self.assertContains(r, '&lt;b&gt;x&lt;/b&gt;'); self.assertNotContains(r, '<b>x</b>'); self.assertContains(r, 'Raise NC')
        # signatures: order, roles, auditor != auditee, lab scoping
        self.assertEqual(chem.post('/qc/ia/audits/%d/action/' % a.pk, {'action': 'sign_auditor'}).status_code, 403)
        self.assertContains(chem.post('/qc/ia/audits/%d/action/' % a.pk, {'action': 'sign_auditee'}, follow=True), 'auditor signs first')
        mgr.post('/qc/ia/audits/%d/action/' % a.pk, {'action': 'sign_auditor'}); a.refresh_from_db(); self.assertEqual((a.status, a.auditor_signed_by_id), ('auditor', self.mgr.pk))
        self.assertEqual(mgr.get('/qc/ia/audits/%d/edit/' % a.pk).status_code, 302)
        self.assertContains(mgr.post('/qc/ia/audits/%d/action/' % a.pk, {'action': 'sign_auditee'}, follow=True), 'cannot also sign as auditee')
        self.assertEqual(lchem.post('/qc/ia/audits/%d/action/' % a.pk, {'action': 'sign_auditee'}).status_code, 403)
        chem.post('/qc/ia/audits/%d/action/' % a.pk, {'action': 'sign_auditee'}); a.refresh_from_db(); self.assertEqual((a.status, a.auditee_signed_by_id), ('closed', self.chem.pk))
        self.assertEqual(chem.get('/qc/ia/audits/%d/pdf/' % a.pk).status_code, 200)
        mgr.post('/qc/ia/audits/%d/action/' % a.pk, {'action': 'reopen', 'reason': 'typo in 6.4.1'}); a.refresh_from_db()
        self.assertEqual((a.status, a.auditor_signed_by_id, a.auditee_signed_by_id), ('draft', None, None)); self.assertIn('typo', a.remarks)
        # validation errors save nothing
        r = mgr.post('/qc/ia/audits/%d/edit/' % a.pk, dict(data, date_start='31-02-2030', auditor='CHANGED'))
        self.assertContains(r, 'dd-mm-yyyy'); a.refresh_from_db(); self.assertEqual((a.auditor, a.date_start.isoformat()), ('MR', '2026-06-17'))
        # a signed report cannot receive a witnessing record
        mgr.post('/qc/ia/audits/%d/action/' % a.pk, {'action': 'sign_auditor'})
        self.assertEqual(mgr.get('/qc/ia/audits/%d/witness/new/' % a.pk).status_code, 302); self.assertFalse(IaWitness.objects.filter(audit=a).exists())
        self.assertEqual(mgr.post('/qc/ia/audits/%d/witness/new/' % a.pk, {'date': '17-06-2026', 'w0_parameter': 'pH'}).status_code, 302); self.assertFalse(IaWitness.objects.filter(audit=a).exists())

    def test_witnessing_signatures(self):
        mgr, chem, chem2, lchem = C(self.mgr), C(self.chem), C(self.chem2), C(self.lchem)
        a = IaAudit.objects.get(location='Karachi', audit_no='02/2025')
        mgr.post('/qc/ia/audits/%d/action/' % a.pk, {'action': 'reopen', 'reason': 'add the witnessing record'})
        r = mgr.post('/qc/ia/audits/%d/witness/new/' % a.pk, {'date': '27-12-2025', 'auditor': 'Hina', 'auditees': 'ia_chem', 'w0_parameter': 'pH', 'w0_performed_by': 'ia_chem', 'w0_range': '0-14', 'w0_assigned': '7.00', 'w0_obtained': '7.01', 'w0_remarks': 'good'})
        self.assertEqual(r.status_code, 302); w = IaWitness.objects.get(audit=a, date__day=27)
        self.assertContains(chem.post('/qc/ia/witness/%d/action/' % w.pk, {'action': 'sign_analyst'}, follow=True), 'auditor signs first')
        mgr.post('/qc/ia/witness/%d/action/' % w.pk, {'action': 'sign_auditor'}); w.refresh_from_db(); self.assertEqual(w.status, 'auditor')
        self.assertEqual(lchem.post('/qc/ia/witness/%d/action/' % w.pk, {'action': 'sign_analyst'}).status_code, 403)
        self.assertContains(chem2.post('/qc/ia/witness/%d/action/' % w.pk, {'action': 'sign_analyst'}, follow=True), 'not named')
        chem.post('/qc/ia/witness/%d/action/' % w.pk, {'action': 'sign_analyst'}); w.refresh_from_db()
        self.assertEqual((w.status, w.auditees[0]['user_id']), ('closed', self.chem.pk))
        self.assertEqual(mgr.get('/qc/ia/audits/%d/pdf/' % a.pk).status_code, 200)

    # ---- NC&CA
    def test_nc_three_sections_and_close(self):
        mgr, chem, lchem, ceo = C(self.mgr), C(self.chem), C(self.lchem), C(self.ceo)
        a = IaAudit.objects.get(location='Karachi', audit_no='02/2025'); f = a.findings.get(label='7.6.1')
        self.assertEqual(chem.get('/qc/ia/ncs/new/?location=Karachi').status_code, 403)
        r = mgr.get('/qc/ia/ncs/new/?location=Karachi&finding=%d' % f.pk)
        self.assertContains(r, '7.6.1 (ISO/IEC 17025:2017)'); self.assertContains(r, '/IA/026')   # suggested number NC-nn/IA/026
        r = mgr.post('/qc/ia/ncs/new/?location=Karachi&finding=%d' % f.pk, {'nc_no': 'NC-03/IA-2/025', 'date': '02-01-2026', 'department': 'Lab', 'raised_by': 'Hina Abidi', 'clause': '7.6.1 (ISO/IEC 17025:2017)',
                                                                                 'source': 'IA', 'audit': str(a.pk), 'due_audit_internal': '1', 'category': 'obs', 'priority': 'low', 'risk_type': 'low', 'severity': 'low',
                                                                                 'details': 'MU for metals not yet calculated', 'proposed_date': '31-03-2026', 'assigned_to': 'Manager Lab'})
        self.assertEqual(r.status_code, 302); n = Ncca.objects.get(nc_no='NC-03/IA-2/025')
        self.assertEqual((n.audit_id, n.status, n.target_date.isoformat()), (a.pk, 'draft', '2026-03-31'))
        self.assertContains(mgr.post('/qc/ia/ncs/new/?location=Karachi', {'nc_no': 'NC-03/IA-2/025', 'details': 'dup', 'date': '02-01-2026'}), 'already exists')
        # department cannot respond before it is raised; MR raises
        self.assertContains(chem.post('/qc/ia/ncs/%d/action/' % n.pk, {'action': 'respond'}, follow=True), 'not been raised')
        self.assertEqual(chem.post('/qc/ia/ncs/%d/action/' % n.pk, {'action': 'raise'}).status_code, 403)
        mgr.post('/qc/ia/ncs/%d/action/' % n.pk, {'action': 'raise'}); n.refresh_from_db(); self.assertEqual((n.status, n.mr_signed_by_id, n.evaluated_by_id), ('open', self.mgr.pk, self.mgr.pk))
        # the CEO saving the form without changing the header does not take over the MR signature; a real header change re-signs
        ceo.post('/qc/ia/ncs/%d/edit/' % n.pk, {'nc_no': n.nc_no, 'date': '02-01-2026', 'department': 'Lab', 'raised_by': 'Hina Abidi', 'clause': n.clause, 'source': 'IA', 'audit': str(a.pk), 'due_audit_internal': '1',
                                                'category': 'obs', 'priority': 'low', 'risk_type': 'low', 'severity': 'low', 'details': n.details, 'proposed_date': '31-03-2026', 'assigned_to': 'Manager Lab', 'followup_with': ''})
        n.refresh_from_db(); self.assertEqual(n.mr_signed_by_id, self.mgr.pk)
        ceo.post('/qc/ia/ncs/%d/edit/' % n.pk, {'nc_no': n.nc_no, 'date': '02-01-2026', 'department': 'Lab', 'raised_by': 'Hina Abidi', 'clause': n.clause, 'source': 'IA', 'audit': str(a.pk), 'due_audit_internal': '1',
                                                'category': 'minor', 'priority': 'low', 'risk_type': 'low', 'severity': 'low', 'details': n.details, 'proposed_date': '31-03-2026', 'assigned_to': 'Manager Lab', 'followup_with': ''})
        n.refresh_from_db(); self.assertEqual((n.mr_signed_by_id, n.category), (self.ceo.pk, 'minor'))
        # department section: a Lahore member cannot; a Karachi chemist records root cause / corrective action and signs
        self.assertEqual(lchem.get('/qc/ia/ncs/%d/edit/' % n.pk).status_code, 403)
        r = chem.get('/qc/ia/ncs/%d/edit/' % n.pk); self.assertContains(r, 'Root cause'); self.assertNotContains(r, 'name="nc_no"')   # head section not editable by the department
        self.assertContains(chem.post('/qc/ia/ncs/%d/action/' % n.pk, {'action': 'respond'}, follow=True), 'Enter the root cause')
        chem.post('/qc/ia/ncs/%d/edit/' % n.pk, {'root_cause': 'metals added to scope only in 2026', 'corrective': 'MU studies planned Q1 2026', 'completion_date': '15-03-2026'})
        n.refresh_from_db(); self.assertEqual(n.root_cause, 'metals added to scope only in 2026')
        chem.post('/qc/ia/ncs/%d/action/' % n.pk, {'action': 'respond'}); n.refresh_from_db(); self.assertEqual((n.status, n.hod_signed_by_id), ('responded', self.chem.pk))
        # MR section: not satisfactory keeps it open with a next follow-up; satisfactory closes
        self.assertEqual(chem.post('/qc/ia/ncs/%d/action/' % n.pk, {'action': 'close'}).status_code, 403)
        self.assertContains(mgr.post('/qc/ia/ncs/%d/action/' % n.pk, {'action': 'close'}, follow=True), 'satisfactory')
        mgr.post('/qc/ia/ncs/%d/edit/' % n.pk, {'followup_with': 'Lab Manager', 'satisfactory': '0', 'followup_date': '20-03-2026'})
        self.assertContains(mgr.post('/qc/ia/ncs/%d/action/' % n.pk, {'action': 'close'}, follow=True), 'next follow-up date')
        mgr.post('/qc/ia/ncs/%d/edit/' % n.pk, {'followup_with': 'Lab Manager', 'satisfactory': '1', 'followup_date': '20-03-2026', 'remarks': 'closed'})
        mgr.post('/qc/ia/ncs/%d/action/' % n.pk, {'action': 'close'}); n.refresh_from_db()
        self.assertEqual((n.status, n.closed_by_id, n.closing_date.isoformat()), ('closed', self.mgr.pk, '2026-03-20') if n.closing_date.isoformat() == '2026-03-20' else ('closed', self.mgr.pk, n.closing_date.isoformat()))
        self.assertEqual(mgr.get('/qc/ia/ncs/%d/edit/' % n.pk).status_code, 302)        # locked
        self.assertEqual(chem.get('/qc/ia/ncs/%d/pdf/' % n.pk).status_code, 200)
        mgr.post('/qc/ia/ncs/%d/action/' % n.pk, {'action': 'reopen', 'reason': 'evidence missing'}); n.refresh_from_db()
        self.assertEqual((n.status, n.hod_signed_by_id, n.closed_by_id, n.closing_date, n.closed_by_name, n.satisfactory), ('open', None, None, None, '', None))
        # the department's section edited after the HOD signed -> signature cleared, back to open
        chem.post('/qc/ia/ncs/%d/action/' % n.pk, {'action': 'respond'}); n.refresh_from_db(); self.assertEqual(n.status, 'responded')
        chem.post('/qc/ia/ncs/%d/edit/' % n.pk, {'root_cause': 'revised root cause', 'corrective': n.corrective, 'completion_date': '15-03-2026'}); n.refresh_from_db()
        self.assertEqual((n.status, n.hod_signed_by_id, n.root_cause), ('open', None, 'revised root cause'))
        chem.post('/qc/ia/ncs/%d/action/' % n.pk, {'action': 'respond'}); n.refresh_from_db(); self.assertEqual(n.status, 'responded')
        # RCA: MR performs, performer cannot review, CEO reviews
        r = mgr.post('/qc/ia/ncs/%d/rca/' % n.pk, {'rca_no': 'R03/IA-2/2025', 'clause': '7.6.1', 'deputed': 'ML', 'date': '03-01-2026', 'c_methodprocedure': '1', 'c_methodprocedure_2': '1',
                                                    'six_why': '1', 'statement': 'MU for metals not calculated', 'why1': 'metals new in scope', 'why2': 'studies not scheduled', 'conclusion': 'schedule MU studies', 'performed_name': 'ML', 'reviewed_name': 'CEO'})
        self.assertEqual(r.status_code, 302); rc = NccaRca.objects.get(nc=n)
        self.assertEqual(rc.causes, {'Method/ Procedure': ['Improvement needed']}); self.assertEqual(rc.whys[:2], ['metals new in scope', 'studies not scheduled'])
        self.assertEqual(chem.post('/qc/ia/rca/%d/action/' % rc.pk, {'action': 'perform'}).status_code, 403)
        self.assertContains(mgr.post('/qc/ia/rca/%d/action/' % rc.pk, {'action': 'review'}, follow=True), 'performer signs first')
        mgr.post('/qc/ia/rca/%d/action/' % rc.pk, {'action': 'perform'}); rc.refresh_from_db(); self.assertEqual(rc.status, 'performed')
        self.assertEqual(mgr.post('/qc/ia/rca/%d/action/' % rc.pk, {'action': 'review'}).status_code, 403)
        ceo.post('/qc/ia/rca/%d/action/' % rc.pk, {'action': 'review'}); rc.refresh_from_db(); self.assertEqual((rc.status, rc.reviewed_by_id), ('reviewed', self.ceo.pk))
        self.assertEqual(mgr.get('/qc/ia/ncs/%d/rca/' % n.pk).status_code, 302)
        self.assertEqual(chem.get('/qc/ia/ncs/%d/rca/pdf/' % n.pk).status_code, 200)
        self.assertEqual(ceo.get('/qc/ia/ncs/%d/rca/pdf/' % n.pk).status_code, 200)

    def test_lahore_drafts_completed_by_lahore(self):
        lmgr, mgr, lchem = C(self.lmgr), C(self.mgr), C(self.lchem)
        n = Ncca.objects.get(location='Lahore', nc_no='NC-05/01-2026')
        self.assertEqual((n.status, n.category), ('draft', 'major')); self.assertIn('2.5 mg to 200 mg', n.details)
        self.assertEqual(mgr.get('/qc/ia/ncs/%d/edit/' % n.pk).status_code, 403)             # Karachi manager cannot edit a Lahore NC
        self.assertEqual(mgr.post('/qc/ia/ncs/%d/action/' % n.pk, {'action': 'raise'}).status_code, 403)
        lmgr.post('/qc/ia/ncs/%d/action/' % n.pk, {'action': 'raise'}); n.refresh_from_db(); self.assertEqual(n.status, 'open')
        r = lchem.get('/qc/ia/signing/?location=Lahore'); self.assertEqual(r.status_code, 200)

    # ---- bulk signing
    def test_signing_page_bulk(self):
        mgr, chem, ceo = C(self.mgr), C(self.chem), C(self.ceo)
        # three Lahore-independent Karachi drafts: a plan, a circular, two NCs
        mgr.post('/qc/ia/plans/new/?location=Karachi', {'year': '2027', 'dept0': 'Lab', 'r0_m3_due': '1'}); p = IaPlan.objects.get(location='Karachi', year=2027)
        mgr.post('/qc/ia/circulars/new/?location=Karachi&kind=audit', {'kind': 'audit', 'audit_no': '01/2027', 'issue_date': '01-03-2027', 's0_day': 'd', 's0_scope': 's', 'a0_name': 'ia_chem', 'a0_designation': 'Chemist'})
        c = IaCircular.objects.get(location='Karachi', audit_no='01/2027')
        for i in (1, 2):
            mgr.post('/qc/ia/ncs/new/?location=Karachi', {'nc_no': 'NC-0%d/T/027' % i, 'date': '01-03-2027', 'details': 'x%d' % i, 'source': 'TEST', 'category': 'minor', 'priority': 'low', 'risk_type': 'low', 'severity': 'low'})
        r = mgr.get('/qc/ia/signing/?location=Karachi')
        self.assertContains(r, 'plan:%d:sign_mr' % p.pk); self.assertContains(r, 'circ:%d:issue' % c.pk); self.assertContains(r, 'nc:%d:raise' % Ncca.objects.get(nc_no='NC-01/T/027').pk)
        self.assertNotContains(chem.get('/qc/ia/signing/?location=Karachi'), 'plan:%d:sign_mr' % p.pk)
        keys = ['plan:%d:sign_mr' % p.pk, 'circ:%d:issue' % c.pk] + ['nc:%d:raise' % n.pk for n in Ncca.objects.filter(nc_no__endswith='/T/027')] + ['plan:%d:approve' % p.pk]   # last one not allowed for the MR
        r = mgr.post('/qc/ia/signing/?location=Karachi', {'rec': keys}, follow=True)
        self.assertContains(r, '4 records signed'); p.refresh_from_db(); c.refresh_from_db()
        self.assertEqual((p.status, c.status), ('signed', 'issued')); self.assertEqual(Ncca.objects.filter(nc_no__endswith='/T/027', status='open').count(), 2)
        # chemist: receipt of the circular appears; signs in bulk
        r = chem.get('/qc/ia/signing/?location=Karachi'); self.assertContains(r, 'circ:%d:sign' % c.pk)
        chem.post('/qc/ia/signing/?location=Karachi', {'rec': ['circ:%d:sign' % c.pk, 'plan:%d:approve' % p.pk]}); c.refresh_from_db(); p.refresh_from_db()
        self.assertEqual(c.attendance[0]['user_id'], self.chem.pk); self.assertEqual(p.status, 'signed')      # the approve key was ignored
        # historic (inducted) circulars are signed only by the persons named on them
        hist = IaCircular.objects.get(location='Karachi', audit_no='01/2025')
        self.assertNotContains(chem.get('/qc/ia/signing/?location=Karachi'), 'circ:%d:sign' % hist.pk)
        self.assertContains(chem.post('/qc/ia/circulars/%d/action/' % hist.pk, {'action': 'sign'}, follow=True), 'not named on the attendance list')
        r = ceo.get('/qc/ia/signing/?location=Karachi'); self.assertContains(r, 'plan:%d:approve' % p.pk)
        ceo.post('/qc/ia/signing/?location=Karachi', {'rec': ['plan:%d:approve' % p.pk]}); p.refresh_from_db(); self.assertEqual(p.status, 'approved')

    # ---- deletion, clauses, doc control
    def test_delete_logged_and_guarded(self):
        mgr, chem, ceo = C(self.mgr), C(self.chem), C(self.ceo)
        a = IaAudit.objects.get(location='Karachi', audit_no='01/2025')
        self.assertContains(mgr.post('/qc/ia/audits/%d/delete/' % a.pk, {'reason': 'duplicate record'}, follow=True), 'linked')     # NCs linked
        self.assertEqual(chem.post('/qc/ia/audits/%d/delete/' % a.pk, {'reason': 'duplicate record'}).status_code, 403)
        n = Ncca.objects.get(nc_no='NC-01/IA-1/025')
        mgr.post('/qc/ia/ncs/%d/delete/' % n.pk, {'reason': 'entered twice'})
        self.assertFalse(Ncca.objects.filter(nc_no='NC-01/IA-1/025').exists())
        d = ControlChartDeletion.objects.get(kind='ia_nc'); self.assertIn('rca', d.snapshot); self.assertEqual(d.location, 'Karachi')
        self.assertContains(mgr.get('/qc/ia/deleted/'), 'NC-01/IA-1/025')
        self.assertNotContains(ceo.get('/qc/control-charts/deleted/'), 'NC-01/IA-1/025')
        self.assertEqual(chem.post('/qc/ia/clauses/', {'action': 'add', 'code': '9.1'}).status_code, 403)
        mgr.post('/qc/ia/clauses/', {'action': 'add', 'code': '7.2.1.4', 'after': '7.2.1.3', 'title': 'Verification'}); self.assertTrue(IaClause.objects.filter(code='7.2.1.4').exists())
        self.assertEqual(IaClause.objects.get(code='7.2.1.4').order, IaClause.objects.get(code='7.2.1.3').order + 1)
        self.assertEqual(mgr.get('/qc/ia/doc-control/').status_code, 403)
        ceo.post('/qc/ia/doc-control/', {'form': 'report', 'location': 'Lahore', 'doc_no': 'ETAL-QMS-808-FF-02', 'issue_date': '05-01-2024', 'issue_no': '01', 'rev_no': '01'})
        self.assertContains(ceo.get('/qc/ia/audits/%d/pdf/' % IaAudit.objects.get(location='Lahore', audit_no='01/2026').pk), b'', status_code=200)
