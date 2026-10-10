from django.db import models

# Create your models here.
class Dw_rds(models.Model):
    sample_id = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now=True)
    rds = models.JSONField(default=dict)
    
    
    def __str__(self):
    
        return f"{self.sample_id} {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
    
    
class Ww_rds(models.Model):
    sample_id = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now=True)
    rds = models.JSONField(default=dict)
    
    
    def __str__(self):
    
        return f"{self.sample_id} {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
    
    
class QCAuditConfig(models.Model):
    use_manual_dw = models.BooleanField(default=False)
    use_manual_ww = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "QC Audit Config"

    def __str__(self):
        return "QC Audit Configuration"
    
    
class TestingResultsOfDWSamples(models.Model):
    sample_id = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now=True)
    results = models.JSONField(default=dict)
    location = models.CharField(max_length=500,null=True)
    
    
class TestingResultsOfWWSamples(models.Model):
    sample_id = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now=True)
    results = models.JSONField(default=dict)
    location = models.CharField(max_length=500,null=True)
    

# --- Phase 1 audit trail (12-07-2026) ---
from simple_history import register as _sh_register
for _m in (Dw_rds, Ww_rds, TestingResultsOfDWSamples, TestingResultsOfWWSamples):
    _ex = [f.name for f in _m._meta.fields if 'image' in f.name.lower()]
    if _ex:
        _sh_register(_m, excluded_fields=_ex)
    else:
        _sh_register(_m)


# --- Control Charts (ETAL-LAB-604-FF-11), 07-10-2026 ---------------------------
# One ControlChart per parameter / concentration level / instrument / laboratory.
# The limits come from a versioned *baseline* (the ~12 intermediate-check results
# of the February activity, SOP ETAL-LAB-P-604): mean +/- 2 SD = warning limits,
# mean +/- 3 SD = action limits. Monthly results are plotted against the current
# baseline; results are reviewed and approved per calendar year (the printed form).
import statistics as _stats


def run_limits(values):
    """Mean / sample SD and the +/-2 SD, +/-3 SD limits of a list of values
    (None when fewer than 2 values). Used for baselines and for Intermediate
    Check runs, whose limits come from the run's own readings."""
    vals = [float(v) for v in values if v not in (None, '')]
    if len(vals) < 2:
        return None
    m, s = _stats.mean(vals), _stats.stdev(vals)
    return {'mean': m, 'sd': s, 'n': len(vals), 'uwl': m + 2 * s, 'lwl': m - 2 * s, 'ul': m + 3 * s, 'll': m - 3 * s}


def classify_value(lim, value, upper_only=False):
    """'ok' | 'warning' (outside +/-2 SD) | 'ooc' (outside +/-3 SD).
    upper_only: one-sided chart (duplicate RPD) - only high values are out of control."""
    if lim is None or value is None:
        return 'ok'
    if value > lim['ul'] or (not upper_only and value < lim['ll']):
        return 'ooc'
    if value > lim['uwl'] or (not upper_only and value < lim['lwl']):
        return 'warning'
    return 'ok'


import re as _re


def parse_values(raw):
    """Parse a list of numbers typed or pasted by a user.
    Separators: comma, semicolon, new line, tab, space.  A decimal comma typed by
    mistake ("1.002, 0,996" or "1,002 1,004") is REJECTED with a clear message - it
    used to be split silently into two numbers (0 and 996).  Returns (values, errors)."""
    raw = (raw or '').strip()
    errors = []
    isolated = _re.findall(r'(?<![\d.])\d+,\d+(?![\d.])', raw)
    ws_tokens = [t for t in _re.split(r'\s+', raw) if t]
    decimal_comma = bool(isolated) and (
        '.' in raw or                                               # mixed: 1.002, 0,996
        (len(ws_tokens) > 1 and all(_re.fullmatch(r'-?\d+,\d+[;]?', t) for t in ws_tokens)))   # 1,002 1,004
    if decimal_comma:
        errors.append('Use a decimal point, not a comma, inside numbers (found: %s). Separate values with commas, '
                      'semicolons, spaces or new lines.' % ', '.join(sorted(set(isolated))[:5]))
        return [], errors
    vals = []
    for tok in _re.split(r'[;,\s]+', raw):
        tok = tok.strip()
        if not tok:
            continue
        try:
            v = float(tok)
        except ValueError:
            errors.append('Not a number: "%s".' % tok[:30])
            continue
        if v != v or v in (float('inf'), float('-inf')):
            errors.append('Not a valid number: "%s".' % tok[:30])
            continue
        vals.append(v)
    return vals, errors


def suspect_values(vals):
    """Indices of values that are far from the rest (likely typing errors):
    more than 10 robust SDs (MAD based) and more than 50 % of the median away."""
    if len(vals) < 4:
        return []
    srt = sorted(vals)
    med = _stats.median(srt)
    mad = _stats.median([abs(v - med) for v in srt]) * 1.4826
    out = []
    for i, v in enumerate(vals):
        d = abs(v - med)
        if d > max(10 * mad, 0.5 * abs(med), 1e-12) and (mad > 0 or d > 0.5 * abs(med)):
            out.append(i)
    return out


# Behaviour and wording of each QC activity (08-10-2026 / 09-10-2026).
#   cadence: monthly = one result per month, 12 rows per cycle (CRM)
#            weekly  = sequential results (week labels) per cycle (RM)
#            batch   = sequential results per cycle, one per analytical batch (Duplicate, Spike)
#            run     = one run of readings per calendar month, limits from the run (IC)
#            reading = monitoring log: several timed readings per day, one sheet per calendar
#                      month, judged against FIXED acceptance limits (MON, added 10-10-2026)
ACTIVITY_PROFILE = {
    'CRM': dict(cadence='monthly', ref='CRM', detail='CRM Detail', value='CRM Certified Value', range='CRM Range',
                result='Monthly CRM result', col='Month', what='TESTING', unit='mg/l',
                desc='CRM Results during Monthly CRM Exercise',
                note='The baseline results were established using data from the February intermediate check activity, as per the '
                     'procedure ETAL-LAB-P-604 (two intermediate check activities are planned: one after calibration and the other '
                     'before PT). Accordingly, the results from the February activity (conducted before PT) were used to establish '
                     'the baseline, and the monthly results are plotted against this baseline.',
                base_hint='Usually the twelve February intermediate-check results (SOP ETAL-LAB-P-604).'),
    'RM': dict(cadence='weekly', ref='RM', detail='RM Detail', value='RM Value', range='RM Range',
               result='Weekly RM result', col='Week', what='RM EXERCISE', unit='mg/l',
               desc='RM Results during Weekly RM Exercise',
               note='The baseline results were established from the first twelve RM results of the exercise (procedure '
                    'ETAL-LAB-P-604); the weekly RM results are plotted against this baseline (mean +/- 2 SD warning, +/- 3 SD action).',
               base_hint='Usually the first twelve results of the RM exercise.'),
    'IC': dict(cadence='run', ref='CRM/RM', detail='CRM/RM Detail', value='CRM/RM Value', range='Acceptance Range',
               result='Intermediate check reading', col='Reading', what='INTERMEDIATE CHECK', unit='mg/l',
               desc='Control chart of Intermediate check for the equipment',
               note='Intermediate check of the equipment (procedure ETAL-LAB-P-604): the readings of the month are plotted against '
                    'the mean and standard deviation of that run (+/- 2 SD warning, +/- 3 SD action).',
               base_hint=''),
    'DUP': dict(cadence='batch', ref='Duplicate', detail='Sample / batch detail', value='Target RPD', range='Acceptance limit (RPD)',
                result='Duplicate RPD', col='Run', what='DUPLICATE ANALYSIS', unit='%',
                desc='Relative percent difference (RPD) of duplicate analyses',
                note='Duplicate analyses (procedure ETAL-LAB-P-604): the relative percent difference of each duplicate pair is plotted '
                     'against the baseline mean and standard deviation. The chart is one-sided - only RPD values above the upper '
                     'warning (+2 SD) and action (+3 SD) limits are out of control.',
                base_hint='Usually the RPD of the first twenty duplicate pairs (at least 12).'),
    'SPK': dict(cadence='batch', ref='Spike', detail='Spike detail', value='Expected recovery', range='Acceptance range (recovery)',
                result='Spike recovery', col='Run', what='SPIKE RECOVERY', unit='%',
                desc='Percent recovery of matrix spikes',
                note='Matrix spike recovery (procedure ETAL-LAB-P-604): the percent recovery of each spiked sample is plotted against '
                     'the baseline mean and standard deviation (+/- 2 SD warning, +/- 3 SD action).',
                base_hint='Usually the recoveries of the first twenty spiked samples (at least 12).'),
    'MON': dict(cadence='reading', ref='Monitoring', detail='Monitoring device', value='Set point / target', range='Acceptance limits',
                result='Reading', col='Time', what='MONITORING', unit='\u00b0C',
                desc='Temperature monitoring of the equipment / room',
                note='Equipment / environmental monitoring: each reading is compared with the fixed acceptance limits of the equipment '
                     'or room (e.g. visi-cooler 2-8 \u00b0C, laboratory 20-25 \u00b0C, relative humidity 30-70 %). A reading outside '
                     'the limits is out of limits and needs a remark / corrective action. Charts that use a baseline (e.g. a '
                     'seasonal baseline) or the month\'s own readings also show the +/- 2 SD warning and +/- 3 SD action limits.',
                base_hint='For a seasonal baseline enter the season\'s baseline readings and set "Established on" to the first day of '
                          'the season (e.g. 01-12-2025 for Winter); each season is a new version and readings are judged against the '
                          'version in force on their date.'),
}


class ControlChart(models.Model):
    LOCATIONS = (('Karachi', 'Karachi'), ('Lahore', 'Lahore'))
    ACTIVITIES = (('CRM', 'CRM (Certified Reference Material)'),
                  ('RM', 'Reference Material'),
                  ('IC', 'Intermediate Check'),
                  ('DUP', 'Duplicate'),
                  ('SPK', 'Spike / Recovery'),
                  ('MON', 'Monitoring (temperature / humidity)'))
    location = models.CharField(max_length=20, choices=LOCATIONS, default='Karachi')
    activity = models.CharField(max_length=10, choices=ACTIVITIES, default='CRM')
    parameter = models.CharField(max_length=120)            # e.g. Cadmium (Cd)
    level = models.CharField(max_length=60, blank=True, default='')   # e.g. 1 ppm
    unit = models.CharField(max_length=30, blank=True, default='mg/l')
    equipment = models.CharField(max_length=160, blank=True, default='')
    equipment_id = models.CharField(max_length=40, blank=True, default='')
    method = models.CharField(max_length=120, blank=True, default='')
    crm_detail = models.CharField(max_length=200, blank=True, default='')  # Product # / Lot #
    crm_value = models.CharField(max_length=40, blank=True, default='')    # certified value
    crm_range_low = models.CharField(max_length=40, blank=True, default='')
    crm_range_high = models.CharField(max_length=40, blank=True, default='')
    description = models.CharField(max_length=200, blank=True,
                                   default='CRM Results during Monthly CRM Exercise')
    decimals = models.IntegerField(default=3)
    # Monitoring charts (MON): how readings are judged (added 10-10-2026, Lahore environmental sheets)
    #   ''/'fixed' = fixed acceptance limits only; 'baseline' = baseline mean +/- 2/3 SD (versioned, e.g. seasonal)
    #   plus the fixed range; 'run' = the month's own readings +/- 2/3 SD plus the fixed range
    LIMIT_MODES = (('fixed', 'Fixed acceptance limits'), ('baseline', 'Baseline (+/- 2/3 SD), e.g. seasonal'),
                   ('run', "The month's own readings (+/- 2/3 SD)"))
    limit_mode = models.CharField(max_length=10, blank=True, default='', choices=LIMIT_MODES)
    # Document number printed on this chart's form when it differs from the laboratory's form number
    doc_no = models.CharField(max_length=60, blank=True, default='')
    # First month of the chart's 12-month record cycle (1 = Jan-Dec, 2 = Feb-Jan, 3 = Mar-Feb ...).
    # Added 08-10-2026: laboratories start a CRM / RM cycle when the baseline is established.
    start_month = models.IntegerField(default=1)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('auth.User', null=True, blank=True,
                                   on_delete=models.SET_NULL, related_name='+')

    class Meta:
        ordering = ['location', 'parameter', 'level', 'equipment_id']

    # ---- record cycle (CRM / RM). Intermediate checks are per calendar month and ignore it.
    @property
    def sm(self):
        try:
            m = int(self.start_month or 1)
        except (TypeError, ValueError):
            m = 1
        return m if (1 <= m <= 12 and not self.period_is_month) else 1

    def cycle_of(self, d):
        """Cycle year a date belongs to (the calendar year in which the cycle starts)."""
        return d.year if d.month >= self.sm else d.year - 1

    def cycle_range(self, year):
        """(first day, last day) of the cycle that starts in `year`."""
        import datetime as _d
        start = _d.date(year, self.sm, 1)
        end = _d.date(year + 1, self.sm, 1) - _d.timedelta(days=1) if self.sm > 1 else _d.date(year, 12, 31)
        return start, end

    def cycle_months(self, year):
        """12 (year, month) pairs of the cycle, in order."""
        out = []
        for i in range(12):
            m = self.sm + i
            out.append((year + (m - 1) // 12, (m - 1) % 12 + 1))
        return out

    def cycle_label(self, year):
        return str(year) if self.sm == 1 else '%d-%s' % (year, str(year + 1)[2:])

    @property
    def cycle_name(self):
        from QC.control_chart_render import MONTHS
        return '%s - %s' % (MONTHS[self.sm - 1], MONTHS[(self.sm + 10) % 12])

    def __str__(self):
        return '%s %s %s [%s] %s' % (self.activity, self.parameter, self.level,
                                     self.equipment_id, self.location)

    @property
    def title(self):
        return ('%s %s' % (self.parameter, self.level)).strip()

    @property
    def crm_range(self):
        if self.crm_range_low and self.crm_range_high:
            return '%s-%s' % (self.crm_range_low, self.crm_range_high)
        if self.crm_range_high:          # one-sided limit (duplicate RPD), e.g. "<= 10"
            return '\u2264 %s' % self.crm_range_high
        if self.crm_range_low:
            return '\u2265 %s' % self.crm_range_low
        return ''

    def current_baseline(self):
        return self.baselines.filter(is_current=True).order_by('-version').first()

    # ---- activity-driven behaviour (08-10-2026: RM and Intermediate Check charts)
    @property
    def cadence(self):
        """'monthly' (CRM: 12 month rows per year), 'weekly' (RM: sequential weekly
        results per year) or 'run' (IC: one run of ~12 readings per calendar month,
        limits computed from the run itself)."""
        return self.profile['cadence']

    @property
    def profile(self):
        return ACTIVITY_PROFILE.get(self.activity, ACTIVITY_PROFILE['CRM'])

    @property
    def upper_only(self):
        """One-sided chart: duplicate RPD (a low RPD is good, never out of control)."""
        return self.activity == 'DUP'

    def outside_range(self, value):
        sl = self.spec_limits()
        return bool(sl and value is not None and ((sl['ul'] is not None and value > sl['ul']) or (sl['ll'] is not None and value < sl['ll'])))

    def classify(self, lim, value):
        if self.spec_limited:
            if value is None:
                return 'ok'
            if self.outside_range(value):          # outside the fixed acceptance range: always out of limits
                return 'ooc'
            if self.fixed_limits or not lim:
                return 'ok'
            return classify_value(lim, value)      # baseline / run limits: warning beyond 2 SD, out of control beyond 3 SD
        return classify_value(lim, value, self.upper_only)

    def within_acceptance(self, value):
        """True / False when the certificate / acceptance range is numeric, else None."""
        try:
            lo = float(self.crm_range_low) if self.crm_range_low not in ('', None) else None
            hi = float(self.crm_range_high) if self.crm_range_high not in ('', None) else None
        except ValueError:
            return None
        if lo is None and hi is None:
            return None
        return (lo is None or value >= lo) and (hi is None or value <= hi)

    @property
    def mon_mode(self):
        if self.activity != 'MON':
            return ''
        return self.limit_mode if self.limit_mode in ('baseline', 'run') else 'fixed'

    @property
    def fixed_limits(self):
        """Monitoring chart judged only against its fixed acceptance limits."""
        return self.mon_mode == 'fixed'

    @property
    def self_limited(self):
        return self.activity == 'IC' or self.mon_mode == 'run'

    @property
    def period_is_month(self):
        return self.cadence in ('run', 'reading')

    @property
    def spec_limited(self):
        """Monitoring charts (any limit mode): fixed acceptance range always checked, timed readings,
        negative values allowed, Within / Out of limits wording."""
        return self.activity == 'MON'

    @property
    def no_baseline(self):
        return self.self_limited or self.fixed_limits

    def spec_limits(self):
        """Fixed limits of a monitoring chart (None for an open side)."""
        def num(x):
            try:
                return float(x) if x not in ('', None) else None
            except ValueError:
                return None
        lo, hi, sp = num(self.crm_range_low), num(self.crm_range_high), num(self.crm_value)
        if lo is None and hi is None:
            return None
        mid = sp if sp is not None else ((lo + hi) / 2.0 if (lo is not None and hi is not None) else None)
        return {'spec': True, 'ul': hi, 'uwl': hi, 'lwl': lo, 'll': lo, 'mean': mid, 'sd': None, 'n': 0}

    @property
    def ooc_label(self):
        return 'Out of limits' if self.spec_limited else 'Out of control'

    def baseline_for(self, d):
        """Baseline in force on date d: the latest version established on or before d (seasonal
        baselines of monitoring charts), else the current one."""
        b = self.baselines.filter(established_on__lte=d).order_by('-established_on', '-version').first()
        return b or self.current_baseline()

    @property
    def ref_label(self):
        return self.profile['ref']

    @property
    def result_label(self):
        return self.profile['result']

    @property
    def period_col(self):
        return self.profile['col']

    @property
    def label_detail(self):
        return self.profile['detail']

    @property
    def label_value(self):
        return self.profile['value']

    @property
    def label_range(self):
        return self.profile['range']

    @property
    def activity_short(self):
        return self.get_activity_display().split(' (')[0]


class ControlChartBaseline(models.Model):
    chart = models.ForeignKey(ControlChart, on_delete=models.CASCADE, related_name='baselines')
    version = models.IntegerField(default=1)
    established_on = models.DateField(null=True, blank=True)
    note = models.CharField(max_length=300, blank=True, default='')
    values = models.JSONField(default=list)        # list of floats, in order
    mean = models.FloatField(null=True, blank=True)
    sd = models.FloatField(null=True, blank=True)
    is_current = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('auth.User', null=True, blank=True,
                                   on_delete=models.SET_NULL, related_name='+')

    class Meta:
        ordering = ['-version']
        unique_together = ('chart', 'version')

    def compute(self):
        vals = [float(v) for v in self.values if v not in (None, '')]
        self.mean = _stats.mean(vals) if vals else None
        self.sd = _stats.stdev(vals) if len(vals) > 1 else None   # sample SD = Excel STDEV
        return self

    @property
    def n(self):
        return len([v for v in self.values if v not in (None, '')])

    def limits(self):
        if self.mean is None or self.sd is None:
            return None
        m, s = self.mean, self.sd
        return {'mean': m, 'sd': s, 'uwl': m + 2 * s, 'lwl': m - 2 * s,
                'ul': m + 3 * s, 'll': m - 3 * s}

    def classify(self, value):
        return classify_value(self.limits(), value, self.chart.upper_only)

    def __str__(self):
        return 'Baseline v%s of %s' % (self.version, self.chart_id)


class ControlChartResult(models.Model):
    STATUS = (('ok', 'In control'), ('warning', 'Warning (>2 SD)'), ('ooc', 'Out of control (>3 SD)'))
    chart = models.ForeignKey(ControlChart, on_delete=models.CASCADE, related_name='results')
    baseline = models.ForeignKey(ControlChartBaseline, null=True, blank=True,
                                 on_delete=models.SET_NULL, related_name='results')
    date = models.DateField()
    time = models.CharField(max_length=5, blank=True, default='')   # HH:MM - monitoring readings (added 10-10-2026)
    reading_1 = models.FloatField(null=True, blank=True)            # monitoring: 1st-half reading (value = average)
    reading_2 = models.FloatField(null=True, blank=True)            # monitoring: 2nd-half reading
    value = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='ok')
    remark = models.TextField(blank=True, default='')       # mandatory when status != ok
    performed_by = models.ForeignKey('auth.User', null=True, blank=True,
                                     on_delete=models.SET_NULL, related_name='+')
    performed_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date', 'time', 'id']

    @property
    def year(self):
        return self.date.year


class ControlChartSignoff(models.Model):
    """Review (QC Manager) and approval (CEO) of one chart's results for one
    calendar year -- the printed form. Approval locks that year's results for
    non-admin users."""
    chart = models.ForeignKey(ControlChart, on_delete=models.CASCADE, related_name='signoffs')
    year = models.IntegerField()
    month = models.IntegerField(default=0)   # 0 = whole year (CRM / RM); 1-12 = one IC run (added 08-10-2026)
    reviewed_by = models.ForeignKey('auth.User', null=True, blank=True,
                                    on_delete=models.SET_NULL, related_name='+')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey('auth.User', null=True, blank=True,
                                    on_delete=models.SET_NULL, related_name='+')
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('chart', 'year', 'month')

    @property
    def locked(self):
        return bool(self.approved_at)


class ControlChartReviewer(models.Model):
    """Laboratory assignment of a QC Manager / Lab Manager (added 07-10-2026).
    A user with one or more assignments may *review* control charts of those
    laboratories only; a superuser without any assignment (CEO / administrator)
    reviews and approves globally."""
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='control_chart_labs')
    location = models.CharField(max_length=20, choices=ControlChart.LOCATIONS)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    class Meta:
        unique_together = ('user', 'location')
        ordering = ['location', 'user__username']

    def __str__(self):
        return '%s - %s' % (self.user.get_username(), self.location)


for _m in (ControlChart, ControlChartBaseline, ControlChartResult, ControlChartSignoff, ControlChartReviewer):
    _sh_register(_m)
