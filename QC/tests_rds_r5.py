"""RDS release R5 (owner requests 27-10-2026): EDTA factor B (QA RDS-23), WW manual acidity (QA RDS-45), WW calcium
APHA 3500 Ca-B buttons (QA RDS-46), quality-control checks (WS / RM / CRM) on the page and the PDF, BOD triplicate,
DW anionic-surfactant working standard label."""
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
from QC.rds_pdf_extras import edta_b
from QC.rds_qc_pdf import checks
from QC.soc_rules import ACCREDITED

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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


QC_WS = {'type': 'WS', 'type_label': 'Working standard (WS)', 'parameter': 'Total Hardness', 'side': '', 'ident': 'WS-Hardness-100ppm',
         'true_value': '100', 'u': '', 'unit': 'mg/L', 'readings': ['98', '99', ''], 'mean': '98.5 (n = 2)', 'result': '98.5',
         'mode': 'rec', 'lo': '90', 'hi': '110', 'abs': '', 'verdict': 'Within acceptance'}


class RdsR5Units(TestCase):
    def test_edta_b(self):
        d = {'hardness_edta_b': '1.02', 'calcium_edta_b_inlet': '0.98', 'magnesium_edta_b': ' 1.000 ', 'hardness_edta_b_outlet': 'x'}
        self.assertEqual(edta_b(d, 'hardness_2_1'), ' X 1.02')
        self.assertEqual(edta_b(d, 'cal_r1_final_inlet'), ' X 0.98')
        self.assertEqual(edta_b(d, 'ch_r2_final'), '')                 # no calcium B on the single side
        self.assertEqual(edta_b(d, 'r1_1_final'), ' X 1.000')
        self.assertEqual(edta_b(d, 'hardness_3_1_outlet'), '')         # not a number
        self.assertEqual(edta_b({}, 'hardness_2_1'), '')               # records saved before R5

    def test_accredited_scope_same_as_soc(self):
        js = src('static', 'js', 'rds_qc.js')
        block = js[js.index('var ACCREDITED = {'):js.index('};', js.index('var ACCREDITED = {'))]
        found = {tuple(k.split('|')): set(re.findall(r"'([^']+)'", v)) for k, v in re.findall(r"'([A-Za-z]+\|[a-z0-9]+)': \[([^\]]*)\]", block)}
        self.assertEqual(found, {k: set(v) for k, v in ACCREDITED.items()})

    def test_qc_checks_parse(self):
        self.assertEqual(len(checks({'qc_print_001': json.dumps(QC_WS), 'qc_print_002': '', 'qc_print_003': 'bad',
                                     'qc_print_004': json.dumps(dict(QC_WS, readings=['', '', '']))})), 1)


class RdsR5Pages(TestCase):
    def test_templates(self):
        for page in ('rds_dw', 'rds_dw_manual', 'rds_ww', 'rds_ww_manual'):
            s = src('templates', page + '.html')
            self.assertIn("rds_qc.js' %}?v=20261027e", s)
            self.assertNotIn('const calc = (sFinal - sInitial) * 1000 / volume;', s)
            self.assertIsNone(re.search(r'\(\((\w+)_final - \1_initial\) \* \1_multiply\)', s))     # every EDTA reading takes B
            self.assertGreaterEqual(s.count("rdsEdtaB('"), 12)
        for page in ('rds_dw', 'rds_dw_manual'):
            self.assertIn('name="ionic_det_head" id="" value="WS-AID-1ppm"', src('templates', page + '.html'))
        m = src('templates', 'rds_ww_manual.html')
        self.assertIn('QA RDS-45', m)
        self.assertNotIn("{% comment %} if (currentReportType == 'in-out') {\n                \n                    const cal_div = document.querySelector('.acidity_cal_div');", m)
        for page in ('rds_ww', 'rds_ww_manual'):
            s = src('templates', page + '.html')
            self.assertIn('QA RDS-46', s); self.assertEqual(s.count('ch_r1_equal.addEventListener'), 1)
        js = src('static', 'js', 'rds_avg.js')
        self.assertIn('window.rdsEdtaB = rdsEdtaB', js)
        lib = src('static', 'js', 'rds_formula_lib.js')
        self.assertIn('HEADALIAS', lib); self.assertIn("title: 'BOD5', method: 'APHA 5210 B / 4500-O C', reps: true", lib)


class RdsR5Pdf(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.u = User.objects.create_superuser('r5_ceo', 'c@x.c', 'x')
        DrinkingWaterForm.objects.create(sample_id='DW-R5', lab_report_no='LR-95', city_location='Lahore', extra_field='[]',
                                         sample_collection_date='21-Oct-2026', **KW)
        Sample_registration.objects.create(sample_id='DW-R5', city_location='Lahore')
        WasteWaterForm2.objects.create(sample_id='WW-R5', lab_report_no='LR-96', in_out='in-out', city_location='Karachi', **KW)

    def pdf(self, model, kind, data):
        c = Client(REMOTE_ADDR='127.0.0.1'); c.force_login(self.u)
        rec = model.objects.create(sample_id=data['sample_id'], rds=data)
        r = c.get('/qc/generate_%s_qc_pdf_response/%d/' % (kind, rec.pk))
        self.assertEqual(r.status_code, 200)
        return text(r.content)

    HARD = {'date_1': '20-Oct-2026', 'parameter_1': 'Total Hardness', 'result_1': '158', 'hardness_head_2': 'hardness:',
            'hardness_reading_1': 'Reading 01', 'hardness_2_1': '10.2', 'hardness_2_2': '2.2', 'hardness_2_3': '50',
            'hardness_ans2': '163.2', 'hardness_param2': 'mg/L'}

    def test_dw_b_and_checks(self):
        d = dict(self.HARD, sample_id='DW-R5', hardness_edta_b='1.02', qc_print_001=json.dumps(QC_WS))
        t = self.pdf(Dw_rds, 'dw', d)
        if t is None:
            return
        self.assertIn('(10.2 - 2.2) X 1.02 X 1000', t)
        self.assertIn('Quality control checks', t); self.assertIn('WS-Hardness-100ppm', t)
        self.assertIn('recovery: 98.5 % (acceptance 90 - 110 %)', t); self.assertIn('Within acceptance', t)
        self.assertIn('END OF THE DOCUMENT', t); self.assertNotIn('None', t)

    def test_dw_before_r5(self):
        t = self.pdf(Dw_rds, 'dw', dict(self.HARD, sample_id='DW-R5'))
        if t is not None:
            self.assertIn('(10.2 - 2.2) X 1000', t); self.assertNotIn('Quality control checks', t)

    def test_ww_in_out_b(self):
        d = {'sample_id': 'WW-R5', 'report_type': 'in-out', 'date_1': '20-Oct-2026', 'parameter_1': 'Total Hardness as CaCO3',
             'hardness_head_2_inlet': 'Hardness (Inlet):', 'hardness_reading_1_inlet': 'Reading 01', 'hardness_2_1_inlet': '12.5',
             'hardness_2_2_inlet': '0.5', 'hardness_2_3_inlet': '50', 'hardness_ans2_inlet': '244.8', 'hardness_param2_inlet': 'mg/L',
             'hardness_edta_b_inlet': '1.02',
             'qc_print_001': json.dumps(dict(QC_WS, type='CRM', type_label='Certified reference material (CRM)', parameter='pH', unit='pH units',
                                             true_value='7.00', readings=['7.02', '7.01', '7.03'], mean='7.02 (n = 3)', result='+0.02', mode='abs', abs='0.05'))}
        t = self.pdf(Ww_rds, 'ww', d)
        if t is not None:
            self.assertIn('(12.5 - 0.5) X 1.02 X 1000', t)
            self.assertIn('Certified reference material (CRM) - pH', t); self.assertIn('acceptance +/- 0.05', t)
