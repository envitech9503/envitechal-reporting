"""R14.2 (owner 04-11-2026): every WS / RM / CRM is worked with its parameter's formula (zero tolerance), the formula
library recognises the spellings used on the reports, new cards for the parameters reported often, observations without
a dilution factor, GC / AOX work subcontracted."""
import os
import subprocess

from django.test import SimpleTestCase

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = lambda *p: open(os.path.join(ROOT, *p), encoding='utf-8').read()


class R142Print(SimpleTestCase):
    def test_ws_reading_prints_with_its_df(self):
        from QC.rds_print_filter import prune
        out = prune({'date_1': '15-08-2026', 'parameter_1': 'Sulphate', 'result_1': '5', 'for_sulphate1': '20.268', 'for_sulphate1_wsdf': '2', 'for_sulphate2': '', 'for_sulphate2_wsdf': '1'}, 'dw')
        self.assertEqual(out.get('for_sulphate1'), '(20.268 X 2)')
        self.assertEqual(out.get('for_sulphate2', ''), '')
        self.assertFalse(any(k.endswith('_wsdf') for k in out))

    def test_single_reading_is_not_a_fraction(self):
        from QC.rds_pdf_extras import tidy
        f, r, d = tidy('(20.268 X 1) + ( X 1) + ( X 1)', '20.268 mg/L', '3')
        self.assertEqual((f, d), ('20.268 X 1', None))
        f, r, d = tidy('(5 X 1) + (6 X 1) + (7 X 1)', '6 mg/L', '3')
        self.assertEqual(d, '3')

    def test_no_fraction_line_without_divisor(self):
        for f in ('dw.py', 'ww.py'):
            s = src('QC', 'views', f)
            self.assertNotIn('\n        pdf.line(line_start_x, old_y+5.5, line_end_x, old_y+5.5)', s.replace('if divisor_text:', ''))  # sanity
            self.assertGreaterEqual(s.count('if divisor_text:   # R14.2'), 2)


class R142Js(SimpleTestCase):
    def test_checks_take_the_section_formula(self):
        s = src('static', 'js', 'rds_qc.js')
        for t in ('function libFor', 'var DIRECT', 'function bareNative', 'function wsDf', 'sulphate|sulfate', 'cod\\\\b|chemical oxygen', 'rq-wsdf', "'_wsdf'"):
            self.assertIn(t.replace('\\\\', '\\'), s)

    def test_library_cards_and_spellings(self):
        s = src('static', 'js', 'rds_formula_lib.js')
        for card in ('sulphide:', 'chlorinity:', 'leg:', 'pa:', 'algae:', 'moist:', 'dsg:', 'fixed:', 'tan:'):
            self.assertIn('    ' + card + ' {', s)
        for t in ('^bi\\s*-?\\s*carbonates?', 'biochemical oxygen', 'slit density', 'trihalomethane', "'fluride': 'fluoride'", "'conductvity': 'conductivity'", 'oxidation.?reduction'):
            self.assertIn(t, s)

    def test_js_parses(self):
        for f in ('rds_qc.js', 'rds_formula_lib.js', 'rds_draft.js'):
            r = subprocess.run(['node', '-e', "new Function(require('fs').readFileSync(process.argv[1],'utf8'))", os.path.join(ROOT, 'static', 'js', f)], capture_output=True)
            self.assertEqual(r.returncode, 0, r.stderr)


class R142Labels(SimpleTestCase):
    def test_labels(self):
        dw = src('templates', 'rds_dw.html')
        self.assertIn('name="hardness_head_1" id="" value="WS-TH-100ppm:"', dw)
        for t in ('rds_dw', 'rds_dw_manual'):
            self.assertNotIn('value="Residual Chloride"', src('templates', t + '.html'))
        for t in ('rds_dw', 'rds_ww', 'rds_dw_manual', 'rds_ww_manual'):
            s = src('templates', t + '.html')
            self.assertNotIn('value="WS-NH3-0.5ppm"', s); self.assertNotIn('value="WS-AID-1ppm"', s)


class R143(SimpleTestCase):
    """R14.3 (owner 04-11-2026, zero tolerance): old records' WS / CRM readings print with the DF the sample uses; the
    "+" CRM is matched to its own bar on whole words (pH is not phenolic)."""
    def test_old_record_readings_take_df(self):
        from QC.rds_print_filter import prune
        d = {'date_1': 'x', 'parameter_1': 'Sulphate', 'result_1': '5', 'for_sulphate1': '20.268', 'for_sulphate2': '', 'for_sulphate1_1_df': '50',
             'for_sulphate1_1': '36.3', 'sulphate_crm_8_1_1': '22.082', 'sulphate_crm_8_1_2': '', 'sulphate_crm_8_1_ans': '22.082'}
        o = prune(d, 'dw')
        self.assertEqual(o['for_sulphate1'], '(20.268 X 1)'); self.assertEqual(o['sulphate_crm_8_1_1'], '(22.082 X 1)')
        self.assertEqual(o['for_sulphate1_1'], '36.3'); self.assertEqual(o['for_sulphate2'], '')

    def test_single_reading_never_averaged(self):
        from QC.rds_pdf_extras import tidy
        self.assertEqual(tidy('(20.268 X 1)', '20.268 mg/L', '1'), ('20.268 X 1', '20.268 mg/L', None))
        self.assertEqual(tidy('(46.4461 - 46.4) X 1000000', '922 mg/L', '50'), ('(46.4461 - 46.4) X 1000000', '922 mg/L', '50'))   # R14.3.1: a volume divisor stays
        self.assertEqual(tidy('(44.4 - 26.4) X 1 X 1000', '360 mg/L', '50')[2], '50')

    def test_bar_match_whole_words(self):
        s = src('static', 'js', 'rds_qc.js')
        self.assertIn('function pref(long, short)', s); self.assertIn('pref(q, p) || pref(p, q)', s)
        for t in ('rds_dw', 'rds_ww', 'rds_dw_manual', 'rds_ww_manual'):
            self.assertIn("rds_qc.js' %}?v=20261104b", src('templates', t + '.html'))
