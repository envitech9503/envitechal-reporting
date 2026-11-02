"""R13 (owner strict QA 02-11-2026): no "Check:" line on any RDS PDF; WS / RM / CRM rows and calculation blocks stay in
step on every page; every saved formula-library line format printed in the sheet's fraction style; one typography."""
import json
import os

from django.conf import settings
from django.test import SimpleTestCase
from fpdf import FPDF

from QC.rds_lib_pdf import parse_line, print_lib_cards, split_fraction, _unwrap

BASE = settings.BASE_DIR if hasattr(settings, 'BASE_DIR') else os.getcwd()


def src(*p):
    with open(os.path.join(str(BASE), *p), encoding='utf-8') as fh:
        return fh.read()


def new_pdf():
    pdf = FPDF()
    root = str(BASE)
    pdf.add_font('Calibri', '', os.path.join(root, 'static/fonts/calibri.ttf'))
    pdf.add_font('Calibri', 'B', os.path.join(root, 'static/fonts/calibrib.ttf'))
    pdf.set_auto_page_break(False); pdf.add_page(); pdf.set_y(20); pdf.set_font('Calibri', '', 10)
    return pdf


def texts(pdf):
    """the strings handed to pdf.cell / multi_cell, in order"""
    out = []
    oc, om = pdf.cell, pdf.multi_cell

    def cell(w=0, h=0, txt='', *a, **k):
        out.append(str(k.get('text', txt))); return oc(w, h, txt, *a, **k)

    def mcell(w, h, txt='', *a, **k):
        out.append(str(k.get('text', txt))); return om(w, h, txt, *a, **k)
    pdf.cell, pdf.multi_cell = cell, mcell
    return out


class RdsR13LibLines(SimpleTestCase):
    def test_old_average_rebuilt_from_readings(self):
        reps = ['57', '60', '60']
        self.assertEqual(parse_line('Average of 3 = 59', reps), [('AVERAGE', None, '(57 + 60 + 60) / 3', '59')])
        self.assertEqual(parse_line('Average = (40 + 36) / 2 = 38'), [('AVERAGE', None, '(40 + 36) / 2', '38')])

    def test_labelled_lines_keep_the_label_out_of_the_numerator(self):
        self.assertEqual(parse_line('Hardness = 1.4 x 1 x 1000 / 50 = 28 mg/L as CaCO3'), [(None, 'Hardness', '1.4 x 1 x 1000 / 50', '28 mg/L as CaCO3')])
        self.assertEqual(parse_line('(as calcium: 1.4 x 1 x 400.8 / 50 = 11.22 mg/L Ca)'), [(None, 'As calcium', '1.4 x 1 x 400.8 / 50', '11.22 mg/L Ca')])
        self.assertEqual(parse_line('Replicate 2: 20 x 100 x 2 / 100 = 40'), [('Reading 02', None, '20 x 100 x 2 / 100', '40')])
        self.assertEqual(parse_line('Replicate 1: (45.1 - 45.0) x 1000000 x DF 2 / 100 = 2000')[0][2], '(45.1 - 45.0) x 1000000 x DF 2 / 100')
        self.assertEqual(parse_line('Result x DF = 26.88 x 2 = 53.76'), [('Dilution factor', None, '26.88 x 2', '53.76')])
        self.assertEqual(len(parse_line('Total = 0.5 x 2 = 1 mg/L;  free = 0.4 mg/L;  combined = 1 - 0.4 = 0.6 mg/L')), 3)

    def test_qc_and_duplicate_lines_not_printed(self):
        self.assertEqual(parse_line('Check standard: 98 / 100 = 98 % recovery'), [])
        self.assertEqual(parse_line('Result = Odourless'), [(None, None, 'Result = Odourless', None)])   # an observation keeps its step

    def test_fraction_helpers(self):
        self.assertEqual(split_fraction('[(8.2 - 4.1) - 0.3] / (5 / 300)'), ('[(8.2 - 4.1) - 0.3]', '(5 / 300)'))
        self.assertEqual(_unwrap('(57 + 60 + 60)'), '57 + 60 + 60')
        self.assertEqual(_unwrap('(45.1 - 45.0) x 1000000'), '(45.1 - 45.0) x 1000000')
        self.assertEqual(_unwrap('[(8.2 - 4.1) - 0.3]'), '(8.2 - 4.1) - 0.3')

    def test_cards_print_no_check_and_no_old_formats(self):
        card = {'parameter': 'Biological Oxygen Demand (BOD5)', 'side': '', 'method': 'HACH 10099', 'calc': 'Instrumental reading', 'unit': 'mg/L',
                'lines': ['Replicate 1: 57 x 1 = 57', 'Replicate 2: 60 x 1 = 60', 'Replicate 3: 60 x 1 = 60', 'Average of 3 = 59', 'Check standard: 9 / 10 = 90 % recovery'],
                'inputs': ['Replicate 1: Reading = 57'], 'result': '59', 'check': 'OK'}
        hard = {'parameter': 'Calcium Hardness as CaCO3', 'calc': 'EDTA titration', 'method': 'ASTM D 1126', 'unit': 'mg/L', 'result': '28', 'check': 'OK',
                'lines': ['Hardness = 1.4 x 1 x 1000 / 50 = 28 mg/L as CaCO3', '(as calcium: 1.4 x 1 x 400.8 / 50 = 11.22 mg/L Ca)']}
        pdf = new_pdf(); t = texts(pdf)
        print_lib_cards(pdf, {'lib_print_001': json.dumps(card), 'lib_print_002': json.dumps(hard)})
        joined = '\n'.join(t)
        self.assertNotIn('Check', joined); self.assertNotIn('recovery', joined)
        self.assertNotIn('of 3', joined)
        self.assertIn('57 + 60 + 60', joined); self.assertIn('Reading 01:', joined)      # the inputs named as the working
        self.assertIn('Hardness = ', t); self.assertIn('1.4 X 1 X 1000', t); self.assertIn('As calcium = ', t)
        self.assertNotIn('Hardness = 1.4', joined)                                        # the label is not in the numerator


class RdsR13Typography(SimpleTestCase):
    def test_subheadings_bold_10_and_capitalised(self):
        from QC.rds_pdf_extras import install_typo
        pdf = new_pdf(); seen = []
        oc = pdf.cell

        def spy(w=0, h=0, txt='', *a, **k):
            seen.append((txt, pdf.font_size_pt)); return oc(w, h, txt, *a, **k)
        pdf.cell = spy                                      # what reaches fpdf after the normaliser
        install_typo(pdf); install_typo(pdf)                # installed once only
        pdf.set_font('Calibri', 'B', 11); pdf.cell(0, 6, 'Hardness Calculation:', ln=True)
        pdf.set_font('Calibri', 'B', 11); pdf.cell(0, 6, 'Reading 02', ln=True)
        pdf.set_font('Calibri', 'B', 11); pdf.cell(0, 6, 'Reading 02 (Inlet):', ln=True)
        pdf.set_font('Calibri', 'B', 11); pdf.cell(0, 6, 'WS-COD-100ppm (Outlet):', ln=True)
        pdf.set_font('Calibri', 'B', 10); pdf.cell(0, 6, 'hardness:', ln=True)
        pdf.set_font('Calibri', 'B', 10); pdf.cell(0, 6, 'pH:', ln=True)
        pdf.set_font('Calibri', 'B', 10); pdf.cell(0, 6, 'arsenic', ln=True)
        pdf.set_font('Calibri', 'B', 10); pdf.cell(0, 6, 'ionic_det', ln=True)
        pdf.set_font('Calibri', 'B', 10); pdf.cell(0, 6, 'Total Chromium =', ln=True)
        self.assertEqual(seen[0], ('Hardness Calculation:', 11))
        self.assertEqual(seen[1][1], 10); self.assertEqual(seen[2][1], 10); self.assertEqual(seen[3][1], 10)
        self.assertEqual(seen[4][0], 'Hardness:'); self.assertEqual(seen[5][0], 'pH:')
        self.assertEqual(seen[6][0], 'Arsenic'); self.assertEqual(seen[7][0], 'Anionic surfactants (MBAS)')
        self.assertEqual(seen[8][0], 'Total Chromium:')

    def test_no_check_note_on_ww(self):
        from QC.views.ww import _rds_note
        pdf = new_pdf(); t = texts(pdf)
        _rds_note(pdf, 'seed-control DO depletion below 2.0')
        self.assertEqual(t, [])

    def test_remarks_fit_their_cell(self):
        for f in ('QC/views/dw.py', 'QC/views/ww.py'):
            self.assertIn("fit_cell(pdf, col_widths[", src(*f.split('/')))
            self.assertNotIn("str(data.get(f'remarks_{row_key}', '')),\n", src(*f.split('/')))


class RdsR13Sync(SimpleTestCase):
    def test_one_removal_and_linked_blocks(self):
        qc = src('static', 'js', 'rds_qc.js')
        for s in ('function dropRow(tr)', 'e.stopImmediatePropagation(); e.preventDefault();', 'function nativeRemove(blk, tr)',
                  "closest('.generate-crm-btn')", 'function syncCounters()', 'R13: an empty heading', 'R13: readings cleared',
                  "if (blk.dataset.type !== 'CRM') return null;", 'sameParam(b.dataset.param, want)'):
            self.assertIn(s, qc)
        for t in ('rds_dw.html', 'rds_ww.html', 'rds_dw_manual.html', 'rds_ww_manual.html'):
            self.assertRegex(src('templates', t), r"rds_qc\.js' %\}\?v=20261102a")


class RdsR13PairLine(SimpleTestCase):
    def test_toxic_metal_label_without_its_equals_sign(self):
        from QC.views.ww import _pair_line
        pdf = new_pdf(); t = texts(pdf)
        _pair_line(pdf, {'toxic_1': 'Cadmium=', 'toxic_1_1': '0.01'}, 'toxic_1', 'toxic_1_1')
        self.assertEqual(t, ['Cadmium = 0.01'])


class RdsR13Production(SimpleTestCase):
    """Production check after R13 (02-11-2026): old records with readings saved without their factor (dw72), a reading
    whose "=" was never pressed (dw440, dw542, dw611) and a result saved as "[object HTMLInputElement]" (dw424)."""
    def test_factorless_readings_and_uncalculated(self):
        from QC.rds_pdf_extras import tidy, bare_factorless
        self.assertEqual(tidy('(10 X ) + (10 X ) + (10 X )', '10 TCU', '3'), ('10 + 10 + 10', '10 TCU', '3'))
        self.assertEqual(tidy('(0 X 1) + (0 X 1) + (0 X )', '0.00 mg/L', '2'), ('(0 X 1) + (0 X 1)', '0.00 mg/L', '2'))   # R12 rule kept
        self.assertEqual(tidy('(49.3275 - 49.2854) X 1000000', ' mg/L', '100')[1], 'not calculated')
        self.assertEqual(tidy('(5 X 1) + (5 X 1)', '5 mg/L', '2')[1], '5 mg/L')
        self.assertEqual(bare_factorless('(-0.9 X )'), '-0.9')

    def test_typo_wrapper_bares_factorless_text(self):
        from QC.rds_pdf_extras import install_typo
        pdf = new_pdf(); seen = []
        oc = pdf.cell
        pdf.cell = lambda w=0, h=0, txt='', *a, **k: (seen.append(txt), oc(w, h, txt, *a, **k))[1]
        install_typo(pdf)
        pdf.cell(0, 6, '(10 X ) + (10 X ) + (10 X ) = 10 TCU', ln=True)
        self.assertEqual(seen, ['10 + 10 + 10 = 10 TCU'])

    def test_object_value_is_blank(self):
        from QC.rds_print_filter import printed_row
        self.assertFalse(printed_row({'parameter_9': 'Chromium III', 'result_9': '[object HTMLInputElement]'}, '9'))


class RdsR13WsBlank(SimpleTestCase):
    def test_ph_buffer_heading_needs_readings(self):
        for f in ('QC/views/dw.py', 'QC/views/ww.py'):
            s = src(*f.split('/'))
            self.assertNotIn('in enumerate(ph_sections, start=1):\n                if data.get(head):\n', s)
            self.assertIn("R13.2: a buffer left blank prints no heading", s)
