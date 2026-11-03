"""R14 (Lab Manager Karachi, e-mail 03-11-2026): point 7 - the WS / RM / CRM checks work each reading from the raw data
with the parameter section's formula; point 8 - the RDS being entered is saved as a draft (server and browser) and can
be resumed; saving the RDS removes its draft."""
import json
import os

from django.contrib.auth.models import User
from django.test import TestCase, Client, SimpleTestCase

from EnviTechAlApp.models import DrinkingWaterForm, Sample_registration
from QC.models import RdsDraft, Dw_rds
from QC.tests_rds_r1 import KW
from QC.tests_rds_r13 import new_pdf
from QC.tests_rds_r135 import pdf_text

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = lambda *p: open(os.path.join(ROOT, *p), encoding='utf-8').read()


class RdsR14Drafts(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.u = User.objects.create_superuser('r14_a', 'a@x.c', 'x')
        cls.v = User.objects.create_superuser('r14_b', 'b@x.c', 'x')
        DrinkingWaterForm.objects.create(sample_id='DW-R14', lab_report_no='R14', city_location='Lahore', extra_field='[]', **KW)
        Sample_registration.objects.create(sample_id='DW-R14', city_location='Lahore', checkinp95=True)

    def client_for(self, u):
        c = Client(REMOTE_ADDR='127.0.0.1'); c.force_login(u); return c

    def post(self, c, url, body):
        return c.post(url, json.dumps(body), content_type='application/json')

    def test_save_list_get_delete_and_privacy(self):
        a, b = self.client_for(self.u), self.client_for(self.v)
        payload = {'v': 1, 'sample_id': 'DW-R14', 'fields': [['parameter_1', 'pH*'], ['result_1', '7.2']], 'subs': [], 'blocks': [], 'cards': []}
        r = self.post(a, '/qc/rds_draft/save/', {'kind': 'dw', 'page': 'add', 'sample_id': 'DW-R14', 'payload': payload})
        self.assertEqual(r.status_code, 200); self.assertEqual(r.json()['status'], 'ok')
        self.post(a, '/qc/rds_draft/save/', {'kind': 'dw', 'page': 'add', 'sample_id': 'DW-R14', 'payload': dict(payload, saved='x')})
        self.assertEqual(RdsDraft.objects.filter(user=self.u).count(), 1)                 # replaced, not added
        self.assertEqual([d['sample_id'] for d in a.get('/qc/rds_draft/list/?kind=dw&page=add').json()['drafts']], ['DW-R14'])
        self.assertEqual(b.get('/qc/rds_draft/list/?kind=dw&page=add').json()['drafts'], [])          # another user's draft is not listed
        self.assertEqual(b.get('/qc/rds_draft/get/?kind=dw&page=add&sample_id=DW-R14').json()['status'], 'none')
        g = a.get('/qc/rds_draft/get/?kind=dw&page=add&sample_id=DW-R14').json()
        self.assertEqual(g['payload']['fields'][1], ['result_1', '7.2'])
        self.assertEqual(self.post(a, '/qc/rds_draft/save/', {'kind': 'xx', 'page': 'add', 'sample_id': 'DW-R14', 'payload': {}}).status_code, 400)
        self.post(a, '/qc/rds_draft/delete/', {'kind': 'dw', 'page': 'add', 'sample_id': 'DW-R14'})
        self.assertFalse(RdsDraft.objects.exists())

    def test_saving_the_rds_removes_its_draft(self):
        a = self.client_for(self.u)
        self.post(a, '/qc/rds_draft/save/', {'kind': 'dw', 'page': 'add', 'sample_id': 'DW-R14', 'payload': {'v': 1}})
        self.post(a, '/qc/rds_draft/save/', {'kind': 'dw', 'page': 'manual', 'sample_id': 'DW-R14', 'payload': {'v': 1}})
        self.assertEqual(RdsDraft.objects.count(), 2)
        r = self.post(a, '/qc/create_dw_qc/', {'sample_id': 'DW-R14', 'date_1': '20-Oct-2026', 'parameter_1': 'pH*', 'result_1': '7.2'})
        self.assertIn(r.status_code, (200, 302))
        self.assertTrue(Dw_rds.objects.filter(sample_id='DW-R14').exists())
        self.assertFalse(RdsDraft.objects.exists())

    def test_old_drafts_removed_after_7_days(self):
        from datetime import timedelta
        from django.utils import timezone
        a = self.client_for(self.u)
        self.post(a, '/qc/rds_draft/save/', {'kind': 'dw', 'page': 'add', 'sample_id': 'DW-R14', 'payload': {'v': 1}})
        RdsDraft.objects.update(updated_at=timezone.now() - timedelta(days=8))
        self.assertEqual(a.get('/qc/rds_draft/list/?kind=dw&page=add').json()['drafts'], [])
        self.assertFalse(RdsDraft.objects.exists())

    def test_login_required(self):
        r = Client(REMOTE_ADDR='127.0.0.1').get('/qc/rds_draft/list/?kind=dw&page=add')
        self.assertNotEqual(r.status_code, 200)


class RdsR14Pages(SimpleTestCase):
    def test_pages_and_scripts(self):
        for page in ('rds_dw', 'rds_ww', 'rds_dw_manual', 'rds_ww_manual'):
            self.assertIn("rds_draft.js' %}?v=20261103b", src('templates', page + '.html'))
        js = src('static', 'js', 'rds_qc.js')
        for key in ("key: 'cl'", "key: 'grav'", "key: 'sulphide'", "key: 'bod'", "key: 'df'", "key: 'acid'"):
            self.assertIn(key, js)
        self.assertIn('if (!tlines.length) tlines = frmLines(blk);', js)
        d = src('static', 'js', 'rds_draft.js')
        for s in ('/qc/rds_draft/save/', 'localStorage', 'pagehide', 'Resume', '.add-row-btn', '.generate-crm-btn', '.rl-addbtn'):
            self.assertIn(s, d)


class RdsR14CrmPrint(SimpleTestCase):
    def test_formula_reading_lines_print_as_fractions(self):
        from QC.rds_pdf_extras import install_df, flush_df
        crm = {'type': 'CRM', 'parameter': 'Chloride', 'side': '', 'unit': 'mg/L', 'readings': ['70.9', '', ''], 'true_value': '70', 'mean': '70.9 (n = 1)',
               'result': '101.3', 'verdict': 'Within acceptance',
               'work': ['Normality of AgNO3 N = 0.0141', 'Reading 1 = [(12.7 - 12.3) - (0.2 - 0.1)] X 0.0141 X 35450 / 100 = 1.4996',
                        'Mean = 1.4996 = 1.4996 mg/L', 'Recovery = 1.4996 / 1.5 X 100 = 100 %']}
        d = {'parameter_1': 'Chloride', 'parameter_1_1': 'Chloride CRM', 'qc_print_001': json.dumps(crm)}
        pdf = new_pdf(); install_df(pdf, d)
        pdf.set_font('Calibri', 'B', 11); pdf.cell(0, 6, 'Chloride Calculation:', ln=True)
        pdf.set_font('Calibri', 'B', 11); pdf.cell(0, 6, 'Fluoride Calculation:', ln=True)
        flush_df(pdf)
        t = pdf_text(pdf)
        self.assertIn('Chloride CRM Calculations', t); self.assertIn('Normality of AgNO3 N = 0.0141', t); self.assertIn('Reading 01', t)
        self.assertIn('[(12.7 - 12.3) - (0.2 - 0.1)] X 0.0141 X 35450 = 1.4996', t); self.assertIn('Result = 1.4996 mg/L', t)
        self.assertNotIn('Recovery', t)
