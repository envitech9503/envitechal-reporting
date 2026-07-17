"""Costing module — full-absorption cost per test parameter.
Ships as a self-contained Django app.

DESIGN NOTE (revised after inspecting the live Chemicals module):
The host Chemicals/Receive module records quantity but NOT cost, so the costing
module OWNS reagent rates in its own ReagentRate table (linked to the host
Chemical). Finance maintains these rates; the lab keeps maintaining inventory
quantities as before."""
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from decimal import Decimal
from simple_history.models import HistoricalRecords

NONNEG = [MinValueValidator(Decimal('0'))]

CHEM_MODEL = getattr(settings, 'COSTING_CHEMICAL_MODEL', 'dashboard.Chemical')


class CostingConfig(models.Model):
    """Global costing levers (single row)."""
    name = models.CharField(max_length=64, default='Default')
    working_days = models.DecimalField('Working days / month', max_digits=6, decimal_places=2, default=Decimal('22'))
    hours_per_day = models.DecimalField('Productive hours / day', max_digits=6, decimal_places=2, default=Decimal('7'))
    utilisation = models.DecimalField('Chargeable utilisation', max_digits=5, decimal_places=3, default=Decimal('0.75'))
    employer_uplift = models.DecimalField('Employer uplift on gross', max_digits=5, decimal_places=3, default=Decimal('0.12'))
    electricity_tariff = models.DecimalField('Electricity (PKR/kWh)', max_digits=10, decimal_places=4, default=Decimal('39.80'))
    di_water_cost = models.DecimalField('DI water (PKR/mL)', max_digits=10, decimal_places=4, default=Decimal('0.50'))
    rework_factor = models.DecimalField('Repeat-rework factor', max_digits=5, decimal_places=3, default=Decimal('0.05'))
    lab_overhead = models.DecimalField('Lab overhead', max_digits=5, decimal_places=3, default=Decimal('0.18'))
    ga_overhead = models.DecimalField('G&A overhead', max_digits=5, decimal_places=3, default=Decimal('0.07'))
    target_margin = models.DecimalField('Target margin (markup)', max_digits=5, decimal_places=3, default=Decimal('0.30'))
    price_rounding = models.DecimalField('Price rounding (PKR)', max_digits=8, decimal_places=2, default=Decimal('10'))
    thin_margin_pct = models.DecimalField('Thin-margin flag threshold (%)', max_digits=5,
                                          decimal_places=1, default=Decimal('15'), validators=NONNEG)
    updated = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Costing configuration'
        verbose_name_plural = 'Costing configuration'

    def __str__(self):
        return f'Costing configuration ({self.name})'

    @property
    def productive_hours_month(self):
        return self.working_days * self.hours_per_day * self.utilisation

    @classmethod
    def current(cls):
        """Single deterministic config row; race-safe via pk=1 get_or_create."""
        obj = cls.objects.order_by('pk').first()
        if obj is not None:
            return obj
        return cls.objects.get_or_create(pk=1)[0]


class ReagentRate(models.Model):
    """Purchase cost per base unit for a chemical — owned by the costing module,
    because the host inventory does not capture cost. One current rate per
    chemical (+ optional location); keep history via effective_from."""
    chemical = models.ForeignKey(CHEM_MODEL, on_delete=models.CASCADE, related_name='+')
    location = models.CharField(max_length=32, blank=True, default='',
                                help_text='Blank = applies to all labs; else Karachi / Lahore')
    unit_cost = models.DecimalField('Unit cost (PKR / base unit)', max_digits=14, decimal_places=4, default=0, validators=NONNEG)
    effective_from = models.DateField(null=True, blank=True)
    source = models.CharField(max_length=128, blank=True, help_text='e.g. Stock valuation 31-07-2026 / PO ref')
    updated = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Reagent rate'
        ordering = ['-effective_from', '-id']
        constraints = [models.UniqueConstraint(fields=['chemical', 'location'],
                                               name='uniq_rate_chemical_location')]

    def __str__(self):
        loc = f' @ {self.location}' if self.location else ''
        return f'{self.chemical}{loc}: PKR {self.unit_cost}'


class LabourGrade(models.Model):
    name = models.CharField(max_length=128)
    office = models.CharField(max_length=32, blank=True)
    gross_month = models.DecimalField('Gross salary / month (PKR)', max_digits=12, decimal_places=2, default=0, validators=NONNEG)
    is_direct = models.BooleanField('Direct (chargeable) staff', default=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.office})' if self.office else self.name

    def loaded_hourly(self, config=None):
        config = config or CostingConfig.current()
        ph = config.productive_hours_month or Decimal('1')
        return (self.gross_month * (Decimal('1') + config.employer_uplift)) / ph


class CostParameter(models.Model):
    code = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=255)
    matrix = models.CharField(max_length=64, blank=True)
    method = models.CharField(max_length=128, blank=True)
    location = models.CharField(max_length=32, default='Karachi')
    batch_size = models.PositiveIntegerField(default=10)
    annual_volume = models.PositiveIntegerField(default=1000)
    electricity_kwh = models.DecimalField('Electricity kWh / sample', max_digits=10, decimal_places=3, default=0, validators=NONNEG)
    di_water_ml = models.DecimalField('DI water mL / sample', max_digits=10, decimal_places=2, default=0, validators=NONNEG)
    instrument_cost = models.DecimalField('Instrument PKR / sample', max_digits=12, decimal_places=2, default=0, validators=NONNEG)
    waste_cost = models.DecimalField('Waste PKR / sample', max_digits=12, decimal_places=2, default=0, validators=NONNEG)
    qc_batch_cost = models.DecimalField('QC & calibration PKR / batch', max_digits=12, decimal_places=2, default=0, validators=NONNEG)
    annual_pool = models.DecimalField('Accreditation/PT/LIMS PKR / year', max_digits=14, decimal_places=2, default=0, validators=NONNEG)
    tax_category = models.CharField(max_length=64, default='SST - services')
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ['code']

    def __str__(self):
        return f'{self.code} — {self.name}'

    def compute(self, batch_size=None, config=None):
        from .services import compute_cost
        return compute_cost(self, batch_size=batch_size, config=config)


class RecipeChemical(models.Model):
    parameter = models.ForeignKey(CostParameter, related_name='chemicals', on_delete=models.CASCADE)
    chemical = models.ForeignKey(CHEM_MODEL, on_delete=models.PROTECT, related_name='+')
    qty_sample = models.DecimalField('Qty / sample', max_digits=12, decimal_places=4, default=0, validators=NONNEG)
    qty_batch = models.DecimalField('Qty / batch', max_digits=12, decimal_places=4, default=0, validators=NONNEG)
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Recipe — chemical'
        verbose_name_plural = 'Recipe — chemicals'

    def __str__(self):
        return f'{self.parameter.code}: {self.chemical}'


class RecipeLabour(models.Model):
    parameter = models.ForeignKey(CostParameter, related_name='labour', on_delete=models.CASCADE)
    grade = models.ForeignKey(LabourGrade, on_delete=models.PROTECT)
    minutes_sample = models.DecimalField('Minutes / sample', max_digits=8, decimal_places=2, default=0, validators=NONNEG)
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Recipe — labour'
        verbose_name_plural = 'Recipe — labour'

    def __str__(self):
        return f'{self.parameter.code}: {self.grade}'
