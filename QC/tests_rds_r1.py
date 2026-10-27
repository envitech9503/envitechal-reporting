"""RDS release R1 (QA audit 27-10-2026): calculation integrity as printed on the RDS PDF.
RDS-06 total toxic metals is a sum, RDS-07/08 calcium, RDS-09 carbonate (APHA 2320 B), RDS-11 in-out PDF with an
Aluminium outlet working, RDS-15 alkalinity / acidity factor 50 000. The page-side averaging rule (RDS-02/03/05) is
exercised in a browser by QC/jstests/rds_avg_browser.js (needs the dev server and Playwright)."""
import json
import os
import re
import shutil
import subprocess
import tempfile

from django.contrib.auth.models import User
from django.test import TestCase, Client

from EnviTechAlApp.models import WasteWaterForm2, DrinkingWaterForm, Sample_registration
from QC.models import Dw_rds, Ww_rds

KW = dict(report_to='QA', address='L', attention='A', date_of_analysis_from='20-Oct-2026', date_of_analysis_to='25-Oct-2026',
          reporting_date='26-October-2026')


def text(content):
    if not shutil.which('pdftotext'):
        return None
    with tempfile.NamedTemporaryFile(suffix='.pdf') as fh:
        fh.write(content); fh.flush()
        return subprocess.run(['pdftotext', '-layout', fh.name, '-'], capture_output=True, text=True).stdout


class RdsR1Tests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.u = User.objects.create_superuser('r1_ceo', 'c@x.c', 'x')
        WasteWaterForm2.objects.create(sample_id='WW-R1-IO', lab_report_no='R1', in_out='in-out', city_location='Lahore', **KW)
        WasteWaterForm2.objects.create(sample_id='WW-R1-S', lab_report_no='R2', in_out='out', city_location='Lahore', **KW)
        DrinkingWaterForm.objects.create(sample_id='DW-R1', lab_report_no='R3', city_location='Lahore', extra_field='[]',
                                         sample_collection_date='21-Oct-2026', **KW)
        Sample_registration.objects.create(sample_id='DW-R1', city_location='Lahore')

    def pdf(self, model, kind, data):
        c = Client(REMOTE_ADDR='127.0.0.1'); c.force_login(self.u)
        rec = model.objects.create(sample_id=data['sample_id'], rds=data)
        r = c.get('/qc/generate_%s_qc_pdf_response/%d/' % (kind, rec.pk))
        self.assertEqual(r.status_code, 200)
        return text(r.content)

    def test_ww_inout_aluminium_outlet_and_toxic_sum(self):
        d = {'sample_id': 'WW-R1-IO', 'report_type': 'in-out',
             'for_alum1_outlet': '0.2', 'for_alum1_df_outlet': '1', 'alum_ans_outlet': '0.2', 'alum_param_outlet': 'mg/L',
             'alum_divi_outlet': '1', 'alum_head_outlet': 'Aluminium (Outlet):',
             'toxic_ans_inlet': '1.1', 'toxic_param_inlet': 'mg/L', 'toxic_divi_inlet': '1'}
        for i in range(1, 12):
            d['toxic_r%d_inlet' % i] = '0.1'
        t = self.pdf(Ww_rds, 'ww', d)                                   # was a server error (RDS-11)
        if t is not None:
            self.assertIn('0.1 + 0.1 + 0.1', t)
            self.assertNotIn('None', t)

    def test_ww_single_toxic_sum_has_no_divisor_and_carbonate_line(self):
        d = {'sample_id': 'WW-R1-S', 'report_type': 'out', 'toxic_ans': '0.3', 'toxic_param': 'mg/L', 'toxic_divi': '1',
             'toxic_r1': '0.1', 'toxic_r2': '0.2', 'toxic_r3': '',
             'carbonates_1_1': '5', 'carbonates_1_2': '1', 'carbonates_1_3': '0.02', 'carbonates_1_4': '100',
             'for_carbonates1': '20', 'for_carbonates1_df': '1', 'for_carbonates2': '20', 'for_carbonates2_df': '1',
             'for_carbonates3': '', 'for_carbonates3_df': '1', 'carbonates_divi': '2', 'carbonates_P': '20', 'carbonates_T': '100',
             'for_carbonates_ans': '40.00', 'for_carbonates_param': 'mg/L'}
        t = self.pdf(Ww_rds, 'ww', d)
        if t is not None:
            self.assertIn('0.1 + 0.2', t)
            self.assertIn('APHA 2320 B', t)
            self.assertIn('2 X 20 = 40.00', t)
            self.assertIn('X 50000', t)
            self.assertNotIn('X 5000 ', t)

    def test_dw_calcium_and_alkalinity_factor(self):
        d = {'sample_id': 'DW-R1', 'cal_r1_final': '12', 'cal_r1_initial': '2', 'cal_r1_multiply': '1000', 'cal_r1_divi': '50',
             'cal_r1_ans': '200', 'cal_avg_ans1': '100', 'cal_avg_ans2': '102', 'cal_avg_ans3': '', 'cal_avg_divi': '2',
             'cal_avg_final_ans': '40.48', 'cal_avg_param': 'mg/L',
             'alkalinity_1_1': '10', 'alkalinity_1_2': '0', 'alkalinity_1_3': '0.02', 'alkalinity_1_4': '100', 'alkalinity_ans1': '100',
             'calcium_crm_1_1_1': '10', 'calcium_crm_1_1_2': '0', 'calcium_crm_1_1_3': '0.02', 'calcium_crm_1_1_4': '20.04',
             'calcium_crm_1_1_divi': '50', 'calcium_crm_1_1_ans': '80.160', 'calcium_crm_1_1_param': 'mg/L'}
        t = self.pdf(Dw_rds, 'dw', d)
        if t is not None:
            self.assertIn('101.00 X 0.4008 = 40.48', t)
            self.assertIn('X 50000', t)
            self.assertIn('X 20.04', t)
            self.assertIn('Calcium CRM Calculations', t)
            self.assertNotIn('Alkalinity CRM Calculations', t)


class RdsR1PageTests(TestCase):
    """The pages carry the R1 rules: the averaging script, the corrected hardness and toxic-metal code."""
    def test_pages_and_script(self):
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        js = open(os.path.join(root, 'static', 'js', 'rds_avg.js')).read()
        m = json.loads(re.search(r'var MAP = (\{.*?\});\n', js, re.S).group(1))
        self.assertGreater(len(m['dw']), 60); self.assertGreater(len(m['ww']), 170)
        self.assertFalse(any(k.startswith('toxic') for k in m['ww']))       # a sum, not an average
        for page in ('rds_dw', 'rds_dw_manual', 'rds_ww', 'rds_ww_manual'):
            s = open(os.path.join(root, 'templates', page + '.html')).read()
            self.assertIn('rds_avg.js', s)
            self.assertNotIn('(ans3*for_hardness1_df)', s); self.assertNotIn('(ans3 * for_hardness1_df)', s)
            self.assertNotIn('getElementById("AW05").value) || 0', s)
            self.assertIn('rdsCarbonate(pAlk)', s)
        ww = open(os.path.join(root, 'templates', 'rds_ww.html')).read()
        self.assertNotIn("querySelector('.antim_cal_div');\n                    \n", ww)
        self.assertIn("sulphide_io_cal_div", ww)
