"""Measurement of Uncertainty - tests (21-10-2026).

    manage.py test QC.tests_mou

Engine: eval_expr, statistics, Type A / Type B, whole budget; the Karachi spec: every complete
study recomputes without errors and the as-printed combined uncertainty of the laboratory's
workbooks is reproduced exactly (using the workbook's own SDs and formula rows, i.e. with its
defects), which proves the Type B arithmetic and the distribution divisors. Module: save,
duplicate-key rule, workflow, versions, lookup, PDF, roles.
"""
import json
import math
import os
import re

from django.contrib.auth.models import User
from django.test import TestCase, Client

from QC import mou_calc as M
from QC.models import MouStudy, MouSource, ControlChartReviewer, ControlChartDeletion

SPEC = os.path.join(os.path.dirname(__file__), 'fixtures', 'mou_karachi_spec.json')


class EngineTests(TestCase):
    def test_eval_expr(self):
        self.assertAlmostEqual(M.eval_expr('0.080/2'), 0.04)
        self.assertAlmostEqual(M.eval_expr('(28-27.4)*(0.000002)*500'), 0.0006)
        self.assertAlmostEqual(M.eval_expr('0.5/sqrt(3)'), 0.5 / math.sqrt(3))
        self.assertAlmostEqual(M.eval_expr(2.5), 2.5)
        for bad in ('', 'abc', '__import__("os")', '1;2', 'I43', '2**1000**1000'):
            with self.assertRaises((ValueError, OverflowError, MemoryError), msg=bad):
                M.eval_expr(bad)

    def test_stats(self):
        s = M.stats([502, 503, 501, 499, 499, 503, 501, 499, 502, 502])
        self.assertEqual(s['n'], 10)
        self.assertAlmostEqual(s['mean'], 501.1)
        self.assertAlmostEqual(s['sd'], 1.5951315, places=6)
        self.assertEqual(M.stats(['', None, '5'])['n'], 1)
        self.assertIsNone(M.stats([5])['sd'])

    def test_type_b_divisors(self):
        rel, u = M.type_b(0.1, 100, 'tri')
        self.assertAlmostEqual(rel, 0.001); self.assertAlmostEqual(u, 0.001 / math.sqrt(6))
        self.assertAlmostEqual(M.type_b(1, 100, 'rect')[1], 0.01 / math.sqrt(3))
        self.assertAlmostEqual(M.type_b(1, 100, 'normal2')[1], 0.005)
        self.assertAlmostEqual(M.type_b(1, 100, 'normal', 2.0)[1], 0.02)

    def test_compute_budget(self):
        A = [502, 503, 501, 499, 499, 503, 501, 499, 502, 502]; B = [502, 504, 500, 500, 499, 499, 501, 500, 501, 502]
        r = M.compute({'range': 900, 'k': 2, 'operators': [{'label': 'A', 'values': A}, {'label': 'B', 'values': B}],
                       'components': [{'kind': 'a_rep'}, {'kind': 'a_repro'},
                                      {'kind': 'b', 'name': 'flask', 'range': 100, 'magnitude': '0.1', 'dist': 'tri', 'ci': 1},
                                      {'kind': 'b', 'name': 'excluded', 'range': 100, 'magnitude': '5', 'dist': 'rect', 'ci': 1, 'included': False}]})
        self.assertEqual(r['errors'], [])
        sa, sb = M.stats(A)['sd'], M.stats(B)['sd']
        u1 = (sa / 900) / math.sqrt(10)
        u2 = (math.sqrt(sa * sa + sb * sb) / 900) / math.sqrt(20)
        u3 = (0.1 / 100) / math.sqrt(6)
        uc = math.sqrt(u1 ** 2 + u2 ** 2 + u3 ** 2)
        self.assertAlmostEqual(r['uc'], uc, places=12)
        self.assertAlmostEqual(r['U'], 2 * uc, places=12)
        self.assertAlmostEqual(r['U_abs'], 2 * uc * (sum(A) + sum(B)) / 20, places=10)
        self.assertAlmostEqual(r['U_pct'], 200 * uc, places=10)
        self.assertFalse(r['components'][3]['included'])

    def test_compute_single_operator_and_errors(self):
        r = M.compute({'range': 900, 'operators': [{'label': 'A', 'values': [1, 2, 3]}], 'components': [{'kind': 'a_rep'}, {'kind': 'a_repro'}]})
        self.assertFalse(r['components'][1]['included'])
        self.assertEqual(r['errors'], [])
        r = M.compute({'range': 0, 'operators': [], 'components': []})
        self.assertTrue(any('range' in e for e in r['errors']) and any('repeatability' in e for e in r['errors']))
        r = M.compute({'range': 10, 'operators': [{'label': 'A', 'values': [11, 12]}], 'components': [{'kind': 'a_rep'}, {'kind': 'b', 'name': 'x', 'magnitude': 'zz', 'dist': 'tri'}]})
        self.assertTrue(any('Magnitude' in e for e in r['errors']) and any('exceeds the range' in w for w in r['warnings']))

    def test_fmt(self):
        self.assertEqual(M.fmt_sig(0.0012345678), '0.001235')
        self.assertEqual(M.fmt_sig(501.03333), '501')
        self.assertEqual(M.fmt_sig(None), '-')


class KarachiSpecTests(TestCase):
    """The induction spec built from the 37 workbooks."""
    @classmethod
    def setUpTestData(cls):
        with open(SPEC, encoding='utf-8') as fh:
            cls.spec = json.load(fh)

    def test_spec_shape(self):
        self.assertEqual(self.spec['location'], 'Karachi')
        self.assertEqual(len(self.spec['studies']), 37)
        self.assertEqual(sum(1 for s in self.spec['studies'] if s['complete']), 36)
        keys = [s['key'] for s in self.spec['sources']]
        self.assertEqual(len(keys), len(set(keys)))

    def test_every_complete_study_recomputes(self):
        for st in self.spec['studies']:
            if not st['complete']:
                continue
            r = M.compute({'range': st['range'], 'k': 2, 'operators': st['operators'], 'components': st['components']})
            self.assertEqual(r['errors'], [], st['file'])
            self.assertGreater(r['uc'], 0)
            # recomputed uc is within 40 % of the workbook's printed uc (the workbook SDs omit two replicates)
            printed = st['legacy']['uc']
            self.assertLess(abs(r['uc'] - printed) / printed, 0.40, st['file'])

    def test_as_printed_combined_reproduced(self):
        """With the workbook's own SDs and its combined-formula rows (including the cubed row of D13),
        the engine's Type B rows reproduce the printed uc to 1e-9 for all 36 complete sheets."""
        raw_path = '/home/claude/mou/mou.json'
        if not os.path.exists(raw_path):
            self.skipTest('workbook extract not present on this machine')
        raw = json.load(open(raw_path))
        n = 0
        for s, st in zip(raw, self.spec['studies']):
            if not st['complete']:
                continue
            typea = [c for c in s['components'] if 'type a' in c['source'].lower()]
            pw = {int(r_): int(p) for r_, p in re.findall(r'Q(\d+)\^(\d)', typea[0]['combined_formula'])}
            u2 = sum(c['u_val'] ** pw[c['row']] for c in typea if c['row'] in pw and c['u_val'] is not None)
            bspec = [c for c in st['components'] if c['kind'] == 'b']
            braw = [c for c in s['components'] if 'type a' not in c['source'].lower()]
            for cs, cr in zip(bspec, braw):
                if cr['row'] in pw:
                    u2 += M.type_b(M.eval_expr(cs['magnitude']), float(cs['range']), cs['dist'], float(cs['ci']))[1] ** pw[cr['row']]
            self.assertAlmostEqual(math.sqrt(u2), typea[0]['combined_val'], places=9, msg=st['file'])
            n += 1
        self.assertEqual(n, 36)


class ModuleTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.chem = User.objects.create_user('t_chem', password='x')
        cls.mgr = User.objects.create_user('t_mgr', password='x')
        cls.adm = User.objects.create_superuser('t_adm', 'a@b.c', 'x')
        ControlChartReviewer.objects.create(user=cls.mgr, location='Karachi')
        cls.src = MouSource.objects.create(location='Karachi', category='glassware', name='Volumetric flask 100 ml', unit='ml', range_value=100, magnitude='0.1', dist='tri')

    def client_for(self, u):
        c = Client(); c.force_login(u); return c

    def form(self, level='500 ppm', shift=0):
        A = [502, 503, 501, 499, 499, 503, 501, 499, 502, 502]; B = [502, 504, 500, 500, 499, 499, 501, 500, 501, 502]; C = [502, 504, 500, 499, 499, 500, 499, 503, 504, 502]
        f = {'location': 'Karachi', 'parameter': 'COD', 'level': level, 'unit': 'mg/L', 'sample_kind': 'WS', 'sample_ref': 'WS-COD', 'method': 'APHA 5220 D',
             'instrument': 'UV-Vis', 'range_value': '1500', 'env_temp': '24.5', 'study_date': '21-10-2026', 'k': '2', 'decimals': '3',
             'c0_kind': 'a_rep', 'c0_name': 'Type A - repeatability (u rep)', 'c0_unit': 'mg/L', 'c0_ci': '1',
             'c1_kind': 'a_repro', 'c1_name': 'Type A - reproducibility (u repro)', 'c1_unit': 'mg/L', 'c1_ci': '1',
             'c2_kind': 'b', 'c2_source': str(self.src.pk), 'c2_name': self.src.name, 'c2_unit': 'ml', 'c2_range': '100', 'c2_magnitude': '0.1', 'c2_dist': 'tri', 'c2_ci': '1', 'c2_included': '1',
             'c3_kind': 'b', 'c3_name': 'Spectro wavelength', 'c3_unit': 'nm', 'c3_range': '637', 'c3_magnitude': '0.08/2', 'c3_dist': 'normal', 'c3_ci': '1', 'c3_included': '1'}
        for i, vals in enumerate((A, B, C)):
            f['op%d_present' % i] = '1'; f['op%d_label' % i] = 'ABC'[i]; f['op%d_analyst' % i] = 'Analyst ' + 'ABC'[i]
            for j, v in enumerate(vals):
                f['op%d_v%d' % (i, j)] = str(v + shift)
        return f

    def test_calc_api_matches_engine(self):
        c = self.client_for(self.chem)
        d = c.post('/qc/mou/api/calc/', self.form()).json()
        self.assertEqual(d['errors'], [])
        self.assertEqual(d['operators'][0]['mean'], '501.100')
        self.assertEqual(c.get('/qc/mou/api/calc/').status_code, 405)

    def test_save_workflow_versions_lookup_pdf(self):
        chem, mgr, adm = self.client_for(self.chem), self.client_for(self.mgr), self.client_for(self.adm)
        r = chem.post('/qc/mou/new/', self.form()); self.assertEqual(r.status_code, 302)
        st = MouStudy.objects.get(level='500 ppm')
        self.assertEqual((st.version, st.status, st.components.count(), st.operators.count()), (1, 'draft', 4, 3))
        self.assertAlmostEqual(st.mean, 501.0333333, places=5)
        # range below the mean refused
        bad = self.form(level='501 ppm'); bad['range_value'] = '100'
        self.assertContains(chem.post('/qc/mou/new/', bad), 'at least the measured mean')
        # duplicate open key refused
        self.assertContains(chem.post('/qc/mou/new/', self.form()), 'already has an open version')
        # roles
        self.assertEqual(chem.post('/qc/mou/%d/action/' % st.pk, {'action': 'review'}).status_code, 403)
        chem.post('/qc/mou/%d/action/' % st.pk, {'action': 'submit'}); st.refresh_from_db(); self.assertEqual(st.status, 'review')
        self.assertEqual(chem.get('/qc/mou/%d/edit/' % st.pk).status_code, 403)
        self.assertEqual(mgr.post('/qc/mou/%d/action/' % st.pk, {'action': 'approve'}).status_code, 403)
        mgr.post('/qc/mou/%d/action/' % st.pk, {'action': 'review'}); st.refresh_from_db(); self.assertEqual((st.status, st.reviewed_by), ('reviewed', self.mgr))
        adm.post('/qc/mou/%d/action/' % st.pk, {'action': 'approve'}); st.refresh_from_db(); self.assertEqual((st.status, st.approved_by), ('approved', self.adm))
        self.assertEqual(adm.get('/qc/mou/%d/edit/' % st.pk).status_code, 403)
        r = chem.get('/qc/mou/api/lookup/?location=Karachi&parameter=cod&level=500 ppm')
        self.assertEqual(r.json()['count'], 1); self.assertAlmostEqual(r.json()['studies'][0]['U_pct'], st.u_pct)
        r = adm.get('/qc/mou/%d/pdf/' % st.pk); self.assertEqual((r.status_code, r['Content-Type']), (200, 'application/pdf')); self.assertGreater(len(r.content), 20000)
        # repeat -> v2 draft with empty replicates; approval supersedes v1
        r = chem.post('/qc/mou/%d/repeat/' % st.pk); v2 = MouStudy.objects.get(level='500 ppm', version=2)
        self.assertEqual((v2.status, v2.supersedes_id, [o.values for o in v2.operators.all()]), ('draft', st.pk, [[], [], []]))
        self.assertEqual(chem.post('/qc/mou/%d/repeat/' % st.pk)['Location'], '/qc/mou/%d/' % v2.pk)
        chem.post('/qc/mou/%d/edit/' % v2.pk, self.form(shift=1))
        for cl, act in ((chem, 'submit'), (mgr, 'review'), (adm, 'approve')):
            cl.post('/qc/mou/%d/action/' % v2.pk, {'action': act})
        st.refresh_from_db(); v2.refresh_from_db(); self.assertEqual((st.status, v2.status), ('superseded', 'approved'))
        self.assertEqual([x['version'] for x in chem.get('/qc/mou/api/lookup/?location=Karachi&parameter=COD').json()['studies']], [2])
        # return to draft, unapprove, delete
        self.assertEqual(adm.post('/qc/mou/%d/action/' % v2.pk, {'action': 'unapprove', 'reason': 'x'}).status_code, 302)
        v2.refresh_from_db(); self.assertEqual(v2.status, 'approved')          # reason too short -> unchanged
        adm.post('/qc/mou/%d/action/' % v2.pk, {'action': 'unapprove', 'reason': 'recheck'}); v2.refresh_from_db(); self.assertEqual(v2.status, 'reviewed')
        mgr.post('/qc/mou/%d/action/' % v2.pk, {'action': 'return', 'reason': 'operator B'}); v2.refresh_from_db()
        self.assertEqual(v2.status, 'draft'); self.assertIn('operator B', v2.remarks)
        self.assertEqual(chem.post('/qc/mou/%d/delete/' % st.pk, {'reason': 'chemist'}).status_code, 403)
        mgr.post('/qc/mou/%d/delete/' % st.pk, {'reason': 'superseded test'})
        self.assertFalse(MouStudy.objects.filter(pk=st.pk).exists())
        d = ControlChartDeletion.objects.get(kind='mou_study'); self.assertEqual(len(d.snapshot['operators']), 3)
        self.assertContains(mgr.get('/qc/mou/deleted/'), 'superseded test')
        self.assertNotContains(adm.get('/qc/control-charts/deleted/'), 'superseded test')

    def test_library_roles_and_validation(self):
        chem, mgr = self.client_for(self.chem), self.client_for(self.mgr)
        data = {'category': 'glassware', 'name': 'Pipette 5 ml', 'unit': 'ml', 'range_value': '5', 'magnitude': '0.015', 'dist': 'tri', 'ci': '1', 'valid_until': '30-06-2027'}
        self.assertEqual(chem.post('/qc/mou/library/?location=Karachi', data).status_code, 403)
        self.assertEqual(mgr.post('/qc/mou/library/?location=Karachi', data).status_code, 302)
        s = MouSource.objects.get(name='Pipette 5 ml'); self.assertEqual(s.validity, 'ok')
        self.assertContains(mgr.post('/qc/mou/library/?location=Karachi', dict(data, name='Bad', magnitude='abc')), 'expression such as')
        self.assertEqual(mgr.post('/qc/mou/library/?location=Lahore', data).status_code, 403)
        self.assertEqual(chem.get('/qc/mou/library/').status_code, 200)

    def test_pages_render(self):
        c = self.client_for(self.adm)
        for u in ('/qc/mou/', '/qc/mou/?show=open', '/qc/mou/?show=all&location=Lahore', '/qc/mou/new/', '/qc/mou/library/', '/qc/mou/doc-control/',
                  '/qc/mou/deleted/', '/qc/mou/manual/', '/qc/mou/api/lookup/', '/qc/qc_main/'):
            self.assertEqual(c.get(u).status_code, 200, u)
        self.assertContains(c.get('/qc/qc_main/'), 'Measurement of Uncertainty')


class StrictQATests(TestCase):
    """Regression tests for the strict QA of 22-10-2026 (findings of the fresh-eyes review)."""
    @classmethod
    def setUpTestData(cls):
        cls.chem = User.objects.create_user('q_chem', password='x')
        cls.other = User.objects.create_user('q_other', password='x')
        cls.mgr = User.objects.create_user('q_mgr', password='x')
        cls.lmgr = User.objects.create_superuser('q_lmgr', 'l@b.c', 'x')      # superuser assigned to Lahore
        cls.adm = User.objects.create_superuser('q_adm', 'a@b.c', 'x')
        ControlChartReviewer.objects.create(user=cls.mgr, location='Karachi')
        ControlChartReviewer.objects.create(user=cls.lmgr, location='Lahore')
        from EnviTechAlApp.models import Signatures
        Signatures.objects.create(user=cls.other, office='Lahore')
        cls.src_l = MouSource.objects.create(location='Lahore', category='glassware', name='Lahore flask', unit='ml', range_value=100, magnitude='0.1', dist='tri')

    def c(self, u):
        c = Client(); c.force_login(u); return c

    def form(self, **over):
        f = {'location': 'Karachi', 'parameter': 'COD', 'level': '500 ppm', 'unit': 'mg/L', 'sample_kind': 'WS', 'range_value': '1500', 'k': '2', 'decimals': '3',
             'c0_kind': 'a_rep', 'c0_name': 'rep', 'c1_kind': 'a_repro', 'c1_name': 'repro',
             'c2_kind': 'b', 'c2_name': 'flask', 'c2_unit': 'ml', 'c2_range': '100', 'c2_magnitude': '0.1', 'c2_dist': 'tri', 'c2_ci': '1', 'c2_included': '1'}
        for i in range(2):
            f['op%d_present' % i] = '1'; f['op%d_label' % i] = 'AB'[i]
            for j, v in enumerate([502, 503, 501, 499, 499, 503, 501, 499, 502, 502]):
                f['op%d_v%d' % (i, j)] = str(v + i)
        f.update(over)
        return f

    def test_eval_expr_division_and_overflow(self):
        for bad in ('1/0', '0/0', '2.0**10000'):
            with self.assertRaises(ValueError):
                M.eval_expr(bad)
        d = self.c(self.chem).post('/qc/mou/api/calc/', self.form(c2_magnitude='1/0')).json()
        self.assertTrue(any('Magnitude' in e for e in d['errors']))
        self.assertEqual(M.fmt_sig(3.2e-12), '3.2e-12')

    def test_submit_requires_lab_membership(self):
        chem, other = self.c(self.chem), self.c(self.other)
        chem.post('/qc/mou/new/', self.form()); st = MouStudy.objects.get()
        self.assertEqual(other.post('/qc/mou/%d/action/' % st.pk, {'action': 'submit'}).status_code, 403)
        self.assertNotContains(other.get('/qc/mou/%d/' % st.pk), 'Submit for review')
        chem.post('/qc/mou/%d/action/' % st.pk, {'action': 'submit'}); st.refresh_from_db(); self.assertEqual(st.status, 'review')

    def test_new_study_location_follows_profile(self):
        r = self.c(self.other).post('/qc/mou/new/', self.form())          # Lahore profile, Karachi study
        self.assertContains(r, 'entered by its own staff'); self.assertEqual(MouStudy.objects.count(), 0)
        self.assertEqual(self.c(self.other).post('/qc/mou/new/', self.form(location='Lahore')).status_code, 302)

    def test_edit_cannot_collide_with_open_version(self):
        chem = self.c(self.chem)
        chem.post('/qc/mou/new/', self.form()); a = MouStudy.objects.get(level='500 ppm')
        chem.post('/qc/mou/new/', self.form(level='600 ppm')); b = MouStudy.objects.get(level='600 ppm')
        r = chem.post('/qc/mou/%d/edit/' % b.pk, self.form(level='500 ppm'))
        self.assertContains(r, 'already has an open version'); b.refresh_from_db(); self.assertEqual(b.level, '600 ppm')
        # key changed on edit to a key with an approved version -> becomes its next version
        for cl, act in ((chem, 'submit'), (self.c(self.mgr), 'review'), (self.c(self.adm), 'approve')):
            cl.post('/qc/mou/%d/action/' % a.pk, {'action': act})
        chem.post('/qc/mou/%d/edit/' % b.pk, self.form(level='500 ppm')); b.refresh_from_db()
        self.assertEqual((b.level, b.version, b.supersedes_id), ('500 ppm', 2, a.pk))

    def test_high_operator_indices_are_kept(self):
        f = self.form()
        for j in range(10):
            f['op7_v%d' % j] = '505'
        f['op7_present'] = '1'; f['op7_label'] = 'C'
        d = self.c(self.chem).post('/qc/mou/api/calc/', f).json()
        self.assertEqual([o['label'] for o in d['operators']], ['A', 'B', 'C'])
        f['c61_kind'] = 'b'; f['c61_name'] = 'late row'; f['c61_range'] = '10'; f['c61_magnitude'] = '1'; f['c61_dist'] = 'rect'; f['c61_included'] = '1'
        d = self.c(self.chem).post('/qc/mou/api/calc/', f).json()
        self.assertEqual(len(d['components']), 4)

    def test_unapprove_and_repeat_lab_scoped(self):
        chem, mgr, adm, lmgr = self.c(self.chem), self.c(self.mgr), self.c(self.adm), self.c(self.lmgr)
        chem.post('/qc/mou/new/', self.form()); st = MouStudy.objects.get()
        for cl, act in ((chem, 'submit'), (mgr, 'review'), (adm, 'approve')):
            cl.post('/qc/mou/%d/action/' % st.pk, {'action': act})
        self.assertEqual(lmgr.post('/qc/mou/%d/action/' % st.pk, {'action': 'unapprove', 'reason': 'lahore tries'}).status_code, 403)
        self.assertEqual(self.c(self.other).post('/qc/mou/%d/repeat/' % st.pk).status_code, 403)
        self.assertEqual(chem.post('/qc/mou/%d/repeat/' % st.pk).status_code, 302)

    def test_library_cross_lab_and_bad_ids(self):
        mgr = self.c(self.mgr)
        self.assertNotContains(mgr.get('/qc/mou/library/?location=Karachi&edit=%d' % self.src_l.pk), 'Lahore flask')
        self.assertEqual(mgr.post('/qc/mou/library/?location=Karachi', {'action': 'deactivate', 'id': 'abc'}).status_code, 404)
        chem = self.c(self.chem)
        chem.post('/qc/mou/new/', self.form(c2_source=str(self.src_l.pk)))
        self.assertIsNone(MouStudy.objects.get().components.get(order=2).source_id)

    def test_approve_confirm_escaped(self):
        chem = self.c(self.chem)
        chem.post('/qc/mou/new/', self.form(parameter="COD');alert(1);//"))
        st = MouStudy.objects.get()
        chem.post('/qc/mou/%d/action/' % st.pk, {'action': 'submit'}); self.c(self.mgr).post('/qc/mou/%d/action/' % st.pk, {'action': 'review'})
        r = self.c(self.adm).get('/qc/mou/%d/' % st.pk)
        self.assertNotContains(r, "COD');alert"); self.assertContains(r, "\\u0027)\\u003Balert")
