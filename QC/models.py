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


def classify_value(lim, value):
    """'ok' | 'warning' (outside +/-2 SD) | 'ooc' (outside +/-3 SD)."""
    if lim is None or value is None:
        return 'ok'
    if value > lim['ul'] or value < lim['ll']:
        return 'ooc'
    if value > lim['uwl'] or value < lim['lwl']:
        return 'warning'
    return 'ok'


class ControlChart(models.Model):
    LOCATIONS = (('Karachi', 'Karachi'), ('Lahore', 'Lahore'))
    ACTIVITIES = (('CRM', 'CRM (Certified Reference Material)'),
                  ('RM', 'Reference Material'),
                  ('IC', 'Intermediate Check'),
                  ('DUP', 'Duplicate'),
                  ('SPK', 'Spike / Recovery'))
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
        if self.crm_range_low or self.crm_range_high:
            return '%s-%s' % (self.crm_range_low, self.crm_range_high)
        return ''

    def current_baseline(self):
        return self.baselines.filter(is_current=True).order_by('-version').first()

    # ---- activity-driven behaviour (08-10-2026: RM and Intermediate Check charts)
    @property
    def cadence(self):
        """'monthly' (CRM: 12 month rows per year), 'weekly' (RM: sequential weekly
        results per year) or 'run' (IC: one run of ~12 readings per calendar month,
        limits computed from the run itself)."""
        return {'RM': 'weekly', 'IC': 'run'}.get(self.activity, 'monthly')

    @property
    def self_limited(self):
        return self.activity == 'IC'

    @property
    def period_is_month(self):
        return self.cadence == 'run'

    @property
    def ref_label(self):
        return {'RM': 'RM', 'IC': 'CRM/RM'}.get(self.activity, 'CRM')

    @property
    def result_label(self):
        return {'RM': 'Weekly RM result', 'IC': 'Intermediate check reading'}.get(self.activity, 'Monthly CRM result')

    @property
    def period_col(self):
        return {'RM': 'Week', 'IC': 'Reading'}.get(self.activity, 'Month')

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
        return classify_value(self.limits(), value)

    def __str__(self):
        return 'Baseline v%s of %s' % (self.version, self.chart_id)


class ControlChartResult(models.Model):
    STATUS = (('ok', 'In control'), ('warning', 'Warning (>2 SD)'), ('ooc', 'Out of control (>3 SD)'))
    chart = models.ForeignKey(ControlChart, on_delete=models.CASCADE, related_name='results')
    baseline = models.ForeignKey(ControlChartBaseline, null=True, blank=True,
                                 on_delete=models.SET_NULL, related_name='results')
    date = models.DateField()
    value = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='ok')
    remark = models.TextField(blank=True, default='')       # mandatory when status != ok
    performed_by = models.ForeignKey('auth.User', null=True, blank=True,
                                     on_delete=models.SET_NULL, related_name='+')
    performed_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date', 'id']

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
