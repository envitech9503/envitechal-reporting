/* RDS formula library - DW and WW, Karachi and Lahore (owner decision 27-10-2026: standard method equations, method
 * default acceptance limits; pesticides, PAH / VOC and alpha / beta emitters are subcontracted - no RDS card).
 *
 * 1. Names: a parameter reported under another name ("Calcium (Ca)", "E. Coli", "Electrical Conductivity", "TSS",
 *    "Total Hardness as CaCO₃" ...) is mapped to the page's own calculation section, whose names are read from the
 *    page's code, so the existing formulae appear; the RDS table keeps the name as reported.
 * 2. Library: every parameter of the sample that still has no section gets a formula card for its method (the
 *    method on the report when the report carries one). Each card computes, checks and stores its working in a
 *    hidden field lib_print_<n> (JSON) that the RDS PDF prints under "Calculations (formula library)".
 * 3. Manual-entry pages and any sample: "Add calculation" adds a card for any library formula.
 *
 * Equations (APHA 23rd ed. unless stated):
 *   Alkalinity 2320 B / ASTM D1067:  P or T (mg/L CaCO3) = A x N x 50 000 / V;  OH, CO3, HCO3 from P and T (2320 B table)
 *   Hardness 2340 C / ASTM D1126, Ca hardness 3500-Ca B: mg CaCO3/L = A x B x 1000 / V;  Ca mg/L = A x B x 400.8 / V
 *   Mg hardness = TH - CaH (Mg mg/L = MgH x 0.2431);  carbonate (temporary) = min(TH, T alk.);  non-carbonate = TH - carbonate
 *   Free CO2 4500-CO2 C: A x N x 44 000 / V;  DPD 4500-Cl G: combined = total - free
 *   Solids 2540 B/D, MLSS, oil & grease (USEPA 1664): (final - initial) g x 10^6 / V mL;  VSS / MLVSS 2540 E: (A - C) x 10^6 / V
 *   Instrumental (reading x dilution factor, replicates averaged; check standard recovery)
 *   SAR = Na / sqrt((Ca + Mg) / 2), RSC = (CO3 + HCO3) - (Ca + Mg)  [meq/L];  LSI = pH - pHs (2330);  salinity PSS-78 (2520 B)
 *   Resistivity = 10^6 / EC;  membrane filtration CFU/100 mL = colonies x 100 x DF / V;  plate count CFU/mL = colonies x DF / V
 *   SDI (ASTM D4189) = (1 - t1/t2) x 100 / T;  BOD 5210 B with seed correction (B1 - B2) / Vc x Vs
 * Checks: replicate spread <= 10 %, check standard 90-110 %, calculated vs reported > 5 % flagged (method defaults).
 */
(function () {
  'use strict';
  var PAGE = /create_ww_qc/.test(location.pathname) ? 'ww' : 'dw';
  var MANUAL = /_manual/.test(location.pathname);
  var TOL_REPORT = 0.05, TOL_REP = 10, REC_LO = 90, REC_HI = 110;

  /* ------------------------------------------------------------------ names */
  function norm(s) {
    return String(s || '').toLowerCase().replace(/\*/g, '').replace(/₃/g, '3').replace(/₂/g, '2').replace(/[⁺²⁻]/g, '')
      .replace(/\)\s*-\s*2\b/g, ')').replace(/\s+/g, ' ').replace(/\s*\(\s*/g, ' (').replace(/\s*\)\s*/g, ') ').trim();
  }
  function bare(s) { return norm(s).replace(/\([^)]*\)/g, '').replace(/[^a-z0-9.+&]+/g, ' ').trim(); }
  var SYN = {          // reported name (bare) -> page name (bare)
    'electrical conductivity': 'conductivity', 'ec': 'conductivity', 'dissolved oxygen': 'do', 'oxygen dissolved': 'do',
    'e.coli': 'e.coli', 'e. coli': 'e.coli', 'e coli': 'e.coli', 'e-coli': 'e.coli', 'e - coli': 'e.coli', 'escherichia coli': 'e.coli',
    'total coliform': 'coliform', 'total coliforms': 'coliform', 'coliforms': 'coliform', 'fecal coliform': 'faecal coliform',
    'faecal coliforms': 'faecal coliform', 'feacal coliform': 'faecal coliform', 'sulfate': 'sulphate', 'tss': 'total suspended solids',
    'tds': 'total dissolved solids', 'total dissolved solids': 'tds', 'total bacterial count': 'total bacterial count',
    'phenolic compounds as phenols': ['phenolic compounds', 'phenol'], 'phenolic compounds': ['phenolic compounds', 'phenol'], 'phenol': 'phenolic compounds', 'phenols': ['phenolic compounds', 'phenol'],
    'total hardness as caco3': 'total hardness', 'total alkalinity': 'alkalinity', 'alkalinity as caco3': 'alkalinity', 'mbas': 'an ionic detergent as mbas', 'anionic surfactants as mbas': 'an-ionic surfactants as mbas',
    'oil grease': 'oil & grease', 'oil and grease': 'oil & grease', 'chemical oxygen demand': 'cod', 'cod': 'chemical oxygen demand',
    'nitrate no3': 'nitrate', 'total chromium': 'chromium', 'aluminum': 'aluminium', 'heterotrophic plate count': 'heterotrophic bacteria',
    'hpc': 'heterotrophic bacteria', 'fecal enterococci': 'fecal enterococci', 'faecal enterococci': 'fecal enterococci', 'ph @ 25°c': 'ph', 'ph @ 20°c': 'ph', 'colour': 'color', 'true colour': 'color', 'apparent colour': 'color'
  };
  var KNOWN = null;
  function known() {
    if (KNOWN) return KNOWN;
    KNOWN = {};
    // first: a section that looks its heading up with qcData.find(item => item.parameter === "X") must receive exactly
    // "X", whichever of its params.includes(...) names the report used (27-10-2026: "Alkalinity" mapped to
    // "Alkalinity*" left find() empty and stopped the page)
    Array.prototype.forEach.call(document.scripts, function (sc) {
      var t = (sc.textContent || '').replace(/^[ \t]*\/\/.*$/gm, ''), re = /if\s*\(((?:\s*\|\|\s*)?(?:params\.includes\("[^"]*"\)(?:\s*\|\|\s*)?)+)\)\s*\{\s*(?:\/\/[^\n]*\s*)*(?:(?:const|let|var)\s+)?[\w.$]+\s*=\s*qcData\.find\(\s*item\s*=>\s*item\.parameter\s*===\s*"([^"]*)"\s*\)/g, m;
      while ((m = re.exec(t))) {
        var target = m[2], names = m[1].match(/"([^"]*)"/g).map(function (q) { return q.slice(1, -1); });
        if (names.indexOf(target) < 0) continue;                    // a section whose look-up names another parameter
        names.concat([target]).forEach(function (name) {
          [norm(name), bare(name)].forEach(function (k) { if (k && !(k in KNOWN)) KNOWN[k] = target; });
        });
      }
    });
    Array.prototype.forEach.call(document.scripts, function (sc) {
      var t = sc.textContent || '', re = /params\.includes\("([^"]*)"\)/g, m;
      while ((m = re.exec(t))) {
        var name = m[1];
        [norm(name), bare(name)].forEach(function (k) { if (k && !(k in KNOWN)) KNOWN[k] = name; });
        var par = norm(name).match(/\(([^)]*)\)/);                 // "Total Suspended Solids (TSS)" also by "tss"
        if (par && !(par[1] in KNOWN)) KNOWN[par[1].trim()] = name;
      }
    });
    return KNOWN;
  }
  function pageName(reported) {
    var K = known(), n = norm(reported), b = bare(reported);
    if (n in K) return K[n];
    if (b in K) return K[b];
    var syn = SYN[b] || SYN[n];
    var list = syn ? (Array.isArray(syn) ? syn : [syn]) : [];
    for (var i = 0; i < list.length; i++) { var t = list[i]; if (t in K) return K[t]; var tb = bare(t); if (tb in K) return K[tb]; }
    var b2 = b.replace(/ as caco3$/, '').replace(/ as phenols?$/, '');
    if (b2 in K) return K[b2];
    return null;
  }

  /* ------------------------------------------------------------------ library definitions */
  function $(id) { return document.getElementById(id); }
  function f(v) { if (v === '' || v === null || v === undefined) return null; var x = parseFloat(v); return isFinite(x) ? x : null; }
  function r(v, dp) { if (v === null || !isFinite(v)) return ''; return String(+v.toFixed(dp === undefined ? 4 : dp)); }
  function avg(a) { return a.reduce(function (s, x) { return s + x; }, 0) / a.length; }
  function spread(a) { if (a.length < 2) return null; var m = avg(a); return m === 0 ? 0 : 100 * (Math.max.apply(null, a) - Math.min.apply(null, a)) / Math.abs(m); }

  var CALC = {
    alk: {
      title: 'Alkalinity titration', method: 'APHA 2320 B / ASTM D1067',
      formula: 'P or T (mg/L as CaCO3) = A x N x 50 000 / V;  OH, CO3, HCO3 from P and T (APHA 2320 B, table 2320:I)',
      inputs: [['v', 'Sample volume V (mL)'], ['n', 'Acid normality N'], ['ap', 'Titrant to pH 8.3, A (mL) - phenolphthalein'], ['at', 'Titrant to pH 4.5, A (mL) - total']],
      run: function (x) {
        if (!x.v || x.n === null || x.at === null) return { err: 'enter V, N and the titrant to pH 4.5' };
        var P = (x.ap || 0) * x.n * 50000 / x.v, T = x.at * x.n * 50000 / x.v, OH = 0, CO3 = 0, HCO3 = 0, e = 1e-9 * Math.max(1, T);
        if (P <= e) { HCO3 = T; } else if (P < T / 2 - e) { CO3 = 2 * P; HCO3 = T - 2 * P; } else if (Math.abs(P - T / 2) <= e) { CO3 = 2 * P; }
        else if (P < T - e) { OH = 2 * P - T; CO3 = 2 * (T - P); } else if (P <= T + e) { OH = T; } else { return { err: 'P alkalinity is greater than total alkalinity - check the titrant volumes' }; }
        return { out: { P: P, T: T, OH: OH, CO3: CO3, HCO3: HCO3, CO3ion: CO3 * 0.6, HCO3ion: HCO3 * 1.22, OHion: OH * 0.34 },
                 lines: ['P = ' + r(x.ap || 0) + ' x ' + r(x.n) + ' x 50000 / ' + r(x.v) + ' = ' + r(P, 2) + ' mg/L as CaCO3',
                         'T = ' + r(x.at) + ' x ' + r(x.n) + ' x 50000 / ' + r(x.v) + ' = ' + r(T, 2) + ' mg/L as CaCO3',
                         'OH = ' + r(OH, 2) + ', CO3 = ' + r(CO3, 2) + ', HCO3 = ' + r(HCO3, 2) + ' mg/L as CaCO3;  as ions: CO3 ' + r(CO3 * 0.6, 2) + ', HCO3 ' + r(HCO3 * 1.22, 2) + ', OH ' + r(OH * 0.34, 2) + ' mg/L'] };
      }
    },
    edta: {
      title: 'EDTA titration', method: 'APHA 2340 C / 3500-Ca B / ASTM D1126',
      formula: 'Hardness (mg/L as CaCO3) = A x B x 1000 / V;  Ca (mg/L) = A x B x 400.8 / V  (B = mg CaCO3 per mL EDTA)',
      inputs: [['v', 'Sample volume V (mL)'], ['a', 'EDTA titrant A (mL)'], ['b', 'B, mg CaCO3 per mL EDTA', '1.0']],
      run: function (x) {
        if (!x.v || x.a === null || x.b === null) return { err: 'enter V, A and B' };
        var H = x.a * x.b * 1000 / x.v, Ca = x.a * x.b * 400.8 / x.v;
        return { out: { H: H, Ca: Ca }, lines: ['Hardness = ' + r(x.a) + ' x ' + r(x.b) + ' x 1000 / ' + r(x.v) + ' = ' + r(H, 2) + ' mg/L as CaCO3', '(as calcium: ' + r(x.a) + ' x ' + r(x.b) + ' x 400.8 / ' + r(x.v) + ' = ' + r(Ca, 2) + ' mg/L Ca)'] };
      }
    },
    mghard: {
      title: 'Magnesium hardness by difference', method: 'APHA 2340 B / 3500-Mg B',
      formula: 'Mg hardness = total hardness - calcium hardness (mg/L as CaCO3);  Mg (mg/L) = Mg hardness x 0.2431',
      inputs: [['th', 'Total hardness (mg/L as CaCO3)'], ['cah', 'Calcium hardness (mg/L as CaCO3)']],
      run: function (x) {
        if (x.th === null || x.cah === null) return { err: 'enter both hardness values' };
        var m = x.th - x.cah;
        return { out: { H: m, Mg: m * 0.2431 }, warn: m < 0 ? ['calcium hardness exceeds total hardness'] : [], lines: ['Mg hardness = ' + r(x.th) + ' - ' + r(x.cah) + ' = ' + r(m, 2) + ' mg/L as CaCO3 (Mg ' + r(m * 0.2431, 2) + ' mg/L)'] };
      }
    },
    carbhard: {
      title: 'Carbonate / non-carbonate hardness', method: 'APHA 2340 B',
      formula: 'Carbonate (temporary) hardness = lesser of total hardness and total alkalinity;  non-carbonate = total hardness - carbonate hardness',
      inputs: [['th', 'Total hardness (mg/L as CaCO3)'], ['alk', 'Total alkalinity (mg/L as CaCO3)']],
      run: function (x) {
        if (x.th === null || x.alk === null) return { err: 'enter total hardness and total alkalinity' };
        var ch = Math.min(x.th, x.alk), nch = Math.max(x.th - x.alk, 0);
        return { out: { CH: ch, NCH: nch }, lines: ['Carbonate hardness = min(' + r(x.th) + ', ' + r(x.alk) + ') = ' + r(ch, 2) + ' mg/L as CaCO3', 'Non-carbonate hardness = ' + r(x.th) + ' - ' + r(ch, 2) + ' = ' + r(nch, 2) + ' mg/L as CaCO3'] };
      }
    },
    co2: {
      title: 'Free carbon dioxide titration', method: 'APHA 4500-CO2 C',
      formula: 'Free CO2 (mg/L) = A x N x 44 000 / V  (NaOH to pH 8.3)',
      inputs: [['v', 'Sample volume V (mL)'], ['a', 'NaOH titrant A (mL)'], ['n', 'NaOH normality N']],
      run: function (x) {
        if (!x.v || x.a === null || x.n === null) return { err: 'enter V, A and N' };
        var c = x.a * x.n * 44000 / x.v; return { out: { R: c }, lines: ['Free CO2 = ' + r(x.a) + ' x ' + r(x.n) + ' x 44000 / ' + r(x.v) + ' = ' + r(c, 2) + ' mg/L'] };
      }
    },
    dpd: {
      title: 'Chlorine by DPD', method: 'APHA 4500-Cl G',
      formula: 'Combined chlorine = total chlorine - free chlorine (each = reading x DF)',
      inputs: [['tot', 'Total chlorine reading (mg/L)'], ['fr', 'Free chlorine reading (mg/L)'], ['df', 'Dilution factor', '1']],
      run: function (x) {
        if (x.tot === null) return { err: 'enter the total chlorine reading' };
        var df = x.df || 1, t = x.tot * df, fr = (x.fr || 0) * df, c = t - fr;
        return { out: { total: t, free: fr, combined: c }, warn: c < 0 ? ['free chlorine exceeds total chlorine'] : [], lines: ['Total = ' + r(x.tot) + ' x ' + r(df) + ' = ' + r(t, 3) + ' mg/L;  free = ' + r(fr, 3) + ' mg/L;  combined = ' + r(t, 3) + ' - ' + r(fr, 3) + ' = ' + r(c, 3) + ' mg/L'] };
      }
    },
    grav: {
      title: 'Gravimetric', method: 'APHA 2540 B / D, USEPA 1664', reps: true,
      formula: 'Result (mg/L) = (final weight - initial weight) g x 1 000 000 / sample volume (mL)',
      inputs: [['w1', 'Initial weight (g)'], ['w2', 'Final weight (g)'], ['v', 'Sample volume (mL)']],
      one: function (x) { if (x.w1 === null || x.w2 === null || !x.v) return null; return { v: (x.w2 - x.w1) * 1e6 / x.v, line: '(' + r(x.w2, 5) + ' - ' + r(x.w1, 5) + ') x 1000000 / ' + r(x.v) }; }
    },
    vss: {
      title: 'Volatile solids', method: 'APHA 2540 E', reps: true,
      formula: 'VSS (mg/L) = (weight before ignition - weight after ignition) g x 1 000 000 / sample volume (mL)',
      inputs: [['a', 'Residue + dish/filter before ignition (g)'], ['c', 'After ignition (g)'], ['v', 'Sample volume (mL)']],
      one: function (x) { if (x.a === null || x.c === null || !x.v) return null; return { v: (x.a - x.c) * 1e6 / x.v, line: '(' + r(x.a, 5) + ' - ' + r(x.c, 5) + ') x 1000000 / ' + r(x.v) }; }
    },
    reading: {
      title: 'Instrumental reading', method: '', reps: true, std: true,
      formula: 'Result = instrument reading x dilution factor (replicates averaged)',
      inputs: [['rd', 'Reading'], ['df', 'Dilution factor', '1']],
      one: function (x) { if (x.rd === null) return null; var df = x.df === null ? 1 : x.df; return { v: x.rd * df, line: r(x.rd) + ' x ' + r(df) }; }
    },
    phosphate: {
      title: 'Phosphate (ascorbic acid)', method: 'APHA 4500-P E', reps: true, std: true,
      formula: 'Phosphate (mg/L PO4) = reading (mg/L P) x dilution factor x 3.066  (enter factor 1 when the instrument reads PO4)',
      inputs: [['rd', 'Reading'], ['df', 'Dilution factor', '1'], ['cf', 'P -> PO4 factor', '3.066']],
      one: function (x) { if (x.rd === null) return null; var df = x.df === null ? 1 : x.df, cf = x.cf === null ? 3.066 : x.cf; return { v: x.rd * df * cf, line: r(x.rd) + ' x ' + r(df) + ' x ' + r(cf) }; }
    },
    diff: {
      title: 'By difference', method: '',
      formula: 'Result = total - reactive/dissolved fraction',
      inputs: [['a', 'Total'], ['b', 'Fraction subtracted']],
      run: function (x) { if (x.a === null || x.b === null) return { err: 'enter both values' }; var d = x.a - x.b; return { out: { R: d }, warn: d < 0 ? ['negative difference'] : [], lines: [r(x.a) + ' - ' + r(x.b) + ' = ' + r(d, 4)] }; }
    },
    tkn: {
      title: 'Kjeldahl nitrogen titration', method: 'APHA 4500-Norg B / 4500-NH3 C',
      formula: 'TKN (mg N/L) = (A - B) x N x 14 000 / V  (A, B = mL H2SO4 for sample and blank)',
      inputs: [['a', 'Titrant for sample A (mL)'], ['b', 'Titrant for blank B (mL)', '0'], ['n', 'H2SO4 normality N'], ['v', 'Sample volume V (mL)']],
      run: function (x) {
        if (x.a === null || x.n === null || !x.v) return { err: 'enter A, N and V' };
        var t = (x.a - (x.b || 0)) * x.n * 14000 / x.v;
        return { out: { R: t }, warn: t < 0 ? ['blank exceeds sample titrant'] : [], lines: ['(' + r(x.a) + ' - ' + r(x.b || 0) + ') x ' + r(x.n) + ' x 14000 / ' + r(x.v) + ' = ' + r(t, 3) + ' mg N/L'] };
      }
    },
    sar: {
      title: 'Sodium adsorption ratio', method: 'USDA Handbook 60 / APHA',
      formula: 'SAR = Na / sqrt((Ca + Mg) / 2), concentrations in meq/L (Na/22.99, Ca/20.04, Mg/12.15)',
      inputs: [['na', 'Sodium (mg/L)'], ['ca', 'Calcium (mg/L)'], ['mg', 'Magnesium (mg/L)']],
      run: function (x) {
        if (x.na === null || x.ca === null || x.mg === null) return { err: 'enter Na, Ca and Mg' };
        var na = x.na / 22.99, ca = x.ca / 20.04, mg = x.mg / 12.15; if (ca + mg <= 0) return { err: 'Ca + Mg must be above zero' };
        var s = na / Math.sqrt((ca + mg) / 2);
        return { out: { R: s }, lines: ['Na ' + r(na, 3) + ', Ca ' + r(ca, 3) + ', Mg ' + r(mg, 3) + ' meq/L;  SAR = ' + r(na, 3) + ' / sqrt((' + r(ca, 3) + ' + ' + r(mg, 3) + ') / 2) = ' + r(s, 2)] };
      }
    },
    rsc: {
      title: 'Residual sodium carbonate', method: 'Eaton (1950) / USDA Handbook 60',
      formula: 'RSC (meq/L) = (CO3/30.00 + HCO3/61.02) - (Ca/20.04 + Mg/12.15), ions in mg/L',
      inputs: [['co3', 'Carbonate as CO3 (mg/L)', '0'], ['hco3', 'Bicarbonate as HCO3 (mg/L)'], ['ca', 'Calcium (mg/L)'], ['mg', 'Magnesium (mg/L)']],
      run: function (x) {
        if (x.hco3 === null || x.ca === null || x.mg === null) return { err: 'enter HCO3, Ca and Mg' };
        var a = (x.co3 || 0) / 30.0 + x.hco3 / 61.02, b = x.ca / 20.04 + x.mg / 12.15, v = a - b;
        return { out: { R: v }, lines: ['(' + r((x.co3 || 0) / 30.0, 3) + ' + ' + r(x.hco3 / 61.02, 3) + ') - (' + r(x.ca / 20.04, 3) + ' + ' + r(x.mg / 12.15, 3) + ') = ' + r(v, 2) + ' meq/L'] };
      }
    },
    lsi: {
      title: 'Langelier saturation index', method: 'APHA 2330 B',
      formula: 'LSI = pH - pHs;  pHs = (9.3 + A + B) - (C + D), A = (log TDS - 1)/10, B = -13.12 log(T+273) + 34.55, C = log Ca(as CaCO3) - 0.4, D = log alkalinity(as CaCO3)',
      inputs: [['ph', 'pH'], ['t', 'Temperature (°C)'], ['tds', 'TDS (mg/L)'], ['cah', 'Calcium hardness (mg/L as CaCO3)'], ['alk', 'Total alkalinity (mg/L as CaCO3)']],
      run: function (x) {
        if ([x.ph, x.t, x.tds, x.cah, x.alk].some(function (v) { return v === null; })) return { err: 'enter all five values' };
        if (x.tds <= 0 || x.cah <= 0 || x.alk <= 0) return { err: 'TDS, calcium hardness and alkalinity must be above zero' };
        var A = (Math.log10(x.tds) - 1) / 10, B = -13.12 * Math.log10(x.t + 273) + 34.55, C = Math.log10(x.cah) - 0.4, D = Math.log10(x.alk), pHs = (9.3 + A + B) - (C + D), L = x.ph - pHs;
        return { out: { R: L, pHs: pHs }, lines: ['A ' + r(A, 4) + ', B ' + r(B, 4) + ', C ' + r(C, 4) + ', D ' + r(D, 4) + ';  pHs = ' + r(pHs, 3) + ';  LSI = ' + r(x.ph) + ' - ' + r(pHs, 3) + ' = ' + r(L, 2)] };
      }
    },
    salinity: {
      title: 'Salinity from conductivity', method: 'APHA 2520 B (PSS-78)',
      formula: 'S = sum a_i Rt^(i/2) + dS(t), Rt = C / C(35,t,0) (Practical Salinity Scale 1978)',
      inputs: [['ec', 'Conductivity at the sample temperature, not compensated (µS/cm)'], ['t', 'Temperature (°C)', '25']],
      run: function (x) {
        if (x.ec === null || x.t === null) return { err: 'enter conductivity and temperature' };
        var t = x.t, C = x.ec / 1000, rt = 0.6766097 + 2.00564e-2 * t + 1.104259e-4 * t * t - 6.9698e-7 * t * t * t + 1.0031e-9 * t * t * t * t;
        var R = C / (42.914 * rt), q = Math.sqrt(R), a = [0.0080, -0.1692, 25.3851, 14.0941, -7.0261, 2.7081], b = [0.0005, -0.0056, -0.0066, -0.0375, 0.0636, -0.0144];
        var S = 0, dS = 0; for (var i = 0; i < 6; i++) { S += a[i] * Math.pow(q, i); dS += b[i] * Math.pow(q, i); }
        S += (t - 15) / (1 + 0.0162 * (t - 15)) * dS;
        return { out: { R: S }, warn: (S < 2 || S > 42) ? ['outside the PSS-78 range 2-42; report with care'] : [], lines: ['Rt = ' + r(R, 5) + ';  S = ' + r(S, 3) + ' (practical salinity, ≈ g/kg)'] };
      }
    },
    resist: {
      title: 'Resistivity from conductivity', method: 'APHA 2510 B',
      formula: 'Resistivity (Ω·cm) = 1 000 000 / conductivity (µS/cm)',
      inputs: [['ec', 'Conductivity (µS/cm)']],
      run: function (x) { if (!x.ec) return { err: 'enter conductivity' }; var v = 1e6 / x.ec; return { out: { R: v }, lines: ['1000000 / ' + r(x.ec) + ' = ' + r(v, 1) + ' Ω·cm (' + r(v / 1000, 3) + ' kΩ·cm)'] }; }
    },
    mf: {
      title: 'Membrane filtration count', method: 'APHA 9222 B/D, 9230 C, USEPA 1604, ISO 16266', reps: true,
      formula: 'CFU/100 mL = colonies counted x 100 x DF / volume filtered (mL)',
      inputs: [['col', 'Colonies counted'], ['v', 'Volume filtered (mL)', '100'], ['df', 'Dilution factor', '1']],
      one: function (x) { if (x.col === null || !x.v) return null; var df = x.df || 1; return { v: x.col * 100 * df / x.v, line: r(x.col) + ' x 100 x ' + r(df) + ' / ' + r(x.v), w: x.col > 200 ? 'more than 200 colonies (TNTC range)' : null, zero: x.col === 0 ? 100 * df / x.v : null }; }
    },
    plate: {
      title: 'Plate count', method: 'APHA 9215 B / ISO 6222', reps: true,
      formula: 'CFU/mL = colonies counted x DF / volume plated (mL)',
      inputs: [['col', 'Colonies counted'], ['v', 'Volume plated (mL)', '1'], ['df', 'Dilution factor', '1']],
      one: function (x) { if (x.col === null || !x.v) return null; var df = x.df || 1; return { v: x.col * df / x.v, line: r(x.col) + ' x ' + r(df) + ' / ' + r(x.v), w: (x.col > 300 || (x.col > 0 && x.col < 30)) ? 'colony count outside 30-300' : null, zero: x.col === 0 ? df / x.v : null }; }
    },
    sdi: {
      title: 'Silt density index', method: 'ASTM D4189',
      formula: 'SDI = (1 - t1 / t2) x 100 / T  (t1, t2 in s; T total test time in min)',
      inputs: [['t1', 't1, first 500 mL (s)'], ['t2', 't2, final 500 mL (s)'], ['T', 'Total time T (min)', '15']],
      run: function (x) {
        if (!x.t1 || !x.t2 || !x.T) return { err: 'enter t1, t2 and T' };
        var p = (1 - x.t1 / x.t2) * 100, s = p / x.T;
        return { out: { R: s }, warn: p > 75 ? ['plugging above 75 %: repeat with a shorter T'] : [], lines: ['%P = (1 - ' + r(x.t1) + ' / ' + r(x.t2) + ') x 100 = ' + r(p, 2) + ';  SDI = ' + r(p, 2) + ' / ' + r(x.T) + ' = ' + r(s, 2)] };
      }
    },
    bod: {
      title: 'BOD5', method: 'APHA 5210 B / 4500-O C', reps: true,
      formula: 'BOD = [(D1 - D2) - (B1 - B2) / Vc x Vs] / P,  P = sample volume / bottle volume  (replicate bottles averaged)',
      inputs: [['sv', 'Sample volume (mL)'], ['bv', 'Bottle volume (mL)', '300'], ['d1', 'D1 initial DO (mg/L)'], ['d2', 'D2 final DO (mg/L)'], ['b1', 'B1 seed-control initial DO (blank if not seeded)'], ['b2', 'B2 seed-control final DO'], ['vc', 'Vc seed in control bottle (mL)'], ['vs', 'Vs seed in sample bottle (mL)']],
      one: function (x) {                                   // one bottle; incomplete (or a partial seed correction) -> null (R5)
        if (!x.sv || !x.bv || x.d1 === null || x.d2 === null) return null;
        var P = x.sv / x.bv, corr = 0, w = [];
        var seed = [x.b1, x.b2, x.vc, x.vs].some(function (v) { return v !== null; });
        if (seed) { if ([x.b1, x.b2, x.vc, x.vs].some(function (v) { return v === null; }) || !x.vc) return null; corr = (x.b1 - x.b2) / x.vc * x.vs; }
        if (x.d1 - x.d2 < 2) w.push('DO depletion below 2.0 mg/L'); if (x.d2 < 1) w.push('residual DO below 1.0 mg/L');
        var b = (x.d1 - x.d2 - corr) / P;
        return { v: b, line: '[(' + r(x.d1) + ' - ' + r(x.d2) + ') - ' + (corr < 0 ? '(' + r(corr, 6) + ')' : r(corr, 6)) + '] / (' + r(x.sv) + ' / ' + r(x.bv) + ')', w: w.join('; ') || null };
      }
    },
    obs: {
      title: 'Direct observation / reading', method: '', obs: true,
      formula: 'Recorded as observed (no calculation)',
      inputs: [['val', 'Observed value'], ['inst', 'Instrument / remarks']]
    }
  };

  /* parameter (bare reported name) -> card; first match wins. out: the output compared with the reported result */
  var MAP = [
    [/pesticide|polyaromatic|\bpah\b|\bvoc\b|volatile organic comp|alpha emit|beta emit|radio/, 'sub'],
    [/^bicarbonates?\b|^hco3/, 'alk', 'HCO3ion'], [/^carbonate hardness|^temporary hardness/, 'carbhard', 'CH'],
    [/^non.?carbonate hardness/, 'carbhard', 'NCH'], [/^carbonates?\b/, 'alk', 'CO3ion'], [/hydroxide alk/, 'alk', 'OH'],
    [/methyl orange alk|^total alkalinity|^alkalinity as caco3|^alkalinity end point|^alkalinity/, 'alk', 'T'], [/phenolphthalein alk/, 'alk', 'P'],
    [/^calcium hardness/, 'edta', 'H'], [/^total hardness|^hardness/, 'edta', 'H'], [/^magnesium hardness/, 'mghard', 'H'],
    [/free (co2|carbon dioxide)/, 'co2', 'R'], [/^total chlorine/, 'dpd', 'total'], [/^combined chlorine/, 'dpd', 'combined'],
    [/^mlvss|^vss|^volatile suspended/, 'vss'], [/^mlss|^total suspended solids|^tss|^total solids?\b|^oil.*grease|^settleable solids? \(grav/, 'grav'],
    [/^phosphates?\b|^ortho.?phosphate/, 'phosphate'],
    [/^tkn\b|kjeldahl/, 'tkn', 'R'],
    [/^colloidal silica/, 'diff', 'R', 'Colloidal silica = total silica - reactive silica'], [/^ferric/, 'diff', 'R', 'Ferric iron = total iron - ferrous iron'],
    [/sodium adsorption|^sar\b/, 'sar', 'R'], [/residual sodium carbonate|^rsc\b/, 'rsc', 'R'], [/langel?l?ier|^lsi\b|saturation index/, 'lsi', 'R'],
    [/^salinity/, 'salinity', 'R'], [/^resistivity/, 'resist', 'R'], [/silt density|^sdi\b/, 'sdi', 'R'],
    [/coliform|coli\b|enterococc|streptococ|pseudomonas|psudomonas|clostridium/, 'mf'],
    [/plate count|colony count|heterotrophic|microbial content|aerobic microbe|bacterial count|viable count|\btpc\b|\bhpc\b|\btbc\b|enterobacteriaceae/, 'plate'],   // Enterobacteriaceae: plate count (owner 28-10-2026)
    [/^bod\b|biological oxygen/, 'bod', 'R'],
    [/^temperature|^odou?r|^taste|^appearance|^flow ?rate|particle size|particulate|corrosivity|settleable|^colou?r|^ph\b/, 'obs']
  ];
  var OUTLABEL = { HCO3ion: 'bicarbonate as HCO3 (mg/L)', CO3ion: 'carbonate as CO3 (mg/L)', OH: 'hydroxide alkalinity (mg/L as CaCO3)', T: 'total alkalinity (mg/L as CaCO3)',
    P: 'phenolphthalein alkalinity (mg/L as CaCO3)', CH: 'carbonate hardness (mg/L as CaCO3)', NCH: 'non-carbonate hardness (mg/L as CaCO3)', H: 'hardness (mg/L as CaCO3)',
    total: 'total chlorine (mg/L)', combined: 'combined chlorine (mg/L)' };
  function cardFor(name, method, unit) {
    var b = bare(name), m = String(method || '').toLowerCase(), cf = { calc: 'reading' };   // default: reading x DF
    for (var i = 0; i < MAP.length; i++) if (MAP[i][0].test(b)) { cf = { calc: MAP[i][1], out: MAP[i][2], note: MAP[i][3] }; break; }
    // R7: a count reported per 100 mL, or by a membrane-filtration method, is worked per 100 mL (x 100 / V)
    if (cf.calc === 'plate' && !/enterobacter/.test(b) && (/9222|9213|9230|1604|16266|membrane/.test(m) || /100\s*ml/i.test(String(unit || '')))) cf = { calc: 'mf' };
    // the method on the report decides between a titration and an instrument read-out
    if (cf.calc === 'tkn' && /hach|10242|spectro|vial/.test(m)) cf = { calc: 'reading' };
    if (cf.calc === 'phosphate' && /hach|8048|phosver/.test(m)) cf.defaults = { cf: '1' };       // HACH PhosVer reads PO4
    if (cf.calc === 'edta' && /3111|3120|aas|icp|flame/.test(m)) cf = { calc: 'reading' };
    if (cf.calc === 'alk' && /hach|8203|digital titrator/.test(m)) cf.note = 'Digital titrator: enter the titrant in mL equivalent';
    return cf;
  }
  function phosphateNote(name) { return /phosph/.test(bare(name)) ? 'phosphate as PO4 = phosphorus as P x 3.066' : null; }

  /* ------------------------------------------------------------------ cards */
  var host = null, nCard = 0;
  function container() {
    if (host && document.body.contains(host)) return host;
    var form = $('qcForm'); if (!form) return null;
    host = document.createElement('div'); host.id = 'rdsLib';
    host.innerHTML = '<div class="rl-head"><h2>Calculations - formula library</h2><span>Parameters of this sample without their own section above, by the method on the report.</span></div><div class="rl-cards"></div>' +
      '<div class="rl-add"><label>Add calculation:</label><select class="rl-pick"></select><input class="rl-pname" placeholder="parameter name (as reported)"><button type="button" class="rl-addbtn">Add</button></div>';
    var sub = form.querySelector('button[type=submit]');
    var anchor = sub ? (sub.closest('div') || sub) : null;
    if (anchor && anchor.parentNode) anchor.parentNode.insertBefore(host, anchor); else form.appendChild(host);
    var pick = host.querySelector('.rl-pick');
    Object.keys(CALC).forEach(function (k) { var o = document.createElement('option'); o.value = k; o.textContent = CALC[k].title + (CALC[k].method ? ' - ' + CALC[k].method : ''); pick.appendChild(o); });
    host.querySelector('.rl-addbtn').addEventListener('click', function () {
      var nm = host.querySelector('.rl-pname').value.trim() || CALC[pick.value].title;
      addCard({ parameter: nm, method: '' }, '', null, { calc: pick.value });
    });
    return host;
  }
  function clearCards() { var h = container(); if (h) h.querySelector('.rl-cards').innerHTML = ''; nCard = 0; }

  function addCard(item, side, reported, forced, target) {      // target: a place on the page instead of the library list (R5)
    var h = container(); if (!h) return;
    var cf = forced || cardFor(item.parameter, item.method, item.unit);
    if (cf.calc === 'sub') return;
    var C = CALC[cf.calc]; if (!C) return;
    var n = ++nCard, id = 'rl' + n, reps = C.reps ? 3 : 1;
    var method = (item.method || '').trim().replace(/^[-–\s]+$/, '') || C.method;
    var card = document.createElement('div'); card.className = 'rl-card'; card.id = id;
    var head = item.parameter + (side ? ' (' + side + ')' : '');
    var rep = reported === null || reported === undefined ? '' : String(reported);
    var html = '<div class="rl-title"><b>' + esc(head) + '</b><span class="rl-meth">' + esc(C.title + (method ? ' - ' + method : '')) + '</span>' +
      (rep ? '<span class="rl-rep">reported: ' + esc(rep) + '</span>' : '') + '</div>' +
      '<div class="rl-formula">' + esc(cf.note ? cf.note + '.  ' : '') + esc(C.formula) + (cf.out && OUTLABEL[cf.out] ? '<br><b>Result shown: ' + esc(OUTLABEL[cf.out]) + '</b>' : '') + (phosphateNote(item.parameter) ? '<br><i>' + esc(phosphateNote(item.parameter)) + '</i>' : '') + '</div>';
    if (C.obs) {
      html += '<div class="rl-grid">' + C.inputs.map(function (p) { return '<label>' + esc(p[1]) + '<input type="text" data-k="' + p[0] + '" name="' + id + '_' + p[0] + '"></label>'; }).join('') + '</div>';
    } else {
      for (var rI = 1; rI <= reps; rI++) {
        html += '<div class="rl-grid">' + (reps > 1 ? '<span class="rl-repl">Replicate ' + rI + '</span>' : '') + C.inputs.map(function (p) {
          return '<label>' + esc(p[1]) + '<input type="number" step="any" data-k="' + p[0] + '" data-r="' + rI + '" name="' + id + '_' + p[0] + (reps > 1 ? '_' + rI : '') + '"' + ((cf.defaults && cf.defaults[p[0]] !== undefined) ? ' value="' + cf.defaults[p[0]] + '"' : (p[2] !== undefined ? ' value="' + p[2] + '"' : '')) + '></label>';
        }).join('') + '</div>';
      }
      if (C.std) html += '<div class="rl-grid"><span class="rl-repl">Check standard (optional)</span><label>True value<input type="number" step="any" data-std="t" name="' + id + '_std_true"></label><label>Measured<input type="number" step="any" data-std="m" name="' + id + '_std_meas"></label></div>';
    }
    html += '<div class="rl-res"><button type="button" class="rl-eq">=</button><input type="text" readonly class="rl-ans" name="' + id + '_ans" placeholder="result"><input type="text" class="rl-unit" name="' + id + '_unit" value="' + esc(item.unit || defaultUnit(cf.calc, item.parameter)) + '"></div>' +
      '<div class="rl-check"><label>Check</label><input type="text" readonly class="rl-chk" name="' + id + '_check"></div>' +
      '<input type="hidden" class="rl-print" name="lib_print_' + String(n).padStart(3, '0') + '">' +
      '<button type="button" class="rl-del" title="Remove this card">Remove</button>';
    card.innerHTML = html;
    (target || h.querySelector('.rl-cards')).appendChild(card);
    card.querySelector('.rl-eq').addEventListener('click', function () { compute(card, item, side, rep, cf, C, method); });
    card.querySelector('.rl-del').addEventListener('click', function () { card.remove(); });
    if (C.obs) card.querySelector('input[data-k=val]').value = rep;
  }
  function defaultUnit(calc, name) {
    var b = bare(name);
    if (calc === 'obs') return /temperature/.test(b) ? '°C' : (/flow/.test(b) ? 'm³/h' : (/colou?r/.test(b) ? 'TCU' : (/turbid/.test(b) ? 'NTU' : '')));   // QA RDS-28
    return { mf: 'CFU/100 mL', plate: 'CFU/mL', sar: '-', rsc: 'meq/L', lsi: '-', salinity: 'PSU', resist: 'Ω·cm', sdi: '-' }[calc] ||
      (/temperature/.test(b) ? '°C' : (/flow/.test(b) ? 'm³/h' : 'mg/L'));
  }
  function esc(s) { return String(s === null || s === undefined ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function reportedNum(rep) { var s = String(rep || '').trim(); if (!s || /^[<>]|n\.?d|n\/a|nil|absent|present|tntc/i.test(s)) return null; var m = s.match(/-?\d+(\.\d+)?/); return m ? parseFloat(m[0]) : null; }

  function rdp(rep, calc) {                              // decimals of the result: those reported plus one (QA RDS-40)
    if (calc === 'mf' || calc === 'plate') return 0;
    var m = String(rep || '').match(/\d(?:\.(\d+))?/); return m ? Math.min(4, (m[1] || '').length + 1) : 4;
  }
  function compute(card, item, side, rep, cf, C, method) {
    var warn = [], lines = [], result = null, dp = 4;
    if (C.obs) {
      result = card.querySelector('input[data-k=val]').value.trim();
      lines.push('Observed: ' + result + ' ' + card.querySelector('.rl-unit').value + (card.querySelector('input[data-k=inst]').value ? '  (' + card.querySelector('input[data-k=inst]').value + ')' : ''));
      card.querySelector('.rl-ans').value = result;
    } else if (C.reps) {
      var vals = [];
      for (var i = 1; i <= 3; i++) {
        var x = {}; C.inputs.forEach(function (p) { var e = card.querySelector('input[data-k=' + p[0] + '][data-r="' + i + '"]'); x[p[0]] = e ? f(e.value) : null; });
        var filled = C.inputs.some(function (p) { return p[2] === undefined && x[p[0]] !== null; });
        if (!filled) continue;
        var o = C.one(x);
        if (!o) { warn.push('replicate ' + i + ' incomplete'); continue; }
        vals.push(o.v); lines.push('Replicate ' + i + ': ' + o.line + ' = ' + r(o.v, 4));
        if (o.w) warn.push('replicate ' + i + ': ' + o.w);
        if (o.v < 0) warn.push('replicate ' + i + ' negative - check the weights/readings');
        if (o.zero !== null && o.zero !== undefined) warn.push('replicate ' + i + ': no colonies - report as < ' + r(o.zero, 2));
      }
      if (!vals.length) { alert('Enter at least one complete replicate.'); return; }
      result = avg(vals);
      if (vals.length > 1) { lines.push('Average of ' + vals.length + ' = ' + r(result, 4)); var sp = spread(vals); if (sp !== null && sp > TOL_REP) warn.push('replicate spread ' + r(sp, 1) + ' % above ' + TOL_REP + ' %'); }
      if (C.std) {
        var t = f(card.querySelector('[data-std=t]').value), m = f(card.querySelector('[data-std=m]').value);
        if (t && m !== null) { var rc = 100 * m / t; lines.push('Check standard: ' + r(m) + ' / ' + r(t) + ' = ' + r(rc, 1) + ' % recovery'); if (rc < REC_LO || rc > REC_HI) warn.push('check standard recovery ' + r(rc, 1) + ' % outside ' + REC_LO + '-' + REC_HI + ' %'); }
      }
      card.querySelector('.rl-ans').value = r(result, rdp(rep, cf.calc));
    } else {
      var y = {}; C.inputs.forEach(function (p) { var e = card.querySelector('input[data-k=' + p[0] + ']'); y[p[0]] = e ? f(e.value) : null; });
      var o2 = C.run(y);
      if (o2.err) { alert(item.parameter + ': ' + o2.err + '.'); return; }
      lines = lines.concat(o2.lines); warn = warn.concat(o2.warn || []);
      var key = cf.out || 'R';
      result = o2.out[key] !== undefined ? o2.out[key] : o2.out.R;
      if (result === undefined) result = o2.out[Object.keys(o2.out)[0]];
      card.querySelector('.rl-ans').value = r(result, rdp(rep, cf.calc));
    }
    var rn = reportedNum(rep), num = typeof result === 'number' ? result : null;
    if (rn !== null && num !== null) {
      var d = Math.abs(num - rn), base = Math.max(Math.abs(rn), 1e-9);
      var dpRep = ((String(rep).match(/\.(\d+)/) || [0, ''])[1]).length, floor = 0.5 * Math.pow(10, -dpRep);   // QA RDS-28: tied to the reported decimals
      if (d / base > TOL_REPORT && d > floor) {
        var alt = /phosph/.test(bare(item.parameter)) ? [num * 3.066, num / 3.066] : [];
        var altOk = alt.some(function (a) { return Math.abs(a - rn) / base <= TOL_REPORT; });
        warn.push('calculated ' + r(num, 3) + ' differs from the reported ' + rep + ' by ' + r(100 * d / base, 1) + ' %' + (altOk ? ' (matches after the P/PO4 conversion)' : ''));
      }
    }
    var sRep = String(rep || '').trim(), bm = sRep.match(/^([<>])\s*=?\s*(-?\d+(?:\.\d+)?)/);   // R7: "<" / ">" / N.D. are checked too
    if (num !== null && bm) {
      var bnd = parseFloat(bm[2]);
      if (bm[1] === '>' && num <= bnd) warn.push('calculated ' + r(num, 3) + ' is not above the reported ' + sRep);
      if (bm[1] === '<' && num >= bnd) warn.push('calculated ' + r(num, 3) + ' is not below the reported ' + sRep);
    }
    if (num !== null && num > 0 && (cf.calc === 'mf' || cf.calc === 'plate') && /^(n\.?\s*d\.?|nil|absent|not detected)/i.test(sRep)) warn.push('calculated ' + r(num, 3) + ' but reported ' + sRep);
    var chk = card.querySelector('.rl-chk');
    chk.value = warn.length ? warn.join('; ') : 'OK'; chk.classList.toggle('rl-warn', warn.length > 0); chk.classList.toggle('rl-ok', !warn.length);
    card.querySelector('.rl-print').value = JSON.stringify({
      parameter: item.parameter, side: side || '', method: method, calc: C.title, formula: C.formula + (cf.out && OUTLABEL[cf.out] ? '  Result shown: ' + OUTLABEL[cf.out] + '.' : ''), lines: lines,
      result: card.querySelector('.rl-ans').value, unit: card.querySelector('.rl-unit').value, reported: rep, check: chk.value
    });
  }

  /* ------------------------------------------------------------------ hook into the page */
  /* the page's own sections that are on screen now (a name the page knows may have no section for this report type,
     e.g. Coliform on inlet/outlet reports): headings in view, normalised */
  function visibleHeads() {
    var form = $('qcForm') || document;
    var all = Array.prototype.filter.call(form.querySelectorAll('h1, p.text-3xl'), function (h) { return !h.closest('#rdsLib'); });
    var buttons = Array.prototype.filter.call(form.querySelectorAll('button'), function (x) { return !x.closest('#rdsLib') && /=|final ans/i.test(x.textContent) && x.offsetParent !== null; });   // R5: also "Final Ans" (toxic metals)
    var out = [];
    all.forEach(function (h, i) {
      if (h.offsetParent === null) return;
      var next = all[i + 1] || null;           // the section: from this heading to the next one; it must hold an "=" button
      var calc = buttons.some(function (btn) {
        var after = h.compareDocumentPosition(btn) & Node.DOCUMENT_POSITION_FOLLOWING;
        var before = !next || (next.compareDocumentPosition(btn) & Node.DOCUMENT_POSITION_PRECEDING);
        return after && before;
      });
      if (calc) out.push(' ' + bare(h.textContent) + ' ');
    });
    return out;
  }
  var HEADALIAS = {     // the page's heading for a section named otherwise (R5: no second card beside the page's own section)
    'total hardness as caco3': ['hardness'], 'phenolic compounds': ['phenolic'],
    'an ionic detergent as mbas': ['an ionic surfactants', 'anionic detergent', 'anionic surfactants']
  };
  function shownOnPage(pn, heads) {
    if (!pn) return false;
    var keys = [bare(pn)].concat(HEADALIAS[bare(pn)] || []), par = norm(pn).match(/\(([^)]*)\)/);
    if (par) keys.push(bare(par[1]));
    var w = bare(pn).split(' ').filter(function (x) { return x.length >= 4; });
    if (w.length === 1) keys.push(w[0]);
    return heads.some(function (h) { return keys.some(function (k) { return k && (h.indexOf(' ' + k + ' ') >= 0 || (k.length >= 6 && h.indexOf(' ' + k) >= 0)); }); });
  }
  function build(qcData, reportType) {
    clearCards();
    var heads = visibleHeads();
    (qcData || []).forEach(function (it) {
      if (shownOnPage(pageName(it.parameter), heads)) return;   // the page shows its own section
      var unitSide = [];
      if (reportType === 'in-out') {
        unitSide.push(['Inlet', it.inlet_result]); unitSide.push(['Outlet', it.outlet_result]);
      } else unitSide.push(['', it.test_result !== undefined ? it.test_result : (it.result !== undefined ? it.result : '')]);
      unitSide.forEach(function (s) { if (/^\s*(n\/?a|-|)\s*$/i.test(String(s[1] === undefined || s[1] === null ? '' : s[1]))) return; addCard(it, s[0], s[1]); });   // no card for a result not reported (QA RDS-28)
    });
  }
  var orig = window.populateQCTable;
  if (typeof orig === 'function') {
    window.populateQCTable = function (qcData) {
      var args = Array.prototype.slice.call(arguments);
      var mapped = (qcData || []).map(function (it) {
        var pn = pageName(it.parameter);
        return (pn && pn !== it.parameter) ? Object.assign({}, it, { parameter: pn, _reported: it.parameter }) : it;
      });
      args[0] = mapped;
      var res = orig.apply(this, args);
      // the RDS table keeps the name as reported. The page leaves out parameters not reported (N/A, rds_page.js), so a
      // row is found by its place among the reported parameters and checked by the name the page wrote in it (R6: the
      // row number of the full list put names on the wrong rows when an N/A parameter came before them)
      var rt = args[3], na = function (v) { return /^\s*(n\/?a|-|)\s*$/i.test(String(v === undefined || v === null ? '' : v)); };
      var kept = mapped.filter(function (it) {
        return rt === 'in-out' ? !(na(it.inlet_result) && na(it.outlet_result)) : !na(it.test_result !== undefined ? it.test_result : it.result);
      });
      var rows = Array.prototype.filter.call(document.querySelectorAll('#qcForm tbody tr'), function (tr) {
        var sn = ((tr.querySelector('.main-sno') || {}).textContent || '').trim(); return sn && sn.indexOf('.') < 0;
      }), used = {};
      kept.forEach(function (it, k) {
        var order = [k].concat(rows.map(function (_, j) { return j; }));
        for (var n = 0; n < order.length; n++) {
          var j = order[n], e = rows[j] && rows[j].querySelector('input[name^="parameter_"]');
          if (used[j] || !e || e.value !== it.parameter) continue;
          used[j] = true;
          if (it._reported) e.value = it._reported;
          break;
        }
      });
      try { build(qcData, PAGE === 'ww' ? args[3] : ''); } catch (e) { if (window.console) console.error('formula library', e); }
      return res;
    };
  }
  window.RDSLib = { norm: norm, bare: bare, pageName: pageName, cardFor: cardFor, CALC: CALC, addCard: addCard, build: build };

  var css = document.createElement('style');
  css.textContent =
    '#rdsLib{margin:30px 0;padding:16px;border:1px solid #cbd5e1;border-radius:10px;background:#fff}' +
    '#rdsLib .rl-head h2{font-size:22px;font-weight:700;color:#0f5132;margin:0}#rdsLib .rl-head span{font-size:13px;color:#64748b}' +
    '.rl-card{border:1px solid #e2e8f0;border-left:4px solid #0f5132;border-radius:8px;padding:12px 14px;margin:14px 0;background:#fcfdfd;position:relative}' +
    '.rl-title{display:flex;flex-wrap:wrap;gap:10px;align-items:baseline;font-size:15px;padding-right:80px}.rl-meth{color:#334155;font-size:13px}.rl-rep{color:#1e40af;font-size:13px;margin-left:auto}' +
    '.rl-formula{font-size:12.5px;color:#475569;background:#f8fafc;border:1px dashed #cbd5e1;border-radius:6px;padding:6px 9px;margin:8px 0}' +
    '.rl-grid{display:flex;flex-wrap:wrap;gap:10px;align-items:flex-end;margin:6px 0}.rl-grid label{display:flex;flex-direction:column;font-size:12px;color:#475569;gap:3px}' +
    '.rl-grid input{border:1px solid #cbd5e1;border-radius:6px;padding:6px 8px;width:150px;font-size:13px}.rl-repl{font-size:12px;font-weight:700;color:#0f5132;min-width:120px;align-self:center}' +
    '.rl-res{display:flex;gap:8px;align-items:center;margin-top:8px}.rl-eq{background:#2563eb;color:#fff;border-radius:7px;padding:6px 16px}' +
    '.rl-ans{border:1px solid #cbd5e1;border-radius:6px;padding:6px 8px;width:170px;background:#f1f5f9;font-weight:700}.rl-unit{border:1px solid #cbd5e1;border-radius:6px;padding:6px 8px;width:110px}' +
    '.rl-check{display:flex;gap:8px;align-items:center;margin-top:8px}.rl-check label{font-weight:700;font-size:13px}.rl-chk{flex:1;border:1px solid #cbd5e1;border-radius:6px;padding:6px 9px;font-size:13px;background:#f8fafc}' +
    '.rl-chk.rl-warn{background:#fff7ed;border-color:#f59e0b;color:#92400e}.rl-chk.rl-ok{background:#f0fdf4;border-color:#22c55e;color:#166534}' +
    '.rl-del{position:absolute;top:8px;right:10px;font-size:12px;color:#b91c1c;background:none;border:none;cursor:pointer}' +
    '.rl-add{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:12px;font-size:13px}.rl-add select,.rl-add input{border:1px solid #cbd5e1;border-radius:6px;padding:6px 8px}.rl-addbtn{background:#0f5132;color:#fff;border-radius:7px;padding:6px 14px}';
  document.head.appendChild(css);
  function ready() { container(); }
  if (document.readyState !== 'loading') ready(); else document.addEventListener('DOMContentLoaded', ready);
})();
