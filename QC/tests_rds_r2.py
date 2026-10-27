"""RDS release R2 (QA audit 27-10-2026): record integrity - validated save with CSRF, laboratory scope of the PDF,
revisions with the latest used by Testing Results, no outside IP look-up."""
import json

from django.contrib.auth.models import User
from django.test import TestCase, Client

from EnviTechAlApp.models import WasteWaterForm2, DrinkingWaterForm, Signatures, Sample_registration
from QC.models import Dw_rds, Ww_rds

KW = dict(report_to='QA', address='L', attention='A', date_of_analysis_from='20-Oct-2026', date_of_analysis_to='25-Oct-2026',
          reporting_date='26-October-2026')
ROW = {'date_1': '20-Oct-2026', 'parameter_1': 'TDS', 'result_1': '471', 'performed_by_1': '1', 'checked_by_1': '1'}


def C(u, csrf=False):
    c = Client(REMOTE_ADDR='127.0.0.1', enforce_csrf_checks=csrf); c.force_login(u); return c


class RdsR2Tests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ceo = User.objects.create_superuser('r2_ceo', 'c@x.c', 'x')
        cls.lhr = User.objects.create_user('r2_lhr', first_name='Lahore')
        Signatures.objects.create(user=cls.lhr, office='Lahore')
        DrinkingWaterForm.objects.create(sample_id='DW-R2-LHR', lab_report_no='A', city_location='Lahore', extra_field='[]',
                                         sample_collection_date='21-Oct-2026', **KW)
        DrinkingWaterForm.objects.create(sample_id='DW-R2-KHI', lab_report_no='B', city_location='Karachi', extra_field='[]',
                                         sample_collection_date='21-Oct-2026', **KW)
        WasteWaterForm2.objects.create(sample_id='WW-R2-LHR', lab_report_no='C', in_out='out', city_location='Lahore', **KW)
        for s in ('DW-R2-LHR', 'DW-R2-KHI'):
            Sample_registration.objects.create(sample_id=s, city_location='Lahore' if 'LHR' in s else 'Karachi')

    def post(self, c, url, body, **kw):
        return c.post(url, json.dumps(body), content_type='application/json', **kw)

    def test_save_is_validated(self):
        c = C(self.lhr)
        r = self.post(c, '/qc/create_dw_qc/', dict(ROW))
        self.assertEqual(r.status_code, 400); self.assertIn('Select a sample', r.json()['message'])
        r = self.post(c, '/qc/create_dw_qc/', dict(ROW, sample_id='NOT-A-SAMPLE'))
        self.assertEqual(r.status_code, 400); self.assertIn('not found', r.json()['message'])
        r = self.post(c, '/qc/create_dw_qc/', dict(ROW, sample_id='DW-R2-KHI'))
        self.assertEqual(r.status_code, 403); self.assertIn('Karachi', r.json()['message'])
        r = self.post(c, '/qc/create_dw_qc/', {'sample_id': 'DW-R2-LHR'})
        self.assertEqual(r.status_code, 400); self.assertIn('no parameter rows', r.json()['message'])
        self.assertEqual(self.post(c, '/qc/create_dw_qc/', dict(ROW, sample_id='DW-R2-LHR')).status_code, 302)
        self.assertEqual(self.post(c, '/qc/create_ww_qc/', dict(ROW, sample_id='WW-R2-LHR')).status_code, 302)
        self.assertEqual(Dw_rds.objects.count(), 1)

    def test_csrf_required(self):
        c = C(self.lhr, csrf=True)
        self.assertEqual(self.post(c, '/qc/create_dw_qc/', dict(ROW, sample_id='DW-R2-LHR')).status_code, 403)
        page = c.get('/qc/create_dw_qc/')
        token = page.cookies['csrftoken'].value if 'csrftoken' in page.cookies else c.cookies['csrftoken'].value
        self.assertEqual(self.post(c, '/qc/create_dw_qc/', dict(ROW, sample_id='DW-R2-LHR'), HTTP_X_CSRFTOKEN=token).status_code, 302)

    def test_pdf_scope_and_revisions(self):
        khi = Dw_rds.objects.create(sample_id='DW-R2-KHI', rds=dict(ROW))
        self.assertEqual(C(self.lhr).get('/qc/generate_dw_qc_pdf_response/%d/' % khi.pk).status_code, 403)
        self.assertEqual(C(self.ceo).get('/qc/generate_dw_qc_pdf_response/%d/' % khi.pk).status_code, 200)
        self.assertEqual(C(self.ceo).get('/qc/generate_dw_qc_pdf_response/999999/').status_code, 404)
        Dw_rds.objects.create(sample_id='DW-R2-LHR', rds=dict(ROW, result_1='470'))
        Dw_rds.objects.create(sample_id='DW-R2-LHR', rds=dict(ROW, result_1='471'))
        r = C(self.lhr).post('/qc/dw_testing_results_sample/', {'sample_id': 'DW-R2-LHR'})
        self.assertEqual(r.status_code, 200); self.assertEqual(r.json()['dw_data']['rds']['result_1'], '471')   # latest
        rows = C(self.lhr).get('/qc/dw_rds_list/').context['list']
        self.assertEqual(sorted((x.rev, x.is_latest) for x in rows), [(1, False), (2, True)])
        page = C(self.lhr).get('/qc/dw_testing_results_sample/')
        self.assertEqual(list(page.context['all_sample_ids']), ['DW-R2-LHR'])                  # own laboratory, once
        self.assertContains(page, "val('Lahore')")
        Ww_rds.objects.create(sample_id='WW-R2-LHR', rds=dict(ROW)); Ww_rds.objects.create(sample_id='WW-R2-LHR', rds=dict(ROW))
        self.assertEqual(C(self.lhr).post('/qc/ww_testing_results_sample/', {'sample_id': 'WW-R2-LHR'}).status_code, 200)

    def test_pages(self):
        c = C(self.lhr)
        for url in ('/qc/create_dw_qc/', '/qc/create_dw_qc_manual/', '/qc/create_ww_qc/', '/qc/create_ww_qc_manual/',
                    '/qc/dw_testing_results_sample/', '/qc/ww_testing_results_sample/'):
            r = c.get(url)
            self.assertEqual(r.status_code, 200, url)
            self.assertNotContains(r, 'ipify'); self.assertNotContains(r, 'ipinfo.io')
            if 'create' in url:
                self.assertContains(r, 'rds_page.js'); self.assertContains(r, 'rdsBeforeSave(data)'); self.assertContains(r, 'rdsPdfResponse')
        self.assertNotContains(c.get('/qc/dw_testing_results_sample/'), 'https://report.envitechal.com')
