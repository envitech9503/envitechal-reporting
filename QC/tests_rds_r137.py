"""R13.7 (Lab Manager Karachi, e-mail 03-11-2026): metal CRM averages to 4 decimals (1); bicarbonate / carbonate /
hydroxide expressed as the ion or as CaCO3 by choice (3); "Free Carbon Di oxide" gets the free CO2 titration card (4);
WW matrix from the report's result column heading (5); Oil & Grease inlet working printed without a TSS CRM and
without the final average (6)."""
import os
import re

from django.contrib.auth.models import User
from django.test import TestCase, Client, SimpleTestCase

from EnviTechAlApp.models import WasteWaterForm2
from QC.models import Ww_rds
from QC.tests_rds_r1 import text, KW

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = lambda *p: open(os.path.join(ROOT, *p), encoding='utf-8').read()


class RdsR137Pages(SimpleTestCase):
    def test_metal_crm_four_decimals(self):
        js = src('static', 'js', 'rds_qc.js')
        self.assertIn('window.rdsCrmDp', js)
        rx = re.search(r"return /(.*)/i\.test\(String\(prefix", js).group(1)
        for p, dp in (('crm_nickel_crm_1_1', 4), ('silver_crm_2_1', 4), ('crm_chromium_vi_crm_3_1', 4), ('crm_calcium_crm_1_1', 3), ('fluoride_crm_1_1', 3)):
            self.assertEqual(4 if re.search(rx.replace('\\\\', '\\'), p, re.I) else 3, dp, p)
        for page in ('rds_dw', 'rds_ww', 'rds_dw_manual', 'rds_ww_manual'):
            s = src('templates', page + '.html')
            body = s[s.index('function performCRMCalculation(prefix)'):]
            body = body[:body.index('function performCRM', 40)]
            self.assertNotIn('result.toFixed(3)', body, page)
            self.assertIn('rdsCrmDp(prefix)', body)
            self.assertIn("rds_qc.js' %}?v=20261103a", s); self.assertIn("rds_formula_lib.js' %}?v=20261103a", s)

    def test_library_bicarbonate_choice_and_free_co2(self):
        js = src('static', 'js', 'rds_formula_lib.js')
        self.assertIn('class="rl-as"', js); self.assertIn('CaCO3 (mg/L as CaCO3)', js)
        rx = re.search(r"\[/(free \(co2[^\n]*?)/, 'co2', 'R'\]", js).group(1)
        for name in ('free carbon di oxide', 'free carbon dioxide', 'free co2', 'free carbon-dioxide'):
            self.assertTrue(re.search(rx, name), name)


class RdsR137Pdf(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.u = User.objects.create_superuser('r137_ceo', 'c@x.c', 'x')
        WasteWaterForm2.objects.create(sample_id='WW-R137', lab_report_no='R137', in_out='in', inlet_result='Test Results',
                                       city_location='Karachi', **KW)
        WasteWaterForm2.objects.create(sample_id='WW-R137-IO', lab_report_no='R137B', in_out='in-out', inlet_result='Equalization Tank',
                                       outlet_result='Final Discharge', city_location='Karachi', **KW)

    def pdf(self, data):
        c = Client(REMOTE_ADDR='127.0.0.1'); c.force_login(self.u)
        rec = Ww_rds.objects.create(sample_id=data['sample_id'], rds=data)
        r = c.get('/qc/generate_ww_qc_pdf_response/%d/' % rec.pk)
        self.assertEqual(r.status_code, 200)
        return text(r.content)

    def test_matrix_from_column_heading_and_og_single(self):
        t = self.pdf({'sample_id': 'WW-R137', 'report_type': 'in', 'date_1': '20-Oct-2026', 'parameter_1': 'Oil & Grease', 'result_1': '92',
                      'oil_head_1': 'Oil and Grease:', 'oil_iw1': '45.2000', 'oil_FW01': '45.2105', 'oil_FW02': '45.2100', 'oil_vs1': '100',
                      'oil_ans1': '92', 'oil_ans_param': 'mg/L'})
        if t is None:
            return
        self.assertIn('Waste water (Test Results)', t)
        self.assertIn('(45.2100 - 45.2000) X 1000000', t)      # the last final weight entered, no final average needed
        self.assertNotIn('None', t)

    def test_og_inlet_without_tss_crm(self):
        t = self.pdf({'sample_id': 'WW-R137-IO', 'report_type': 'in-out', 'date_1': '20-Oct-2026', 'parameter_1': 'Oil & Grease',
                      'inlet_1': '9', 'outlet_1': '5', 'oil_head_1_inlet': 'Oil and Grease Inlet:', 'oil_read_1_inlet': 'Reading 01',
                      'oil_iw1_inlet': '58.3211', 'oil_FW01_inlet': '58.3268', 'oil_FW02_inlet': '58.3246', 'oil_FW03_inlet': '58.3231',
                      'oil_FW04_inlet': '58.3224', 'oil_FW05_inlet': '58.3220', 'oil_vs1_inlet': '100', 'oil_ans1_inlet': '9',
                      'oil_ans_param_inlet': 'mg/L'})
        if t is None:
            return
        self.assertIn('Waste water (Equalization Tank and Final', t); self.assertIn('Discharge)', t)   # the value wraps in its column
        self.assertIn('Oil & Grease Calculation', t)
        self.assertIn('(58.3220 - 58.3211) X 1000000', t)
        self.assertNotIn('Average of Oil & Grease (Inlet)', t)
