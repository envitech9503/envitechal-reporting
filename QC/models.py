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
    def unit_label(self):
        """Unit as printed on forms and graphs (19-10-2026, Lab Manager item 1): litre written with a capital L
        (mg/l -> mg/L, ug/l -> ug/L), as in the laboratory's controlled forms."""
        import re as _re
        return _re.sub(r'/l\b', '/L', self.unit or '')

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
    # Prepared By (owner request 23-10-2026, both laboratories): the analyst who prepared the form on the system
    # and signed it as preparer. Blank = derived from the results when one analyst recorded them all.
    prepared_by = models.ForeignKey('auth.User', null=True, blank=True,
                                    on_delete=models.SET_NULL, related_name='+')
    prepared_at = models.DateTimeField(null=True, blank=True)

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


# =====================================================================================
# Measurement of Uncertainty (form ETAL-LAB-706-FF-01) - 21-10-2026
# One function for both laboratories under Quality: an uncertainty-source library per
# laboratory, studies (parameter / level / sample) with operators x replicates and a
# relative uncertainty budget, review / approval, versions and a register of current U.
# Arithmetic lives in QC/mou_calc.py (pure Python, unit-tested against the Karachi workbooks).
# =====================================================================================
class MouSource(models.Model):
    """Library entry: an instrument, glassware, reagent / CRM or environmental source of
    uncertainty with its magnitude, distribution and the certificate it rests on. A study
    copies the values at the time it is made (MouComponent), so a later re-calibration never
    silently changes an approved study."""
    CATEGORIES = (('instrument', 'Instrument'), ('glassware', 'Volumetric glassware'), ('reference', 'CRM / reference standard'),
                  ('reagent', 'Reagent purity'), ('environment', 'Environment'), ('other', 'Other'))
    location = models.CharField(max_length=20, default='Karachi')
    category = models.CharField(max_length=12, choices=CATEGORIES, default='instrument')
    name = models.CharField(max_length=160)
    unit = models.CharField(max_length=20, blank=True, default='')
    range_value = models.FloatField(help_text='x - the range / nominal value the magnitude is expressed against')
    magnitude = models.CharField(max_length=60, help_text='a - number or expression, e.g. 0.08/2')
    dist = models.CharField(max_length=10, default='normal')
    ci = models.FloatField(default=1.0)
    reference = models.CharField(max_length=160, blank=True, default='', help_text='certificate / calibration report no.')
    calibrated_on = models.DateField(null=True, blank=True)
    valid_until = models.DateField(null=True, blank=True)
    note = models.CharField(max_length=300, blank=True, default='')
    active = models.BooleanField(default=True)
    created_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['location', 'category', 'name']

    def __str__(self):
        return '%s - %s' % (self.location, self.name)

    @property
    def magnitude_value(self):
        from QC.mou_calc import eval_expr
        try:
            return eval_expr(self.magnitude)
        except ValueError:
            return None

    @property
    def validity(self):
        """'ok' / 'due' (within 30 days) / 'expired' / '' (no validity recorded). Informative only -
        the owner decided (21-10-2026) that validity never blocks a study."""
        if not self.valid_until:
            return ''
        from datetime import date as _d
        days = (self.valid_until - _d.today()).days
        return 'expired' if days < 0 else ('due' if days <= 30 else 'ok')


class MouStudy(models.Model):
    KINDS = (('CRM', 'CRM (certified reference material)'), ('RM', 'Reference material (RM / PT sample)'), ('WS', 'Working standard'), ('SAMPLE', 'Sample / other'))
    STATUSES = (('draft', 'Draft'), ('review', 'Submitted for review'), ('reviewed', 'Reviewed'),
                ('approved', 'Approved'), ('superseded', 'Superseded'))
    location = models.CharField(max_length=20, default='Karachi')
    parameter = models.CharField(max_length=80)
    level = models.CharField(max_length=60, blank=True, default='', help_text='nominal level, e.g. 500 ppm')
    unit = models.CharField(max_length=20, blank=True, default='mg/L')
    sample_kind = models.CharField(max_length=8, choices=KINDS, default='CRM')
    sample_ref = models.CharField(max_length=200, blank=True, default='', help_text='CRM product / lot or working-standard ID')
    method = models.CharField(max_length=120, blank=True, default='')
    instrument = models.CharField(max_length=120, blank=True, default='')
    equipment_id = models.CharField(max_length=60, blank=True, default='')
    range_value = models.FloatField(null=True, blank=True, help_text='x - method / calibration range the Type A terms are expressed against')
    env_temp = models.FloatField(null=True, blank=True)
    study_date = models.DateField(null=True, blank=True)
    k = models.FloatField(default=2.0)
    decimals = models.PositiveSmallIntegerField(default=3)
    remarks = models.TextField(blank=True, default='')
    status = models.CharField(max_length=10, choices=STATUSES, default='draft')
    version = models.PositiveIntegerField(default=1)
    supersedes = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='repeats')
    # cached results (recomputed on every save of the study / operators / components)
    n_total = models.PositiveIntegerField(default=0)
    mean = models.FloatField(null=True, blank=True)
    uc = models.FloatField(null=True, blank=True)             # relative combined
    u_exp = models.FloatField(null=True, blank=True)          # relative expanded (k * uc)
    u_abs = models.FloatField(null=True, blank=True)          # expanded, absolute (unit of the measurand)
    u_pct = models.FloatField(null=True, blank=True)          # expanded, % of the measured mean
    calc_errors = models.JSONField(default=list, blank=True)
    # legacy: the figures the laboratory's workbook printed (induction) and the discrepancy notes
    legacy = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    submitted_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    submitted_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['location', 'parameter', 'level', '-version']
        verbose_name_plural = 'MOU studies'

    def __str__(self):
        return '%s %s %s v%d (%s)' % (self.location, self.parameter, self.level, self.version, self.status)

    @property
    def title(self):
        return ('%s %s' % (self.parameter, self.level)).strip()

    @property
    def locked(self):
        return self.status in ('reviewed', 'approved', 'superseded')

    @property
    def is_current(self):
        return self.status == 'approved'

    def as_calc(self):
        """Dict for QC.mou_calc.compute()."""
        return {'range': self.range_value, 'k': self.k,
                'operators': [{'label': o.label, 'values': o.values} for o in self.operators.all()],
                'components': [{'kind': c.kind, 'name': c.name, 'unit': c.unit, 'range': c.range_value, 'magnitude': c.magnitude,
                                'dist': c.dist, 'ci': c.ci, 'included': c.included} for c in self.components.all()]}

    def recompute(self, save=True):
        from QC.mou_calc import compute
        r = compute(self.as_calc())
        self.n_total = r['grand']['n']
        self.mean = r['grand']['mean']
        self.uc, self.u_exp, self.u_abs, self.u_pct = r['uc'], r['U'], r['U_abs'], r['U_pct']
        self.calc_errors = r['errors']
        if save:
            self.save(update_fields=['n_total', 'mean', 'uc', 'u_exp', 'u_abs', 'u_pct', 'calc_errors', 'updated_at'])
        return r


class MouOperator(models.Model):
    study = models.ForeignKey(MouStudy, on_delete=models.CASCADE, related_name='operators')
    order = models.PositiveSmallIntegerField(default=0)
    label = models.CharField(max_length=4, default='A')
    analyst = models.CharField(max_length=80, blank=True, default='')
    date = models.DateField(null=True, blank=True)
    values = models.JSONField(default=list, blank=True)        # replicates, floats

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return 'Operator %s of %s' % (self.label, self.study_id)


class MouComponent(models.Model):
    """One row of the uncertainty budget. Type A rows hold no magnitude (it is the SD of the
    replicates); Type B rows copy the library values when the source is picked."""
    KINDS = (('a_rep', 'Type A - repeatability'), ('a_repro', 'Type A - reproducibility'), ('b', 'Type B'))
    study = models.ForeignKey(MouStudy, on_delete=models.CASCADE, related_name='components')
    order = models.PositiveSmallIntegerField(default=0)
    kind = models.CharField(max_length=8, choices=KINDS, default='b')
    source = models.ForeignKey(MouSource, null=True, blank=True, on_delete=models.SET_NULL, related_name='uses')
    name = models.CharField(max_length=160)
    unit = models.CharField(max_length=20, blank=True, default='')
    range_value = models.FloatField(null=True, blank=True)
    magnitude = models.CharField(max_length=60, blank=True, default='')
    dist = models.CharField(max_length=10, default='normal')
    ci = models.FloatField(default=1.0)
    included = models.BooleanField(default=True)
    note = models.CharField(max_length=300, blank=True, default='')

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.name


for _m in (MouSource, MouStudy, MouOperator, MouComponent):
    _sh_register(_m)


# ====================================================================================================
# Quality - Internal Audit (ETAL-QMS-808-FF-01/02/03) and Non-conformance & Corrective Action
# (ETAL-QMS-710-FF-01 / 01A / 02). 22-10-2026. One function for both laboratories, lab-scoped.
# ====================================================================================================
class IaClause(models.Model):
    """Master checklist row: ISO/IEC 17025:2017 clause (or a PNAC policy) with the laboratory's own
    checklist wording. Findings copy the wording at audit time, so editing the master never changes
    a signed report."""
    code = models.CharField(max_length=12, unique=True)             # 4.1.1, 7.8.2.1, PNAC-1
    title = models.CharField(max_length=400, blank=True, default='')
    requirement = models.TextField(blank=True, default='')
    level = models.PositiveSmallIntegerField(default=1)
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'code']

    def __str__(self):
        return '%s %s' % (self.code, self.title)

    @property
    def is_heading(self):
        return self.level == 1 or self.code == 'PNAC'


class IaPlan(models.Model):
    """Annual Internal Audit Plan (ETAL-QMS-808-FF-01): departments x months, Due / Done marks.
    Signed by the Management Representative, approved by the CEO."""
    STATUSES = (('draft', 'Draft'), ('signed', 'Signed by MR - awaiting CEO'), ('approved', 'Approved'))
    location = models.CharField(max_length=20, default='Karachi')
    year = models.PositiveIntegerField()
    rows = models.JSONField(default=list, blank=True)      # [{'department': str, 'months': {'3': {'due': True, 'done': False}}}]
    remarks = models.TextField(blank=True, default='')
    status = models.CharField(max_length=10, choices=STATUSES, default='draft')
    mr_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    mr_at = models.DateTimeField(null=True, blank=True)
    mr_name = models.CharField(max_length=120, blank=True, default='')      # printed name when inducted
    mr_date = models.DateField(null=True, blank=True)
    ceo_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    ceo_at = models.DateTimeField(null=True, blank=True)
    ceo_name = models.CharField(max_length=120, blank=True, default='')
    ceo_date = models.DateField(null=True, blank=True)
    legacy = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-year', 'location']
        unique_together = ('location', 'year')

    @property
    def inducted(self):
        """True for a record inducted from the laboratory's paper / Word record (legacy.key is set by the import)."""
        return bool((self.legacy or {}).get('key') or (self.legacy or {}).get('inducted'))

    def __str__(self):
        return 'Annual Internal Audit Plan %d - %s' % (self.year, self.location)

    @property
    def locked(self):
        return self.status == 'approved'


class IaAudit(models.Model):
    """Internal Audit Report (ETAL-QMS-808-FF-02): header, clause-by-clause findings, summary,
    conclusion; signed by the internal auditor, then acknowledged by the auditee."""
    STATUSES = (('draft', 'Draft - being audited'), ('auditor', 'Signed by auditor - awaiting auditee'), ('closed', 'Signed by auditor and auditee'))
    location = models.CharField(max_length=20, default='Karachi')
    audit_no = models.CharField(max_length=20)                        # 01/2025
    year = models.PositiveIntegerField()
    seq = models.PositiveSmallIntegerField(default=1)
    date_start = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)
    days = models.PositiveSmallIntegerField(default=2)
    auditor = models.CharField(max_length=120, blank=True, default='')
    auditor_title = models.CharField(max_length=120, blank=True, default='')
    auditor_user = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    auditee = models.CharField(max_length=160, blank=True, default='')
    auditee_title = models.CharField(max_length=120, blank=True, default='')
    auditee_user = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    address = models.CharField(max_length=250, blank=True, default='')
    scope = models.CharField(max_length=300, blank=True, default='To check all clauses of ISO/IEC 17025:2017 (technical & management) and to evaluate the performance of testing activities.')
    n_obs = models.PositiveSmallIntegerField(default=0)
    n_minor = models.PositiveSmallIntegerField(default=0)
    n_major = models.PositiveSmallIntegerField(default=0)
    timeframe = models.CharField(max_length=400, blank=True, default='')
    conclusion = models.TextField(blank=True, default='')
    status = models.CharField(max_length=10, choices=STATUSES, default='draft')
    auditor_signed_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    auditor_signed_at = models.DateTimeField(null=True, blank=True)
    auditor_sign_date = models.DateField(null=True, blank=True)       # date printed on the form
    auditee_signed_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    auditee_signed_at = models.DateTimeField(null=True, blank=True)
    auditee_sign_date = models.DateField(null=True, blank=True)
    remarks = models.TextField(blank=True, default='')
    legacy = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-year', '-seq', 'location']
        unique_together = ('location', 'audit_no')

    @property
    def inducted(self):
        """True for a record inducted from the laboratory's paper / Word record (legacy.key is set by the import)."""
        return bool((self.legacy or {}).get('key') or (self.legacy or {}).get('inducted'))

    def __str__(self):
        return 'Internal Audit %s - %s' % (self.audit_no, self.location)

    @property
    def locked(self):
        return self.status != 'draft'

    @property
    def n_total(self):
        return self.n_minor + self.n_major

    def recount(self, save=True):
        """Summary counts from the findings (the printed summary of an inducted report is kept in legacy)."""
        c = {'obs': 0, 'minor': 0, 'major': 0}
        for f in self.findings.all():
            if f.result in c:
                c[f.result] += 1
        self.n_obs, self.n_minor, self.n_major = c['obs'], c['minor'], c['major']
        if save:
            self.save(update_fields=['n_obs', 'n_minor', 'n_major', 'updated_at'])
        return c


class IaFinding(models.Model):
    """One checklist row of an audit report. Wording is copied from the master / the previous audit
    so the report stays as written even when the master changes."""
    RESULTS = (('', '-'), ('c', 'Conforms'), ('obs', 'Observation'), ('minor', 'Minor NC'), ('major', 'Major NC'), ('na', 'Not applicable'))
    audit = models.ForeignKey(IaAudit, on_delete=models.CASCADE, related_name='findings')
    order = models.PositiveIntegerField(default=0)
    clause = models.ForeignKey(IaClause, null=True, blank=True, on_delete=models.SET_NULL, related_name='findings')
    label = models.CharField(max_length=12, blank=True, default='')        # printed clause number ('' for a continuation row)
    requirement = models.TextField(blank=True, default='')
    ref = models.CharField(max_length=400, blank=True, default='')           # Lab's reference to its QMS
    finding = models.TextField(blank=True, default='')
    result = models.CharField(max_length=6, choices=RESULTS, blank=True, default='')
    tag = models.CharField(max_length=40, blank=True, default='')            # NC-01, MNC-02, Obs-01 ...

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return '%s %s' % (self.label, self.result)


class IaCircular(models.Model):
    """Internal Audit Circular (ETAL-QMS-808-FF-03) - the audit notice with the schedule and the
    attendance list; also used for witnessing circulars. Issued by the MR; attendees sign receipt."""
    KINDS = (('audit', 'Internal audit'), ('witness', 'Witnessing'))
    STATUSES = (('draft', 'Draft'), ('issued', 'Issued'))
    location = models.CharField(max_length=20, default='Karachi')
    kind = models.CharField(max_length=8, choices=KINDS, default='audit')
    audit = models.ForeignKey(IaAudit, null=True, blank=True, on_delete=models.SET_NULL, related_name='circulars')
    audit_no = models.CharField(max_length=20, blank=True, default='')
    issue_date = models.DateField(null=True, blank=True)
    audit_date_text = models.CharField(max_length=80, blank=True, default='')
    to_text = models.CharField(max_length=160, blank=True, default='Concerned Persons/All relevant HODs')
    from_text = models.CharField(max_length=120, blank=True, default='Management Representative')
    sessions = models.JSONField(default=list, blank=True)     # [{'sr','day','time_from','time_to','scope','criteria','auditors','auditee'}]
    attendance = models.JSONField(default=list, blank=True)   # [{'name','designation','user_id','signed_at'}]
    ceo_name = models.CharField(max_length=120, blank=True, default='')
    status = models.CharField(max_length=8, choices=STATUSES, default='draft')
    issued_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    issued_at = models.DateTimeField(null=True, blank=True)
    legacy = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-issue_date', '-id']

    @property
    def inducted(self):
        """True for a record inducted from the laboratory's paper / Word record (legacy.key is set by the import)."""
        return bool((self.legacy or {}).get('key') or (self.legacy or {}).get('inducted'))

    def __str__(self):
        return '%s circular %s - %s' % (self.get_kind_display(), self.audit_no, self.location)

    @property
    def locked(self):
        return self.status == 'issued'


class IaWitness(models.Model):
    """Witnessing record (part of the audit report): tests witnessed with assigned vs obtained
    values and the auditor's remarks; signed by the auditor and the analysts witnessed."""
    STATUSES = (('draft', 'Draft'), ('auditor', 'Signed by auditor'), ('closed', 'Signed by auditor and analysts'))
    audit = models.ForeignKey(IaAudit, on_delete=models.CASCADE, related_name='witnessings')
    circular = models.ForeignKey(IaCircular, null=True, blank=True, on_delete=models.SET_NULL, related_name='witnessings')
    date = models.DateField(null=True, blank=True)
    rows = models.JSONField(default=list, blank=True)      # [{'parameter','performed_by','range','assigned','obtained','remarks'}]
    auditor = models.CharField(max_length=120, blank=True, default='')
    auditor_signed_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    auditor_signed_at = models.DateTimeField(null=True, blank=True)
    auditees = models.JSONField(default=list, blank=True)  # [{'name','user_id','signed_at'}]
    sign_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=8, choices=STATUSES, default='draft')
    legacy = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date', 'id']

    @property
    def inducted(self):
        """True for a record inducted from the laboratory's paper / Word record (legacy.key is set by the import)."""
        return bool((self.legacy or {}).get('key') or (self.legacy or {}).get('inducted'))

    def __str__(self):
        return 'Witnessing %s' % self.date

    @property
    def locked(self):
        return self.status != 'draft'


class Ncca(models.Model):
    """Non-conformance & Corrective Action form (ETAL-QMS-710-FF-01) and the row it occupies in
    the NC&CA Log (710-FF-02). Raised by the auditor / MR, answered by the concerned department
    (root cause, corrective action), followed up and closed by the MR."""
    SOURCES = (('IA', 'Internal audit'), ('EA', 'External assessment (PNAC)'), ('CC', 'Customer complaint'), ('TEST', 'Testing'), ('CAL', 'Calibration'), ('OTHER', 'Other / management system'))
    CATEGORIES = (('pfi', 'Point for improvement'), ('obs', 'Observation'), ('minor', 'Minor nonconformance'), ('major', 'Major nonconformance'), ('critical', 'Critical nonconformance'))
    LEVELS = (('high', 'High'), ('medium', 'Medium'), ('low', 'Low'))
    STATUSES = (('draft', 'Draft'), ('open', 'Raised - awaiting department response'), ('responded', 'Department responded - awaiting MR follow-up'), ('closed', 'Closed'))
    location = models.CharField(max_length=20, default='Karachi')
    nc_no = models.CharField(max_length=40)
    date = models.DateField(null=True, blank=True)
    department = models.CharField(max_length=80, blank=True, default='Lab')
    raised_by = models.CharField(max_length=120, blank=True, default='')
    raised_user = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    clause = models.CharField(max_length=60, blank=True, default='')
    source = models.CharField(max_length=6, choices=SOURCES, default='IA')
    audit = models.ForeignKey(IaAudit, null=True, blank=True, on_delete=models.SET_NULL, related_name='ncs')
    finding = models.ForeignKey(IaFinding, null=True, blank=True, on_delete=models.SET_NULL, related_name='ncs')
    # Raised due to
    due_audit_internal = models.BooleanField(default=False)
    due_audit_external = models.BooleanField(default=False)
    due_testing = models.BooleanField(default=False)
    due_cal_internal = models.BooleanField(default=False)
    due_cal_external = models.BooleanField(default=False)
    due_complaint = models.BooleanField(default=False)
    due_other = models.CharField(max_length=120, blank=True, default='')
    # Category / significance / nature (evaluated by the MR)
    category = models.CharField(max_length=8, choices=CATEGORIES, default='major')
    category_also_critical = models.BooleanField(default=False)
    sig_legal = models.BooleanField(default=False)
    sig_risk = models.BooleanField(default=False)
    sig_halt = models.BooleanField(default=False)
    sig_preventive = models.BooleanField(default=False)
    sig_non_significant = models.BooleanField(default=False)
    priority = models.CharField(max_length=6, choices=LEVELS, default='medium')
    risk_type = models.CharField(max_length=6, choices=LEVELS, default='medium')
    severity = models.CharField(max_length=6, choices=LEVELS, default='medium')
    impact_past = models.BooleanField(default=False)
    evaluated_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    evaluated_at = models.DateTimeField(null=True, blank=True)
    evaluated_date = models.DateField(null=True, blank=True)
    details = models.TextField(blank=True, default='')
    proposed_date = models.DateField(null=True, blank=True)
    mr_signed_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    mr_signed_at = models.DateTimeField(null=True, blank=True)
    # Concerned department section
    root_cause = models.TextField(blank=True, default='')
    corrective = models.TextField(blank=True, default='')
    completion_date = models.DateField(null=True, blank=True)
    hod_signed_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    hod_signed_at = models.DateTimeField(null=True, blank=True)
    # MR section
    followup_with = models.CharField(max_length=120, blank=True, default='')
    satisfactory = models.BooleanField(null=True, blank=True)
    followup_date = models.DateField(null=True, blank=True)
    next_followup_date = models.DateField(null=True, blank=True)
    followup_desc = models.TextField(blank=True, default='')
    closed_by_name = models.CharField(max_length=120, blank=True, default='')
    closed_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    closed_at = models.DateTimeField(null=True, blank=True)
    closing_date = models.DateField(null=True, blank=True)
    remarks = models.CharField(max_length=300, blank=True, default='')
    # NC&CA log columns
    log_sno = models.PositiveIntegerField(null=True, blank=True)
    assigned_to = models.CharField(max_length=120, blank=True, default='')
    assigned_date = models.DateField(null=True, blank=True)
    target_date = models.DateField(null=True, blank=True)
    log_only = models.BooleanField(default=False)          # row in the log without a form in the record
    status = models.CharField(max_length=10, choices=STATUSES, default='draft')
    legacy = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-id']
        unique_together = ('location', 'nc_no')

    @property
    def inducted(self):
        """True for a record inducted from the laboratory's paper / Word record (legacy.key is set by the import)."""
        return bool((self.legacy or {}).get('key') or (self.legacy or {}).get('inducted'))

    def __str__(self):
        return '%s (%s)' % (self.nc_no, self.location)

    @property
    def locked(self):
        return self.status == 'closed'

    @property
    def is_nc(self):
        return self.category in ('minor', 'major', 'critical')

    @property
    def rca_list(self):
        """All root cause analyses of this NC&CA (one per root cause: a, b, c ...), in order. Uses a prefetch if present."""
        return sorted(self.rcas.all(), key=lambda r: (r.part or '', r.id or 0))

    @property
    def rca(self):
        """The first RCA (most NC&CAs have exactly one) - kept for the pages and PDFs written for one RCA."""
        rows = self.rca_list
        return rows[0] if rows else None

    @property
    def verified(self):
        """Sign-off that this inducted record matches the signed paper form: {'by', 'user', 'at'} or None (26-10-2026)."""
        return (self.legacy or {}).get('verified') or None

    LOG_ONLY_TEXT = 'Entry of the NC&CA log (ETAL-QMS-710-FF-02); the NC&CA form is not in the inducted record.'

    @property
    def form_gaps(self):
        """Sections of an inducted NC&CA form that were not in the record supplied for induction (complaint 26-10-2026:
        the forms 'looked empty'). Empty list = nothing missing, or not an inducted record."""
        if not self.inducted:
            return []
        gaps = []
        if self.log_only or not (self.details or '').strip() or (self.details or '').strip() == self.LOG_ONLY_TEXT:
            gaps.append('non-conformity details')
        if not (self.root_cause or '').strip():
            gaps.append('root cause')
        if not (self.corrective or '').strip():
            gaps.append('corrective action')
        if not self.completion_date:
            gaps.append('completion date')
        if self.satisfactory is None and not (self.followup_desc or '').strip():
            gaps.append('MR follow-up')
        blank = set((self.legacy or {}).get('blank_on_form') or [])     # left blank on the signed paper form itself: not a gap of the software
        return [g for g in gaps if g not in blank]


class NccaRca(models.Model):
    """Root Cause Analysis (ETAL-QMS-710-FF-01A): potential causes ticked, 6-Why chain, conclusion;
    performed by the person deputed (MR), reviewed by the CEO."""
    MAIN_CAUSES = (('Personnel', ['Training Needed', 'Skill Improvement', 'Random Error', 'Behavior or Attitude Issue', 'Stress/ Over Load']),
                   ('Method/ Procedure', ['Procedure needed', 'In-adequate', 'Improvement needed', 'Inappropriate', 'Too Lengthy', 'Complicated']),
                   ('Environmental Conditions', ['In-adequate', 'Improvement needed', 'Inappropriate', 'Required Conditions not met', 'Un-realistic']),
                   ('Management System', ['Policy not available', 'Improvement needed', 'Inappropriate', 'Complicated', 'Un-realistic']),
                   ('QSP', ['Quality System Procedure not available', 'Improvement needed', 'Inappropriate', 'Complicated', 'Un-realistic']),
                   ('Material', ['Required material not available', 'Improvement needed', 'Inappropriate', 'Poor Quality', 'Storage Conditions']),
                   ('Equipment', ['Required material not available', 'Improvement needed', 'Inappropriate', 'Not Calibrated', 'Poor Handling / Transportation']))
    STATUSES = (('draft', 'Draft'), ('performed', 'Performed - awaiting CEO review'), ('reviewed', 'Reviewed by CEO'))
    nc = models.ForeignKey(Ncca, on_delete=models.CASCADE, related_name='rcas')
    part = models.CharField(max_length=4, blank=True, default='')   # a / b / c when one NC&CA carries several root causes (26-10-2026)
    rca_no = models.CharField(max_length=40, blank=True, default='')
    clause = models.CharField(max_length=60, blank=True, default='')
    deputed = models.CharField(max_length=120, blank=True, default='')
    date = models.DateField(null=True, blank=True)
    causes = models.JSONField(default=dict, blank=True)     # {'Personnel': ['Random Error'], ...}; 'other' keys per main cause as '<main>:other'
    other = models.CharField(max_length=300, blank=True, default='')
    six_why = models.BooleanField(default=True)
    statement = models.TextField(blank=True, default='')
    whys = models.JSONField(default=list, blank=True)       # six strings
    conclusion = models.TextField(blank=True, default='')
    performed_name = models.CharField(max_length=120, blank=True, default='')
    performed_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    performed_at = models.DateTimeField(null=True, blank=True)
    performed_date = models.DateField(null=True, blank=True)
    reviewed_name = models.CharField(max_length=120, blank=True, default='')
    reviewed_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUSES, default='draft')
    legacy = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def inducted(self):
        """True for a record inducted from the laboratory's paper / Word record (legacy.key is set by the import)."""
        return bool((self.legacy or {}).get('key') or (self.legacy or {}).get('inducted'))

    class Meta:
        ordering = ['part', 'id']

    def __str__(self):
        return 'RCA %s of %s' % (self.rca_no, self.nc_id)

    @property
    def locked(self):
        return self.status == 'reviewed'


for _m in (IaClause, IaPlan, IaAudit, IaFinding, IaCircular, IaWitness, Ncca, NccaRca):
    _sh_register(_m)


# ================================================================ Management Review (ISO/IEC 17025:2017 clause 8.9)
# Owner request 23-10-2026: Management Records - MRM. Forms of the procedure ETAL-QMS-P-809:
#   809-FF-01 Circular of the Management Review Meeting (agenda, distribution, receiving attendance)
#   809-FF-02 Minutes of the Management Review Meeting (participants, roles, agenda items with inputs, outputs /
#             decisions, resources, responsibility and target date; addendum)
#   809-FF-03 Management Review (Meeting) Plan of the year (departments x months, Due / Done)
#   809-FF-04 MRM Checklist (every input of clause 8.9.2 discussed, referenced or justified)
MRM_INPUTS = [   # ISO/IEC 17025:2017 8.9.2 a) - o) as on the laboratory's checklist (ETAL-QMS-809-FF-04)
    ('8.9.2 a)', 'Changes in internal and external issues that are relevant to the laboratory'),
    ('8.9.2 b)', 'Fulfilment of objectives'),
    ('8.9.2 c)', 'Suitability of policies and procedures'),
    ('8.9.2 d)', 'Status of actions from previous management reviews'),
    ('8.9.2 e)', 'Outcomes of recent internal audits'),
    ('8.9.2 f)', 'Corrective actions'),
    ('8.9.2 g)', 'Assessments by external bodies'),
    ('8.9.2 h)', 'Changes in the volume and type of work or in the range of laboratory activities'),
    ('8.9.2 i)', 'Customer and Personnel feedback'),
    ('8.9.2 j)', 'Complaints'),
    ('8.9.2 k)', 'Effectiveness of any implemented improvements'),
    ('8.9.2 l)', 'Adequacy of Resources'),
    ('8.9.2 m)', 'Results of Risk Identification'),
    ('8.9.2 n)', 'Outcomes of the Assurance of the validity of results'),
    ('8.9.2 o)', 'Other relevant factors (e.g., monitoring activities and training)'),
]


class MrmPlan(models.Model):
    """Management Review Plan of the year (ETAL-QMS-809-FF-03): departments x months, Due / Done.
    Prepared and signed by the Management Representative, approved by the CEO."""
    STATUSES = (('draft', 'Draft'), ('signed', 'Signed by MR - awaiting CEO'), ('approved', 'Approved'))
    location = models.CharField(max_length=20, default='Karachi')
    year = models.PositiveIntegerField()
    rows = models.JSONField(default=list, blank=True)      # [{'department': str, 'months': {'3': {'due': True, 'done': False}}}]
    remarks = models.TextField(blank=True, default='')
    status = models.CharField(max_length=10, choices=STATUSES, default='draft')
    mr_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    mr_at = models.DateTimeField(null=True, blank=True)
    mr_name = models.CharField(max_length=120, blank=True, default='')
    mr_date = models.DateField(null=True, blank=True)
    ceo_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    ceo_at = models.DateTimeField(null=True, blank=True)
    ceo_name = models.CharField(max_length=120, blank=True, default='')
    ceo_date = models.DateField(null=True, blank=True)
    legacy = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-year', 'location']
        unique_together = ('location', 'year')

    @property
    def inducted(self):
        return bool((self.legacy or {}).get('key') or (self.legacy or {}).get('inducted'))

    @property
    def locked(self):
        return self.status == 'approved'

    def __str__(self):
        return 'Management Review Plan %d - %s' % (self.year, self.location)


class MrmMeeting(models.Model):
    """One Management Review Meeting with its circular (809-FF-01), checklist (809-FF-04) and minutes (809-FF-02).
    The circular is issued by the CEO and receipt is signed by each person listed; the minutes are prepared and signed
    by the MR and approved by the CEO (then locked)."""
    STATUSES = (('draft', 'Draft'), ('prepared', 'Prepared (MR signed) - awaiting CEO'), ('approved', 'Approved by CEO'))
    CIRC_STATUSES = (('draft', 'Draft'), ('issued', 'Issued'))
    location = models.CharField(max_length=20, default='Karachi')
    meeting_no = models.CharField(max_length=20)                     # 01/2026
    year = models.PositiveIntegerField()
    seq = models.PositiveSmallIntegerField(default=1)
    meeting_date = models.DateField(null=True, blank=True)
    time_text = models.CharField(max_length=80, blank=True, default='')
    venue = models.CharField(max_length=200, blank=True, default='')
    review_type = models.CharField(max_length=120, blank=True, default='Regular (ISO/IEC 17025:2017)')
    subject = models.CharField(max_length=200, blank=True, default='Management Review Meeting')
    # circular (809-FF-01)
    circular_date = models.DateField(null=True, blank=True)
    circular_intro = models.TextField(blank=True, default='')
    agenda = models.JSONField(default=list, blank=True)              # ['Review of Internal Audit Report', ...]
    distribute_to = models.JSONField(default=list, blank=True)       # ['CEO', 'Display on notice board', 'All Employees']
    attendance = models.JSONField(default=list, blank=True)          # [{'name','designation','user_id','signed_at'}]
    circular_status = models.CharField(max_length=8, choices=CIRC_STATUSES, default='draft')
    circular_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    circular_at = models.DateTimeField(null=True, blank=True)
    circular_signer = models.CharField(max_length=120, blank=True, default='')      # printed name (CEO)
    # minutes (809-FF-02)
    participants = models.JSONField(default=list, blank=True)        # [{'name','designation'}]
    chair = models.CharField(max_length=120, blank=True, default='')
    facilitator = models.CharField(max_length=120, blank=True, default='')
    minutes_taker = models.CharField(max_length=120, blank=True, default='')
    documenter = models.CharField(max_length=120, blank=True, default='')
    next_mrm = models.CharField(max_length=60, blank=True, default='')
    distributed_to = models.CharField(max_length=200, blank=True, default='All Participants')
    addendum_date = models.DateField(null=True, blank=True)
    # checklist (809-FF-04)
    checklist = models.JSONField(default=list, blank=True)           # [{'code','item','discussed':'yes'|'no'|'','remarks','justification'}]
    checklist_date = models.DateField(null=True, blank=True)
    # sign-off of the minutes and the checklist
    status = models.CharField(max_length=10, choices=STATUSES, default='draft')
    mr_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    mr_at = models.DateTimeField(null=True, blank=True)
    mr_name = models.CharField(max_length=120, blank=True, default='')
    mr_date = models.DateField(null=True, blank=True)
    ceo_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    ceo_at = models.DateTimeField(null=True, blank=True)
    ceo_name = models.CharField(max_length=120, blank=True, default='')
    ceo_date = models.DateField(null=True, blank=True)
    remarks = models.TextField(blank=True, default='')
    legacy = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-year', '-seq', 'location']
        unique_together = ('location', 'meeting_no')

    @property
    def inducted(self):
        return bool((self.legacy or {}).get('key') or (self.legacy or {}).get('inducted'))

    @property
    def locked(self):
        return self.status == 'approved'

    @property
    def circular_locked(self):
        return self.circular_status == 'issued'

    def __str__(self):
        return 'MRM %s - %s' % (self.meeting_no, self.location)

    def checklist_rows(self):
        """The 15 inputs of 8.9.2 with what was recorded for each."""
        have = {r.get('code'): r for r in (self.checklist or [])}
        return [dict({'code': c, 'item': t, 'discussed': '', 'remarks': '', 'justification': ''}, **have.get(c, {})) for c, t in MRM_INPUTS]

    def checklist_complete(self):
        """Every input discussed / referenced, or justified (the note of the form)."""
        return all(r.get('discussed') == 'yes' or (r.get('justification') or '').strip() for r in self.checklist_rows())


class MrmItem(models.Model):
    """One row of the minutes (or of the addendum): agenda, inputs / details of discussion, outputs / decision &
    direction, resources needed, responsibility and target date. A row with a responsibility and a target is an
    action, followed up until done (8.9.2 d - status of actions from previous management reviews)."""
    PARTS = (('minutes', 'Minutes'), ('addendum', 'Addendum'))
    ACTION = (('', 'Not an action'), ('open', 'Open'), ('done', 'Done'), ('na', 'Not applicable'))
    meeting = models.ForeignKey(MrmMeeting, on_delete=models.CASCADE, related_name='items')
    part = models.CharField(max_length=10, choices=PARTS, default='minutes')
    order = models.PositiveIntegerField(default=0)
    sno = models.CharField(max_length=12, blank=True, default='')
    clause = models.CharField(max_length=12, blank=True, default='')            # 8.9.2 x)
    agenda = models.TextField(blank=True, default='')
    inputs = models.TextField(blank=True, default='')
    outputs = models.TextField(blank=True, default='')
    resources = models.TextField(blank=True, default='')
    responsibility = models.TextField(blank=True, default='')
    target_text = models.CharField(max_length=60, blank=True, default='')      # as printed (12.03.2026, July 2025, Continuous, N.A)
    target_date = models.DateField(null=True, blank=True)
    action_status = models.CharField(max_length=6, choices=ACTION, blank=True, default='')
    done_note = models.CharField(max_length=500, blank=True, default='')
    done_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    done_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['part', 'order', 'id']

    def __str__(self):
        return '%s %s %s' % (self.meeting, self.sno, (self.agenda or self.inputs)[:40])


for _m in (MrmPlan, MrmMeeting, MrmItem):
    _sh_register(_m)
