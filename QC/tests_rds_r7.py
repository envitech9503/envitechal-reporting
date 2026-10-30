"""RDS release R7 (full mock QA 28-10-2026): calculation sections kept in view, old result-only microbiology boxes
replaced by the library count cards, staff on WW manual inlet-only / outlet-only rows, PDF formula fixes."""
import os
import re
import shutil
import subprocess
import tempfile

from django.contrib.auth.models import User
from django.test import TestCase, Client

from EnviTechAlApp.models import WasteWaterForm2, DrinkingWaterForm, Sample_registration
from QC.models import Dw_rds, Ww_rds

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ('rds_dw', 'rds_dw_manual', 'rds_ww', 'rds_ww_manual')
KW = dict(report_to='QA Mills', address='L', attention='A', date_of_analysis_from='20-Oct-2026', date_of_analysis_to='25-Oct-2026',
          reporting_date='26-October-2026')


def src(*p):
    return open(os.path.join(ROOT, *p), encoding='utf-8').read()


def text(content):
    if not shutil.which('pdftotext'):
        return None
    with tempfile.NamedTemporaryFile(suffix='.pdf') as fh:
        fh.write(content); fh.flush()
        return subprocess.run(['pdftotext', '-layout', fh.name, '-'], capture_output=True, text=True).stdout


class RdsR7Pages(TestCase):
    def test_templates(self):
        for page in PAGES:
            s = src('templates', page + '.html')
            self.assertIsNone(re.search(r'<input[^>]*>\s*<p class="px-1">\s*\+\s*</p>\s*<p class="px-1">\s*X\s*</p>', s), page)
            self.assertIsNone(re.search(r'<p class="px-\d">\s*\)\s*</p>\s*<p class="px-\d">\s*\(\s*</p>', s), page)
            self.assertIsNone(re.search(r'id="(ferrous|freechlorine)_param"[^>]*value="TCU"', s), page)
            self.assertRegex(s, r"rds_qc.js' %}\?v=20261(02[89]|03[01])\w")
        m = src('templates', 'rds_ww_manual.html')
        self.assertIn('<option value="">Performed By</option>${sigOpts}', m)

    def test_js(self):
        page = src('static', 'js', 'rds_page.js')
        self.assertIn('#qcForm .flex{flex-wrap:wrap}', page); self.assertIn('#qcForm .w-min{width:auto!important', page)
        qc = src('static', 'js', 'rds_qc.js')
        for t in ('function legacyMicro()', 'function dfDefault()', 'negative result', 'is incomplete'):
            self.assertIn(t, qc)
        lib = src('static', 'js', 'rds_formula_lib.js')
        self.assertIn('cardFor(item.parameter, item.method, item.unit)', lib); self.assertIn('is not above the test report value', lib)   # wording 30-10-2026 (on screen only)


class RdsR7Pdf(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.u = User.objects.create_superuser('r7_ceo', 'c@x.c', 'x')
        DrinkingWaterForm.objects.create(sample_id='DW-R7', lab_report_no='LR-97', city_location='Lahore', extra_field='[]',
                                         sample_collection_date='21-Oct-2026', **KW)
        Sample_registration.objects.create(sample_id='DW-R7', city_location='Lahore')
        WasteWaterForm2.objects.create(sample_id='WW-R7', lab_report_no='LR-98', in_out='in-out', city_location='Karachi', **KW)

    def pdf(self, model, kind, data):
        c = Client(REMOTE_ADDR='127.0.0.1'); c.force_login(self.u)
        rec = model.objects.create(sample_id=data['sample_id'], rds=data)
        r = c.get('/qc/generate_%s_qc_pdf_response/%d/' % (kind, rec.pk))
        self.assertEqual(r.status_code, 200)
        return text(r.content)

    def test_dw(self):
        d = {'sample_id': 'DW-R7', 'date_1': '20-Oct-2026', 'parameter_1': 'Ammonium', 'result_1': '5.1',
             'for_ammonium1_1': '5.0', 'for_ammonium1_1_df': '1', 'for_ammonium1_2': '5.1', 'for_ammonium1_2_df': '1',
             'for_ammonium1_3': '5.2', 'for_ammonium1_3_df': '1', 'ammonium_ans_1': '5.1', 'ammonium_param_1': 'mg/L', 'ammonium_divi': '3',
             'chloride_reading_1': 'Reading 01', 'chloride_1_1': '9.9', 'chloride_1_2': '1.2', 'chloride_1_3': '0.6', 'chloride_1_4': '0.1',
             'chloride_1_5': '0.0141', 'chloride_1_6': '100', 'chloride_ans1': '40.99', 'chloride_param1': 'mg/L', 'chloride_head': 'Chloride:'}
        t = self.pdf(Dw_rds, 'dw', d)
        if t is None:
            return
        self.assertIn('(5.0 X 1) + (5.1 X 1) + (5.2 X 1) = 5.1', t)
        self.assertIn('[(9.9 - 1.2) - (0.6 - 0.1)] X 0.0141 X 35450', t)
        self.assertNotIn('None', t)

    def test_ww_ph_outlet(self):
        d = {'sample_id': 'WW-R7', 'report_type': 'in-out', 'date_1': '20-Oct-2026', 'parameter_1': 'pH', 'inlet_1': '7.3', 'outlet_1': '7.23',
             'ph_head_4_outlet': 'Sample pH (Outlet):', 'for_ph1_outlet_sample': '7.20', 'for_ph2_outlet_sample': '7.30',
             'for_ph3_outlet_sample': '7.20', 'ph_ans_4_outlet': '7.23', 'ph_divi_4_outlet': '3'}
        t = self.pdf(Ww_rds, 'ww', d)
        if t is not None:
            self.assertIn('7.20 + 7.30 + 7.20 = 7.23', t); self.assertNotIn(' +  + ', t)

    def test_dw_sample_ph_only(self):
        d = {'sample_id': 'DW-R7', 'date_1': '20-Oct-2026', 'parameter_1': 'pH', 'result_1': '7.3', 'ph_head_1': 'WS-pH-4.005:',
             'ph_head_4': 'pH:', 'for4_ph1': '7.20', 'for4_ph2': '7.30', 'for4_ph3': '7.40', 'ph_ans_4': '7.3', 'ph_divi_4': '3'}
        t = self.pdf(Dw_rds, 'dw', d)
        if t is not None:
            self.assertIn('7.20 + 7.30 + 7.40 = 7.3', t); self.assertNotIn(' +  + ', t)

    def test_manual_signatures_fresh(self):
        c = Client(REMOTE_ADDR='127.0.0.1'); c.force_login(self.u)
        for url in ('/qc/create_dw_qc_manual/', '/qc/create_ww_qc_manual/'):
            self.assertEqual(c.get(url, secure=True, HTTP_X_FORWARDED_PROTO='https').status_code, 200)
        self.assertIn('_signs = Signatures.objects.filter(user__is_active=True)', src('QC', 'views', 'dw.py'))
        self.assertIn('set_y(max(old_y, 35))', src('QC', 'views', 'core.py'))
