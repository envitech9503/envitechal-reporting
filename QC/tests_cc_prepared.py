"""Control charts - "Prepared By" replaces "Performed By" (owner request 23-10-2026, both laboratories).
The Prepared By box carries the name and e-signature of the person who prepared the form on the system.
Run:  manage.py test QC.tests_cc_prepared
"""
import datetime as _dt
from io import BytesIO

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.utils import timezone

from EnviTechAlApp.models import Signatures
from QC.models import ControlChart, ControlChartResult, ControlChartBaseline, ControlChartReviewer, ControlChartSignoff


def _client(u):
    c = Client(); c.force_login(u); return c


def _pdf_text(resp):
    try:
        from pypdf import PdfReader
    except ImportError:
        return None
    return '\n'.join(p.extract_text() for p in PdfReader(BytesIO(resp.content)).pages)


class PreparedByTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('adm', 'a@x', 'x', first_name='Imran', last_name='Kazmi')
        self.tay = User.objects.create_user('tay', 't@x', 'x', first_name='Tayyaba', last_name='Akhlaque')
        self.mar = User.objects.create_user('mar', 'm@x', 'x', first_name='Maryam', last_name='Fatima')
        self.sana = User.objects.create_user('sana', 's@x', 'x', first_name='Sana', last_name='Ashraf')
        self.hina = User.objects.create_user('hina', 'h@x', 'x', first_name='Hina', last_name='Abidi')
        ControlChartReviewer.objects.create(user=self.sana, location='Lahore', created_by=self.admin)
        for u, office in ((self.tay, 'Lahore'), (self.mar, 'Lahore'), (self.sana, 'Lahore'), (self.hina, 'Karachi')):
            Signatures.objects.create(user=u, office=office)
        self.c = ControlChart.objects.create(location='Lahore', activity='CRM', parameter='Chloride', level='', unit='mg/l', equipment='Burette',
                                             equipment_id='ENVI-LAB-EQP-30', method='SM 4500', decimals=2, crm_value='50', crm_range_low='45', crm_range_high='55')
        b = ControlChartBaseline(chart=self.c, version=1, established_on=_dt.date(2026, 1, 1), values=[50, 50.2, 49.8, 50.1, 49.9, 50.0], is_current=True)
        b.compute(); b.save()
        self.b = b
        self.y = 2026

    def _res(self, month, user, value=50.0):
        return ControlChartResult.objects.create(chart=self.c, baseline=self.b, date=_dt.date(self.y, month, 10), value=value, status='ok',
                                                 performed_by=user, performed_at=timezone.now() if user else None)

    def _act(self, user, action, code=302):
        r = _client(user).post('/qc/control-charts/%d/signoff/' % self.c.pk, {'year': self.y, 'action': action})
        self.assertEqual(r.status_code, code)
        return r

    def _so(self):
        return ControlChartSignoff.objects.filter(chart=self.c, year=self.y, month=0).first()

    def test_single_analyst_is_the_preparer(self):
        from QC.views.control_chart import _preparer
        self._res(1, self.tay); self._res(2, self.tay)
        who, explicit, analysts = _preparer(self.c, self.y)
        self.assertEqual((who, explicit, analysts), (self.tay, False, [self.tay]))
        r = _client(self.sana).get('/qc/control-charts/%d/?year=%d' % (self.c.pk, self.y))
        self.assertContains(r, '<b>Prepared by</b>'); self.assertContains(r, 'recorded every result')
        self.assertNotContains(r, 'Performed by'); self.assertNotContains(r, 'Sign as preparer</button>')
        pdf = _client(self.sana).get('/qc/control-charts/%d/pdf/?year=%d' % (self.c.pk, self.y))
        self.assertEqual(pdf.status_code, 200)
        t = _pdf_text(pdf)
        if t is not None:
            self.assertIn('Prepared By', t); self.assertNotIn('Performed By', t); self.assertIn('Tayyaba Akhlaque', t)
        self._act(self.sana, 'review')
        self.assertTrue(self._so().reviewed_at)

    def test_several_analysts_need_a_preparer(self):
        from QC.views.control_chart import _preparer
        self._res(1, self.tay); self._res(2, self.mar)
        self.assertIsNone(_preparer(self.c, self.y)[0])
        r = _client(self.sana).get('/qc/control-charts/%d/?year=%d' % (self.c.pk, self.y))
        self.assertContains(r, "awaiting the preparer"); self.assertContains(r, 'Results recorded by'); self.assertContains(r, 'Sign as preparer</button>')
        # review and approval are refused without a preparer
        r = _client(self.sana).post('/qc/control-charts/%d/signoff/' % self.c.pk, {'year': self.y, 'action': 'review'}, follow=True)
        self.assertContains(r, 'has no Prepared-by signature'); self.assertIsNone(self._so())
        # a Karachi analyst may not prepare a Lahore record
        self._act(self.hina, 'sign', 403)
        r = _client(self.mar).post('/qc/control-charts/%d/signoff/' % self.c.pk, {'year': self.y, 'action': 'sign'}, follow=True)
        self.assertContains(r, 'You signed 2026 as Prepared by')
        so = self._so()
        self.assertEqual((so.prepared_by, bool(so.prepared_at)), (self.mar, True))
        # a second signature is refused
        r = _client(self.tay).post('/qc/control-charts/%d/signoff/' % self.c.pk, {'year': self.y, 'action': 'sign'}, follow=True)
        self.assertContains(r, 'already prepared by Maryam Fatima')
        t = _pdf_text(_client(self.sana).get('/qc/control-charts/%d/pdf/?year=%d' % (self.c.pk, self.y)))
        if t is not None:
            self.assertIn('Maryam Fatima', t); self.assertNotIn('Tayyaba', t)
        self._act(self.sana, 'review'); self._act(self.admin, 'approve')
        so = self._so(); self.assertTrue(so.reviewed_at and so.approved_at)

    def test_imported_results_and_earlier_review(self):
        self._res(1, None); self._res(2, None)
        # a legacy review made before the form had a preparer (as on 6 Lahore CRM forms) - approval is refused
        ControlChartSignoff.objects.create(chart=self.c, year=self.y, month=0, reviewed_by=self.sana, reviewed_at=timezone.now())
        r = _client(self.admin).post('/qc/control-charts/%d/signoff/' % self.c.pk, {'year': self.y, 'action': 'approve'}, follow=True)
        self.assertContains(r, 'has no Prepared-by signature'); self.assertIsNone(self._so().approved_at)
        r = _client(self.tay).post('/qc/control-charts/%d/signoff/' % self.c.pk, {'year': self.y, 'action': 'sign'}, follow=True)
        self.assertContains(r, '2 imported results now carry your name'); self.assertContains(r, 'earlier review was cleared')
        so = self._so()
        self.assertEqual((so.prepared_by, so.reviewed_at), (self.tay, None))
        self.assertEqual(set(self.c.results.values_list('performed_by', flat=True)), {self.tay.pk})

    def test_change_by_another_user_clears_the_preparer(self):
        r1 = self._res(1, self.tay); self._res(2, self.mar)
        self._act(self.tay, 'sign')
        # the preparer corrects her own result: signature kept
        _client(self.tay).post('/qc/control-charts/%d/result/' % self.c.pk, {'date': '2026-01-10', 'value': '50.1', 'result_id': r1.pk})
        self.assertEqual(self._so().prepared_by, self.tay)
        # another analyst changes a result: signature cleared, warning shown
        r = _client(self.mar).post('/qc/control-charts/%d/result/' % self.c.pk, {'date': '2026-03-10', 'value': '50.0'}, follow=True)
        self.assertContains(r, 'Prepared-by signature of 2026 was cleared')
        self.assertIsNone(self._so().prepared_by)

    def test_withdraw(self):
        self._res(1, self.tay); self._res(2, self.mar)
        self._act(self.tay, 'sign')
        self.assertContains(_client(self.tay).get('/qc/control-charts/%d/?year=%d' % (self.c.pk, self.y)), 'Withdraw preparer signature')
        self._act(self.mar, 'unprepare', 403)
        self._act(self.tay, 'unprepare')
        self.assertIsNone(self._so().prepared_by)
        self._act(self.tay, 'sign'); self._act(self.sana, 'review')
        r = _client(self.tay).post('/qc/control-charts/%d/signoff/' % self.c.pk, {'year': self.y, 'action': 'unprepare'}, follow=True)
        self.assertContains(r, 'already reviewed'); self.assertEqual(self._so().prepared_by, self.tay)

    def test_bulk_signing_page(self):
        self._res(1, self.tay); self._res(2, self.mar)
        r = _client(self.tay).get('/qc/control-charts/signing/?location=Lahore&show=sign')
        self.assertContains(r, 'awaiting preparer'); self.assertContains(r, 'Sign selected as preparer'); self.assertContains(r, 'Prepared by')
        self.assertNotContains(r, 'Performed')
        r = _client(self.tay).post('/qc/control-charts/signing/?location=Lahore&show=sign', {'action': 'sign', 'rec': '%d:%d:0' % (self.c.pk, self.y)}, follow=True)
        self.assertContains(r, '1 record signed as Prepared by')
        self.assertEqual(self._so().prepared_by, self.tay)
        r = _client(self.sana).get('/qc/control-charts/signing/?location=Lahore&show=review')
        self.assertContains(r, 'Tayyaba Akhlaque')

    def test_baseline_form_label(self):
        self.b.created_by = self.sana; self.b.save()
        r = _client(self.sana).get('/qc/control-charts/%d/pdf/?year=%d&baseline=1' % (self.c.pk, self.y))
        self.assertEqual(r.status_code, 200)
        t = _pdf_text(r)
        if t is not None:
            self.assertIn('Prepared By', t); self.assertNotIn('Performed By', t)
