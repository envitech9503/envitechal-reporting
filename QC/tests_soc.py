"""Decision rule / statement of conformity module (26-10-2026).

    manage.py test QC.tests_soc
"""
import io
import json
import os

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase, Client
from django.utils import timezone

from EnviTechAlApp.models import Sample_registration, DrinkingWaterForm, WasteWaterForm2, Signatures
from QC.models import SocRecord, SocRequest, MouStudy, ControlChartReviewer, ControlChartDeletion
from QC import soc_rules as R

SPEC = os.path.join(os.path.dirname(__file__), 'fixtures', 'soc_karachi_spec.json')
KHI = '110.93.247.168'


def C(u):
    c = Client(); c.force_login(u); return c


class SocTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.chem = User.objects.create_user('s_chem', password='x')
        cls.lchem = User.objects.create_user('s_lchem', password='x')
        cls.mgr = User.objects.create_user('s_mgr', password='x')
        cls.ceo = User.objects.create_superuser('s_ceo', 'c@x.c', 'x')
        ControlChartReviewer.objects.create(user=cls.mgr, location='Karachi')
        Signatures.objects.create(user=cls.chem, office='Karachi'); Signatures.objects.create(user=cls.lchem, office='Lahore'); Signatures.objects.create(user=cls.mgr, office='Karachi')
        Sample_registration.objects.create(sample_id='WW-202610001', city_location='Karachi', checkinp107=True, checkinp110=True, inp112='SEQS limits', inp7='20-10-2026')
        Sample_registration.objects.create(sample_id='DW-202610002', city_location='Karachi', checkinp110=True)
        Sample_registration.objects.create(sample_id='WW-202610003', city_location='Karachi')             # nothing requested
        WasteWaterForm2.objects.create(sample_id='WW-202610001', report_to='Test Mills Ltd', address='Korangi', attention='Mr A', lab_report_no='202610001-TM-WW',
                                       sample_Col_date='20-Oct-2026', select='SEQS', city_location='Karachi', result_2_2='7.36', method_2='*APHA 4500 H-B',
                                       result_5_5='70', method_5='**HACH 8000', result_6_6='2040', method_6='*APHA 2540-C', result_7_7='N.D.', result_1_1='27.5')
        DrinkingWaterForm.objects.create(sample_id='DW-202610002', report_to='Soorty Test', address='Landhi', attention='Mr B', lab_report_no='202610002-ST-DW',
                                         sample_collection_date='21-Oct-2026', select='SEQS', city_location='Karachi', water_sr1='7.0', method_1='*APHA 4500 H-B',
                                         water_sr2='264', method_2='*APHA 2540-C', water_sr13='<0.0080', water_sr10='143.95',
                                         extra_field=json.dumps([{'sr': '33', 'parameters': 'Alkalinity', 'methods': 'APHA 2320 B', 'unit': 'mg/L', 'result': '120', 'limit': '-'}]))
        MouStudy.objects.create(location='Karachi', parameter='pH', level='7', unit='-', sample_kind='SAMPLE', status='approved', u_abs=0.197, u_exp=0.028, approved_at=timezone.now())
        MouStudy.objects.create(location='Karachi', parameter='COD', level='100 ppm', unit='mg/L', sample_kind='CRM', status='approved', u_abs=2.441, approved_at=timezone.now())
        MouStudy.objects.create(location='Karachi', parameter='TDS', level='1000 ppm', unit='mg/L', sample_kind='CRM', status='draft', u_abs=9.9)   # not approved: not used

    def test_rules(self):
        self.assertEqual(R.parse_limit('6-9'), (6.0, 9.0)); self.assertEqual(R.parse_limit('6.5 - 8.5'), (6.5, 8.5)); self.assertEqual(R.parse_limit('6 to 9'), (6.0, 9.0))
        self.assertEqual(R.parse_limit('<1000'), (None, 1000.0)); self.assertEqual(R.parse_limit('<= 250'), (None, 250.0)); self.assertEqual(R.parse_limit('150'), (None, 150.0))
        self.assertEqual(R.parse_limit('-'), (None, None)); self.assertEqual(R.parse_limit('Non-Objectionable'), (None, None))
        self.assertIsNone(R.to_float('N.D.')); self.assertIsNone(R.to_float('<0.0080')); self.assertEqual(R.to_float('2,040'), 2040.0)
        el = R.eligible_samples('Karachi')
        self.assertEqual([s['sample_id'] for s in el], ['DW-202610002', 'WW-202610001'])
        self.assertEqual(R.eligible_samples('Lahore'), [])
        rows = R.report_parameters('ww2', WasteWaterForm2.objects.get(), 'Karachi')
        by = {r['parameter']: r for r in rows}
        self.assertEqual(set(by), {'Temperature', 'pH', 'COD', 'TDS', 'TSS'})
        self.assertEqual((by['pH']['u'], by['pH']['lower'], by['pH']['upper'], by['pH']['accredited']), (0.197, 6.0, 9.0, True))
        self.assertEqual((by['COD']['u'], by['COD']['upper']), (2.441, 150.0))
        self.assertIsNone(by['TDS']['u']); self.assertIsNone(by['TSS']['value']); self.assertFalse(by['Temperature']['accredited'])
        rows = R.report_parameters('dw', DrinkingWaterForm.objects.get(), 'Karachi')
        by = {r['parameter']: r for r in rows}
        self.assertEqual(by['Alkalinity']['value'], 120.0); self.assertFalse(by['Alkalinity']['accredited']); self.assertEqual((by['Nickel']['value'], by['Nickel']['value_text']), (0.008, '<0.0080'))
        self.assertTrue(R.report_parameters('dw', DrinkingWaterForm.objects.get(), 'Lahore')[0]['accredited'])

    def test_full_flow(self):
        chem, lchem, mgr, ceo = C(self.chem), C(self.lchem), C(self.mgr), C(self.ceo)
        r = chem.get('/qc/soc/?location=Karachi&show=pending'); self.assertContains(r, 'WW-202610001'); self.assertContains(r, 'DW-202610002'); self.assertNotContains(r, 'WW-202610003')
        r = chem.get('/qc/soc/api/sample/?sample_id=WW-202610001&location=Karachi'); d = r.json()
        self.assertEqual((d['report_type'], d['header']['customer'], d['requisition']['soc'], len(d['parameters'])), ('ww2', 'Test Mills Ltd', True, 5))
        self.assertEqual(chem.get('/qc/soc/api/sample/?sample_id=NOPE&location=Karachi').status_code, 404)
        self.assertEqual(lchem.get('/qc/soc/new/?location=Karachi').status_code, 403)           # Lahore staff cannot prepare Karachi statements
        self.assertContains(chem.get('/qc/soc/new/?location=Karachi&sample=WW-202610001'), 'WW-202610001')
        post = {'sample_id': 'WW-202610001', 'report_type': 'ww2', 'report_pk': str(WasteWaterForm2.objects.get().pk), 'standard': 'Sindh Environmental Quality Standard 2016',
                'p1_on': '1', 'p1_parameter': 'pH', 'p1_method': '*APHA 4500 H-B', 'p1_unit': '-', 'p1_result': '7.36', 'p1_v0': '7.36', 'p1_d0': '20-10-2026', 'p1_v1': '7.36', 'p1_v2': '7.37',
                'p1_lower': '6', 'p1_upper': '9', 'p1_limit': '6-9', 'p1_u': '0.197', 'p1_usrc': 'MOU register: pH', 'p1_mou': str(MouStudy.objects.get(parameter='pH').pk),
                'p2_on': '1', 'p2_parameter': 'COD', 'p2_method': '**HACH 8000', 'p2_unit': 'mg/L', 'p2_result': '70', 'p2_v0': '70', 'p2_v1': '170', 'p2_v2': '69', 'p2_limit': '150', 'p2_u': '2.441',
                'p3_on': '1', 'p3_parameter': 'TDS', 'p3_unit': 'mg/L', 'p3_v0': '2040', 'p3_limit': '-'}          # TDS: no limit -> error, not created
        r = chem.post('/qc/soc/new/?location=Karachi', post, follow=True)
        self.assertContains(r, 'specification limit'); self.assertEqual(SocRecord.objects.count(), 2)
        ph = SocRecord.objects.get(parameter='pH'); cod = SocRecord.objects.get(parameter='COD')
        self.assertEqual((ph.status, ph.overall, ph.mou_study.parameter, round(ph.mean, 4)), ('draft', 'Pass', 'pH', 7.3633))
        self.assertEqual((cod.verdicts, cod.overall, cod.lower, cod.upper), (['Pass', 'Fail', 'Pass'], 'Fail', None, 150.0))
        # duplicate guarded
        chem.post('/qc/soc/new/?location=Karachi', post); self.assertEqual(SocRecord.objects.count(), 2)
        r = chem.get('/qc/soc/%d/' % ph.pk); self.assertContains(r, 'Statement: Pass'); self.assertContains(r, 'Sign as performed'); self.assertContains(r, '<svg')
        # Lahore staff cannot sign Karachi; chemist signs; manager reviews; CEO approves
        self.assertEqual(lchem.post('/qc/soc/%d/action/' % ph.pk, {'action': 'perform'}).status_code, 403)
        chem.post('/qc/soc/%d/action/' % ph.pk, {'action': 'perform'}); ph.refresh_from_db(); self.assertEqual((ph.status, ph.performed_by_id), ('performed', self.chem.pk))
        self.assertEqual(chem.post('/qc/soc/%d/action/' % ph.pk, {'action': 'review'}).status_code, 403)
        self.assertEqual(chem.get('/qc/soc/%d/edit/' % ph.pk).status_code, 403)                 # a chemist cannot edit after signing
        mgr.post('/qc/soc/%d/action/' % ph.pk, {'action': 'review'}); ph.refresh_from_db(); self.assertEqual(ph.status, 'reviewed')
        self.assertEqual(mgr.post('/qc/soc/%d/action/' % ph.pk, {'action': 'approve'}).status_code, 403)
        ceo.post('/qc/soc/%d/action/' % ph.pk, {'action': 'approve'}); ph.refresh_from_db(); self.assertEqual((ph.status, ph.locked), ('approved', True))
        self.assertEqual(mgr.get('/qc/soc/%d/edit/' % ph.pk).status_code, 403)
        # manager edits the COD draft; a reviewed record edited by the manager goes back to draft
        r = mgr.post('/qc/soc/%d/edit/' % cod.pk, {'parameter': 'COD', 'method': 'HACH 8000', 'unit': 'mg/L', 'standard': cod.standard, 'limit_text': '150', 'upper': '150', 'uncertainty': '2.441',
                                                     'v0': '70', 'd0': '20-10-2026', 'v1': '70', 'v2': '69', 'decision_rule': SocRecord.RULE})
        cod.refresh_from_db(); self.assertEqual((cod.overall, cod.values), ('Pass', [70.0, 70.0, 69.0]))
        # sample-level actions and PDFs
        chem.post('/qc/soc/sample/WW-202610001/action/?location=Karachi', {'action': 'perform'}); cod.refresh_from_db(); self.assertEqual(cod.status, 'performed')
        mgr.post('/qc/soc/sample/WW-202610001/action/?location=Karachi', {'action': 'review'}); ceo.post('/qc/soc/sample/WW-202610001/action/?location=Karachi', {'action': 'approve'})
        cod.refresh_from_db(); self.assertEqual(cod.status, 'approved')
        for u in ('/qc/soc/%d/pdf/' % ph.pk, '/qc/soc/sample/WW-202610001/pdf/?location=Karachi', '/qc/soc/?location=Karachi&show=approved', '/qc/soc/?location=Karachi&show=all'):
            self.assertEqual(chem.get(u).status_code, 200, u)
        r = chem.get('/qc/soc/?location=Karachi&show=approved'); self.assertContains(r, 'Result = Pass')
        # unapprove / return / delete
        self.assertContains(ceo.post('/qc/soc/%d/action/' % ph.pk, {'action': 'unapprove', 'reason': 'x'}, follow=True), 'at least 5')
        ceo.post('/qc/soc/%d/action/' % ph.pk, {'action': 'unapprove', 'reason': 'recheck U'}); ph.refresh_from_db(); self.assertEqual(ph.status, 'reviewed')
        mgr.post('/qc/soc/%d/action/' % ph.pk, {'action': 'return', 'reason': 'repeat result 3'}); ph.refresh_from_db(); self.assertEqual((ph.status, ph.performed_by_id), ('draft', None))
        self.assertEqual(chem.post('/qc/soc/%d/delete/' % ph.pk, {'reason': 'entered twice'}).status_code, 403)
        mgr.post('/qc/soc/%d/delete/' % ph.pk, {'reason': 'entered twice'})
        self.assertFalse(SocRecord.objects.filter(pk=ph.pk).exists()); self.assertEqual(ControlChartDeletion.objects.get(kind='soc').location, 'Karachi')
        self.assertContains(mgr.get('/qc/soc/deleted/?location=Karachi'), 'entered twice')
        self.assertEqual(chem.get('/qc/soc/deleted/?location=Karachi').status_code, 403)

    def test_request_form(self):
        chem, mgr = C(self.chem), C(self.mgr)
        r = chem.get('/qc/soc/request/new/?location=Karachi&sample=DW-202610002')
        self.assertContains(r, 'Soorty Test'); self.assertContains(r, 'Alkalinity')
        r = chem.post('/qc/soc/request/new/?location=Karachi', {'sample_id': 'DW-202610002', 'date': '21-10-2026', 'reason': 'SEQS', 'organization': 'Soorty Test', 'customer_name': 'Mr B',
                                                                 'analysis': 'dw', 'parameters': 'pH, TDS', 'req_mou': '1', 'req_soc': '1', 'reporting': 'SEQS limits'})
        q = SocRequest.objects.get(sample_id='DW-202610002'); self.assertEqual((q.analysis, q.req_soc, q.decision), ('dw', True, ''))
        self.assertContains(chem.post('/qc/soc/request/new/?location=Karachi', {'sample_id': 'DW-202610002', 'date': '21-10-2026'}, follow=True), 'exists already')
        self.assertEqual(chem.post('/qc/soc/request/%d/action/' % q.pk, {'action': 'authorise'}).status_code, 403)
        mgr.post('/qc/soc/request/%d/action/' % q.pk, {'action': 'authorise'}); q.refresh_from_db()
        self.assertEqual((q.decision, q.authorised_by_id, q.locked), ('approved', self.mgr.pk, True))
        self.assertEqual(chem.get('/qc/soc/request/%d/edit/' % q.pk).status_code, 403)
        self.assertEqual(chem.get('/qc/soc/request/%d/pdf/' % q.pk).status_code, 200)
        # records made afterwards link to the request
        chem.post('/qc/soc/new/?location=Karachi', {'sample_id': 'DW-202610002', 'report_type': 'dw', 'p0_on': '1', 'p0_parameter': 'pH', 'p0_v0': '7.0', 'p0_limit': '6.5 - 8.5'})
        self.assertEqual(SocRecord.objects.get(parameter='pH').request_id, q.pk)
        self.assertContains(chem.get('/qc/soc/request/%d/' % q.pk), 'pH')

    def test_induction_and_doc_control(self):
        ceo, chem = C(self.ceo), C(self.chem)
        out = io.StringIO(); call_command('import_soc_spec', SPEC, '--apply', stdout=out)
        self.assertIn('requests 2, records 9', out.getvalue())
        out = io.StringIO(); call_command('import_soc_spec', SPEC, '--apply', stdout=out); self.assertIn('skipped 11', out.getvalue())
        rec = SocRecord.objects.get(sample_id='WW-202405120', parameter='COD')
        self.assertEqual((rec.status, rec.overall, rec.inducted, round(rec.sd, 4), rec.request.organization[:8]), ('approved', 'Pass', True, 0.5774, 'Artistic'))
        self.assertEqual(SocRecord.objects.get(sample_id='DW-202409012', parameter='Nickel').overall, 'Pass')
        for u in ('/qc/soc/%d/' % rec.pk, '/qc/soc/%d/pdf/' % rec.pk, '/qc/soc/sample/DW-202409012/pdf/?location=Karachi', '/qc/soc/sample/WW-202405120/pdf/?location=Karachi',
                  '/qc/soc/request/%d/' % rec.request.pk, '/qc/soc/request/%d/pdf/' % rec.request.pk, '/qc/soc/manual/', '/qc/qc_main/', '/qc/document-control/'):
            self.assertEqual(chem.get(u).status_code, 200, u)
        self.assertContains(chem.get('/qc/qc_main/'), 'Decision Rule')
        # document control: Karachi and Lahore print their own numbers
        from EnviTechAlApp.doccontrol import doc_control
        self.assertEqual(doc_control('soc_record', 'Karachi')['doc_no'], 'ETAL-LAB-708-FF-20')
        self.assertEqual(doc_control('soc_request', 'Lahore')['issue_date'], '09-03-2026')
        self.assertEqual(doc_control('soc_report_ww', 'Lahore')['doc_no'], 'ETAL-LAB-708-FF-18')
        self.assertEqual(doc_control('soc_report_ww', 'Karachi')['doc_no'], 'TBA')
        self.assertEqual(chem.get('/qc/soc/doc-control/').status_code, 403)
        self.assertEqual(ceo.get('/qc/soc/doc-control/').status_code, 200)
        self.assertEqual(chem.get('/qc/soc/sample/NOPE/pdf/?location=Karachi').status_code, 404)

    def test_corrections_and_below_loq(self):
        call_command('import_soc_spec', SPEC, '--apply', stdout=io.StringIO())
        corr = os.path.join(os.path.dirname(__file__), 'fixtures', 'soc_karachi_corrections.json')
        out = io.StringIO(); call_command('correct_soc_spec', corr, stdout=out)
        self.assertIn('DRY RUN', out.getvalue())
        self.assertEqual(SocRecord.objects.get(sample_id='WW-202405120', parameter='COD').uncertainty, 2.441)     # dry run rolled back
        out = io.StringIO(); call_command('correct_soc_spec', corr, '--apply', stdout=out)
        self.assertIn('corrected 8, added 1', out.getvalue())
        out = io.StringIO(); call_command('correct_soc_spec', corr, '--apply', stdout=out)
        self.assertIn('corrected 0, added 0, skipped 9', out.getvalue())
        cod = SocRecord.objects.get(sample_id='WW-202405120', parameter='COD')
        self.assertEqual((cod.uncertainty, cod.status), (1.341, 'approved'))
        self.assertIn('2.441 -> 1.341', cod.remarks)
        self.assertEqual(cod.history.first().uncertainty, 1.341); self.assertEqual(cod.history.last().uncertainty, 2.441)
        ni = SocRecord.objects.get(sample_id='DW-202409012', parameter='Nickel')
        self.assertEqual(([SocRecord.result_text(r) for r in ni.results], ni.mean_text, ni.sd_text, ni.overall, ni.uncertainty),
                         (['<0.0080'] * 3, '<0.0080', '-', 'Pass', 0.017))
        no3 = SocRecord.objects.get(sample_id='DW-202409012', parameter='Nitrate')
        self.assertEqual((no3.overall, no3.sd_text, no3.paper_sign_text), ('Pass', '-', 'Signed on the issued test report'))
        self.assertEqual(SocRecord.objects.get(sample_id='DW-202409012', parameter='pH').upper, 9)
        chem = C(self.chem)
        r = chem.get('/qc/soc/%d/' % ni.pk); self.assertContains(r, '&lt;0.0080'); self.assertContains(r, 'Correction 26-10-2026')
        self.assertContains(chem.get('/qc/soc/%d/' % no3.pk), 'Signed on the issued test report')
        for u in ('/qc/soc/%d/pdf/' % ni.pk, '/qc/soc/%d/pdf/' % no3.pk, '/qc/soc/sample/DW-202409012/pdf/?location=Karachi'):
            self.assertEqual(chem.get(u).status_code, 200, u)
        # parsing: a below-LOQ report result is offered and judged at the LOQ
        self.assertEqual(R.parse_result('<0.0080'), (0.008, '<0.0080'))
        self.assertEqual(R.parse_result('N.D.'), (None, ''))
        self.assertEqual(R.parse_result('7.36'), (7.36, ''))
