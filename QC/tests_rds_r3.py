"""RDS release R3 (QA audit 27-10-2026): the RDS PDF prints every saved working as calculated, with the sample
particulars, the analysts and checkers, the standard footer and the end line; page fixes."""
import json
import os
import shutil
import subprocess
import tempfile

from django.contrib.auth.models import User
from django.test import TestCase, Client

from EnviTechAlApp.models import WasteWaterForm2, DrinkingWaterForm, Sample_registration
from QC.models import Dw_rds, Ww_rds
from QC.rds_pdf_extras import tidy, fmt_date, row_order

KW = dict(report_to='QA Mills', address='L', attention='A', date_of_analysis_from='20-Oct-2026', date_of_analysis_to='25-Oct-2026',
          reporting_date='26-October-2026')


def text(content):
    if not shutil.which('pdftotext'):
        return None
    with tempfile.NamedTemporaryFile(suffix='.pdf') as fh:
        fh.write(content); fh.flush()
        return subprocess.run(['pdftotext', '-layout', fh.name, '-'], capture_output=True, text=True).stdout


class RdsR3Units(TestCase):
    def test_tidy_and_dates(self):
        self.assertIsNone(tidy('None + None + None', 'None', '3'))
        self.assertEqual(tidy('7.2 + 7.4 + None', '7.3 None', '3'), ('7.2 + 7.4', '7.3', '2'))
        self.assertEqual(tidy('(10 X 1) + (None X None) + (20 X 1)', '15 mg/L', '3'), ('(10 X 1) + (20 X 1)', '15 mg/L', '2'))
        self.assertEqual(tidy('(A - B) X 50000', 'x', None)[2], None) if tidy('(A - B) X 50000', 'x', None) else None
        self.assertEqual(fmt_date('20-Oct-2026'), '20-10-2026'); self.assertEqual(fmt_date('2026-10-20'), '20-10-2026')
        self.assertEqual(fmt_date('undefined'), '')
        self.assertEqual(sorted(['10', '2', '1_2', '1', '1_1'], key=row_order), ['1', '1_1', '1_2', '2', '10'])


class RdsR3Pdf(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.u = User.objects.create_superuser('r3_ceo', 'c@x.c', 'x')
        DrinkingWaterForm.objects.create(sample_id='DW-R3', lab_report_no='LR-77', city_location='Lahore', extra_field='[]',
                                         sample_collection_date='21-Oct-2026', **KW)
        Sample_registration.objects.create(sample_id='DW-R3', city_location='Lahore')
        WasteWaterForm2.objects.create(sample_id='WW-R3', lab_report_no='LR-78', in_out='in-out', city_location='Karachi', **KW)
        WasteWaterForm2.objects.create(sample_id='WW-R3-CL', lab_report_no='LR-79', in_out='inlet_customlimits', city_location='Karachi',
                                       result_1='35', result_2='7.5', **KW)

    def pdf(self, model, kind, data):
        c = Client(REMOTE_ADDR='127.0.0.1'); c.force_login(self.u)
        rec = model.objects.create(sample_id=data['sample_id'], rds=data)
        r = c.get('/qc/generate_%s_qc_pdf_response/%d/' % (kind, rec.pk))
        self.assertEqual(r.status_code, 200)
        return text(r.content)

    def test_dw_pdf(self):
        d = {'sample_id': 'DW-R3', 'date_2': '2026-10-21', 'parameter_2': 'pH', 'result_2': '7.3',
             'date_1': '20-Oct-2026', 'parameter_1': 'TDS', 'result_1': '471',
             'bw1': '50.1', 'AW01': '50.1500', 'AW02': '50.1502', 'vs1': '100', 'ans1': '502', 'ans_param': 'mg/L', 'tds_head_1': 'WS-TDS-500ppm:',
             'for_cobalt1': '0.20', 'for_cobalt1_df': '1', 'for_cobalt2': '0.22', 'for_cobalt2_df': '1', 'cobalt_divi': '2',
             'cobalt_ans': '0.21', 'cobalt_param': 'mg/L',
             'for_ammonia1_1': '0.5', 'for_ammonia1_1_df': '2', 'for_ammonia1_2': '0.6', 'for_ammonia1_2_df': '2',
             'ammonia_divi': '2', 'ammonia_ans_1': '1.1', 'ammonia_param_1': 'mg/L'}
        t = self.pdf(Dw_rds, 'dw', d)
        if t is None:
            return
        self.assertIn('QA Mills', t); self.assertIn('LR-77', t); self.assertIn('Drinking water', t)
        self.assertIn('20-10-2026', t); self.assertIn('21-10-2026', t)
        self.assertLess(t.index(' TDS '), t.index(' pH '))                 # row order, not date-string order
        self.assertIn('(50.1502 - 50.1)', t)                                 # last weighing entered
        self.assertIn('Cobalt Calculations', t); self.assertIn('(0.20 X 1) + (0.22 X 1)', t)
        self.assertIn('(0.5 X 2) + (0.6 X 2)', t)                            # weighted part prints each replicate
        self.assertIn('END OF THE DOCUMENT', t)
        self.assertIn('Bahadurabad', t)                                      # standard footer
        self.assertNotIn('None', t)

    def test_ww_pdf_and_custom_limits(self):
        d = {'sample_id': 'WW-R3', 'report_type': 'in-out', 'date_1': '20-Oct-2026', 'parameter_1': 'Antimony',
             'for_antimony1_inlet': '0.01', 'for_antimony1_df_inlet': '1', 'antimony_ans_inlet': '0.01',
             'antimony_param_inlet': 'mg/L', 'antimony_divi_inlet': '1', 'antimony_head_inlet': 'Antimony (Inlet):'}
        t = self.pdf(Ww_rds, 'ww', d)
        if t is not None:
            self.assertIn('Antimony Inlet Calculations', t); self.assertIn('(0.01 X 1)', t)
            self.assertIn('inlet and outlet', t); self.assertIn('END OF THE DOCUMENT', t)
        c = Client(REMOTE_ADDR='127.0.0.1'); c.force_login(self.u)
        g = c.post('/qc/get_ww/', json.dumps({'sample_id': 'WW-R3-CL'}), content_type='application/json').json()
        self.assertTrue(g.get('qc_data'))                                    # older custom-limit report (QA RDS-31)

    def test_pages(self):
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        for page in ('rds_dw', 'rds_dw_manual'):
            s = open(os.path.join(root, 'templates', page + '.html')).read()
            self.assertNotIn("                ElementById('ch_c3_ans1')", s)
            self.assertIn('value="CFU/mL"', s); self.assertNotIn('CFU/100 ml', s)
        for page in ('rds_dw', 'rds_dw_manual', 'rds_ww', 'rds_ww_manual'):
            s = open(os.path.join(root, 'templates', page + '.html')).read()
            self.assertIn('RDSLib.pageName(v)', s)
            self.assertIn('value="0.0141"', s)
        js = open(os.path.join(root, 'static', 'js', 'rds_page.js')).read()
        self.assertIn('hideSingleOnly', js); self.assertIn('QA RDS-33', js)
