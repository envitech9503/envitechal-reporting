"""RDS release R10 (analyst feedback 30-10-2026, Tayyaba): no "RDS saved" on the PDF; the RDS table by date of analysis;
no comparison with the test report on the RDS; a parameter not reported on an in-out report gets no row or section;
each replicate's result shown; working standards of titrimetric parameters calculated from the titration."""
import json
import os
import shutil
import subprocess
import tempfile

from django.contrib.auth.models import User
from django.test import TestCase, Client

from EnviTechAlApp.models import WasteWaterForm2, Signatures
from QC.models import Dw_rds, Ww_rds
from QC.rds_pdf_extras import chrono_key, method_checks

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KW = dict(report_to='QA Mills (TEST)', address='L', attention='A', date_of_analysis_from='15-Aug-2026', date_of_analysis_to='17-Aug-2026',
          reporting_date='18-August-2026')


def src(*p):
    return open(os.path.join(ROOT, *p), encoding='utf-8').read()


def text(content):
    if not shutil.which('pdftotext'):
        return None
    with tempfile.NamedTemporaryFile(suffix='.pdf') as fh:
        fh.write(content); fh.flush()
        return subprocess.run(['pdftotext', '-opw', 'karachi123', '-layout', fh.name, '-'], capture_output=True, text=True).stdout


class RdsR10(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.u = User.objects.create_superuser('r10_ceo', 'c@x.c', 'x')

    def test_helpers(self):
        data = {'date_1': '15-08-2026', 'date_2': '17-08-2026', 'date_3': '15-08-2026', 'date_3_1': '', 'date_4': '', 'date_5': '2026-08-14'}
        self.assertEqual(sorted(['1', '2', '3', '3_1', '4', '5'], key=chrono_key(data)), ['5', '1', '3', '3_1', '2', '4'])
        self.assertEqual(method_checks('replicate 1: DO depletion below 2.0 mg/L; calculated 33.685 differs from the reported 32 by 5.3 %'),
                         'replicate 1: DO depletion below 2.0 mg/L')
        self.assertEqual(method_checks('calculated 5 is not below the reported <1'), '')
        self.assertEqual(method_checks('OK'), 'OK')

    def test_pdf_order_no_saved_date_no_reported(self):
        c = Client(REMOTE_ADDR='127.0.0.1'); c.force_login(self.u)
        WasteWaterForm2.objects.create(sample_id='WW-R10', lab_report_no='LR-R10', in_out='out', city_location='Lahore', **KW)
        lib = {'parameter': 'Biological Oxygen Demand (BOD5)', 'side': '', 'method': 'APHA 5210 B', 'calc': 'BOD5', 'formula': 'BOD = ...',
               'lines': ['Replicate 1: [(8.2 - 6.4) - 0] / (30 / 300) = 18', 'Average = (18) / 1 = 18'], 'result': '18', 'unit': 'mg/L', 'reported': '32',
               'check': 'replicate 1: DO depletion below 2.0 mg/L; calculated 18 differs from the reported 32 by 43.8 %'}
        d = {'sample_id': 'WW-R10', 'report_type': 'out', 'date_1': '17-08-2026', 'parameter_1': 'Chromium', 'result_1': '0.1',
             'date_2': '15-08-2026', 'parameter_2': 'Colour', 'result_2': '5', 'date_3': '16-08-2026', 'parameter_3': 'Turbidity', 'result_3': '1',
             'lib_print_001': json.dumps(lib)}
        rec = Ww_rds.objects.create(sample_id='WW-R10', rds=d)
        r = c.get('/qc/generate_ww_qc_pdf_response/%d/' % rec.pk); self.assertEqual(r.status_code, 200)
        t = text(r.content)
        if t is None:
            return
        self.assertNotIn('RDS saved', t)
        self.assertLess(t.index('Colour'), t.index('Turbidity')); self.assertLess(t.index('Turbidity'), t.index('Chromium'))
        self.assertNotIn('reported: 32', t); self.assertNotIn('differs from the reported', t); self.assertIn('DO depletion below 2.0', t)

    def test_in_out_parameter_not_reported_has_no_row(self):
        c = Client(REMOTE_ADDR='127.0.0.1'); c.force_login(self.u)
        sd = {'standard_parameters': [{'sr_no': 2, 'parameter': 'pH', 'inlet_result': '', 'outlet_result': ''},
                                      {'sr_no': 8, 'parameter': 'Oil & Grease', 'inlet_result': '', 'outlet_result': ''},
                                      {'sr_no': 5, 'parameter': 'Chemical Oxygen Demand(COD)', 'inlet_result': '', 'outlet_result': ''}], 'report_type': 'in-out'}
        WasteWaterForm2.objects.create(sample_id='WW-R10-IO', lab_report_no='202608088-TEST', in_out='in-out', city_location='Lahore', structured_data=json.dumps(sd),
                                       result_2='7.1', result_2_2='7.3', result_8='-', result_8_8='', result_5='', result_5_5='88', **KW)
        d = c.post('/qc/get_ww/', json.dumps({'sample_id': 'WW-R10-IO'}), content_type='application/json').json()
        self.assertEqual([x['parameter'] for x in d['qc_data']], ['pH', 'Chemical Oxygen Demand(COD)'])

    def test_js(self):
        lib = src('static', 'js', 'rds_formula_lib.js')
        for t in ('rl-rres', 'Result, replicate', 'rl-info', 'not printed', "'Average = ('"):
            self.assertIn(t, lib)
        self.assertNotIn('reported: rep, check', lib)
        qc = src('static', 'js', 'rds_qc.js')
        for t in ('Readings from the titration', 'function titrLines', 'X 50000 / Volume of sample', 'X 1000 / Volume of sample'):
            self.assertIn(t, qc)
        self.assertIn('For information (not printed)', src('static', 'js', 'rds_ww_calc.js'))
        self.assertNotIn("('RDS saved'", src('QC', 'rds_pdf_extras.py'))
