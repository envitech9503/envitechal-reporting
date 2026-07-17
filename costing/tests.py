"""Costing regression suite — engine golden values, permissions, CRUD,
validators, constraints, history, export. Run:
  USE_POSTGRES=1 PG_PASSWORD=... python manage.py test costing --keepdb
"""
from decimal import Decimal as D
from unittest import mock

from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase, Client, override_settings

from .models import (CostingConfig, ReagentRate, LabourGrade, CostParameter,
                     RecipeChemical, RecipeLabour)
from .permissions import can_manage_costing
from .services import compute_cost, resolve_rate

Chem = apps.get_model(settings.COSTING_CHEMICAL_MODEL)
User = get_user_model()


def mk_config(**kw):
    d = dict(working_days=D('22'), hours_per_day=D('7'), utilisation=D('0.75'),
             employer_uplift=D('0.12'), electricity_tariff=D('40'),
             di_water_cost=D('0.5'), rework_factor=D('0.05'),
             lab_overhead=D('0.18'), ga_overhead=D('0.07'),
             target_margin=D('0.30'), price_rounding=D('10'),
             thin_margin_pct=D('15'))
    d.update(kw)
    return CostingConfig.objects.create(**d)


def mk_param(**kw):
    d = dict(code='T1', name='Test Param', matrix='Water', method='M',
             batch_size=10, annual_volume=1000, electricity_kwh=D('0'),
             di_water_ml=D('0'), instrument_cost=D('0'), waste_cost=D('0'),
             qc_batch_cost=D('0'), annual_pool=D('0'))
    d.update(kw)
    return CostParameter.objects.create(**d)


class EngineGoldenTests(TestCase):
    """Hand-computed golden values for the full-absorption engine."""

    def setUp(self):
        self.cfg = mk_config()
        self.chem = Chem.objects.create(name='Golden Reagent X')
        ReagentRate.objects.create(chemical=self.chem, location='', unit_cost=D('10'))
        self.grade = LabourGrade.objects.create(name='Analyst G', gross_month=D('84000'))

    def test_labour_loaded_hourly(self):
        # 84000 * 1.12 / (22*7*0.75 = 115.5) = 814.5454...
        self.assertAlmostEqual(float(self.grade.loaded_hourly(self.cfg)), 814.5455, places=3)

    def test_full_absorption_golden(self):
        p = mk_param(qc_batch_cost=D('100'), annual_pool=D('1000'))
        RecipeChemical.objects.create(parameter=p, chemical=self.chem,
                                      qty_sample=D('2'), qty_batch=D('5'))
        RecipeLabour.objects.create(parameter=p, grade=self.grade, minutes_sample=D('30'))
        r = compute_cost(p, config=self.cfg)
        # reagents/sample 2*10=20 ; labour 814.5455*30/60=407.2727
        # batch-shared (5*10+100)/10=15 ; vol 1000/1000=1 ; pre=443.2727
        # rework 22.1636 ; overhead (pre+rework)*0.25=116.3591
        # cost 581.7955 ; margin 174.5386 ; raw 756.33 -> price 760
        self.assertAlmostEqual(r['per_sample'], 427.27, places=1)
        self.assertAlmostEqual(r['pre_overhead'], 443.27, places=1)
        self.assertAlmostEqual(r['cost'], 581.80, places=1)
        self.assertEqual(r['price'], 760.0)
        self.assertEqual(r['missing_rates'], 0)

    def test_zero_batch_guarded(self):
        p = mk_param(code='T2', batch_size=10)
        r = compute_cost(p, batch_size=0, config=self.cfg)
        self.assertEqual(r['batch_size'], 10)  # 0 falls back to the parameter's own batch size
        r = compute_cost(p, batch_size=-5, config=self.cfg)
        self.assertEqual(r['batch_size'], 1)  # negative clamped, no division by zero

    def test_missing_rate_flagged_not_crashing(self):
        lonely = Chem.objects.create(name='Unpriced Reagent Z')
        p = mk_param(code='T3')
        RecipeChemical.objects.create(parameter=p, chemical=lonely,
                                      qty_sample=D('1'), qty_batch=D('0'))
        r = compute_cost(p, config=self.cfg)
        self.assertEqual(r['missing_rates'], 1)
        self.assertEqual(r['reagents_sample'], 0.0)


class RateResolutionTests(TestCase):
    def setUp(self):
        self.chem = Chem.objects.create(name='Rate Chem')

    def test_location_specific_beats_blank(self):
        ReagentRate.objects.create(chemical=self.chem, location='', unit_cost=D('5'))
        ReagentRate.objects.create(chemical=self.chem, location='Karachi', unit_cost=D('7'))
        rate, src = resolve_rate(self.chem, 'Karachi')
        self.assertEqual((rate, src), (D('7'), 'table'))
        rate, _ = resolve_rate(self.chem, 'Lahore')  # falls back to blank
        self.assertEqual(rate, D('5'))

    def test_missing(self):
        rate, src = resolve_rate(self.chem, 'Karachi')
        self.assertEqual((rate, src), (D('0'), 'missing'))

    def test_unique_constraint_blocks_duplicates(self):
        ReagentRate.objects.create(chemical=self.chem, location='Karachi', unit_cost=D('7'))
        with self.assertRaises(IntegrityError), transaction.atomic():
            ReagentRate.objects.create(chemical=self.chem, location='Karachi', unit_cost=D('9'))


class ValidatorTests(TestCase):
    def test_negative_money_rejected(self):
        chem = Chem.objects.create(name='V Chem')
        rr = ReagentRate(chemical=chem, location='', unit_cost=D('-1'))
        with self.assertRaises(ValidationError):
            rr.full_clean()
        p = mk_param(code='V1', electricity_kwh=D('-0.5'))
        with self.assertRaises(ValidationError):
            p.full_clean()

    def test_config_singleton_current(self):
        a = CostingConfig.current()
        b = CostingConfig.current()
        self.assertEqual(a.pk, b.pk)
        self.assertEqual(CostingConfig.objects.count(), 1)


class PermissionTests(TestCase):
    def setUp(self):
        self.su = User.objects.create_superuser('t_admin', 'a@e.com', 'x')
        self.staff = User.objects.create_user('t_staff', 's@e.com', 'x')
        self.cfg = mk_config()
        self.p = mk_param(code='P1')

    def test_superuser_manages(self):
        self.assertTrue(can_manage_costing(self.su))

    def test_plain_user_cannot_manage(self):
        self.assertFalse(can_manage_costing(self.staff))

    def test_manager_role_manages(self):
        with mock.patch('costing.permissions.user_role_name', return_value='Assistant Manager'):
            self.assertTrue(can_manage_costing(self.staff))
        with mock.patch('costing.permissions.user_role_name', return_value='Deputy Analyst'):
            self.assertFalse(can_manage_costing(self.staff))

    @override_settings(ALLOWED_HOSTS=['*'])
    def test_staff_can_view_but_not_mutate(self):
        c = Client()
        c.force_login(self.staff)
        self.assertEqual(c.get('/dashboard/costing/', secure=True).status_code, 200)
        n0 = CostParameter.objects.count()
        r = c.post('/dashboard/costing/%d/clone/' % self.p.pk, secure=True)
        self.assertEqual(r.status_code, 302)
        self.assertEqual(CostParameter.objects.count(), n0)  # blocked
        c.post('/dashboard/costing/%d/archive/' % self.p.pk, secure=True)
        self.p.refresh_from_db()
        self.assertTrue(self.p.active)  # unchanged

    @override_settings(ALLOWED_HOSTS=['*'])
    def test_manager_crud_clone_archive(self):
        c = Client()
        c.force_login(self.su)
        n0 = CostParameter.objects.count()
        c.post('/dashboard/costing/%d/clone/' % self.p.pk, secure=True)
        self.assertEqual(CostParameter.objects.count(), n0 + 1)
        c.post('/dashboard/costing/%d/archive/' % self.p.pk, secure=True)
        self.p.refresh_from_db()
        self.assertFalse(self.p.active)
        r = c.get('/dashboard/costing/%d/history/' % self.p.pk, secure=True)
        self.assertEqual(r.status_code, 200)


class HistoryTests(TestCase):
    def test_history_rows_written(self):
        mk_config()
        p = mk_param(code='H1')
        self.assertEqual(p.history.count(), 1)
        p.name = 'Renamed'
        p.save()
        self.assertEqual(p.history.count(), 2)
        diff = p.history.first().diff_against(p.history.all()[1])
        self.assertIn('name', [c.field for c in diff.changes])


class ExportTests(TestCase):
    @override_settings(ALLOWED_HOSTS=['*'])
    def test_csv_export(self):
        mk_config()
        mk_param(code='E1')
        u = User.objects.create_user('t_export', 'e@e.com', 'x')
        c = Client()
        c.force_login(u)
        r = c.get('/dashboard/costing/export.csv', secure=True)
        self.assertEqual(r.status_code, 200)
        self.assertIn('text/csv', r['Content-Type'])
        body = r.content.decode()
        self.assertIn('E1', body)
        self.assertIn('Recommended price', body)
