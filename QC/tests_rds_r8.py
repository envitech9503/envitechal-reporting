"""RDS release R8 (chemist feedback 28-10-2026, Tayyaba): WW RDS loads the report's current results (structured_data is
written only at creation), the latest report of a sample, long client names wrap, empty gravimetric readings are not
printed, oil & grease and TSS first readings shown, carbonate / bicarbonate by APHA 2320 B, EDTA card in triplicate, one
plate for counts, working of every check shown, and every WS / RM / CRM check gets its row in the results table."""
import json
import os
import shutil
import subprocess
import tempfile

from django.contrib.auth.models import User
from django.test import TestCase, Client

from EnviTechAlApp.models import WasteWaterForm2, DrinkingWaterForm, Sample_registration, Signatures
from QC.models import Dw_rds, Ww_rds
from QC.ww_live import live_structured

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


SD = {'standard_parameters': [{'sr_no': 1, 'parameter': 'Temperature 40 °C', 'inlet_result': '8.283', 'outlet_result': ''},
                              {'sr_no': 2, 'parameter': 'pH', 'inlet_result': '', 'outlet_result': ''},
                              {'sr_no': 6, 'parameter': 'Total Dissolved Solids (TDS)', 'inlet_result': '1298', 'outlet_result': ''}],
      'extra_parameters': [{'sr_no': 33, 'parameter': 'Nitrate', 'inlet_result': '0.96', 'methods': 'HACH', 'unit': 'mg/L'}], 'report_type': 'in'}


class RdsR8Data(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.u = User.objects.create_superuser('r8_ceo', 'c@x.c', 'x')
        cls.lhr = User.objects.create_user('r8_lhr', first_name='Tayyaba')
        Signatures.objects.create(user=cls.lhr, office='Lahore')
        WasteWaterForm2.objects.create(sample_id='WW-R8-LHR', lab_report_no='OLD', in_out='in', city_location='Lahore', structured_data=json.dumps(SD), **KW)
        cls.ww = WasteWaterForm2.objects.create(sample_id='WW-R8-LHR', lab_report_no='R8', in_out='in', city_location='Lahore', structured_data=json.dumps(SD),
                                                result_2='8.288', result_6='156',
                                                extra_field=json.dumps([{'parameters': 'Nitrate', 'methods': 'HACH', 'unit': 'mg/L', 'result': 'N.D.'}]), **KW)

    def test_live_results(self):
        sd = live_structured(self.ww)
        rows = {p['parameter']: p['inlet_result'] for p in sd['standard_parameters']}
        self.assertEqual(rows, {'Temperature 40 °C': '', 'pH': '8.288', 'Total Dissolved Solids (TDS)': '156'})
        self.assertEqual(sd['extra_parameters'][0]['inlet_result'], 'N.D.')

    def test_get_ww_loads_the_current_report(self):
        c = Client(REMOTE_ADDR='127.0.0.1'); c.force_login(self.u)
        d = c.post('/qc/get_ww/', json.dumps({'sample_id': 'WW-R8-LHR'}), content_type='application/json').json()
        got = {x['parameter']: x['test_result'] for x in d['qc_data']}
        self.assertEqual(got, {'pH': '8.288', 'Total Dissolved Solids (TDS)': '156', 'Nitrate': 'N.D.'})
        self.assertEqual(d['report_info']['lab_report_no'], 'R8')                       # the latest report of the sample

    def test_soc_extra_rows_current(self):
        from QC.soc_rules import extra_parameters
        self.assertEqual(extra_parameters('ww', self.ww)[0]['result'], 'N.D.')


class RdsR8Pdf(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.u = User.objects.create_superuser('r8p_ceo', 'c@x.c', 'x')
        WasteWaterForm2.objects.create(sample_id='WW-R8P', lab_report_no='LR-R8', in_out='out', city_location='Lahore',
                                       **dict(KW, report_to='The Aga Khan Hospital & Medical College Foundation (AKUH) Karachi Campus'))

    def pdf(self, data):
        c = Client(REMOTE_ADDR='127.0.0.1'); c.force_login(self.u)
        rec = Ww_rds.objects.create(sample_id=data['sample_id'], rds=data)
        r = c.get('/qc/generate_ww_qc_pdf_response/%d/' % rec.pk)
        self.assertEqual(r.status_code, 200)
        return text(r.content)

    def test_client_wraps_tss_only_entered_and_check_working(self):
        d = {'sample_id': 'WW-R8P', 'report_type': 'out', 'date_1': '20-Oct-2026', 'parameter_1': 'Total Suspended Solids (TSS)', 'result_1': '12',
             'tss_final_ans': '12', 'tss_head_2': 'Total Suspended Solids:', 'tss_read_1': 'Reading 01', 'iw2': '45.1', 'FW10': '45.1012', 'tss_vs2': '100',
             'tss_ans2': '12', 'tss_ans_param_2': 'mg/L', 'tss_head_3': 'Total Suspended Solids:', 'tss_read_2': 'Reading 02', 'iw3': '', 'tss_ans3': '',
             'tss_head_4': 'Total Suspended Solids:', 'tss_read_3': 'Reading 03',
             'qc_print_001': json.dumps({'type': 'WS', 'type_label': 'Working standard (WS)', 'parameter': 'TSS', 'side': '', 'ident': 'WS-TSS-20ppm',
                                         'true_value': '20', 'unit': 'mg/L', 'readings': ['19.6', '20.2', ''], 'mean': '19.9 (n = 2)', 'result': '99.5',
                                         'mode': 'rec', 'lo': '90', 'hi': '110', 'verdict': 'Within acceptance',
                                         'work': ['Mean = (19.6 + 20.2) / 2 = 19.9 mg/L', 'Recovery = 19.9 / 20 X 100 = 99.5 %']})}
        t = self.pdf(d)
        if t is None:
            return
        self.assertIn('The Aga Khan Hospital & Medical College', t); self.assertIn('Lab report no.:', t)
        self.assertIn('Reading 01', t); self.assertNotIn('Reading 02', t); self.assertNotIn('Reading 03', t)
        self.assertIn('Mean = (19.6 + 20.2) / 2 = 19.9 mg/L', t); self.assertIn('Recovery = 19.9 / 20 X 100 = 99.5 %', t)


class RdsR8Pages(TestCase):
    def test_js_and_templates(self):
        qc = src('static', 'js', 'rds_qc.js')
        for t in ('function linkRow(blk)', 'function fillRow(blk', 'window.rdsMaxSub', "tr.dataset.rqLinked = '1'", 'rq-work'):
            self.assertIn(t, qc)
        lib = src('static', 'js', 'rds_formula_lib.js')
        self.assertIn("reps: true, nrep: 1", lib); self.assertIn("title: 'EDTA titration', method: 'APHA 2340 C / 3500-Ca B / ASTM D1126', reps: true", lib)
        self.assertIn('Table 2320:II', lib); self.assertIn("div.carbonates", lib); self.assertIn('rl-work', lib)
        for page in ('rds_dw', 'rds_dw_manual', 'rds_ww', 'rds_ww_manual'):
            s = src('templates', page + '.html')
            self.assertIn('window.rdsMaxSub(mainSnoBase)', s); self.assertRegex(s, r"rds_qc.js' %}\?v=2026102[89]\w")
        ww = src('templates', 'rds_ww.html')
        self.assertIn("document.querySelectorAll('.oil_div > .cal_div')", ww); self.assertIn("document.querySelectorAll('.tss_div > .cal_div')", ww)
