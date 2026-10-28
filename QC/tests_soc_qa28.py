"""Decision rule / statement of conformity - strict QA 28-10-2026 (Lab Manager review, Sana Ashraf).

    manage.py test QC.tests_soc_qa28

End to end as the laboratory works: a new customer demand (requisition) -> customer request form FF-17 raised before
any report -> authorised by the Lab Manager -> report prepared (inlet / outlet / drinking water) -> report approved ->
records -> performed / reviewed / approved -> lab test report with decision rule. Statement wording in every case.
"""
import json
import os
import shutil
import subprocess
import tempfile

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.utils import timezone

from EnviTechAlApp.models import Sample_registration, DrinkingWaterForm, WasteWaterForm2, Signatures, ApprovalStatus
from QC.models import SocRecord, SocRequest, MouStudy, ControlChartReviewer, SocLegendSet
from QC import soc_rules as R
from QC import soc_report as SR


D8 = dict(date_of_analysis_from='28-Oct-2026', date_of_analysis_to='29-Oct-2026', reporting_date='30-October-2026')


def C(u):
    c = Client(); c.force_login(u); return c


def text(content):
    if not shutil.which('pdftotext'):
        return None
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as fh:
        fh.write(content); path = fh.name
    dump = os.environ.get('SOC_QA_DUMP')
    if dump:
        os.makedirs(dump, exist_ok=True)
        shutil.copy(path, os.path.join(dump, '%d.pdf' % len(os.listdir(dump))))
    return subprocess.run(['pdftotext', '-opw', 'karachi123', '-layout', path, '-'], capture_output=True, text=True).stdout


def records_post(d, u='0.2', pick=None):
    """The form as a chemist submits it: every accredited row with a result ticked (as the page pre-ticks them)."""
    P = {'sample_id': d['sample_id'], 'report_type': d['report_type'], 'report_pk': d['report_pk'], 'standard': d['header']['standard']}
    for i, p in enumerate(d['parameters']):
        if p['accredited'] and p['value'] is not None and (pick is None or p['parameter'] in pick):
            P.update({'p%d_on' % i: '1', 'p%d_parameter' % i: p['parameter'], 'p%d_method' % i: p['method'], 'p%d_unit' % i: p['unit'],
                      'p%d_v0' % i: p['value_text'] or p['value'], 'p%d_v1' % i: p['value'], 'p%d_v2' % i: p['value'],
                      'p%d_upper' % i: p['upper'] if p['upper'] is not None else '', 'p%d_lower' % i: p['lower'] if p['lower'] is not None else '',
                      'p%d_limit' % i: p['limit'], 'p%d_u' % i: p['u'] if p['u'] is not None else u, 'p%d_result' % i: p['result']})
    return P


class SocQA(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.lchem = User.objects.create_user('qa_lchem', password='x', first_name='Lahore', last_name='Chemist')
        cls.lmgr = User.objects.create_user('qa_lmgr', password='x', first_name='Lahore', last_name='Manager')
        cls.kchem = User.objects.create_user('qa_kchem', password='x')
        cls.kmgr = User.objects.create_user('qa_kmgr', password='x')
        cls.ceo = User.objects.create_superuser('qa_ceo', 'c@x.c', 'x')
        ControlChartReviewer.objects.create(user=cls.lmgr, location='Lahore'); ControlChartReviewer.objects.create(user=cls.kmgr, location='Karachi')
        for u, o in ((cls.lchem, 'Lahore'), (cls.lmgr, 'Lahore'), (cls.kchem, 'Karachi'), (cls.kmgr, 'Karachi')):
            Signatures.objects.create(user=u, office=o)
        MouStudy.objects.create(location='Lahore', parameter='pH', level='7', unit='-', sample_kind='SAMPLE', status='approved', u_abs=0.098, approved_at=timezone.now())
        MouStudy.objects.create(location='Lahore', parameter='Calcium', level='50 ppm', unit='mg/L', sample_kind='CRM', status='approved', u_abs=1.2, approved_at=timezone.now())

    # ------------------------------------------------------------------ helpers
    def authorise(self, sid, mou=True, soc=True, loc='Lahore', chem=None, mgr=None):
        chem, mgr = chem or C(self.lchem), mgr or C(self.lmgr)
        P = {'sample_id': sid, 'date': '28-10-2026', 'organization': 'QA Test Industries', 'customer_name': 'Mr QA', 'analysis': 'dw' if sid.startswith('DW') else 'ww',
             'parameters': 'pH, TDS', 'reporting': 'PEQS limits'}
        if mou:
            P['req_mou'] = '1'
        if soc:
            P['req_soc'] = '1'
        r = chem.post('/qc/soc/request/new/?location=%s' % loc, P)
        self.assertEqual(r.status_code, 302, getattr(r, 'content', b'')[:300])
        q = SocRequest.objects.get(location=loc, sample_id=sid)
        mgr.post('/qc/soc/request/%d/action/' % q.pk, {'action': 'authorise'})
        q.refresh_from_db(); self.assertTrue(q.locked)
        return q

    def flow(self, sid, loc='Lahore'):
        chem, mgr, ceo = (C(self.lchem), C(self.lmgr), C(self.ceo)) if loc == 'Lahore' else (C(self.kchem), C(self.kmgr), C(self.ceo))
        chem.post('/qc/soc/sample/%s/action/?location=%s' % (sid, loc), {'action': 'perform'})
        mgr.post('/qc/soc/sample/%s/action/?location=%s' % (sid, loc), {'action': 'review'})
        ceo.post('/qc/soc/sample/%s/action/?location=%s' % (sid, loc), {'action': 'approve'})
        self.assertEqual(set(SocRecord.objects.filter(location=loc, sample_id=sid).values_list('status', flat=True)), {'approved'})

    # ------------------------------------------------------------------ 1, 4: a new customer demand, start to end (WW inlet, Lahore)
    def test_new_demand_ww_inlet_lahore(self):
        chem, mgr = C(self.lchem), C(self.lmgr)
        sid = 'WW-202610901-LHR'
        Sample_registration.objects.create(sample_id=sid, city_location='Lahore', checkinp107=True, checkinp110=True, inp112='PEQS', inp7='28-10-2026')
        # listed as awaiting, with "Raise FF-17" as the next step, before any report exists
        r = chem.get('/qc/soc/?location=Lahore&show=pending'); self.assertContains(r, sid); self.assertContains(r, 'Raise FF-17')
        d = chem.get('/qc/soc/api/sample/', {'sample_id': sid, 'location': 'Lahore'})
        self.assertEqual(d.status_code, 404); d = d.json()
        self.assertTrue(d['no_report']); self.assertIn('Raise and authorise the customer request form', d['error'])
        self.assertFalse(d['gate']['ok']); self.assertEqual([s['done'] for s in d['gate']['steps']], [False, False, False, False, False])
        # the FF-17 is raised before the report (prefilled from the requisition)
        r = chem.get('/qc/soc/request/new/?location=Lahore&sample=' + sid); self.assertEqual(r.status_code, 200); self.assertContains(r, 'PEQS')
        q = self.authorise(sid)
        d = chem.get('/qc/soc/api/sample/', {'sample_id': sid, 'location': 'Lahore'}).json()
        self.assertEqual([s['done'] for s in d['gate']['steps']], [True, True, True, False, False])
        self.assertEqual((d['request_form']['mou'], d['request_form']['soc'], d['request_form']['authorised']), (True, True, True))
        # the inlet report is prepared: its results are in result_N (they were read from the empty outlet fields: "The report has no results")
        ww = WasteWaterForm2.objects.create(sample_id=sid, **D8, report_to='QA Test Industries', address='Lahore', attention='Mr QA', lab_report_no='202610901-QA-WW',
                                            sample_Col_date='28-Oct-2026', select='PEQS', city_location='Lahore', in_out='in',
                                            result_2='7.42', method_2='*APHA 4500 H-B', result_6='1850', method_6='*APHA 2540-C', result_21='410', method_21='*APHA 4500 Cl-B',
                                            result_26='1250', method_26='HACH 8051', result_5='310')
        d = chem.get('/qc/soc/api/sample/', {'sample_id': sid, 'location': 'Lahore'}).json()
        by = {p['parameter']: p for p in d['parameters']}
        self.assertEqual(d['side'], 'inlet'); self.assertEqual(set(by), {'pH', 'COD', 'TDS', 'Chloride', 'Sulphate'})
        self.assertEqual({k for k, p in by.items() if p['accredited']}, {'pH', 'TDS', 'Chloride', 'Sulphate'})
        self.assertEqual(by['pH']['u'], 0.098)
        self.assertFalse(d['gate']['ok']); self.assertEqual(d['gate']['steps'][4]['done'], False)          # report not approved yet
        r = chem.post('/qc/soc/new/?location=Lahore', records_post(d), follow=True)
        self.assertContains(r, 'Test report approved: not done'); self.assertFalse(SocRecord.objects.filter(sample_id=sid).exists())
        ApprovalStatus.objects.create(model_key='ww2', record_id=ww.pk, approved_by=self.ceo)
        d = chem.get('/qc/soc/api/sample/', {'sample_id': sid, 'location': 'Lahore'}).json()
        self.assertTrue(d['gate']['ok'])
        r = chem.post('/qc/soc/new/?location=Lahore', records_post(d))
        self.assertEqual(r.status_code, 302)
        recs = {x.parameter: x for x in SocRecord.objects.filter(sample_id=sid)}
        self.assertEqual(set(recs), {'pH', 'TDS', 'Chloride', 'Sulphate'}); self.assertEqual(recs['pH'].request_id, q.pk)
        self.flow(sid)
        r = chem.get('/qc/soc/sample/%s/pdf/' % sid, {'location': 'Lahore'}); self.assertEqual(r.status_code, 200)
        t = text(r.content)
        if t:
            self.assertIn('Statement of Conformity', t); self.assertIn('Uncertainty', t); self.assertNotIn('NOT APPROVED', t)
            self.assertIn('Result = Fail', t)                         # Sulphate 1250 / Chloride 410 above the PEQS inlet limits as printed
            self.assertIn('***', t)

    # ------------------------------------------------------------------ 4, WW4 / DW1: the FF-17 governs, not the requisition
    def test_ff17_governs_and_requisition_mismatch(self):
        chem = C(self.lchem)
        sid = 'DW-202610902-LHR'
        Sample_registration.objects.create(sample_id=sid, city_location='Lahore')           # requisition: nothing ticked
        dw = DrinkingWaterForm.objects.create(sample_id=sid, **D8, report_to='QA Water', address='L', attention='A', lab_report_no='202610902-QA-DW', sample_collection_date='28-Oct-2026',
                                              select='PEQS', city_location='Lahore', water_sr1='7.6', method_1='*APHA 4500 H-B', water_sr2='880', method_2='*APHA 2540-C')
        self.authorise(sid)
        d = chem.get('/qc/soc/api/sample/', {'sample_id': sid, 'location': 'Lahore'}).json()
        self.assertEqual((d['requisition']['mou'], d['requisition']['soc']), (False, False))
        self.assertEqual((d['request_form']['mou'], d['request_form']['soc']), (True, True))
        # listed for the laboratory although the requisition did not tick MOU / SOC
        self.assertIn(sid, [s['sample_id'] for s in R.eligible_samples('Lahore')])
        r = chem.get('/qc/soc/new/?location=Lahore'); self.assertContains(r, sid); self.assertContains(r, '[report not approved]')
        ApprovalStatus.objects.create(model_key='dw', record_id=dw.pk)
        self.assertTrue(chem.get('/qc/soc/api/sample/', {'sample_id': sid, 'location': 'Lahore'}).json()['gate']['ok'])

    def test_gate_open_or_denied_request(self):
        chem, mgr = C(self.lchem), C(self.lmgr)
        sid = 'WW-202610903-LHR'
        ww = WasteWaterForm2.objects.create(sample_id=sid, **D8, report_to='QA', lab_report_no='X', city_location='Lahore', in_out='out', select='PEQS', result_2_2='7.1')
        ApprovalStatus.objects.create(model_key='ww2', record_id=ww.pk)
        d = chem.get('/qc/soc/api/sample/', {'sample_id': sid, 'location': 'Lahore'}).json()
        self.assertFalse(d['gate']['ok']); self.assertFalse(d['gate']['steps'][0]['done'])
        chem.post('/qc/soc/request/new/?location=Lahore', {'sample_id': sid, 'date': '28-10-2026', 'analysis': 'ww', 'req_soc': '1'})
        q = SocRequest.objects.get(sample_id=sid)
        r = chem.post('/qc/soc/new/?location=Lahore', records_post(d), follow=True)
        self.assertContains(r, 'approved and authorised by the QC / Lab Manager: not done'); self.assertEqual(SocRecord.objects.count(), 0)
        mgr.post('/qc/soc/request/%d/action/' % q.pk, {'action': 'deny', 'comment': 'customer withdrew'})
        d = chem.get('/qc/soc/api/sample/', {'sample_id': sid, 'location': 'Lahore'}).json()
        self.assertFalse(d['gate']['ok']); self.assertEqual(d['gate']['steps'][2]['note'], 'denied')

    # ------------------------------------------------------------------ DW2: accredited parameters without a limit (PEQS): U only, no statement
    def test_no_limit_parameters_report_u_only(self):
        chem = C(self.lchem)
        sid = 'DW-202610904-LHR'
        dw = DrinkingWaterForm.objects.create(sample_id=sid, **D8, report_to='QA Water', address='L', attention='A', lab_report_no='202610904-QA-DW', sample_collection_date='28-Oct-2026',
                                              select='PEQS', city_location='Lahore', water_sr1='7.6', method_1='*APHA 4500 H-B', water_sr2='880', method_2='*APHA 2540-C',
                                              extra_field=json.dumps([{'sr': '29', 'parameters': 'Calcium', 'methods': 'ASTM D 1126', 'unit': 'mg/L', 'result': '52.8', 'limit': '-'},
                                                                      {'sr': '30', 'parameters': 'Sulphate', 'methods': 'APHA 4500 SO4-E', 'unit': 'mg/L', 'result': '106.6', 'limit': '-'}]))
        ApprovalStatus.objects.create(model_key='dw', record_id=dw.pk)
        self.authorise(sid)
        d = chem.get('/qc/soc/api/sample/', {'sample_id': sid, 'location': 'Lahore'}).json()
        by = {p['parameter']: p for p in d['parameters']}
        self.assertTrue(by['Calcium']['accredited']); self.assertEqual((by['Calcium']['lower'], by['Calcium']['upper']), (None, None)); self.assertEqual(by['Calcium']['u'], 1.2)
        r = chem.post('/qc/soc/new/?location=Lahore', records_post(d, u='2.5'))
        self.assertEqual(r.status_code, 302)
        recs = {x.parameter: x for x in SocRecord.objects.filter(sample_id=sid)}
        self.assertEqual(set(recs), {'pH', 'TDS', 'Calcium', 'Sulphate'})
        ca = recs['Calcium']
        self.assertEqual((ca.no_limit, ca.verdicts, ca.overall, ca.uncertainty, ca.legacy.get('no_limit')), (True, ['N.A'] * 3, '', 1.2, True))
        self.assertEqual(C(self.ceo).get('/qc/soc/%d/' % ca.pk).status_code, 200)
        self.assertEqual(chem.get('/qc/soc/%d/pdf/' % ca.pk).status_code, 200)
        self.flow(sid)
        ctx = SR.soc_context(list(SocRecord.objects.filter(sample_id=sid).order_by('id')))
        self.assertEqual((sorted(ctx['na']), ctx['result'], ctx['no_statement']), (['Calcium', 'Sulphate'], 'Pass', False))
        st = SR.statement_text(ctx)
        self.assertIn('no specification limit for Calcium & Sulphate', st); self.assertIn('pH & TDS', st)
        r = chem.get('/qc/soc/sample/%s/pdf/' % sid, {'location': 'Lahore'}); self.assertEqual(r.status_code, 200)
        t = text(r.content)
        if t:
            self.assertIn('1.2', t); self.assertIn('no specification limit', t)

    def test_no_limit_without_mou_is_refused(self):
        chem = C(self.lchem)
        sid = 'DW-202610905-LHR'
        dw = DrinkingWaterForm.objects.create(sample_id=sid, **D8, report_to='QA Water', lab_report_no='Y', select='PEQS', city_location='Lahore', water_sr1='7.6',
                                              extra_field=json.dumps([{'parameters': 'Calcium', 'unit': 'mg/L', 'result': '52.8', 'limit': '-'}]))
        ApprovalStatus.objects.create(model_key='dw', record_id=dw.pk)
        self.authorise(sid, mou=False, soc=True)
        d = chem.get('/qc/soc/api/sample/', {'sample_id': sid, 'location': 'Lahore'}).json()
        r = chem.post('/qc/soc/new/?location=Lahore', records_post(d), follow=True)
        self.assertContains(r, 'gives no specification limit'); self.assertEqual(list(SocRecord.objects.filter(sample_id=sid).values_list('parameter', flat=True)), ['pH'])

    # ------------------------------------------------------------------ MOU only: the uncertainty column, no statement of conformity
    def test_mou_only_request(self):
        chem = C(self.lchem)
        sid = 'DW-202610906-LHR'
        dw = DrinkingWaterForm.objects.create(sample_id=sid, **D8, report_to='QA Water', address='L', attention='A', lab_report_no='Z', sample_collection_date='28-Oct-2026', select='PEQS',
                                              city_location='Lahore', water_sr1='7.6', method_1='*APHA 4500 H-B')
        ApprovalStatus.objects.create(model_key='dw', record_id=dw.pk)
        self.authorise(sid, mou=True, soc=False)
        d = chem.get('/qc/soc/api/sample/', {'sample_id': sid, 'location': 'Lahore'}).json()
        self.assertEqual(chem.post('/qc/soc/new/?location=Lahore', records_post(d)).status_code, 302)
        ctx = SR.soc_context(list(SocRecord.objects.filter(sample_id=sid)))
        self.assertTrue(ctx['no_statement'])
        r = chem.get('/qc/soc/sample/%s/pdf/' % sid, {'location': 'Lahore'}); self.assertEqual(r.status_code, 200)
        t = text(r.content)
        if t:
            self.assertIn('Uncertainty', t); self.assertNotIn('Statement of Conformity', t)

    # ------------------------------------------------------------------ 2: accredited parameters (source and matching)
    def test_accredited_matching(self):
        L = R.ACCREDITED[('Lahore', 'dw')]
        for name, exp in (('pH @ 25 °C', True), ('Total Dissolved Solids (TDS)', True), ('TDS', True), ('Total Hardness as CaCO3', True), ('Hardness', True),
                          ('Calcium', True), ('Calcium Hardness', False), ('Alkalinity as CaCO3', True), ('Sulphate', True), ('Chloride (Cl)', True),
                          ('Nitrite', False), ('Residual Chlorine', False), ('Phenolic Compounds', False), ('Magnesium', False), ('Turbidity', True), ('pH***', True)):
            self.assertEqual(R.is_accredited(name, L), exp, name)
        K = R.ACCREDITED[('Karachi', 'dw')]                 # names as typed on the Karachi reports (production DW-202409012)
        for name in ('pH***', 'Total Dissolved Solids (TDS)***', 'Total Hardness as CaCO3**', 'Nitrate (NO3)***', 'Nickel (Ni)***'):
            self.assertTrue(R.is_accredited(name, K), name)
        self.assertFalse(R.is_accredited('Total Bacterial Count', K))
        self.assertEqual((R.lab_of('karachi.'), R.lab_of(' Lahore '), R.lab_of('')), ('Karachi', 'Lahore', ''))
        K = R.ACCREDITED[('Karachi', 'ww2')]
        self.assertTrue(R.is_accredited('Chemical Oxygen Demand (COD)', K)); self.assertFalse(R.is_accredited('Biological Oxygen Demand(BOD)5', K))
        self.assertFalse(R.is_accredited('Chloride', K))

    # ------------------------------------------------------------------ 3: statement wording in every case
    def test_statement_every_case(self):
        class Rec:
            def __init__(s, p, res, lo=None, hi=None, u=0.0, lim=''):
                s.parameter, s.results, s.lower, s.upper, s.uncertainty, s.limit_text = p, [{'value': v} for v in res], lo, hi, u, lim
                s.location, s.report_type, s.status, s.decision_rule, s.request_id, s.request = 'Lahore', 'dw', 'approved', SocRecord.RULE, None, None
            values = SocRecord.values; verdict = SocRecord.verdict; verdicts = SocRecord.verdicts; overall = SocRecord.overall
            band_within = SocRecord.band_within; strict = SocRecord.strict; no_limit = SocRecord.no_limit
        cases = {
            'one pass': ([Rec('pH', [7.2], 6.5, 8.5, 0.1)], 'Pass', ['The measured value of pH along with its uncertainty band was within', 'this parameter is considered as Pass']),
            'all pass': ([Rec('pH', [7.2], 6.5, 8.5, 0.1), Rec('TDS', [500], None, 1000, 5)], 'Pass', ['pH & TDS along with their respective uncertainty bands were within', 'these parameters are']),
            'one fail high': ([Rec('TDS', [1200], None, 1000, 5)], 'Fail', ['TDS was outside the acceptance limit', 'this parameter is considered as Fail']),
            'pH fail low': ([Rec('pH', [6.2], 6.5, 8.5, 0.1)], 'Fail', ['pH was outside']),
            'mixed': ([Rec('pH', [7.2], 6.5, 8.5, 0.1), Rec('Chloride', [300], None, 250, 1), Rec('Sulphate', [700], None, 600, 2)], 'Fail',
                      ['pH along with its uncertainty band was within', 'Chloride & Sulphate were outside', 'these parameters are considered as Fail']),
            'band crosses limit': ([Rec('TDS', [998], None, 1000, 5)], 'Pass', ['TDS was within the acceptance limit while its uncertainty band extends beyond it', 'guard band = 0']),
            'at limit, <=': ([Rec('Chloride', [250], None, 250, 0, '<= 250')], 'Pass', ['Chloride along with its uncertainty band was within']),
            'at limit, strict <': ([Rec('TDS', [1000], None, 1000, 0, '<1000')], 'Fail', ['TDS was outside']),
            'replicate fails': ([Rec('Nitrate', [48, 51, 49], None, 50, 0.5)], 'Fail', ['Nitrate was outside']),
            'no limit only': ([Rec('Calcium', [52.8], u=1.2)], '-', ['no specification limit for Calcium']),
        }
        for name, (recs, result, phrases) in cases.items():
            ctx = SR.soc_context(recs)
            self.assertEqual(ctx['result'], result, name)
            st = SR.statement_text(ctx)
            for ph in phrases:
                self.assertIn(ph, st, '%s: %s' % (name, st))
            self.assertTrue(st.startswith('Statement of conformity only applicable on accredited parameters'), name)
        self.assertTrue(SR.soc_context(cases['no limit only'][0])['no_statement'])

    # ------------------------------------------------------------------ Karachi WW outlet, start to end (regression)
    def test_karachi_ww_outlet(self):
        sid = 'WW-202610907'
        Sample_registration.objects.create(sample_id=sid, city_location='Karachi', checkinp107=True, checkinp110=True)
        ww = WasteWaterForm2.objects.create(sample_id=sid, **D8, report_to='QA Mills', address='K', attention='A', lab_report_no='202610907-QA-WW', sample_Col_date='28-Oct-2026', select='SEQS',
                                            city_location='Karachi', in_out='out', result_2_2='7.36', method_2='*APHA 4500 H-B', result_5_5='70', result_6_6='2040')
        ApprovalStatus.objects.create(model_key='ww2', record_id=ww.pk)
        self.authorise(sid, loc='Karachi', chem=C(self.kchem), mgr=C(self.kmgr))
        chem = C(self.kchem)
        d = chem.get('/qc/soc/api/sample/', {'sample_id': sid, 'location': 'Karachi'}).json()
        self.assertEqual(d['side'], 'outlet'); self.assertTrue(d['gate']['ok'])
        self.assertEqual(chem.post('/qc/soc/new/?location=Karachi', records_post(d)).status_code, 302)
        self.assertEqual(set(SocRecord.objects.filter(sample_id=sid).values_list('parameter', flat=True)), {'pH', 'COD', 'TDS'})
        self.flow(sid, 'Karachi')
        r = chem.get('/qc/soc/sample/%s/pdf/' % sid, {'location': 'Karachi'}); self.assertEqual(r.status_code, 200)
        # Lahore staff see nothing of it
        self.assertEqual(C(self.lchem).get('/qc/soc/api/sample/', {'sample_id': sid, 'location': 'Karachi'}).status_code, 403)
        self.assertNotIn(sid, [s['sample_id'] for s in R.eligible_samples('Lahore')])


class ScopeRegisterTests(TestCase):
    """Accreditation scope register (owner approval 29-10-2026)."""
    @classmethod
    def setUpTestData(cls):
        cls.lchem = User.objects.create_user('sr_lchem', password='x'); cls.lmgr = User.objects.create_user('sr_lmgr', password='x')
        cls.kmgr = User.objects.create_user('sr_kmgr', password='x'); cls.ceo = User.objects.create_superuser('sr_ceo', 'c@x.c', 'x')
        ControlChartReviewer.objects.create(user=cls.lmgr, location='Lahore'); ControlChartReviewer.objects.create(user=cls.kmgr, location='Karachi')
        for u, o in ((cls.lchem, 'Lahore'), (cls.lmgr, 'Lahore'), (cls.kmgr, 'Karachi')):
            Signatures.objects.create(user=u, office=o)

    def test_seeded_from_the_fixed_list(self):
        from QC.models import AccreditationScope, AccreditationCertificate
        self.assertEqual(AccreditationScope.objects.count(), 23); self.assertEqual(AccreditationCertificate.objects.count(), 2)
        for key, names in R.ACCREDITED.items():
            self.assertEqual(R.accredited_set(*key), set(names), key)

    def test_manage_view_withdraw_alias_pdf(self):
        from QC.models import AccreditationScope
        from datetime import date, timedelta
        chem, mgr, kmgr = C(self.lchem), C(self.lmgr), C(self.kmgr)
        r = chem.get('/qc/soc/scope/?location=Lahore'); self.assertEqual(r.status_code, 200); self.assertContains(r, 'to be entered'); self.assertNotContains(r, 'Add to drinking water scope')
        self.assertEqual(chem.post('/qc/soc/scope/?location=Lahore', {'act': 'cert', 'certificate_no': 'X'}).status_code, 403)
        r = kmgr.get('/qc/soc/scope/?location=Lahore'); self.assertEqual((r.status_code, r['Location']), (302, '/qc/soc/scope/?location=Karachi'))
        self.assertContains(mgr.get('/qc/soc/scope/?location=Lahore'), 'Add to drinking water scope')
        mgr.post('/qc/soc/scope/?location=Lahore', {'act': 'cert', 'body': 'PNAC', 'standard': 'ISO/IEC 17025:2017', 'certificate_no': 'LAB-000 (TEST)', 'issue_date': '01-01-2025', 'valid_until': '31-12-2028'})
        # add with an alias; a duplicate in force is refused
        mgr.post('/qc/soc/scope/?location=Lahore', {'act': 'add', 'matrix': 'ww2', 'parameter': 'COD', 'aliases': 'Chemical Oxygen Demand', 'method': 'HACH 8000', 'pnac_ref': 'Scope item 12 (TEST)'})
        self.assertIn('COD', R.accredited_set('Lahore', 'ww2')); self.assertTrue(R.is_accredited('Chemical Oxygen Demand(COD)', R.accredited_set('Lahore', 'ww2')))
        r = mgr.post('/qc/soc/scope/?location=Lahore', {'act': 'add', 'matrix': 'ww2', 'parameter': 'cod'}, follow=True); self.assertContains(r, 'in the register already')
        # withdraw Chloride (WW): not accredited from that date; a reason is required
        cl = AccreditationScope.objects.get(location='Lahore', matrix='ww2', parameter='Chloride')
        r = mgr.post('/qc/soc/scope/?location=Lahore', {'act': 'withdraw', 'id': cl.pk, 'reason': 'x'}, follow=True); self.assertContains(r, 'at least 5'); cl.refresh_from_db(); self.assertIsNone(cl.withdrawn_on)
        mgr.post('/qc/soc/scope/?location=Lahore', {'act': 'withdraw', 'id': cl.pk, 'reason': 'removed at PNAC re-assessment (TEST)'})
        cl.refresh_from_db(); self.assertEqual(cl.withdrawn_on, timezone.localdate())
        self.assertNotIn('Chloride', R.accredited_set('Lahore', 'ww2')); self.assertIn('Chloride', R.accredited_set('Lahore', 'ww2', timezone.localdate() - timedelta(days=1)))
        # a record made before the withdrawal keeps its *** / statement; one made today is out of scope
        old = SocRecord.objects.create(location='Lahore', report_type='ww2', sample_id='WW-SR-1', parameter='Chloride', upper=1000, results=[{'value': 300}])
        SocRecord.objects.filter(pk=old.pk).update(created_at=timezone.now() - timedelta(days=3)); old.refresh_from_db()
        new = SocRecord.objects.create(location='Lahore', report_type='ww2', sample_id='WW-SR-2', parameter='Chloride', upper=1000, results=[{'value': 300}])
        self.assertTrue(SR._acc(old)); self.assertFalse(SR._acc(new))
        # reinstate, history, PDF
        mgr.post('/qc/soc/scope/?location=Lahore', {'act': 'reinstate', 'id': cl.pk, 'reason': 'withdrawn in error (TEST)'})
        cl.refresh_from_db(); self.assertIsNone(cl.withdrawn_on); self.assertIn('Reinstated', cl.remarks)
        r = mgr.get('/qc/soc/scope/?location=Lahore'); self.assertContains(r, 'Change history'); self.assertContains(r, 'Scope item 12 (TEST)')
        r = chem.get('/qc/soc/scope/pdf/?location=Lahore'); self.assertEqual(r.status_code, 200)
        t = text(r.content)
        if t is not None:
            self.assertIn('ACCREDITATION SCOPE REGISTER', t); self.assertIn('LAB-000 (TEST)', t); self.assertIn('COD', t)
        self.assertEqual(C(self.ceo).get('/qc/soc/scope/?location=Karachi').status_code, 200)
        self.assertEqual(C(self.ceo).get('/qc/soc/manual/').status_code, 200)


class LegendTests(TestCase):
    """Legends of the lab test report with decision rule (owner request 29-10-2026)."""
    @classmethod
    def setUpTestData(cls):
        cls.lchem = User.objects.create_user('lg_lchem', password='x'); cls.lmgr = User.objects.create_user('lg_lmgr', password='x')
        cls.ceo = User.objects.create_superuser('lg_ceo', 'c@x.c', 'x')
        ControlChartReviewer.objects.create(user=cls.lmgr, location='Lahore')
        Signatures.objects.create(user=cls.lchem, office='Lahore'); Signatures.objects.create(user=cls.lmgr, office='Lahore')
        cls.dw = DrinkingWaterForm.objects.create(sample_id='DW-LG-1', **D8, report_to='QA Water (TEST)', address='L', attention='A', lab_report_no='LG-1', sample_collection_date='28-Oct-2026',
                                                  select='PEQS', city_location='Lahore', water_sr1='7.6', method_1='*APHA 4500 H-B',
                                                  edit_note='Measurement of uncertainty will be provided on customer demand.',
                                                  legend_1='*** Indicates that the parameter is in our accreditation scope.', legend_2='PEQS Limits = Punjab Environmental Quality Standards (TEST LEGEND B)')
        cls.rec = SocRecord.objects.create(location='Lahore', report_type='dw', report_pk=cls.dw.pk, sample_id='DW-LG-1', parameter='pH', lower=6.5, upper=8.5,
                                           uncertainty=0.098, results=[{'value': 7.6}], customer='QA Water (TEST)')

    def test_starting_set_edit_reset_lock(self):
        chem, mgr, ceo = C(self.lchem), C(self.lmgr), C(self.ceo)
        from QC.soc_report import default_legends
        items = default_legends('Lahore', 'dw', self.dw)
        texts = [i['text'] for i in items]
        self.assertEqual(texts[0], 'Note: Measurement of uncertainty will be provided on customer demand.')
        self.assertEqual([i['src'] for i in items[:3]], ['report', 'report', 'report'])
        self.assertEqual(len([t for t in texts if t.startswith('***')]), 1)                 # the report's *** line; the standard one not repeated
        self.assertTrue(any(t.startswith('Uncertainty') for t in texts))
        url = '/qc/soc/sample/DW-LG-1/legends/?location=Lahore'
        r = chem.get(url); self.assertEqual(r.status_code, 200); self.assertContains(r, 'not edited yet'); self.assertContains(r, 'TEST LEGEND B')
        t0 = text(chem.get('/qc/soc/sample/DW-LG-1/pdf/?location=Lahore').content)
        if t0 is not None:
            self.assertIn('TEST LEGEND B', t0); self.assertIn('k = 2', t0)
        # remove the PEQS line, reword the note, move the Uncertainty line first, add a new line
        P = {}
        for n, i in enumerate(items, 1):
            P['text_%d' % n], P['src_%d' % n], P['pos_%d' % n] = i['text'], i['src'], str(n + 1)
            if i['text'].startswith('PEQS'):
                P['del_%d' % n] = '1'
            if i['text'].startswith('Note:'):
                P['text_%d' % n] = 'Note: Uncertainty is reported as requested on the FF-17 (EDITED).'
            if i['text'].startswith('Uncertainty'):
                P['pos_%d' % n] = '0'
        P.update({'text_99': 'Sampling was carried out by the customer (ADDED LINE).', 'src_99': 'user', 'pos_99': '50'})
        chem.post(url, P)
        s = SocLegendSet.objects.get(location='Lahore', matrix='dw', sample_id='DW-LG-1')
        got = [i['text'] for i in s.items]
        self.assertTrue(got[0].startswith('Uncertainty')); self.assertNotIn('TEST LEGEND B', ' '.join(got)); self.assertIn('(EDITED)', ' '.join(got))
        self.assertEqual(s.items[-1], {'text': 'Sampling was carried out by the customer (ADDED LINE).', 'src': 'user'})
        t1 = text(chem.get('/qc/soc/sample/DW-LG-1/pdf/?location=Lahore').content)
        if t1 is not None:
            self.assertNotIn('TEST LEGEND B', t1); self.assertIn('(ADDED LINE)', t1); self.assertIn('(EDITED)', t1)
            self.assertLess(t1.index('k = 2'), t1.index('(ADDED LINE)'))
        self.dw.refresh_from_db(); self.assertIn('TEST LEGEND B', self.dw.legend_2)            # the normal test report is not changed
        # reset; lock after approval
        chem.post(url, {'act': 'reset'}); self.assertFalse(SocLegendSet.objects.filter(sample_id='DW-LG-1').exists())
        SocRecord.objects.filter(pk=self.rec.pk).update(status='approved')
        self.assertEqual(chem.post(url, P).status_code, 403); self.assertContains(chem.get(url), 'Locked')

    def test_standard_legends(self):
        chem, mgr = C(self.lchem), C(self.lmgr)
        self.assertEqual(SocLegendSet.objects.filter(sample_id='').count(), 4)
        self.assertEqual(chem.get('/qc/soc/legends/?location=Lahore&matrix=ww2').status_code, 200)
        self.assertEqual(chem.post('/qc/soc/legends/?location=Lahore', {'matrix': 'dw', 'text_1': 'X'}).status_code, 403)
        mgr.post('/qc/soc/legends/?location=Lahore', {'matrix': 'dw', 'text_1': 'STANDARD LINE ONE (TEST)', 'pos_1': '1', 'text_2': 'removed', 'pos_2': '2', 'del_2': '1'})
        s = SocLegendSet.objects.get(location='Lahore', matrix='dw', sample_id='')
        self.assertEqual(s.items, [{'text': 'STANDARD LINE ONE (TEST)', 'src': 'standard'}])
        from QC.soc_report import default_legends
        self.assertEqual(default_legends('Lahore', 'dw', self.dw)[-1]['text'], 'STANDARD LINE ONE (TEST)')
        self.assertEqual(SocLegendSet.objects.get(location='Karachi', matrix='dw', sample_id='').items[0]['src'], 'standard')   # the other laboratory untouched
        self.assertContains(mgr.get('/qc/soc/legends/?location=Lahore&matrix=dw'), 'Change history')
