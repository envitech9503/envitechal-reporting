"""Document Control register with revision history (owner decision 23-10-2026): a new revision of a form applies to
documents dated from its effective date; documents dated earlier keep the revision they were issued with.
Run:  manage.py test QC.tests_doccontrol
"""
import datetime as _dt

from django.contrib.auth.models import User
from django.test import TestCase, Client

from EnviTechAlApp import doccontrol as DC
from EnviTechAlApp.models import DocControlRevision, InventoryDocControl
from QC.models import ControlChart, IaPlan

D = _dt.date
TODAY = _dt.date.today()


def _client(u):
    c = Client(REMOTE_ADDR='127.0.0.1'); c.force_login(u); return c


def _vals(doc_no, issue_date='01-01-2020', issue_no='01', rev_no='00'):
    return {'doc_no': doc_no, 'issue_date': issue_date, 'issue_no': issue_no, 'rev_no': rev_no}


class RevisionSelectionTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('adm', 'a@x', 'x')

    def test_old_documents_keep_their_revision(self):
        DC.doc_control('job_completion', 'Karachi', D(2025, 1, 1), default=_vals('ETAL-LAB-704-FF-08', '15-05-2026'))
        DC.issue_revision('job_completion', 'Karachi', _vals('ETAL-LAB-704-FF-08', '01-11-2026', '02', '00'), D(2026, 11, 1), 'form revised', self.admin)
        self.assertEqual(DC.doc_control('job_completion', 'Karachi', D(2026, 10, 31))['issue_no'], '01')
        self.assertEqual(DC.doc_control('job_completion', 'Karachi', D(2026, 11, 1))['issue_no'], '02')
        self.assertEqual(DC.doc_control('job_completion', 'Karachi', D(2020, 1, 1))['issue_date'], '15-05-2026')
        # the other laboratory is untouched
        self.assertEqual(DC.doc_control('equipment', 'Lahore', D(2027, 1, 1), default=_vals('L-1'))['doc_no'], 'L-1')
        self.assertEqual(DC.doc_control('job_completion', 'Lahore', D(2027, 1, 1))['issue_no'], '01')

    def test_future_revision_is_scheduled_and_mirror_shows_today(self):
        DC.issue_revision('equipment', 'Karachi', _vals('EQ-1'), D(2000, 1, 1), 'baseline', self.admin)
        DC.issue_revision('equipment', 'Karachi', _vals('EQ-2'), TODAY + _dt.timedelta(days=10), 'scheduled', self.admin)
        self.assertEqual(DC.doc_control('equipment', 'Karachi')['doc_no'], 'EQ-1')
        self.assertEqual(InventoryDocControl.objects.get(module='equipment', location='Karachi').doc_no, 'EQ-1')
        self.assertEqual(DC.doc_control('equipment', 'Karachi', TODAY + _dt.timedelta(days=10))['doc_no'], 'EQ-2')

    def test_first_issue_keeps_values_printed_so_far(self):
        InventoryDocControl.objects.create(module='chemicals', location='Lahore', doc_no='CH-OLD', issue_date='01-01-2021')
        DocControlRevision.objects.filter(module='chemicals').delete()        # as before revision history existed
        DC.issue_revision('chemicals', 'Lahore', _vals('CH-NEW'), D(2026, 11, 1), 'revised', self.admin)
        self.assertEqual(DC.doc_control('chemicals', 'Lahore', D(2026, 6, 1))['doc_no'], 'CH-OLD')
        self.assertEqual(DC.doc_control('chemicals', 'Lahore', D(2026, 11, 2))['doc_no'], 'CH-NEW')

    def test_module_page_save_becomes_revision_from_today(self):
        m = InventoryDocControl.objects.create(module='mou', location='Lahore', doc_no='MOU-1', issue_date='01-01-2024')
        revs = list(DC.revisions('mou', 'Lahore'))
        # Lahore had no number: older studies keep "TBA", the number applies from today
        self.assertEqual([(r.effective_from, r.doc_no) for r in revs], [(TODAY, 'MOU-1'), (DC.BASELINE, '')])
        self.assertEqual(DC.doc_control('mou', 'Lahore', TODAY - _dt.timedelta(days=1))['doc_no'], 'TBA')
        m.doc_no = 'MOU-2'; m.save()
        self.assertEqual(DC.revisions('mou', 'Lahore').first().doc_no, 'MOU-2')
        self.assertEqual(DC.doc_control('mou', 'Lahore', TODAY)['doc_no'], 'MOU-2')
        n = DC.revisions('mou', 'Lahore').count()
        m.save()                                                             # unchanged save: no new revision
        self.assertEqual(DC.revisions('mou', 'Lahore').count(), n)

    def test_first_save_keeps_reader_default_for_older_documents(self):
        InventoryDocControl.objects.create(module='ia_nc', location='Lahore', doc_no='ETAL-QMS-710-FF-01', issue_date='01-11-2026', issue_no='04')
        self.assertEqual(DC.doc_control('ia_nc', 'Lahore', D(2025, 1, 1))['issue_no'], '03')      # the built-in default
        self.assertEqual(DC.doc_control('ia_nc', 'Lahore', TODAY)['issue_no'], '04')

    def test_blank_fields_filled_from_default_as_before(self):
        from QC.views.ia import _ia_docctrl
        DC._create('ia_nc', 'Karachi', {'doc_no': 'ETAL-QMS-710-FF-01'}, DC.BASELINE, 'seed', None)
        d = _ia_docctrl('nc', 'Karachi', D(2025, 1, 1))
        self.assertEqual((d['issue_date'], d['issue_no'], d['rev_no']), ('11-03-2023', '03', '02'))

    def test_issue_on_unused_form_keeps_older_documents(self):
        DC.issue_revision('control_chart_rm', 'Lahore', _vals('RM-1'), D(2026, 11, 1), 'first number', self.admin)
        self.assertEqual(DC.doc_control('control_chart_rm', 'Lahore', D(2025, 1, 1))['doc_no'], 'TBA')
        self.assertEqual(DC.doc_control('control_chart_rm', 'Lahore', D(2026, 11, 1))['doc_no'], 'RM-1')

    def test_correction_keeps_history(self):
        r = DC.issue_revision('ia_nc', 'Karachi', _vals('ETAL-QMS-710-FF-0I'), D(2000, 1, 1), 'baseline', self.admin)
        DC.correct_revision(r, _vals('ETAL-QMS-710-FF-01'), 'typing error', self.admin)
        r.refresh_from_db()
        self.assertEqual(r.doc_no, 'ETAL-QMS-710-FF-01')
        self.assertIn('typing error', r.note)
        self.assertEqual(r.history.count(), 2)

    def test_doc_date_and_first_saved(self):
        class O: pass
        o = O(); o.study_date = None; o.date = D(2024, 5, 6)
        self.assertEqual(DC.doc_date(o, 'study_date'), D(2024, 5, 6))
        self.assertEqual(DC._day('07-08-2025'), D(2025, 8, 7))


class ChartOwnFormTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('adm', 'a@x', 'x')
        self.c = ControlChart.objects.create(location='Lahore', activity='MON', parameter='Laboratory temperature', level='', unit='C',
                                             equipment='Meter', equipment_id='E-1', method='NA', decimals=1, limit_mode='fixed',
                                             crm_range_low='20', crm_range_high='30')

    def test_period_dates(self):
        from QC.views.control_chart import _period_start
        self.assertEqual(_period_start(self.c, 2025, 3), D(2025, 3, 31))
        self.assertEqual(_period_start(self.c, TODAY.year, TODAY.month), TODAY)

    def test_own_form_from_today_and_withdrawal(self):
        from QC.views.control_chart import _chart_docctrl
        a = _client(self.admin)
        a.post('/qc/control-charts/doc-control/', {'chart': self.c.pk, 'doc_no': 'ETAL-LAB-603-FF-07', 'issue_date': '10-01-2024'})
        self.assertTrue(_chart_docctrl(self.c, TODAY)['own'])
        self.assertFalse(_chart_docctrl(self.c, D(2025, 3, 31))['own'])     # closed periods keep the laboratory form
        a.post('/qc/control-charts/doc-control/', {'chart': self.c.pk, 'action': 'clear'})
        self.assertFalse(_chart_docctrl(self.c, TODAY)['own'])
        self.assertEqual(DocControlRevision.objects.filter(module='cc_chart_%d' % self.c.pk, location='*').count(), 2)

    def test_master_number_history(self):
        from QC.views.control_chart import _chart_docctrl
        ControlChart.objects.filter(pk=self.c.pk).update(doc_no='MASTER-1'); self.c.refresh_from_db()
        a = _client(self.admin)
        a.post('/qc/control-charts/doc-control/', {'chart': self.c.pk, 'doc_no': 'OWN-2', 'issue_date': '10-01-2024'})
        self.assertEqual(_chart_docctrl(self.c, D(2025, 3, 31))['doc_no'], 'MASTER-1')
        self.assertEqual(_chart_docctrl(self.c, TODAY)['doc_no'], 'OWN-2')

    def test_lab_form_revision_does_not_change_closed_periods(self):
        from QC.views.control_chart import _chart_docctrl
        DC.issue_revision('control_chart_mon', 'Lahore', _vals('MON-1'), D(2000, 1, 1), 'baseline', self.admin)
        DC.issue_revision('control_chart_mon', 'Lahore', _vals('MON-2', issue_no='02'), TODAY, 'revised', self.admin)
        self.assertEqual(_chart_docctrl(self.c, D(2025, 3, 31))['doc_no'], 'MON-1')
        self.assertEqual(_chart_docctrl(self.c, TODAY)['doc_no'], 'MON-2')


class RegisterPageTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('adm', 'a@x', 'x')
        self.chem = User.objects.create_user('chem', 'c@x', 'x')

    def test_permissions(self):
        # every logged-in user views, filters and downloads; only the administrator issues / corrects (24-10-2026)
        r = _client(self.chem).get('/qc/document-control/')
        self.assertEqual(r.status_code, 200)
        self.assertNotContains(r, 'name="action" value="issue"')
        self.assertContains(r, 'Download PDF')
        self.assertEqual(_client(self.chem).post('/qc/document-control/', {'action': 'issue'}).status_code, 403)
        self.assertEqual(Client(REMOTE_ADDR='127.0.0.1').get('/qc/document-control/').status_code, 302)
        r = _client(self.admin).get('/qc/document-control/')
        self.assertContains(r, 'Document Control register')
        self.assertContains(r, 'Job completion form')
        self.assertContains(r, 'name="action" value="issue"')

    def test_filters_and_downloads(self):
        import io, zipfile
        DC.issue_revision('mou', 'Lahore', _vals('MOU-L1'), D(2000, 1, 1), 'baseline', self.admin)
        DC.issue_revision('mou', 'Lahore', _vals('MOU-L2', issue_no='02'), TODAY + _dt.timedelta(days=5), 'scheduled revision', self.admin)
        c = _client(self.chem)
        r = c.get('/qc/document-control/?loc=Karachi&show=current')
        self.assertNotContains(r, 'MOU-L1')
        r = c.get('/qc/document-control/?loc=Lahore&show=history')
        self.assertContains(r, 'MOU-L1'); self.assertContains(r, 'MOU-L2')
        for loc in ('All', 'Karachi', 'Lahore'):
            for show in ('both', 'current', 'history'):
                r = c.get('/qc/document-control/?loc=%s&show=%s&export=pdf' % (loc, show))
                self.assertEqual((r.status_code, r['Content-Type']), (200, 'application/pdf'))
                self.assertTrue(r.content.startswith(b'%PDF'))
                r = c.get('/qc/document-control/?loc=%s&show=%s&export=xlsx' % (loc, show))
                self.assertEqual(r.status_code, 200)
                self.assertIn('attachment', r['Content-Disposition'])
                z = zipfile.ZipFile(io.BytesIO(r.content))
                sheets = [n for n in z.namelist() if n.startswith('xl/worksheets/')]
                self.assertEqual(len(sheets), 2 if show == 'both' else 1)
                body = b''.join(z.read(n) for n in sheets)
                self.assertEqual(b'MOU-L2' in body, loc in ('All', 'Lahore'), (loc, show))

    def test_issue_and_correct(self):
        a = _client(self.admin)
        base = {'module': 'ia_rca', 'location': 'Karachi', 'doc_no': 'ETAL-QMS-710-FF-01A', 'issue_date': '01-12-2026', 'issue_no': '02',
                'rev_no': '00', 'effective_from': '2026-12-01'}
        r = a.post('/qc/document-control/', dict(base, action='issue', note='x'), follow=True)          # reason too short
        self.assertContains(r, 'Nothing was changed')
        self.assertEqual(DocControlRevision.objects.filter(module='ia_rca').count(), 0)
        r = a.post('/qc/document-control/', dict(base, action='issue', note='form revised by CEO'), follow=True)
        self.assertContains(r, 'New revision of ia_rca')
        self.assertEqual(DC.doc_control('ia_rca', 'Karachi', D(2026, 12, 1))['issue_no'], '02')
        r = a.post('/qc/document-control/', dict(base, action='issue', note='same values again'), follow=True)
        self.assertContains(r, 'Nothing was changed: the values are the same')
        rev = DocControlRevision.objects.get(module='ia_rca', effective_from=D(2026, 12, 1))
        self.assertEqual(DC.doc_control('ia_rca', 'Karachi', D(2026, 11, 30))['issue_no'], '01')     # older documents keep the default
        a.post('/qc/document-control/', dict(base, action='correct', rev=rev.pk, issue_date='02-12-2026', note='typing error'))
        rev.refresh_from_db()
        self.assertEqual(rev.issue_date, '02-12-2026')
        self.assertEqual(a.post('/qc/document-control/', dict(base, location='Mars', action='issue', note='bad lab')).status_code, 400)
        self.assertEqual(a.post('/qc/document-control/', dict(base, location='*', action='issue', note='not read by any document')).status_code, 400)
        self.assertEqual(a.post('/qc/document-control/', dict(base, action='correct', rev='x1', note='bad id given')).status_code, 404)


class IaPlanDateTests(TestCase):
    def test_plan_uses_its_year(self):
        from QC.views.ia import _ia_docctrl, _ia_on
        admin = User.objects.create_superuser('adm', 'a@x', 'x')
        p = IaPlan.objects.create(location='Karachi', year=2025)
        self.assertEqual(_ia_on(p), D(2025, 1, 1))
        _ia_docctrl('plan', 'Karachi', _ia_on(p))                              # first use records the default as baseline
        DC.issue_revision('ia_plan', 'Karachi', _vals('ETAL-QMS-808-FF-01', '01-01-2026', '03', '00'), D(2026, 1, 1), 'revised', admin)
        self.assertNotEqual(_ia_docctrl('plan', 'Karachi', _ia_on(p))['issue_no'], '03')
        self.assertEqual(_ia_docctrl('plan', 'Karachi', D(2026, 1, 1))['issue_no'], '03')


class SeededHardCodedTests(TestCase):
    """Migration 0031 moves the numbers typed into the PDF code into the register unchanged."""
    def test_seeds_print_as_before(self):
        exp = {('job_completion', 'Karachi'): ('ETAL-LAB-704-FF-08', '15-05-2026', '01', '00'),
               ('job_completion', 'Lahore'): ('ETAL-LAB-704-FF-08', '15-05-2026', '01', '00'),
               ('logging_sheet', 'Karachi'): ('ETAL-LAB-704-FF-1(A)', '17-12-2021', '01', '00'),
               ('logging_sheet', 'Lahore'): ('ETAL-LAB-704-FF-1(A)', '05-01-2023', '01', '00'),
               ('qc_rds', '*'): ('ETAL-LAB-704-FF-05', '22-12-2025', '02', '01'),
               ('qc_test_results', 'Karachi'): ('ETAL-LAB-704-FF-07', '01-08-2022', '01', '00'),
               ('qc_test_results', 'Lahore'): ('ETAL-LAB-704-FF-07', '05-01-2023', '01', '00'),
               ('qc_test_results', '*'): ('ETAL-LAB-704-FF-05', '22-12-2025', '02', '01')}
        for (m, loc), v in exp.items():
            for d in (D(2019, 1, 1), TODAY):
                c = DC.doc_control(m, loc, d)
                self.assertEqual((c['doc_no'], c['issue_date'], c['issue_no'], c['rev_no']), v, (m, loc, d))

    def test_first_saved_uses_history(self):
        from QC.models import Dw_rds
        o = Dw_rds.objects.create(sample_id='S-1')
        self.assertEqual(DC.first_saved(o), _dt.date.today())
        self.assertEqual(DC.first_saved(object()), _dt.date.today())


class ManagementModuleTests(TestCase):
    """Management Records / Reports module (24-10-2026): home with the ISO/IEC 17025 clause map, main-menu button,
    Internal Audit and the Document Control register in its sidebar; old addresses unchanged."""
    def setUp(self):
        self.chem = User.objects.create_user('chem', 'c@x', 'x')

    def test_home_and_navigation(self):
        c = _client(self.chem)
        r = c.get('/management/')
        self.assertEqual(r.status_code, 200)
        for t in ('Management Records / Reports', '8.3', '8.8', '8.9', 'Planned', 'Document Control register (8.3)', 'Internal Audit (8.8)'):
            self.assertContains(r, t)
        self.assertEqual(c.get('/management/?loc=Lahore').status_code, 200)
        self.assertEqual(c.get('/management/ia/')['Location'], '/qc/ia/')
        self.assertEqual(c.get('/management/document-control/?loc=Lahore')['Location'], '/qc/document-control/?loc=Lahore')
        self.assertContains(c.get('/qc/ia/'), 'Management Records</p>')
        self.assertContains(c.get('/qc/document-control/'), 'Management Records</p>')
        r = c.get('/qc/qc_main/')
        self.assertContains(r, 'QC Forms</p>'); self.assertNotContains(r, 'id="etqcIA"')
        self.assertContains(r, 'href="/management/"')
        self.assertEqual(Client(REMOTE_ADDR='127.0.0.1').get('/management/').status_code, 302)
