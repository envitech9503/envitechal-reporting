"""RDS PDF - only the results and their own calculations are printed (owner 30-10-2026, zero-error check of the RDS).

prune(data, kind)   applied to the saved RDS before the DW / WW raw data sheet is drawn, for old and new records alike:
  1. a row of the results table without a parameter or without a result (blank, "-", "N/A") is not printed;
  2. a calculation is printed only when its parameter is in the printed results table: the fields of each calculation
     section belong to the parameter(s) that reveal the section on the Add page (QC/rds_field_owners.json, generated
     from the pages); the fields of the other sections are left out. A field the map does not know is kept;
  3. a formula-library card or a quality-control check is printed only when its parameter is in the table.
The reported name is matched to the page's name as the page itself does it (static/js/rds_formula_lib.js pageName).
"""
import json
import os
import re
from functools import lru_cache

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMPTY = {'', '-', '--', '---', 'n/a', 'na', 'n.a', 'n.a.', 'none', 'null', 'nan'}
GENERIC = {'total', 'dissolved', 'solids', 'free', 'caco3', 'compounds', 'residual', 'count', 'water', 'calculation',
           'calculations', 'reading', 'readings', 'average', 'standard', 'working'}
RESULT_FIELDS = ('result_', 'inlet_', 'outlet_')

SYN = {
    'electrical conductivity': 'conductivity', 'ec': 'conductivity', 'dissolved oxygen': 'do', 'oxygen dissolved': 'do',
    'e.coli': 'e.coli', 'e. coli': 'e.coli', 'e coli': 'e.coli', 'e-coli': 'e.coli', 'e - coli': 'e.coli', 'escherichia coli': 'e.coli',
    'total coliform': 'coliform', 'total coliforms': 'coliform', 'coliforms': 'coliform', 'fecal coliform': 'faecal coliform',
    'faecal coliforms': 'faecal coliform', 'feacal coliform': 'faecal coliform', 'sulfate': 'sulphate', 'tss': 'total suspended solids',
    'tds': 'total dissolved solids', 'total dissolved solids': 'tds', 'total bacterial count': 'total bacterial count',
    'phenolic compounds as phenols': ['phenolic compounds', 'phenol'], 'phenolic compounds': ['phenolic compounds', 'phenol'],
    'phenol': 'phenolic compounds', 'phenols': ['phenolic compounds', 'phenol'],
    'total hardness as caco3': 'total hardness', 'total alkalinity': 'alkalinity', 'alkalinity as caco3': 'alkalinity',
    'mbas': 'an ionic detergent as mbas', 'anionic surfactants as mbas': 'an-ionic surfactants as mbas',
    'oil grease': 'oil & grease', 'oil and grease': 'oil & grease', 'chemical oxygen demand': 'cod', 'cod': 'chemical oxygen demand',
    'nitrate no3': 'nitrate', 'total chromium': 'chromium', 'aluminum': 'aluminium', 'heterotrophic plate count': 'heterotrophic bacteria',
    'hpc': 'heterotrophic bacteria', 'fecal enterococci': 'fecal enterococci', 'faecal enterococci': 'fecal enterococci',
    'tbc': 'total bacterial count', 'tpc': 'total bacterial count', 'total plate count': 'total bacterial count',   # R11.1
    'total viable count': 'total bacterial count', 'total coliforms': 'coliform', 'faecal coliform': 'faecal coliform', 'fecal coliforms': 'faecal coliform',
    'ph @ 25°c': 'ph', 'ph @ 20°c': 'ph', 'colour': 'color', 'true colour': 'color', 'apparent colour': 'color',
}


def norm(s):
    s = str(s or '').lower().replace('*', '').replace('₃', '3').replace('₂', '2')
    s = re.sub('[⁺²⁻]', '', s)
    s = re.sub(r'\)\s*-\s*2\b', ')', s)
    s = re.sub(r'\s+', ' ', s)
    s = re.sub(r'\s*\(\s*', ' (', s)
    s = re.sub(r'\s*\)\s*', ') ', s)
    return s.strip()


def bare(s):
    return re.sub(r'[^a-z0-9.+&]+', ' ', re.sub(r'\([^)]*\)', '', norm(s))).strip()


def words(s):
    return {w for w in re.split(r'[^a-z0-9]+', bare(s) + ' ' + norm(s)) if len(w) >= 4 and w not in GENERIC}


@lru_cache(maxsize=4)
def _owners(kind):
    try:
        with open(os.path.join(BASE, 'QC', 'rds_field_owners.json'), encoding='utf-8') as fh:
            return json.load(fh).get(kind) or {}
    except (OSError, ValueError):
        return {}


@lru_cache(maxsize=4)
def _known(kind):
    """reported-name keys -> page name, from the page names in the field map (the page's params.includes names)."""
    k = {}
    pages = set()
    for owners in _owners(kind).values():
        pages.update(owners)
    for _rx, names in STEM_PAGES:                     # sections the map holds no field of (R11.1)
        pages.update(names)
    for name in sorted(pages):
        for key in (norm(name), bare(name)):
            if key and key not in k:
                k[key] = name
        m = re.search(r'\(([^)]*)\)', norm(name))
        if m and m.group(1).strip() not in k:
            k[m.group(1).strip()] = name
    return k


def page_name(kind, reported):
    K = _known(kind)
    n, b = norm(reported), bare(reported)
    if n in K:
        return K[n]
    if b in K:
        return K[b]
    syn = SYN.get(b) or SYN.get(n)
    for t in (syn if isinstance(syn, list) else [syn] if syn else []):
        if t in K:
            return K[t]
        if bare(t) in K:
            return K[bare(t)]
    b2 = re.sub(r' as phenols?$', '', re.sub(r' as caco3$', '', b))
    if b2 in K:
        return K[b2]
    if re.search(r'colony counts?|viable count|plate count|bacterial count|\bcfu\b', b):   # R11.1: plate counts (22 / 37 °C)
        return K.get('heterotrophic bacteria') or K.get('total bacterial count')
    return None


# Sections whose fields the Add-page map does not hold (microbiology; carbonates are kept, their working also serves
# bicarbonate / carbonate hardness rows) and older spellings of saved records
# (R11.1, production check 30-10-2026): the key's stem names its parameter.
STEM_PAGES = [
    (r'^(for_)?total_?coliform', ['Coliform']),
    (r'^(for_)?fecalentero', ['Fecal Enterococci']),
    (r'^(for_)?hetro|^(for_)?hetero', ['Heterotrophic Bacteria', 'Total Bacterial Count']),   # plate counts: one family
    (r'^(for_)?enterobact', ['Enterobacteriaceae']),
    (r'^(for_)?ecoli|^(for_)?e_coli', ['E.coli']),
    (r'^(for_)?fa?ecal', ['Faecal coliform']),
    (r'^(for_)?bacteria', ['Total Bacterial Count', 'Heterotrophic Bacteria']),
    (r'^(for_)?coliform', ['Coliform']),
]


def _stem(key):
    k = re.sub(r'^for\d*_', '', str(key).lower())
    m = re.match(r'[a-z]+', k)
    return m.group(0) if m else ''


@lru_cache(maxsize=4096)
def infer_owners(kind, key):
    """Owners of a field the map does not hold: by the explicit stems above, else by its stem when exactly one page
    parameter starts with it (an older spelling, e.g. "for_berylium1_1" -> Beryllium); () when unclear (kept)."""
    lk = str(key).lower()
    for rx, pages in STEM_PAGES:
        if re.match(rx, lk):
            return tuple(pages)
    st = _stem(key)
    if len(st) < 5 or st in GENERIC or st in ('final', 'reading', 'sample', 'blank', 'head', 'param', 'divi', 'equal', 'ans'):
        return ()
    groups = {}
    for name in set(n for o in _owners(kind).values() for n in o):
        for w in re.split(r'[^a-z0-9]+', bare(name)):
            if len(w) >= 5 and w not in GENERIC and (w.startswith(st[:5]) or st.startswith(w[:5])):
                groups.setdefault(bare(name).replace(' ', ''), set()).add(name)
    if len(groups) == 1:
        return tuple(sorted(next(iter(groups.values()))))
    return ()


def _blank(v):
    return str(v if v is not None else '').strip().lower() in EMPTY


def row_keys(data):
    return [k[5:] for k, v in data.items() if k.startswith('date_') and v]


def printed_row(data, rk):
    if _blank(data.get('parameter_' + rk)):
        return False
    return any(not _blank(data.get(p + rk)) for p in RESULT_FIELDS)


class Present:
    """The parameters of the printed results table, as page names and as words (a name the page does not know)."""
    def __init__(self, kind, names):
        self.kind = kind
        self.names = [n for n in names if str(n).strip()]
        self.pages = {page_name(kind, n) for n in self.names} - {None}
        self.norms = {norm(n) for n in self.names} | {bare(n) for n in self.names}
        self.loose = set()
        for n in self.names:
            if page_name(kind, n) is None:
                self.loose |= words(n)                 # unknown name: keep what shares a word with it (never drop by doubt)
        self.roww = [words(n) for n in self.names]

    def owns(self, owners):
        if any(o in self.pages for o in owners):
            return True
        return bool(self.loose) and any(words(o) & self.loose for o in owners)

    def __call__(self, name):                          # a library card / QC check parameter
        if not str(name or '').strip():
            return False
        if norm(name) in self.norms or bare(name) in self.norms:
            return True
        pn = page_name(self.kind, name)
        if pn is not None and pn in self.pages:
            return True
        return self.close(name)                          # otherwise by its words

    def close(self, name):
        """A row whose name is the same words (at least 60 % shared): "Biological Oxygen Demand (BOD5)" and
        "Biological Oxygen Demand(BOD)5", not "Chemical Oxygen Demand"."""
        w = words(name)
        return bool(w) and any(r and len(w & r) / len(w | r) >= 0.6 for r in self.roww)


def prune(data, kind):
    """A copy of the saved RDS holding only the printed rows and the calculations of their parameters."""
    out = dict(data or {})
    rows = row_keys(out)
    kept = []
    for rk in rows:
        if printed_row(out, rk):
            kept.append(rk)
        else:
            out.pop('date_' + rk, None)                  # the row is not drawn
    present = Present(kind, [out.get('parameter_' + rk) for rk in kept])
    owners = _owners(kind)
    if owners:
        for key in list(out):
            o = owners.get(key) or (infer_owners(kind, key) if not re.match(r'^(date|parameter|result|inlet|outlet|performed_by|checked_by|performed|checked|remarks)_|^(lib_print|qc_print)_|^(sample_id|report_type)$', key) else ())
            if o and not present.owns(o):
                out.pop(key, None)
    for key in list(out):
        if key.startswith('lib_print_') or key.startswith('qc_print_'):
            try:
                c = json.loads(out[key] or '{}')
            except (TypeError, ValueError):
                continue
            if isinstance(c, dict) and (not present(c.get('parameter')) or (key.startswith('lib_print_') and not str(c.get('result') or '').strip())):
                out.pop(key, None)
    return out
