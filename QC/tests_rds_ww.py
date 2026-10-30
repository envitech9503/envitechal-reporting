"""RDS WW (owner review 27-10-2026): sample list of the user's laboratory, laboratory staff as signers, list filtered
by laboratory, BOD seed-control term and calculation checks printed on the RDS PDF, COD outlet working standard."""
import json
import shutil
import subprocess
import tempfile

from django.contrib.auth.models import User
from django.test import TestCase, Client

from EnviTechAlApp.models import WasteWaterForm2, Signatures
from QC.models import Ww_rds

KW = dict(report_to='QA Mills', address='Lahore', attention='Mr A', sample_Col_date='20-Oct-2026', select='PEQS',
          date_of_analysis_from='20-Oct-2026', date_of_analysis_to='25-Oct-2026', reporting_date='26-October-2026')


def C(u):
    c = Client(REMOTE_ADDR='127.0.0.1'); c.force_login(u); return c


def pdf_text(content):
    if not shutil.which('pdftotext'):
        return None
    with tempfile.NamedTemporaryFile(suffix='.pdf') as fh:
        fh.write(content); fh.flush()
        return subprocess.run(['pdftotext', '-layout', fh.name, '-'], capture_output=True, text=True).stdout


class RdsWwTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ceo = User.objects.create_superuser('r_ceo', 'c@x.c', 'x')
        cls.lhr = User.objects.create_user('r_lhr', first_name='Tayyaba')
        cls.lmgr = User.objects.create_user('r_lmgr', first_name='Sana')
        cls.khi = User.objects.create_user('r_khi', first_name='Karachi')
        Signatures.objects.create(user=cls.lhr, office='Lahore')
        cls.lsig = Signatures.objects.create(user=cls.lmgr, office='Lahore')
        Signatures.objects.create(user=cls.khi, office='Karachi')
        WasteWaterForm2.objects.create(sample_id='WW-T1-LHR', lab_report_no='T1', in_out='out', city_location='Lahore',
                                       result_2_2='7.5', result_4_4='40', result_5_5='75', lab_manager_signature=cls.lsig, **KW)
        WasteWaterForm2.objects.create(sample_id='WW-T2-LHR', lab_report_no='T2', in_out='in-out', city_location='Lahore', **KW)
        WasteWaterForm2.objects.create(sample_id='WW-T3-KHI', lab_report_no='T3', in_out='out', city_location='Karachi', **KW)

    def test_sample_list_and_signers(self):
        r = C(self.lhr).get('/qc/create_ww_qc/')
        self.assertEqual(r.status_code, 200)
        samples = [x['fields']['sample_id'] for x in json.loads(r.context['sample'])]
        self.assertEqual(samples, ['WW-T2-LHR', 'WW-T1-LHR'])                 # own laboratory, waste water, newest first
        everyone = [x['fields']['sample_id'] for x in json.loads(C(self.ceo).get('/qc/create_ww_qc/').context['sample'])]
        self.assertIn('WW-T3-KHI', everyone)
        self.assertContains(r, 'rds_ww_calc.js')
        self.assertContains(C(self.lhr).get('/qc/create_ww_qc_manual/'), 'rds_ww_calc.js')
        d = C(self.lhr).post('/qc/get_ww/', json.dumps({'sample_id': 'WW-T1-LHR'}), content_type='application/json').json()
        names = [s['name'] for s in d['signatures']]
        self.assertTrue(any('Tayyaba' in n for n in names))                  # the laboratory's staff, not only the report's signers
        self.assertFalse(any('Karachi' in n for n in names))
        self.assertEqual(len([n for n in names if 'r_lmgr' in n or 'Sana' in n]), 1)   # no duplicate of the report signer

    def test_list_by_laboratory_and_pdf(self):
        lc = C(self.lhr)
        base = {'sample_id': 'WW-T1-LHR', 'date_1': '25-10-2026', 'parameter_1': 'Biological Oxygen Demand(BOD)5', 'result_1': '40',
                'bod_head_2': 'BOD5: (APHA 4500 O-C, 5210 B)', 'bod_sv': '30', 'bod_tv': '300', 'bod_1_p': '0.1',
                'bod_initial': '8.2', 'bod_final': '4.0', 'bod_seed_1': '8.0', 'bod_seed_2': '2.0', 'bod_seed_ctrl': '15', 'bod_seed_vol': '2',
                'bod_ans': '34', 'bod_param': 'mg/L', 'bod_divi': '0.1', 'bod_check': 'DO depletion 1.80 mg/L is below 2.0 (APHA 5210 B); calculated 34 differs from the reported 40 by 15.0 %',
                'cod_head': 'WS-COD-100ppm:', 'for_cod1': '98', 'for_cod2': '101', 'cod_divi1': '2', 'cod_ans': '99.5', 'cod_param': 'mg/L',
                'cod_ws_check': 'recovery 99.5 % of 100 mg/L - acceptable',
                'cod_head_1': 'Chemical Oxygen Demand (COD):', 'for_cod1_1': '74', 'for_cod1_1_df': '1', 'for_cod1_2': '76', 'for_cod1_2_df': '1',
                'cod_divi': '2', 'cod_ans_1': '75', 'cod_param_1': 'mg/L', 'cod_check': 'OK'}
        r = lc.post('/qc/create_ww_qc/', json.dumps(base), content_type='application/json')
        self.assertEqual(r.status_code, 302)
        rds = Ww_rds.objects.get(sample_id='WW-T1-LHR')
        p = lc.get('/qc/generate_ww_qc_pdf_response/%d/' % rds.pk)
        self.assertEqual(p.status_code, 200)
        t = pdf_text(p.content)
        if t is not None:
            self.assertIn('/ 15 X 2', t)                                      # seed-control volume in the BOD working
            self.assertIn('Check: DO depletion 1.80', t); self.assertNotIn('differs from the reported', t)   # analyst 30-10-2026: no comparison with the report on the RDS
            self.assertIn('recovery 99.5', t)
            self.assertIn('(74 X 1) + (76 X 1)', t)                           # replicates 1 and 2 (was replicate 1 twice)
        io = {'sample_id': 'WW-T2-LHR', 'report_type': 'in-out', 'date_1': '25-10-2026', 'parameter_1': 'COD', 'for_cod1_outlet': '99', 'for_cod2_outlet': '100', 'cod_divi1_outlet': '2', 'cod_ans_outlet': '99.5',
              'cod_head_outlet': 'WS-COD-100ppm (Outlet):', 'cod_ws_check_outlet': 'recovery 99.5 % of 100 mg/L - acceptable',
              'bod_initial_outlet': '8.2', 'bod_final_outlet': '4.0', 'bod_seed_1_outlet': '8', 'bod_seed_2_outlet': '2', 'bod_seed_ctrl_outlet': '15',
              'bod_seed_vol_outlet': '2', 'bod_ans_outlet': '34', 'bod_param_outlet': 'mg/L', 'bod_divi_outlet': '0.1', 'bod_1_p_outlet': '0.1',
              'bod_sv_outlet': '30', 'bod_tv_outlet': '300', 'bod_check_outlet': 'OK'}
        self.assertEqual(lc.post('/qc/create_ww_qc/', json.dumps(io), content_type='application/json').status_code, 302)
        p2 = lc.get('/qc/generate_ww_qc_pdf_response/%d/' % Ww_rds.objects.get(sample_id='WW-T2-LHR').pk)
        self.assertEqual(p2.status_code, 200)
        t2 = pdf_text(p2.content)
        if t2 is not None:
            self.assertIn('WS-COD-100ppm (Outlet)', t2)
            self.assertIn('/ 15 X 2', t2)
        Ww_rds.objects.create(sample_id='WW-T3-KHI', rds={})
        own = [x.sample_id for x in C(self.lhr).get('/qc/ww_rds_list/').context['list']]
        self.assertNotIn('WW-T3-KHI', own); self.assertIn('WW-T1-LHR', own)
        allr = [x.sample_id for x in C(self.ceo).get('/qc/ww_rds_list/').context['list']]
        self.assertIn('WW-T3-KHI', allr)
        only = [x.sample_id for x in C(self.ceo).get('/qc/ww_rds_list/?lab=Karachi').context['list']]
        self.assertEqual(only, ['WW-T3-KHI'])
