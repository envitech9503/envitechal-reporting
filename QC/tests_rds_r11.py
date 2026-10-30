"""RDS release R11 (owner zero-error check 30-10-2026): a calculation only for a parameter of the results table (Add and
manual pages, PDF of old and new records); no blank result row or blank calculation (no empty CALCULATION page); every
calculation with its formula steps (formula-library observation cards, all the readings of a QC check); one size and
colour for the working (Calibri 10, black)."""
import json
import os
import re

from django.contrib.auth.models import User
from django.test import TestCase, Client

from EnviTechAlApp.models import DrinkingWaterForm, WasteWaterForm2
from QC.models import Dw_rds, Ww_rds
from QC.rds_print_filter import prune, Present, page_name
from QC.tests_rds_r10 import KW, src, text

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def card(**kw):
    c = {'parameter': 'Odour', 'side': '', 'method': '', 'calc': 'Direct observation / reading',
         'formula': 'Recorded as observed (no calculation)', 'lines': ['Observed: Odourless mg/L'], 'result': 'Odourless', 'unit': 'mg/L', 'check': 'OK'}
    c.update(kw)
    return json.dumps(c)


class RdsR11Filter(TestCase):
    def test_map(self):
        m = json.load(open(os.path.join(ROOT, 'QC', 'rds_field_owners.json')))
        self.assertIn('Chloride', m['dw']['chloride_1_1'])
        self.assertEqual(m['ww']['tss_head_1'], ['Total Suspended Solids (TSS)'])          # TDS no longer opens TSS / O&G
        self.assertEqual(m['ww']['oil_head_1'], ['Oil & Grease'])
        self.assertFalse([k for k in list(m['dw']) + list(m['ww']) if re.match(r'^(qc_\d+_|rl\d+_|lib_print|qc_print|parameter_|result_)', k)])
        js = src('static', 'js', 'rds_field_owners.js')
        self.assertEqual(json.loads(js[js.index('=') + 1:].strip().rstrip(';')), m)

    def test_names(self):
        self.assertEqual(page_name('dw', 'Chloride'), 'Chloride')
        self.assertEqual(page_name('ww', 'Total Suspended Solids'), 'Total Suspended Solids (TSS)')
        p = Present('ww', ['Biological Oxygen Demand(BOD)5'])
        self.assertTrue(p('Biological Oxygen Demand (BOD5)'))
        self.assertFalse(Present('ww', ['Chemical Oxygen Demand(COD)'])('Biological Oxygen Demand (BOD5)'))
        self.assertFalse(Present('dw', ['Calcium Hardness'])('Total Hardness'))

    def test_prune(self):
        d = {'date_1': '15-08-2026', 'parameter_1': 'Chloride', 'result_1': '44',
             'date_2': '15-08-2026', 'parameter_2': 'Iron', 'result_2': '',                # blank result: no row
             'date_3': '15-08-2026', 'parameter_3': '', 'result_3': '5',                   # no parameter: no row
             'date_4': '16-08-2026', 'parameter_4': 'Fluoride', 'result_4': 'N/A',
             'chloride_1_1': '9.8', 'iron_ans': '0.3', 'for_iron1': '0.3', 'some_unknown_field': 'x',
             'lib_print_001': card(), 'lib_print_002': card(parameter='Chloride', result=''),
             'lib_print_003': card(parameter='Chloride', result='44'),
             'qc_print_001': json.dumps({'type': 'WS', 'parameter': 'Iron', 'readings': ['1']}),
             'qc_print_002': json.dumps({'type': 'WS', 'parameter': 'Chloride', 'readings': ['1']})}
        m = json.load(open(os.path.join(ROOT, 'QC', 'rds_field_owners.json')))['dw']
        iron = [k for k in ('iron_ans', 'for_iron1') if 'Iron' in m.get(k, [])]
        self.assertTrue(iron)
        out = prune(d, 'dw')
        self.assertEqual(sorted(k for k in out if k.startswith('date_')), ['date_1'])
        self.assertIn('chloride_1_1', out); self.assertIn('some_unknown_field', out)
        for k in iron:
            self.assertNotIn(k, out)
        self.assertNotIn('lib_print_001', out)                      # Odour is not in the table
        self.assertNotIn('lib_print_002', out); self.assertIn('lib_print_003', out)
        self.assertNotIn('qc_print_001', out); self.assertIn('qc_print_002', out)
        self.assertEqual(d['iron_ans'], '0.3')                       # the saved record is not changed


class RdsR11Unknown(TestCase):
    """R11.1 (production check 30-10-2026): fields the Add-page map does not hold."""
    def test_infer(self):
        from QC.rds_print_filter import infer_owners
        self.assertEqual(infer_owners('dw', 'ecoli_ans'), ('E.coli',))
        self.assertEqual(infer_owners('dw', 'fecal_ans'), ('Faecal coliform',))
        self.assertEqual(infer_owners('dw', 'fecalentero_ans'), ('Fecal Enterococci',))
        self.assertEqual(infer_owners('dw', 'total_coliform_ans'), ('Coliform',))
        self.assertEqual(infer_owners('dw', 'for_berylium1_1'), ('Beryllium',))          # older spelling
        self.assertEqual(infer_owners('dw', 'for_chloride9'), ())                          # chloride / chlorine: unclear, kept
        self.assertEqual(infer_owners('dw', 'sample_id'), ())

    def test_prune_unknown(self):
        d = {'date_1': '15-08-2026', 'parameter_1': 'Coliform', 'result_1': '0',
             'fecal_ans': '0', 'fecal_param': 'CFU/100 mL', 'ecoli_ans': '0', 'total_coliform_ans': '0', 'for_berylium1_1': '0.1',
             'for_chloride9': '5'}
        out = prune(d, 'dw')
        for k in ('fecal_ans', 'fecal_param', 'ecoli_ans', 'for_berylium1_1'):
            self.assertNotIn(k, out)
        self.assertIn('total_coliform_ans', out); self.assertIn('for_chloride9', out)
        out2 = prune({'date_1': 'x', 'parameter_1': 'TBC', 'result_1': '5', 'bacteria_ans': '5', 'fecal_ans': '1'}, 'dw')
        self.assertIn('bacteria_ans', out2); self.assertNotIn('fecal_ans', out2)   # an abbreviation keeps its own working
        out3 = prune({'date_1': 'x', 'parameter_1': 'Colony counts at 22 °C', 'result_1': '5', 'hetrobacteria_ans': '5', 'bacteria_ans': '3',
                      'carbonates_1_1': '2', 'date_2': 'x', 'parameter_2': 'Bicarbonate', 'result_2': '9'}, 'dw')
        for k in ('hetrobacteria_ans', 'bacteria_ans', 'carbonates_1_1'):
            self.assertIn(k, out3)                                                           # plate counts one family; carbonates kept


class RdsR11Pdf(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.u = User.objects.create_superuser('r11_ceo', 'c@x.c', 'x')

    def setUp(self):
        self.c = Client(REMOTE_ADDR='127.0.0.1'); self.c.force_login(self.u)

    def dw(self, sid, d):
        DrinkingWaterForm.objects.create(sample_id=sid, lab_report_no='LR-' + sid, city_location='Lahore', **KW)
        rec = Dw_rds.objects.create(sample_id=sid, rds=dict(d, sample_id=sid))
        r = self.c.get('/qc/generate_dw_qc_pdf_response/%d/' % rec.pk)
        self.assertEqual(r.status_code, 200)
        return text(r.content)

    def test_no_empty_calculation_page(self):
        t = self.dw('DW-R11A', {'date_1': '15-08-2026', 'parameter_1': 'Beryllium', 'result_1': '<0.001'})
        if t is None:
            return
        self.assertNotIn('CALCULATION', t); self.assertIn('Beryllium', t); self.assertIn('END OF THE DOCUMENT', t)
        self.assertIn('Page No: 1 of 1', t)

    def test_only_table_parameters_and_steps(self):
        d = {'date_1': '15-08-2026', 'parameter_1': 'Odour', 'result_1': 'Odourless',
             'date_2': '15-08-2026', 'parameter_2': 'Taste', 'result_2': '',
             'lib_print_001': card(), 'lib_print_002': card(parameter='Taste', result='Unobjectionable'),
             'qc_print_001': json.dumps({'type': 'WS', 'type_label': 'Working standard (WS)', 'parameter': 'Odour', 'true_value': '5',
                                         'readings': ['5', '5', '5'], 'mean': '5 (n = 3)', 'result': '100', 'lo': '90', 'hi': '110', 'unit': 'mg/L',
                                         'work': ['EDTA factor B = 1', 'Reading 1 = a', 'Reading 2 = b', 'Reading 3 = c']})}
        t = self.dw('DW-R11B', d)
        if t is None:
            return
        self.assertIn('CALCULATION', t)
        self.assertNotIn('Taste', t); self.assertNotIn('Unobjectionable', t)               # blank row and its card
        self.assertNotIn('Recorded as observed', t); self.assertNotIn('Odourless mg/L', t)
        self.assertIn('Formula:', t); self.assertIn('Observed value = Odourless', t); self.assertIn('Result: Odourless', t)
        self.assertIn('Reading 3 = c', t)                                                   # every line of the QC working

    def test_micro_steps_and_unknown_fields(self):
        t = self.dw('DW-R11C', {'date_1': '15-08-2026', 'parameter_1': 'Total Bacterial Count', 'result_1': '06',
                                'bacteria_ans': '06', 'bacteria_param': 'CFU/100 ml', 'fecal_ans': '40', 'fecal_param': 'CFU/100 ml'})
        if t is None:
            return
        self.assertIn('Total Bacterial Count:', t); self.assertIn('Colonies counted = 06', t); self.assertIn('direct count', t)
        self.assertNotIn('Faecal Coliform', t)                                              # no Faecal coliform row

    def test_ww_blank_row(self):
        WasteWaterForm2.objects.create(sample_id='WW-R11', lab_report_no='LR-WW-R11', in_out='out', city_location='Lahore', **KW)
        rec = Ww_rds.objects.create(sample_id='WW-R11', rds={'sample_id': 'WW-R11', 'report_type': 'out', 'date_1': '15-08-2026', 'parameter_1': 'Chromium',
                                                            'result_1': '0.1', 'date_2': '15-08-2026', 'parameter_2': 'Zinc', 'result_2': '---'})
        r = self.c.get('/qc/generate_ww_qc_pdf_response/%d/' % rec.pk); self.assertEqual(r.status_code, 200)
        t = text(r.content)
        if t is None:
            return
        self.assertIn('Chromium', t); self.assertNotIn('Zinc', t); self.assertNotIn('CALCULATION', t)


class RdsR11Style(TestCase):
    def test_fonts(self):
        from fpdf import FPDF
        from QC.rds_lib_pdf import print_lib_cards
        from QC.rds_qc_pdf import print_qc_checks
        sizes, colours = [], []

        class Spy(FPDF):
            def set_font(self, family=None, style='', size=0):
                sizes.append(size); return super().set_font('Helvetica', style.replace('I', ''), size)

            def set_text_color(self, r, g=-1, b=-1):
                colours.append((r, g, b)); return super().set_text_color(r, g, b)
        pdf = Spy(); pdf.add_page()
        data = {'lib_print_001': card(parameter='TPC', formula='CFU/mL = colonies x DF / volume', lines=['5 x 1 / 1 = 5'], result='5', unit='CFU/mL',
                                      inputs=['Colonies counted = 5;  Volume plated (mL) = 1'], check='OK'),
                'qc_print_001': json.dumps({'type': 'WS', 'parameter': 'TPC', 'readings': ['1'], 'work': ['a']})}
        print_lib_cards(pdf, data); print_qc_checks(pdf, data)
        self.assertTrue(sizes); self.assertGreaterEqual(min(sizes), 10)
        self.assertFalse([c for c in colours if c != (0, 0, 0)])
        for f in ('QC/rds_lib_pdf.py', 'QC/rds_qc_pdf.py'):
            self.assertNotRegex(src(*f.split('/')), r'8\.5|9\.5|\[:3\]')
        self.assertNotIn("'I', 8.5", src('QC', 'views', 'ww.py'))

    def test_pages(self):
        for t in ('rds_dw_manual.html', 'rds_ww_manual.html'):
            s = src('templates', t)
            self.assertIn('rds_field_owners.js', s); self.assertIn('rds_manual_gate.js', s)
        g = src('static', 'js', 'rds_manual_gate.js')
        self.assertIn('rds-gated', g); self.assertIn("input[name^=\"parameter_\"]", g)
        self.assertIn('fecalentero', g); self.assertIn('rdsInline', g)                       # R11.2: unmapped sections gated, page hide lifted
        for t in ('rds_dw_manual.html', 'rds_ww_manual.html'):
            self.assertIn('rds_manual_gate.js\' %}?v=20261031a', src('templates', t))
        lib = src('static', 'js', 'rds_formula_lib.js')
        self.assertNotIn('Recorded as observed', lib); self.assertIn('inputs: ins', lib); self.assertIn('SYN: SYN', lib)
        self.assertIn("div.closest('.tss_div, .oil_div')", src('templates', 'rds_ww.html'))
