"""RDS formula library (owner request 27-10-2026): methods and units reach the RDS pages, the drinking-water RDS
offers the laboratory's reports and staff, both RDS lists are by laboratory, and the library cards print on both
RDS PDFs. The equations themselves are checked in the browser QA (hand-worked values, 38 cases)."""
import json
import shutil
import subprocess
import tempfile

from django.contrib.auth.models import User
from django.test import TestCase, Client

from EnviTechAlApp.models import WasteWaterForm2, DrinkingWaterForm, Signatures, Sample_registration
from QC.models import Dw_rds, Ww_rds
from QC.rds_lib_pdf import print_lib_cards

KW = dict(report_to='QA', address='L', attention='A', date_of_analysis_from='20-Oct-2026', date_of_analysis_to='25-Oct-2026', reporting_date='26-October-2026')
CARD = {'parameter': 'Bicarbonate', 'side': '', 'method': 'APHA 2320 B', 'calc': 'Alkalinity titration', 'formula': 'P or T = A x N x 50 000 / V',
        'lines': ['T = 12 x 0.02 x 50000 / 100 = 120 mg/L as CaCO3'], 'result': '97.6', 'unit': 'mg/L', 'reported': '97.6', 'check': 'OK'}


def C(u):
    c = Client(REMOTE_ADDR='127.0.0.1'); c.force_login(u); return c


def text(content):
    if not shutil.which('pdftotext'):
        return None
    with tempfile.NamedTemporaryFile(suffix='.pdf') as fh:
        fh.write(content); fh.flush()
        return subprocess.run(['pdftotext', '-layout', fh.name, '-'], capture_output=True, text=True).stdout


class RdsLibTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ceo = User.objects.create_superuser('l_ceo', 'c@x.c', 'x')
        cls.lhr = User.objects.create_user('l_lhr', first_name='Maryam')
        cls.khi = User.objects.create_user('l_khi', first_name='Karachi')
        Signatures.objects.create(user=cls.lhr, office='Lahore'); Signatures.objects.create(user=cls.khi, office='Karachi')
        sd = {'standard_parameters': [], 'extra_parameters': [{'sr_no': 1, 'parameter': 'Bicarbonate', 'outlet_result': '97.6', 'unit': 'mg/L', 'methods': 'ASTM-D 1067'}]}
        WasteWaterForm2.objects.create(sample_id='WW-L1-LHR', lab_report_no='L1', in_out='out', city_location='Lahore', structured_data=json.dumps(sd), **KW)
        ex = [{'parameters': 'Potassium', 'methods': 'APHA 3111-B', 'unit': 'mg/L', 'result': '5.3'}]
        DrinkingWaterForm.objects.create(sample_id='DW-L2-LHR', lab_report_no='L2', city_location='Lahore', extra_field=json.dumps(ex), sample_collection_date='21-Oct-2026', **KW)
        DrinkingWaterForm.objects.create(sample_id='DW-L3-KHI', lab_report_no='L3', city_location='Karachi', extra_field='[]', sample_collection_date='21-Oct-2026', **KW)
        DrinkingWaterForm.objects.create(sample_id='DW-L4-LHR', lab_report_no='L4', city_location='Lahore', extra_field='[]', sample_collection_date='21-Oct-2026', **KW)
        for s in ('DW-L2-LHR', 'DW-L3-KHI'):
            Sample_registration.objects.create(sample_id=s, city_location='Lahore' if 'LHR' in s else 'Karachi')

    def test_method_unit_samples_signers(self):
        lc = C(self.lhr)
        d = lc.post('/qc/get_ww/', json.dumps({'sample_id': 'WW-L1-LHR'}), content_type='application/json').json()
        it = [x for x in d['qc_data'] if x['parameter'] == 'Bicarbonate'][0]
        self.assertEqual((it['method'], it['unit']), ('ASTM-D 1067', 'mg/L'))
        g = lc.post('/qc/get_dw/', json.dumps({'sample_id': 'DW-L2-LHR'}), content_type='application/json').json()
        k = [x for x in g['qc_data'] if x['parameter'] == 'Potassium'][0]
        self.assertEqual(k['method'], 'APHA 3111-B')
        names = [s['name'] for s in g['signatures']]
        self.assertTrue(any('Maryam' in n for n in names)); self.assertFalse(any('Karachi' in n for n in names))
        r = lc.get('/qc/create_dw_qc/')
        self.assertEqual([x['fields']['sample_id'] for x in json.loads(r.context['sample'])], ['DW-L2-LHR'])   # own lab, registered only
        self.assertContains(r, 'rds_formula_lib.js')
        for u in ('/qc/create_dw_qc_manual/', '/qc/create_ww_qc/', '/qc/create_ww_qc_manual/'):
            self.assertContains(lc.get(u), 'rds_formula_lib.js')
        Dw_rds.objects.create(sample_id='DW-L3-KHI', rds={}); Dw_rds.objects.create(sample_id='DW-L2-LHR', rds={})
        self.assertEqual([x.sample_id for x in lc.get('/qc/dw_rds_list/').context['list']], ['DW-L2-LHR'])
        self.assertEqual(len(C(self.ceo).get('/qc/dw_rds_list/').context['list']), 2)

    def test_cards_print_on_both_pdfs(self):
        lc = C(self.lhr)
        for url, sid, model in (('/qc/create_dw_qc/', 'DW-L2-LHR', Dw_rds), ('/qc/create_ww_qc/', 'WW-L1-LHR', Ww_rds)):
            body = {'sample_id': sid, 'date_1': '25-10-2026', 'parameter_1': 'Bicarbonate', 'result_1': '97.6', 'lib_print_001': json.dumps(CARD), 'lib_print_002': ''}
            self.assertEqual(lc.post(url, json.dumps(body), content_type='application/json').status_code, 302)
            rec = model.objects.filter(sample_id=sid).latest('id')
            p = lc.get('/qc/generate_%s_qc_pdf_response/%d/' % ('dw' if model is Dw_rds else 'ww', rec.pk))
            self.assertEqual(p.status_code, 200)
            t = text(p.content)
            if t is not None:
                self.assertIn('Calculations - formula library', t)
                self.assertIn('T = 12 x 0.02 x 50000 / 100 = 120', t)
                self.assertIn('Result: 97.6 mg/L', t)

    def test_printer_ignores_bad_entries(self):
        from fpdf import FPDF
        pdf = FPDF(); pdf.add_page()
        print_lib_cards(pdf, {'lib_print_001': 'not json', 'lib_print_002': '', 'other': 'x'})
        print_lib_cards(pdf, {'lib_print_001': json.dumps(CARD)})
        self.assertGreater(len(bytes(pdf.output())), 500)

    def test_rds_without_dated_rows_prints(self):
        lc = C(self.lhr)
        for M, k, sid in ((Dw_rds, 'dw', 'DW-L2-LHR'), (Ww_rds, 'ww', 'WW-L1-LHR')):
            rec = M.objects.create(sample_id=sid, rds={})                         # no dated rows (was a server error on DW)
            self.assertEqual(lc.get('/qc/generate_%s_qc_pdf_response/%d/' % (k, rec.pk)).status_code, 200)


class RdsLibNameMapJsTest(TestCase):
    def test_every_reported_name_reaches_its_section(self):
        node = shutil.which('node')
        if not node:
            self.skipTest('node not installed')
        import os
        r = subprocess.run([node, os.path.join(os.path.dirname(__file__), 'jstests', 'rds_lib_names.js')], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout[-2000:] + r.stderr[-2000:])
