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


_DATE_TOK = _re.compile(r'^\s*(\d{1,2})[-/.](\d{1,2})[-/.](\d{2,4})\s*[,;\t ]\s*(\S+)\s*$')


def parse_dated_values(raw):
    """Baseline values with their dates (item 4, 10-10-2026): one "dd-mm-yyyy value" per line.
    Returns (dates, values, errors); dates is [] when the text holds plain values only."""
    lines = [ln for ln in (raw or '').splitlines() if ln.strip()]
    if not lines or not any(_DATE_TOK.match(ln) for ln in lines):
        vals, errs = parse_values(raw)
        return [], vals, errs
    import datetime as _d
    dates, vals, errs = [], [], []
    for i, ln in enumerate(lines, 1):
        m = _DATE_TOK.match(ln)
        if not m:
            errs.append('Line %d: use "dd-mm-yyyy value" on every line when dates are given ("%s").' % (i, ln.strip()[:40]))
            continue
        dd, mm, yy, tok = m.groups()
        yy = int(yy) + (2000 if len(yy) == 2 else 0)
        try:
            d = _d.date(yy, int(mm), int(dd))
        except ValueError:
            errs.append('Line %d: not a valid date ("%s").' % (i, ln.strip()[:40]))
            continue
        if ',' in tok and '.' not in tok and _re.fullmatch(r'-?\d+,\d+', tok):
            errs.append('Line %d: use a decimal point, not a comma ("%s").' % (i, tok))
            continue
        try:
            v = float(tok)
            if v != v or v in (float('inf'), float('-inf')):
                raise ValueError
        except ValueError:
            errs.append('Line %d: not a number ("%s").' % (i, tok[:30]))
            continue
        dates.append(d.isoformat()); vals.append(v)
    return dates, vals, errs


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
    'WS': dict(cadence='ws', ref='Working Standard', detail='Working Standard Detail', value='Working Standard (C.V)',
               range='Performance Range', result='Monthly working standard result', col='Run', what='WORKING STANDARD',
               unit='mg/l', desc='Working Standard Results during Monthly Exercise',
               note='The baseline results were established using data from the February working-standard activity, as per the '
                    'procedure ETAL-LAB-P-604 (two intermediate check activities are planned: one after calibration and the other '
                    'before PT). Accordingly, the results from the February activity (conducted before PT) were used to establish '
                    'the baseline, and the monthly results are plotted against this baseline.',
               base_hint='Usually the twelve February working-standard results (SOP ETAL-LAB-P-604).'),
    # 13-10-2026 (Karachi Lab Manager request): monthly equipment control charts under Intermediate Checks - the
    # equipment's intermediate-check run is the baseline and the month's daily checks are plotted against it
    'EQ': dict(cadence='ws', ref='Check standard', detail='Check standard detail', value='Nominal value',
               range='Acceptance range', result='Monthly result', col='Run', what='EQUIPMENT MONTHLY CHECK',
               unit='g', desc='Monthly control charts for equipment performance',
               note='The baseline results were established using data from the February intermediate check activity, as per the '
                    'procedure ETAL-LAB-P-604 (two intermediate check activities are planned: one after calibration and the other '
                    'before PT). Accordingly, the results from the February activity (conducted before PT) were used to establish '
                    'the baseline, and the monthly results are plotted against this baseline.',
               base_hint='Choose the intermediate-check run of this equipment below ("Use this run as baseline"); the Lab Manager '
                         'or the CEO then finalises it.'),
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
                  ('MON', 'Monitoring (temperature / humidity)'),
                  ('WS', 'Working Standard'),
                  ('EQ', 'Equipment monthly chart (IC baseline)'))
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
    # Training / reference charts (owner decision 11-10-2026): watermarked TRAINING on every form and
    # deletable by the Lab Manager / CEO even when signed and approved
    is_training = models.BooleanField(default=False)
    # Unit of the raw working of duplicate / spike charts (Result A / B, unspiked / spiked / added), e.g. mg/L
    raw_unit = models.CharField(max_length=30, blank=True, default='')
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

    # ---- raw working of duplicate / spike charts (11-10-2026)
    @property
    def raw_mode(self):
        return self.activity in ('DUP', 'SPK')

    @property
    def raw_fields(self):
        """[(field, label)] of the raw working entered for one result."""
        if self.activity == 'DUP':
            return [('raw_a', 'Result A'), ('raw_b', 'Result B')]
        if self.activity == 'SPK':
            return [('raw_a', 'Unspiked sample'), ('raw_b', 'Spiked sample'), ('raw_c', 'Spike added')]
        return []

    def raw_value(self, a, b, c=None):
        """Computed result from the raw working: RPD % (DUP) or recovery % (SPK); None if incomplete / invalid."""
        try:
            if self.activity == 'DUP' and a is not None and b is not None and (a + b) > 0:
                return abs(a - b) / ((a + b) / 2.0) * 100.0
            if self.activity == 'SPK' and a is not None and b is not None and c is not None and c > 0:
                return (b - a) / c * 100.0
        except (TypeError, ZeroDivisionError):
            pass
        return None

    def range_pair(self, b=None):
        """(low, high) text of the acceptance / certificate range. Monitoring charts can carry the
        range per baseline version (owner decision 11-10-2026): the given baseline, else the one the
        page is showing (_view_baseline), overrides the chart master when it has a range of its own."""
        src = b if b is not None else getattr(self, '_view_baseline', None)
        if self.activity == 'MON' and src is not None and (getattr(src, 'range_low', '') or getattr(src, 'range_high', '')):
            return src.range_low or '', src.range_high or ''
        return self.crm_range_low or '', self.crm_range_high or ''

    def range_text(self, b=None):
        lo, hi = self.range_pair(b)
        if lo and hi:
            return '%s-%s' % (lo, hi)
        if hi:                           # one-sided limit (duplicate RPD), e.g. "<= 10"
            return '\u2264 %s' % hi
        if lo:
            return '\u2265 %s' % lo
        return ''

    @property
    def crm_range(self):
        return self.range_text()

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

    def outside_range(self, value, b=None):
        sl = self.spec_limits(b)
        return bool(sl and value is not None and ((sl['ul'] is not None and value > sl['ul']) or (sl['ll'] is not None and value < sl['ll'])))

    def classify(self, lim, value, b=None):
        if self.spec_limited:
            if value is None:
                return 'ok'
            if self.outside_range(value, b):          # outside the fixed acceptance range: always out of limits
                return 'ooc'
            if self.fixed_limits or not lim:
                return 'ok'
            return classify_value(lim, value)      # baseline / run limits: warning beyond 2 SD, out of control beyond 3 SD
        return classify_value(lim, value, self.upper_only)

    def within_acceptance(self, value):
        """True / False when the certificate / acceptance range is numeric, else None."""
        rlo, rhi = self.range_pair()
        try:
            lo = float(rlo) if rlo not in ('', None) else None
            hi = float(rhi) if rhi not in ('', None) else None
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
        """Monitoring chart judged only against its fixed acceptance limits. A baseline-mode chart
        shows a period before its first baseline as a fixed-limit sheet (_view_fixed, set per page)."""
        return self.mon_mode == 'fixed' or bool(getattr(self, '_view_fixed', False))

    @property
    def self_limited(self):
        return self.activity == 'IC' or self.mon_mode == 'run'

    def ic_sources(self):
        """Intermediate-check charts of the same laboratory, equipment ID, parameter and level (monthly
        equipment charts take their baseline from one of their runs)."""
        return ControlChart.objects.filter(activity='IC', location=self.location, equipment_id__iexact=self.equipment_id,
                                           parameter__iexact=self.parameter, level__iexact=self.level).order_by('-active', 'pk')

    def eq_chart(self):
        """The monthly equipment chart that belongs to this intermediate-check chart, if any."""
        return ControlChart.objects.filter(activity='EQ', location=self.location, equipment_id__iexact=self.equipment_id,
                                           parameter__iexact=self.parameter, level__iexact=self.level).order_by('-active', 'pk').first()

    @property
    def period_is_month(self):
        return self.cadence in ('run', 'reading', 'ws')     # WS: one form per month (added 13-10-2026)

    @property
    def spec_limited(self):
        """Monitoring charts (any limit mode): fixed acceptance range always checked, timed readings,
        negative values allowed, Within / Out of limits wording."""
        return self.activity == 'MON'

    @property
    def no_baseline(self):
        return self.self_limited or self.fixed_limits

    def spec_limits(self, b=None):
        """Fixed limits of a monitoring chart (None for an open side); per-baseline range if set."""
        def num(x):
            try:
                return float(x) if x not in ('', None) else None
            except ValueError:
                return None
        rlo, rhi = self.range_pair(b)
        lo, hi, sp = num(rlo), num(rhi), num(self.crm_value)
        if lo is None and hi is None:
            return None
        mid = sp if sp is not None else ((lo + hi) / 2.0 if (lo is not None and hi is not None) else None)
        return {'spec': True, 'ul': hi, 'uwl': hi, 'lwl': lo, 'll': lo, 'mean': mid, 'sd': None, 'n': 0}

    @property
    def ooc_label(self):
        return 'Out of limits' if self.spec_limited else 'Out of control'

    def baseline_for(self, d):
        """Baseline in force on date d: the latest version established on or before d (seasonal
        baselines of monitoring charts). Before the first baseline a monitoring chart has none (its
        readings are judged against the acceptance range only); other charts fall back to the current."""
        b = self.baselines.filter(established_on__lte=d).order_by('-established_on', '-version').first()
        if b is None and self.activity == 'MON':
            return None
        return b or self.current_baseline()

    def effective_baseline(self, r):
        """Baseline a result belongs to (None for charts without baselines / before the first one)."""
        if self.self_limited or self.mon_mode == 'fixed':
            return None
        if r.baseline_id:
            return r.baseline
        return self.baseline_for(r.date) if self.mon_mode == 'baseline' else self.current_baseline()

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
    # 11-10-2026: date of each baseline value (ISO, parallel to values; may be empty for old versions)
    dates = models.JSONField(default=list, blank=True)
    # monitoring charts: acceptance range in force with this baseline (blank = the chart master's range)
    range_low = models.CharField(max_length=40, blank=True, default='')
    range_high = models.CharField(max_length=40, blank=True, default='')
    # mean / SD entered from a printed record whose data points were not supplied
    stats_only = models.BooleanField(default=False)
    n_points = models.IntegerField(null=True, blank=True)
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
        if self.stats_only:
            return self
        vals = [float(v) for v in self.values if v not in (None, '')]
        self.mean = _stats.mean(vals) if vals else None
        self.sd = _stats.stdev(vals) if len(vals) > 1 else None   # sample SD = Excel STDEV
        return self

    @property
    def n(self):
        if self.stats_only:
            return self.n_points or 0
        return len([v for v in self.values if v not in (None, '')])

    @property
    def n_text(self):
        return '-' if (self.stats_only and not self.n_points) else str(self.n)

    @property
    def established_label(self):
        """Month and year only (item 3, 10-10-2026): Mmm-yyyy."""
        return self.established_on.strftime('%b-%Y') if self.established_on else '-'

    def points(self):
        """[(date or None, value)] of the baseline data points."""
        ds = list(self.dates or [])
        out = []
        for i, v in enumerate(self.values or []):
            if v in (None, ''):
                continue
            d = ds[i] if i < len(ds) else None
            try:
                import datetime as _d
                d = _d.date.fromisoformat(d) if d else None
            except (TypeError, ValueError):
                d = None
            out.append((d, float(v)))
        return out

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


class ControlChartBaselineDraft(models.Model):
    """Baseline being prepared (owner decision 13-10-2026): analysts enter / paste the baseline points, review the live
    chart and correct points; the laboratory's Lab Manager or the CEO / administrator finalises it into a version.
    A draft is never used to judge results."""
    chart = models.OneToOneField(ControlChart, on_delete=models.CASCADE, related_name='baseline_draft')
    values = models.JSONField(default=list)
    dates = models.JSONField(default=list)
    established_on = models.DateField(null=True, blank=True)
    note = models.CharField(max_length=300, blank=True, default='')
    range_low = models.CharField(max_length=40, blank=True, default='')
    range_high = models.CharField(max_length=40, blank=True, default='')
    created_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    updated_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def lines(self):
        """The draft as 'dd-mm-yyyy value' lines (the format the baseline form accepts)."""
        out = []
        for i, v in enumerate(self.values or []):
            d = (self.dates or [None] * len(self.values))[i] if i < len(self.dates or []) else None
            ds = ''
            if d:
                try:
                    y, m, dd = str(d)[:10].split('-')
                    ds = '%s-%s-%s ' % (dd, m, y)
                except ValueError:
                    ds = ''
            t = repr(float(v))
            out.append(ds + (t[:-2] if t.endswith('.0') else t))
        return '\n'.join(out)


class ControlChartResult(models.Model):
    STATUS = (('ok', 'In control'), ('warning', 'Warning (>2 SD)'), ('ooc', 'Out of control (>3 SD)'))
    chart = models.ForeignKey(ControlChart, on_delete=models.CASCADE, related_name='results')
    baseline = models.ForeignKey(ControlChartBaseline, null=True, blank=True,
                                 on_delete=models.SET_NULL, related_name='results')
    date = models.DateField()
    time = models.CharField(max_length=5, blank=True, default='')   # HH:MM - monitoring readings (added 10-10-2026)
    reading_1 = models.FloatField(null=True, blank=True)            # monitoring: 1st-half reading (value = average)
    reading_2 = models.FloatField(null=True, blank=True)            # monitoring: 2nd-half reading
    # Raw working of duplicate / spike charts (added 11-10-2026). DUP: raw_a = Result A, raw_b = Result B,
    # value = RPD %.  SPK: raw_a = unspiked sample, raw_b = spiked sample, raw_c = spike added, value = recovery %.
    sample_id = models.CharField(max_length=60, blank=True, default='')
    raw_a = models.FloatField(null=True, blank=True)
    raw_b = models.FloatField(null=True, blank=True)
    raw_c = models.FloatField(null=True, blank=True)
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


class ControlChartDeletion(models.Model):
    """Audit trail of deleted control-chart records (owner decision 11-10-2026): who deleted what,
    when and why, with a copy of the deleted data. Deletion is reserved to the laboratory's
    QC / Lab Manager and the CEO / administrator."""
    KINDS = (('chart', 'Chart'), ('result', 'Result'), ('baseline', 'Baseline'))
    kind = models.CharField(max_length=10, choices=KINDS)
    chart_ref = models.IntegerField(null=True, blank=True)        # id of the chart (it may no longer exist)
    location = models.CharField(max_length=20, blank=True, default='')
    activity = models.CharField(max_length=10, blank=True, default='')
    label = models.CharField(max_length=300, blank=True, default='')
    reason = models.TextField()
    snapshot = models.JSONField(default=dict, blank=True)
    deleted_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    deleted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-deleted_at']

    def __str__(self):
        return '%s %s deleted %s' % (self.kind, self.label, self.deleted_at)


for _m in (ControlChart, ControlChartBaseline, ControlChartResult, ControlChartSignoff, ControlChartReviewer):
    _sh_register(_m)
