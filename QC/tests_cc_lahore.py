"""Control charts - Lahore Lab Manager's items of 23-10-2026 (Sana Ashraf):
per-chart document-control rows (item 2) and re-filing a baseline-mode monitoring chart as a monthly
equipment chart (items 3 / 4).  Run:  manage.py test QC.tests_cc_lahore
"""
import datetime as _dt
from io import StringIO

from django.contrib.auth.models import User
from django.core.management import call_command, CommandError
from django.test import TestCase, Client

from EnviTechAlApp.models import InventoryDocControl
from QC.models import ControlChart, ControlChartResult, ControlChartBaseline, ControlChartReviewer


def _client(u):
    c = Client(); c.force_login(u); return c


def _chart(**kw):
    d = dict(location='Lahore', activity='MON', parameter='Laboratory temperature', level='', unit='°C', equipment='Digital Thermo-Humidity Meter',
             equipment_id='ENVI-LAB-EQP-20', method='Not Applicable', decimals=1, limit_mode='fixed', crm_range_low='20', crm_range_high='30')
    d.update(kw)
    return ControlChart.objects.create(**d)


class DocControlPerChartTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('adm', 'a@x', 'x')
        self.chem = User.objects.create_user('chem', 'c@x', 'x', first_name='Maryam')
        self.mgr = User.objects.create_user('sana', 's@x', 'x', first_name='Sana')
        ControlChartReviewer.objects.create(user=self.mgr, location='Lahore', created_by=self.admin)
        self.t = _chart(doc_no='ETAL-LAB-603-FF-07')
        self.h = _chart(parameter='Laboratory humidity', unit='%', doc_no='ETAL-LAB-603-FF-07A')
        self.v = _chart(parameter='Visi-cooler temperature', equipment='Visi-cooler', equipment_id='ENVI-LAB-EQP-12', limit_mode='run')

    def test_admin_only(self):
        for u, code in ((self.chem, 403), (self.mgr, 403)):
            self.assertEqual(_client(u).get('/qc/control-charts/doc-control/').status_code, code)
            self.assertEqual(_client(u).post('/qc/control-charts/doc-control/', {'chart': self.t.pk, 'doc_no': 'X'}).status_code, code)
        self.assertEqual(_client(self.admin).get('/qc/control-charts/doc-control/').status_code, 200)

    def test_master_number_listed_then_row_takes_precedence(self):
        from QC.views.control_chart import _chart_docctrl
        a = _client(self.admin)
        r = a.get('/qc/control-charts/doc-control/')
        self.assertContains(r, 'ETAL-LAB-603-FF-07A')
        self.assertEqual(r.content.count(b'from chart master'), 2)
        d = _chart_docctrl(self.t)
        self.assertEqual((d['doc_no'], d['issue_date'], d['own'], d['set']), ('ETAL-LAB-603-FF-07', '-', True, True))
        r = a.post('/qc/control-charts/doc-control/', {'chart': self.t.pk, 'doc_no': 'ETAL-LAB-603-FF-07', 'issue_date': '10-01-2024', 'issue_no': '02', 'rev_no': '01'}, follow=True)
        self.assertContains(r, 'Document control updated for chart #%d' % self.t.pk)
        d = _chart_docctrl(self.t)
        self.assertEqual((d['doc_no'], d['issue_date'], d['issue_no'], d['rev_no'], d['own']), ('ETAL-LAB-603-FF-07', '10-01-2024', '02', '01', True))
        self.assertEqual(InventoryDocControl.objects.get(module='cc_chart_%d' % self.t.pk, location='Lahore').issue_no, '02')
        # the laboratory's MON form number is untouched and the other charts keep their master numbers
        self.assertEqual(_chart_docctrl(self.h)['doc_no'], 'ETAL-LAB-603-FF-07A')
        self.assertEqual(_chart_docctrl(self.v)['own'], False)
        r = a.get('/qc/control-charts/%d/' % self.t.pk)
        self.assertContains(r, 'chart-specific form'); self.assertContains(r, '10-01-2024')
        self.assertNotContains(_client(self.chem).get('/qc/control-charts/%d/' % self.v.pk), 'chart-specific form')

    def test_add_and_clear(self):
        from QC.views.control_chart import _chart_docctrl
        a = _client(self.admin)
        a.post('/qc/control-charts/doc-control/', {'chart': self.v.pk, 'doc_no': 'ETAL-LAB-603-FF-07B', 'issue_date': '10-01-2024', 'issue_no': '01', 'rev_no': '00'})
        self.v.refresh_from_db()
        self.assertEqual(self.v.doc_no, 'ETAL-LAB-603-FF-07B')          # the chart master mirrors the number
        self.assertEqual(_chart_docctrl(self.v)['doc_no'], 'ETAL-LAB-603-FF-07B')
        r = a.get('/qc/control-charts/doc-control/')
        self.assertEqual(r.content.count(b'id="ownf'), 3)
        r = a.post('/qc/control-charts/doc-control/', {'chart': self.v.pk, 'action': 'clear'}, follow=True)
        self.assertContains(r, 'now prints the Lahore MON form number')
        self.v.refresh_from_db()
        self.assertEqual(self.v.doc_no, '')
        self.assertFalse(InventoryDocControl.objects.filter(module='cc_chart_%d' % self.v.pk).exists())
        self.assertEqual(_chart_docctrl(self.v)['own'], False)
        self.assertEqual(a.get('/qc/control-charts/doc-control/').content.count(b'id="ownf'), 2)
        self.assertEqual(a.post('/qc/control-charts/doc-control/', {'chart': '999999', 'doc_no': 'X'}).status_code, 404)

    def test_blank_number_clears_lab_move_master_edit_and_deletion(self):
        from QC.views.control_chart import _chart_docctrl
        a = _client(self.admin)
        a.post('/qc/control-charts/doc-control/', {'chart': self.t.pk, 'doc_no': 'ETAL-LAB-603-FF-07', 'issue_date': '10-01-2024', 'issue_no': '02', 'rev_no': '01'})
        # blank number = clear
        a.post('/qc/control-charts/doc-control/', {'chart': self.t.pk, 'doc_no': '  ', 'issue_date': '10-01-2024'})
        self.t.refresh_from_db()
        self.assertEqual(self.t.doc_no, ''); self.assertFalse(InventoryDocControl.objects.filter(module='cc_chart_%d' % self.t.pk).exists())
        # the row follows the chart when the master changes its number or laboratory
        a.post('/qc/control-charts/doc-control/', {'chart': self.h.pk, 'doc_no': 'ETAL-LAB-603-FF-07A', 'issue_date': '10-01-2024', 'issue_no': '02', 'rev_no': '01'})
        form = {'location': 'Karachi', 'activity': 'MON', 'parameter': 'Laboratory humidity', 'level': '', 'unit': '%', 'equipment': 'Digital Thermo-Humidity Meter',
                'equipment_id': 'ENVI-LAB-EQP-20', 'method': 'Not Applicable', 'decimals': '1', 'limit_mode': 'fixed', 'crm_range_low': '30', 'crm_range_high': '70',
                'doc_no': 'ETAL-LAB-603-FF-07A-R1', 'description': 'x', 'crm_detail': '', 'crm_value': '', 'raw_unit': '', 'start_month': '1', 'active': '1'}
        r = a.post('/qc/control-charts/%d/edit/' % self.h.pk, form, follow=True)
        self.assertEqual(r.status_code, 200)
        self.h.refresh_from_db()
        self.assertEqual((self.h.location, self.h.doc_no), ('Karachi', 'ETAL-LAB-603-FF-07A-R1'))
        own = InventoryDocControl.objects.get(module='cc_chart_%d' % self.h.pk)
        self.assertEqual((own.location, own.doc_no, own.issue_date), ('Karachi', 'ETAL-LAB-603-FF-07A-R1', '10-01-2024'))
        d = _chart_docctrl(self.h)
        self.assertEqual((d['doc_no'], d['issue_date'], d['issue_no']), ('ETAL-LAB-603-FF-07A-R1', '10-01-2024', '02'))
        self.assertEqual(InventoryDocControl.objects.filter(module='cc_chart_%d' % self.h.pk).count(), 1)
        # deleting the chart removes its row
        r = a.post('/qc/control-charts/%d/delete/' % self.h.pk, {'reason': 'test deletion of the humidity chart'}, follow=True)
        self.assertEqual(r.status_code, 200)
        self.assertFalse(ControlChart.objects.filter(pk=self.h.pk).exists())
        self.assertFalse(InventoryDocControl.objects.filter(module='cc_chart_%d' % self.h.pk).exists())

    def test_pdf_prints_own_numbers(self):
        a = _client(self.admin)
        a.post('/qc/control-charts/doc-control/', {'chart': self.h.pk, 'doc_no': 'ETAL-LAB-603-FF-07A', 'issue_date': '05-02-2024', 'issue_no': '03', 'rev_no': '02'})
        ControlChartResult.objects.create(chart=self.h, date=_dt.date(2026, 6, 1), time='09:00', value=55.0, status='ok', performed_by=self.chem)
        r = a.get('/qc/control-charts/%d/pdf/?year=2026&month=6' % self.h.pk)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r['Content-Type'], 'application/pdf')
        try:
            from pypdf import PdfReader
        except ImportError:
            return
        from io import BytesIO
        text = PdfReader(BytesIO(r.content)).pages[0].extract_text()
        self.assertIn('ETAL-LAB-603-FF-07A', text); self.assertIn('05-02-2024', text); self.assertIn('03', text)


class MonToEqTests(TestCase):
    """A Lahore-style balance record: IC chart with February and April runs; MON chart in baseline mode
    with v1 = February run (March results), v2 = April run (May results)."""
    def setUp(self):
        self.admin = User.objects.create_superuser('adm', 'a@x', 'x')
        self.mgr = User.objects.create_user('sana', 's@x', 'x', first_name='Sana')
        ControlChartReviewer.objects.create(user=self.mgr, location='Lahore', created_by=self.admin)
        common = dict(location='Lahore', parameter='Weight', level='200 g', unit='g', equipment='Analytical Balance', equipment_id='ENVI-LAB-EQP-02',
                      method='Not Applicable', decimals=4)
        self.ic = ControlChart.objects.create(activity='IC', **common)
        feb = [199.9999, 200.0002, 200.0003, 199.9997, 199.9998, 200.0003, 200.0002, 200.0004, 199.9998, 199.9999, 200.0003, 199.9997]
        apr = [199.9998, 200.0002, 200.0001, 199.9998, 199.9999, 200.0002, 199.9999, 199.9997, 199.9998, 200.0003, 200.0002, 199.9998]
        for i, v in enumerate(feb):
            ControlChartResult.objects.create(chart=self.ic, date=_dt.date(2026, 2, 16 + i), value=v, status='ok')
        for i, v in enumerate(apr):
            ControlChartResult.objects.create(chart=self.ic, date=_dt.date(2026, 4, 16 + i), value=v, status='ok')
        self.mon = ControlChart.objects.create(activity='MON', limit_mode='baseline', crm_value='200', crm_range_low='199.9997', crm_range_high='200.0003',
                                               crm_detail='Dead weight 200 g', **common)
        self.b1 = ControlChartBaseline(chart=self.mon, version=1, established_on=_dt.date(2026, 2, 1), note='February intermediate check (before PT)', values=feb, is_current=False)
        self.b1.compute(); self.b1.save()
        self.b2 = ControlChartBaseline(chart=self.mon, version=2, established_on=_dt.date(2026, 4, 16), note='April intermediate check (after calibration)', values=apr, is_current=True)
        self.b2.compute(); self.b2.save()
        for i, v in enumerate([199.9998, 200.0004, 200.0002, 199.9997]):          # 200.0004 is outside the +/-0.0003 acceptance range
            ControlChartResult.objects.create(chart=self.mon, baseline=self.b1, date=_dt.date(2026, 3, 2 + i), value=v, status='ooc' if v > 200.0003 else 'ok')
        for i, v in enumerate([199.9998, 200.0002, 200.0003, 200.0001]):
            ControlChartResult.objects.create(chart=self.mon, baseline=self.b2, date=_dt.date(2026, 5, 2 + i), value=v, status='ok')

    def _run(self, *args):
        out = StringIO(); call_command('cc_mon_to_eq', *args, stdout=out); return out.getvalue()

    def test_dry_run_changes_nothing(self):
        out = self._run(str(self.mon.pk))
        self.assertIn('DRY RUN', out); self.assertIn('baseline v1 (n=12, est. 2026-02-01) = IC run Feb-2026', out); self.assertIn('= IC run Apr-2026', out)
        self.mon.refresh_from_db()
        self.assertEqual(self.mon.activity, 'MON')
        self.assertEqual(self.mon.results.filter(status='ooc').count(), 1)
        self.assertEqual(ControlChartBaseline.objects.get(pk=self.b1.pk).dates, [])

    def test_apply(self):
        out = self._run(str(self.mon.pk), '--apply')
        self.assertIn('APPLIED', out)
        self.mon.refresh_from_db(); self.b1.refresh_from_db(); self.b2.refresh_from_db()
        self.assertEqual((self.mon.activity, self.mon.limit_mode), ('EQ', ''))
        self.assertEqual(self.ic.eq_chart().pk, self.mon.pk)
        self.assertEqual(self.b1.dates[0], '2026-02-16'); self.assertEqual(len(self.b2.dates), 12)
        self.assertTrue(self.b1.note.startswith('February intermediate check (before PT); Intermediate check Feb-2026'))
        self.assertIn('IC chart #%d' % self.ic.pk, self.b2.note)
        # results keep their baseline; statuses re-judged by the baseline rule (200.0004 < mean + 2 SD of v1)
        self.assertEqual(set(self.mon.results.filter(date__month=3).values_list('baseline_id', flat=True)), {self.b1.pk})
        self.assertEqual(self.mon.results.filter(status='ooc').count(), 0)
        self.assertEqual(self.mon.results.count(), 8)
        # a second run is refused; so is a chart with fixed limits / without an IC chart
        with self.assertRaises(CommandError):
            self._run(str(self.mon.pk))
        other = _chart(location='Lahore', parameter='Weight', level='200 g', equipment_id='ENVI-LAB-EQP-02', limit_mode='fixed')
        with self.assertRaises(CommandError):
            self._run(str(other.pk))
        other.limit_mode = 'baseline'; other.equipment_id = 'ENVI-LAB-EQP-99'; other.save()
        with self.assertRaises(CommandError):
            self._run(str(other.pk))
        with self.assertRaises(CommandError):
            self._run('999999')

    def test_refuses_reviewed_month_unless_forced(self):
        from django.utils import timezone
        from QC.models import ControlChartSignoff
        ControlChartSignoff.objects.create(chart=self.mon, year=2026, month=3, reviewed_by=self.mgr, reviewed_at=timezone.now())
        out = self._run(str(self.mon.pk), '--apply')
        self.assertIn('REFUSED', out); self.assertIn('NOT APPLIED', out); self.assertIn('03-03-2026  200.0004  ooc -> ok  (month reviewed', out)
        self.mon.refresh_from_db(); self.assertEqual(self.mon.activity, 'MON')
        self.assertEqual(self.mon.results.filter(status='ooc').count(), 1)
        out = self._run(str(self.mon.pk), '--apply', '--force')
        self.assertIn('APPLIED', out)
        self.mon.refresh_from_db(); self.assertEqual(self.mon.activity, 'EQ')
        self.assertEqual(self.mon.results.filter(status='ooc').count(), 0)

    def test_sop_note_wording(self):
        from QC.views.control_chart import _sop_note
        self._run(str(self.mon.pk), '--apply')
        self.mon.refresh_from_db(); self.b1.refresh_from_db(); self.b2.refresh_from_db()
        self.assertIn('from the February intermediate check activity', _sop_note(self.mon, self.b1)); self.assertIn('(conducted before PT)', _sop_note(self.mon, self.b1))
        self.assertIn('from the April intermediate check activity', _sop_note(self.mon, self.b2)); self.assertIn('(conducted after calibration)', _sop_note(self.mon, self.b2))
        # a February run with no stated purpose keeps the profile wording (Karachi charts created from the IC run)
        self.b1.note = 'Intermediate check Feb-2026 of the Analytical Balance (Weight 200 g; IC chart #1) - ETAL-LAB-P-604'
        self.assertEqual(_sop_note(self.mon, self.b1), self.mon.profile['note'])
        self.b2.note = 'Intermediate check Apr-2026 of the Analytical Balance - ETAL-LAB-P-604'
        self.assertNotIn('(conducted', _sop_note(self.mon, self.b2)); self.assertIn('from the April intermediate', _sop_note(self.mon, self.b2))
        self.b2.note = 'Run before calibration, department note'
        self.assertNotIn('(conducted', _sop_note(self.mon, self.b2))
        self.b2.note = 'Adopted (PT).'
        self.assertIn('(conducted before PT)', _sop_note(self.mon, self.b2))
        self.assertEqual(_sop_note(self.mon, None), self.mon.profile['note'])
        self.assertEqual(_sop_note(self.ic, self.b2), self.ic.profile['note'])

    def test_pages_after_conversion(self):
        self._run(str(self.mon.pk), '--apply')
        c = _client(self.mgr)
        r = c.get('/qc/control-charts/equipment/?location=Lahore')
        self.assertContains(r, 'Mar-2026'); self.assertContains(r, 'May-2026')
        self.assertNotContains(c.get('/qc/control-charts/?location=Lahore&activity=MON&year=2026'), 'Analytical Balance')
        self.assertContains(c.get('/qc/control-charts/?location=Lahore&activity=EQ&year=2026'), 'Analytical Balance')
        # each month names the run it was judged against
        r = c.get('/qc/control-charts/%d/?year=2026&month=3' % self.mon.pk)
        self.assertContains(r, 'from the February intermediate check activity'); self.assertContains(r, '(conducted before PT)')
        r = c.get('/qc/control-charts/%d/?year=2026&month=5' % self.mon.pk)
        self.assertContains(r, 'from the April intermediate check activity'); self.assertContains(r, '(conducted after calibration)')
        for m in (3, 5):
            r = c.get('/qc/control-charts/%d/pdf/?year=2026&month=%d' % (self.mon.pk, m))
            self.assertEqual((r.status_code, r['Content-Type']), (200, 'application/pdf'))
        self.assertEqual(c.get('/qc/control-charts/%d/baseline/' % self.mon.pk).status_code, 200)
        self.assertEqual(c.get('/qc/control-charts/%d/pdf/?year=2026&month=3&baseline=1' % self.mon.pk).status_code, 200)
        # a new result in the open month goes to the current baseline; the EQ rule judges it
        today = _dt.date.today()
        r = c.post('/qc/control-charts/%d/result/' % self.mon.pk, {'date': today.strftime('%d-%m-%Y'), 'value': '200.0001', 'year': today.year, 'month': today.month}, follow=True)
        self.assertEqual(r.status_code, 200)
        last = self.mon.results.order_by('-date').first()
        self.assertEqual((last.baseline_id, last.status), (self.b2.pk, 'ok'))
