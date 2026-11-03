"""R14.1 (owner 03-11-2026): Chromium III / VI have their own results; no QC verdict on any RDS PDF; a calcium check
offers both formulas; the browser copy of the draft is removed once the RDS is saved."""
import json
import os

from django.test import TestCase, SimpleTestCase, RequestFactory

from EnviTechAlApp.models import DrinkingWaterForm, Sample_registration

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = lambda *p: open(os.path.join(ROOT, *p), encoding='utf-8').read()


class R141Chromium(TestCase):
    def test_chromium_iii_and_vi_rows(self):
        from QC.views.dw import get_dw
        Sample_registration.objects.create(sample_id='DW-R141', city_location='Lahore', other_param_26=True, other_param_27=True, checkinp64=True)
        DrinkingWaterForm.objects.create(sample_id='DW-R141', city_location='Lahore', water_sr1='7.2', water_sr21='0.004',
                                         extra_field="[{'parameters': 'Chromium (III)', 'result': '0.012'}, {'parameters': 'Chromium VI', 'result': '<0.005'}]")
        r = get_dw(RequestFactory().post('/', json.dumps({'sample_id': 'DW-R141'}), content_type='application/json'))
        rows = [(x['parameter'], x['test_result']) for x in json.loads(r.content)['qc_data']]
        d = dict(rows)
        self.assertEqual(d.get('Chromium III'), '0.012')
        self.assertEqual(d.get('Chromium VI'), '<0.005')
        self.assertEqual(len([p for p, _ in rows if 'hromium' in p and 'III' in p]), 1)   # "Chromium (III)" not added twice
        self.assertEqual(d.get('Selenium'), '0.004')                                   # its own report field, not Chromium VI


class R141Verdict(SimpleTestCase):
    def test_remark_filter(self):
        from QC.rds_pdf_extras import remark
        for v in ['Within acceptance', 'Outside acceptance', 'Check: OK', 'within acceptable limits.', 'Within limits',
                  'Satisfactory', 'Unsatisfactory', 'OK', 'Passed']:
            self.assertEqual(remark({'remarks_1_1': v}, '1_1'), '', v)
        for v in ['Sample diluted 1:10', 'Repeated on 02-11-2026', 'N.D.']:
            self.assertEqual(remark({'remarks_1': v}, '1'), v)
        self.assertEqual(remark({}, '1'), '')

    def test_tables_use_the_filter(self):
        for f in ('dw.py', 'ww.py'):
            s = src('QC', 'views', f)
            self.assertNotIn("str(data.get(f'remarks_{row_key}', ''))", s)
        self.assertEqual(src('QC', 'views', 'ww.py').count('.remark(data, row_key)'), 2)
        self.assertEqual(src('QC', 'views', 'dw.py').count('.remark(data, row_key)'), 1)

    def test_page_does_not_write_the_verdict_into_remarks(self):
        s = src('static', 'js', 'rds_qc.js')
        self.assertNotIn('if (rm && verdict) rm.value = verdict', s)


class R141Js(SimpleTestCase):
    def test_calcium_offers_both(self):
        s = src('static', 'js', 'rds_qc.js')
        for t in ['function camHtml', 'rq-cam', 'value="df"', 'value="edta"', 'camOf(blk) !== \'edta\'']:
            self.assertIn(t, s)

    def test_draft_cleared_on_save(self):
        s = src('static', 'js', 'rds_draft.js')
        self.assertIn('create_(dw|ww)_qc(_manual)?', s); self.assertIn('localStorage.removeItem(LS + sid)', s)

    def test_versions(self):
        for page in ('rds_dw', 'rds_ww', 'rds_dw_manual', 'rds_ww_manual'):
            t = src('templates', page + '.html')
            for js in ('rds_qc.js', 'rds_draft.js', 'rds_formula_lib.js'):
                self.assertRegex(t, r"%s' %%\}\?v=2026110\d[a-z]" % js.replace('.', r'\.'))
