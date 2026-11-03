"""R13.5 (owner 03-11-2026): the RDS loads every result entered on the DW test report, ticked on the registration or
not (WS-202610041-KHI); a result entered under "Other parameters" fills its ticked row (" Faecal Coliform", "Barium");
a CRM check made from the WS / RM / CRM bar prints its working (readings and average) at the end of its parameter's
section - not its certified value, recovery or verdict."""
import json
import subprocess
import tempfile

from django.contrib.auth.models import User
from django.test import TestCase, SimpleTestCase, RequestFactory

from EnviTechAlApp.models import DrinkingWaterForm, Sample_registration
from QC.tests_rds_r13 import new_pdf


def pdf_text(pdf):
    with tempfile.NamedTemporaryFile(suffix='.pdf') as fh:
        pdf.output(fh.name)
        return subprocess.run(['pdftotext', '-layout', fh.name, '-'], capture_output=True, text=True).stdout


class RdsR135GetDw(TestCase):
    def test_report_results_load_ticked_or_not(self):
        from QC.views.dw import get_dw
        Sample_registration.objects.create(sample_id='DW-R135', city_location='Lahore', checkinp64=True, checkinp100=True, other_param_27=True)
        DrinkingWaterForm.objects.create(sample_id='DW-R135', city_location='Lahore', water_sr1='7.64', water_sr2='308', water_sr3='146',
                                         extra_field="[{'parameters': ' Faecal Coliform', 'result': 'N.D.'}]")
        r = get_dw(RequestFactory().post('/', json.dumps({'sample_id': 'DW-R135'}), content_type='application/json'))
        rows = {x['parameter']: x['test_result'] for x in json.loads(r.content)['qc_data']}
        self.assertEqual(rows.get('pH*'), '7.64')                 # not ticked, on the report
        self.assertEqual(rows.get('TDS'), '308')                  # not ticked, on the report
        self.assertEqual(rows.get('Total Hardness*'), '146')      # ticked
        self.assertEqual(rows.get('Faecal coliform'), 'N.D.')     # ticked, entered under "Other parameters"
        self.assertNotIn('Selenium', rows)                        # the Chromium VI box is not the selenium row
        self.assertEqual(len([k for k in rows if 'aecal' in k]), 1)


class RdsR135Crm(SimpleTestCase):
    def data(self):
        crm = {'type': 'CRM', 'parameter': 'Chemical Oxygen Demand(COD)', 'side': '', 'unit': 'mg/L', 'readings': ['99', '100', '101'],
               'true_value': '100', 'mean': '100 (n = 3)', 'result': '100.0', 'verdict': 'Within acceptance',
               'work': ['Mean = (99 + 100 + 101) / 3 = 100 mg/L', 'Recovery = 100 / 100 X 100 = 100.0 %']}
        crm2 = dict(crm, parameter='Total Hardness', work=['EDTA factor B = 1 mg CaCO3 / mL', 'Reading 1 = (5 - 0) X 1 X 1000 / 50 = 100',
                                                           'Mean = 100 = 100 mg/L', 'Recovery = 100 / 100 X 100 = 100.0 %'])
        orphan = dict(crm, parameter='Chloride')                  # no "Chloride CRM" row in the table: not printed
        return {'parameter_1': 'Chemical Oxygen Demand (COD)', 'parameter_1_1': 'Chemical Oxygen Demand (COD) CRM',
                'parameter_2': 'Total Hardness*', 'parameter_2_1': 'Total Hardness CRM',
                'qc_print_001': json.dumps(crm), 'qc_print_002': json.dumps(crm2), 'qc_print_003': json.dumps(orphan)}

    def test_matching(self):
        from QC.rds_pdf_extras import _cw, _names, _abbr
        self.assertTrue(_names(_cw('TDS'), 'Total Dissolved Solids (TDS) Calculation:'))
        self.assertFalse(_names(_cw('Total Hardness'), 'Total Dissolved Solids (TDS) Calculation:'))
        self.assertTrue(_names(_cw('pH'), 'pH Calculation:'))
        self.assertEqual(_abbr('Chemical Oxygen Demand(COD)'), {'cod'})

    def test_printed_at_end_of_section_without_qc(self):
        from QC.rds_pdf_extras import install_df, closing, flush_df, crm_records
        d = self.data()
        self.assertEqual(len(crm_records(d)), 2)
        pdf = new_pdf(); install_df(pdf, d)
        b11 = lambda t: (pdf.set_font('Calibri', 'B', 11), pdf.cell(0, 6, t, ln=True))
        b11('COD Calculation'); pdf.set_font('Calibri', '', 10); pdf.cell(0, 6, '5 + 5 + 5 = 5 mg/L', ln=True)
        b11('Chemical Oxygen Demand (COD) (Inlet):'); pdf.set_font('Calibri', '', 10); pdf.cell(0, 6, '(5 X 1) = 5 mg/L', ln=True)
        b11('Hardness Calculation:'); pdf.set_font('Calibri', '', 10); pdf.cell(0, 6, '(9 - 1) X 1000 / 50 = 160 mg/L', ln=True)
        b11('Chloride Calculation:')
        flush_df(pdf)
        t = pdf_text(pdf)
        self.assertLess(t.index('(5 X 1) = 5 mg/L'), t.index('Chemical Oxygen Demand (COD) CRM Calculations'))
        self.assertLess(t.index('Chemical Oxygen Demand (COD) CRM Calculations'), t.index('Hardness Calculation:'))
        self.assertLess(t.index('Total Hardness CRM Calculations'), t.index('Chloride Calculation:'))
        self.assertIn('99 + 100 + 101 = 100 mg/L', t); self.assertIn('Reading 01', t); self.assertIn('EDTA factor B', t)
        for qc in ('Recovery', 'Within acceptance', 'Certified', 'Chloride CRM'):
            self.assertNotIn(qc, t)
