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
from QC.models import SocRecord, SocRequest, MouStudy, ControlChartReviewer
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
