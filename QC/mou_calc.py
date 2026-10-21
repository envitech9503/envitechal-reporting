"""Measurement of Uncertainty (MOU) - calculation engine (form ETAL-LAB-706-FF-01). 21-10-2026.

Pure Python, no Django: the same arithmetic is used by the study pages, the PDF, the register
and the legacy induction, and is unit-tested against the laboratory's own workbooks.

The laboratory's model (GUM-based, relative budget - identical in all Karachi workbooks):

  per operator (A, B, C ...):  n, mean, SD = sqrt( sum (x_i - mean)^2 / (n - 1) )
  Type A repeatability         u = (SD_A / range) / sqrt(n_A)              (first operator)
  Type A reproducibility       u = (sqrt(sum SD_i^2) / range) / sqrt(sum n_i)   (operators with data; only when >= 2)
  Type B component             rel = magnitude / range ; u = rel / divisor * ci
                               divisor 1 (normal, k=1), 2 (normal, k=2), sqrt3 (rectangular), sqrt6 (triangular), sqrt2 (U-shaped)
  combined                     uc = sqrt( sum u_i^2 )            (relative)
  expanded                     U  = k * uc                        (relative; k = 2, 95 % confidence)
  absolute                     U_abs = U * grand mean (all replicates of all operators)
  percent                      U_pct = U * 100

"range" is the method / calibration working range the laboratory expresses the component against
(e.g. COD 900, pH 14), entered per study and validated >= the measured mean.
"""
import ast
import math
import operator as _op

K_DEFAULT = 2.0

# distribution key -> (label, divisor)
DISTRIBUTIONS = (
    ('normal', 'Normal (k=1)', 1.0),
    ('normal2', 'Normal (k=2)', 2.0),
    ('rect', 'Rectangular (sqrt3)', math.sqrt(3.0)),
    ('tri', 'Triangular (sqrt6)', math.sqrt(6.0)),
    ('ushape', 'U-shaped (sqrt2)', math.sqrt(2.0)),
)
DIST_LABEL = {k: lbl for k, lbl, _ in DISTRIBUTIONS}
DIST_DIV = {k: d for k, _, d in DISTRIBUTIONS}
DIST_PRINT = {'normal': 'Normal (k=1)', 'normal2': 'Normal (k=2)', 'rect': 'Rectangular', 'tri': 'Triangular', 'ushape': 'U-shaped'}
DIST_DIV_TXT = {'normal': '1', 'normal2': '2', 'rect': '√3', 'tri': '√6', 'ushape': '√2'}

KIND_REPEAT, KIND_REPRO, KIND_B = 'a_rep', 'a_repro', 'b'


def dist_key(text):
    """Map a distribution as written in the workbooks ('Normal (k=1)', 'Triangular', 'Rectangular',
    blank) to a key. Blank / unknown -> None (the caller decides; the workbooks default to sqrt6)."""
    t = (text or '').strip().lower().replace(' ', '').replace('\n', '')
    if not t:
        return None
    if t in DIST_DIV:
        return t
    if t.startswith('normal'):
        return 'normal2' if 'k=2' in t else 'normal'
    if t.startswith('rect'):
        return 'rect'
    if t.startswith('tri'):
        return 'tri'
    if t.startswith('u'):
        return 'ushape'
    return None


# ------------------------------------------------------------------ safe arithmetic expressions
_BIN = {ast.Add: _op.add, ast.Sub: _op.sub, ast.Mult: _op.mul, ast.Div: _op.truediv, ast.Pow: _op.pow}
_UN = {ast.USub: _op.neg, ast.UAdd: _op.pos}
_FUN = {'sqrt': math.sqrt, 'abs': abs}


def eval_expr(text):
    """Evaluate a magnitude expression such as '0.080/2', '0.1/sqrt(3)', '1.2e-3'. Numbers pass
    through; anything that is not plain arithmetic raises ValueError. Returns float."""
    if text is None:
        raise ValueError('empty')
    if isinstance(text, (int, float)):
        return float(text)
    s = str(text).strip().replace('√', 'sqrt').replace('^', '**').replace(',', '')
    if not s:
        raise ValueError('empty')
    try:
        tree = ast.parse(s, mode='eval')
    except SyntaxError:
        raise ValueError('not a number or expression: %r' % text)

    def ev(n):
        if isinstance(n, ast.Expression):
            return ev(n.body)
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)) and not isinstance(n.value, bool):
            return float(n.value)
        if isinstance(n, ast.BinOp) and type(n.op) in _BIN:
            return _BIN[type(n.op)](ev(n.left), ev(n.right))
        if isinstance(n, ast.UnaryOp) and type(n.op) in _UN:
            return _UN[type(n.op)](ev(n.operand))
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in _FUN and len(n.args) == 1 and not n.keywords:
            return _FUN[n.func.id](ev(n.args[0]))
        raise ValueError('not a number or expression: %r' % text)
    v = ev(tree)
    if isinstance(v, complex) or math.isnan(v) or math.isinf(v):
        raise ValueError('not a finite number: %r' % text)
    return float(v)


# ------------------------------------------------------------------ statistics
def clean_values(values):
    """Replicates as floats; blanks / None / '' are dropped (a blank cell is 'not measured', never 0)."""
    out = []
    for v in values or []:
        if v is None or (isinstance(v, str) and not v.strip()):
            continue
        out.append(float(v))
    return out


def stats(values):
    """n, mean, SD (sample, n-1) of the replicates; SD is None when n < 2."""
    xs = clean_values(values)
    n = len(xs)
    if n == 0:
        return {'n': 0, 'mean': None, 'sd': None, 'ss': None}
    mean = sum(xs) / n
    ss = sum((x - mean) ** 2 for x in xs)
    sd = math.sqrt(ss / (n - 1)) if n > 1 else None
    return {'n': n, 'mean': mean, 'sd': sd, 'ss': ss}


def type_a_repeat(sd, rng, n):
    return (sd / rng) / math.sqrt(n)


def type_a_repro(sds, rng, n_total):
    return (math.sqrt(sum(s * s for s in sds)) / rng) / math.sqrt(n_total)


def type_b(magnitude, rng, dist, ci=1.0):
    rel = magnitude / rng
    return rel, rel / DIST_DIV[dist] * ci


# ------------------------------------------------------------------ whole budget
def compute(study):
    """study: {'range': float, 'k': float, 'operators': [{'label','values'}], 'components': [
        {'kind': 'a_rep'|'a_repro'|'b', 'name', 'unit', 'range' (Type B, defaults to study range),
         'magnitude' (number or expression; Type B), 'dist', 'ci', 'included': True}],
      'measured': optional float - value the % uncertainty is expressed against (default grand mean)}
    Returns {'operators': [...], 'grand': {...}, 'components': [...], 'uc', 'U', 'U_abs', 'U_pct', 'k', 'warnings': [...], 'errors': [...]}.
    Errors stop the calculation (uc etc. are None); warnings do not."""
    errors, warnings = [], []
    k = float(study.get('k') or K_DEFAULT)
    try:
        rng = float(study.get('range') or 0)
    except (TypeError, ValueError):
        rng = 0.0
    if rng <= 0:
        errors.append('The range (x) must be a positive number.')

    ops = []
    for i, o in enumerate(study.get('operators') or []):
        st = stats(o.get('values'))
        st['label'] = o.get('label') or chr(65 + i)
        st['values'] = clean_values(o.get('values'))
        ops.append(st)
    with_data = [o for o in ops if o['n'] > 0]
    allv = [v for o in with_data for v in o['values']]
    grand = stats(allv)
    if not with_data:
        errors.append('No replicate values have been entered.')
    elif with_data[0]['n'] < 2:
        errors.append('Operator %s needs at least 2 replicates for a standard deviation.' % with_data[0]['label'])
    for o in with_data:
        if o['n'] < 2:
            warnings.append('Operator %s has a single value; it is counted in the mean but has no standard deviation.' % o['label'])
    if rng > 0 and grand['mean'] is not None and grand['mean'] > rng:
        warnings.append('The measured mean (%.4g) exceeds the range (%.4g): relative factors above 1 - check the range basis.' % (grand['mean'], rng))

    comps, u_sq = [], 0.0
    sds = [o['sd'] for o in with_data if o['sd'] is not None]
    n_tot = sum(o['n'] for o in with_data if o['sd'] is not None)
    seen_rep = seen_repro = False
    for c in study.get('components') or []:
        row = {'kind': c.get('kind'), 'name': c.get('name') or '', 'unit': c.get('unit') or '', 'ci': 1.0,
               'included': c.get('included', True), 'range': None, 'magnitude': None, 'rel': None, 'u': None,
               'dist': c.get('dist') or 'normal', 'divisor': None, 'note': ''}
        try:
            row['ci'] = float(c.get('ci') if c.get('ci') not in (None, '') else 1.0)
        except (TypeError, ValueError):
            errors.append('Sensitivity coefficient of "%s" is not a number.' % row['name'])
        if row['kind'] == KIND_REPEAT:
            seen_rep = True
            row['range'] = rng
            row['dist'], row['divisor'] = 'normal', 'sqrt(n)'
            if with_data and with_data[0]['sd'] is not None and rng > 0:
                o = with_data[0]
                row['magnitude'] = o['sd']
                row['rel'] = o['sd'] / rng
                row['u'] = type_a_repeat(o['sd'], rng, o['n']) * row['ci']
                row['note'] = 'SD of operator %s / x / sqrt(%d)' % (o['label'], o['n'])
        elif row['kind'] == KIND_REPRO:
            seen_repro = True
            row['range'] = rng
            row['dist'], row['divisor'] = 'normal', 'sqrt(sum n)'
            if len(sds) >= 2 and rng > 0:
                row['magnitude'] = math.sqrt(sum(s * s for s in sds))
                row['rel'] = row['magnitude'] / rng
                row['u'] = type_a_repro(sds, rng, n_tot) * row['ci']
                row['note'] = 'sqrt(sum SD^2) / x / sqrt(%d)' % n_tot
            else:
                row['included'] = False
                row['note'] = 'single operator - no reproducibility term'
        else:
            row['kind'] = KIND_B
            if row['dist'] not in DIST_DIV:
                errors.append('Distribution of "%s" is not set.' % row['name'])
                row['dist'] = 'normal'
            row['divisor'] = DIST_DIV_TXT[row['dist']]
            try:
                crng = c.get('range')
                crng = float(crng) if crng not in (None, '') else rng
                if crng <= 0:
                    raise ValueError
                row['range'] = crng
            except (TypeError, ValueError):
                errors.append('Range of "%s" must be a positive number.' % row['name'])
            try:
                row['magnitude'] = eval_expr(c.get('magnitude'))
                if row['magnitude'] < 0:
                    errors.append('Magnitude of "%s" is negative.' % row['name'])
            except ValueError:
                errors.append('Magnitude of "%s" is not a number or expression (e.g. 0.08/2).' % row['name'])
            if row['range'] and row['magnitude'] is not None:
                row['rel'], row['u'] = type_b(row['magnitude'], row['range'], row['dist'], row['ci'])
        if row['included'] and row['u'] is not None:
            u_sq += row['u'] ** 2
        comps.append(row)
    if not seen_rep:
        errors.append('The Type A repeatability row is missing.')
    if not any(r['kind'] == KIND_B and r['included'] and r['u'] is not None for r in comps):
        warnings.append('No Type B component is included in the budget.')

    out = {'operators': ops, 'grand': grand, 'components': comps, 'k': k, 'range': rng,
           'uc': None, 'U': None, 'U_abs': None, 'U_pct': None, 'measured': None, 'warnings': warnings, 'errors': errors}
    if errors:
        return out
    uc = math.sqrt(u_sq)
    U = k * uc
    measured = study.get('measured')
    measured = float(measured) if measured not in (None, '') else grand['mean']
    out.update(uc=uc, U=U, U_abs=U * grand['mean'], U_pct=U * 100.0, measured=measured,
               U_abs_measured=U * measured, U_pct_measured=(U * measured / measured * 100.0) if measured else None)
    return out


def fmt_sig(v, sig=4):
    """Format for the forms: 4 significant figures, no exponent for ordinary magnitudes."""
    if v is None:
        return '-'
    if v == 0:
        return '0'
    try:
        d = sig - int(math.floor(math.log10(abs(v)))) - 1
        d = max(0, min(d, 10))
        s = ('%.' + str(d) + 'f') % v
        if '.' in s:
            s = s.rstrip('0').rstrip('.')
        return s
    except (ValueError, OverflowError):
        return str(v)


def fmt_fix(v, dp=3):
    if v is None:
        return '-'
    return ('%.' + str(dp) + 'f') % v
