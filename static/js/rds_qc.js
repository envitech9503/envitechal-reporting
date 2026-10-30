/* RDS release R5 (owner requests 27-10-2026), loaded after rds_formula_lib.js on the four RDS pages.
 *
 * 1. EDTA factor B (QA RDS-23): every EDTA titration (total hardness, calcium, magnesium) takes the standardised
 *    factor B (mg CaCO3 equivalent to 1.00 mL EDTA) from one box at the top of its section; the readings use it
 *    (rdsEdtaB in rds_avg.js), it is saved with the RDS and printed in the formula. A reading entered without B
 *    stops the save.
 * 2. Quality-control checks: every calculation section and library card has "+ Working standard (WS)",
 *    "+ Reference material (RM)" and "+ Certified reference material (CRM)". A check takes its identification,
 *    the true / certified value, three readings, the acceptance limits, and gives mean, recovery and verdict;
 *    it is saved in qc_print_<n> (JSON) and printed on the RDS PDF (QC/rds_qc_pdf.py). Parameters in the
 *    laboratory's accreditation scope (as QC/soc_rules.ACCREDITED) get a WS check by default when their section
 *    carries no working standard of its own. The table's "+" (CRM row) gives a CRM check where the page has no
 *    CRM block of its own for that parameter.
 * 3. BOD (WW): triplicate cards (HACH 10099 readings and APHA 5210 B bottles) at the top of the BOD section; the
 *    previous single-determination layout stays available under "Single-determination layout".
 * 4. A sample whose report carries no reported result says so instead of showing an empty page; a "Sections" list
 *    jumps to any calculation on the page.
 */
(function () {
  'use strict';
  var PAGE = /create_ww_qc/.test(location.pathname) ? 'ww' : 'dw';
  var SFX = ['', '_inlet', '_outlet'];
  var DEFAULT_CHECKS = ['WS'];                // added by default to accredited parameters without a working standard
  // mirrors QC/soc_rules.ACCREDITED (QC.tests_rds_r5 keeps the two equal)
  var ACCREDITED = {
    'Karachi|dw': ['pH', 'TDS', 'Hardness', 'Nitrate', 'Chloride', 'Fluoride', 'Nickel'],
    'Karachi|ww2': ['pH', 'COD', 'TDS'],
    'Lahore|dw': ['pH', 'Turbidity', 'TDS', 'Chloride', 'Hardness', 'Nitrate', 'Alkalinity', 'Sulphate', 'Calcium'],
    'Lahore|ww2': ['pH', 'TDS', 'Chloride', 'Sulphate']
  };
  var ACC_RE = {
    ph: /^ph\b/, tds: /^tds\b|^total dissolved solids/, hardness: /^(total )?hardness\b/, nitrate: /^nitrate\b/, chloride: /^chloride\b/,
    fluoride: /^fluoride\b/, nickel: /^nickel\b/, turbidity: /^turbidity\b/, alkalinity: /^(total )?alkalinity\b/,
    sulphate: /^(sulphate|sulfate)\b/, calcium: /^calcium\b(?! hardness)/, cod: /^cod\b|^chemical oxygen demand/
  };
  var TYPES = { WS: 'Working standard (WS)', RM: 'Reference material (RM)', CRM: 'Certified reference material (CRM)' };

  function $(id) { return document.getElementById(id); }
  function form() { return $('qcForm'); }
  function vis(e) { return !!(e && e.offsetParent !== null); }
  function esc(s) { return String(s === null || s === undefined ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function num(v) { if (v === null || v === undefined || String(v).trim() === '') return null; var x = parseFloat(v); return isFinite(x) ? x : null; }
  function rd(v, dp) { return (v === null || !isFinite(v)) ? '' : String(+v.toFixed(dp === undefined ? 4 : dp)); }
  function after(a, b) { return !!(a.compareDocumentPosition(b) & Node.DOCUMENT_POSITION_FOLLOWING); }
  function headings() {
    var f = form(); if (!f) return [];
    return Array.prototype.filter.call(f.querySelectorAll('h1, p.text-3xl'), function (h) { return !h.closest('#rdsLib') && !h.closest('table') && !h.closest('.rq-block') && !h.closest('[id^="calc_"]'); });   // not a CRM row's own block
  }
  function headingBefore(el) {
    var hs = headings(), last = null;
    for (var i = 0; i < hs.length; i++) { if (after(hs[i], el)) last = hs[i]; else break; }
    return last;
  }
  function insertAfterHeading(h, node) {
    var p = h.parentElement;      // a heading alone in its wrapper: insert after the wrapper
    if (p && p !== form() && p.children.length === 1 && !p.classList.contains('flex')) p.insertAdjacentElement('afterend', node);
    else h.insertAdjacentElement('afterend', node);
  }

  /* ------------------------------------------------------------------ lab and accreditation */
  function sampleId() {
    var o = document.querySelector('#samples option:checked');
    if (!o || !o.value) return '';
    try { return JSON.parse(o.value).sample_id || ''; } catch (e) { return o.getAttribute('data-sample-id') || ''; }
  }
  function lab() {
    var s = sampleId();
    if (/-LHR\b/i.test(s)) return 'Lahore';
    if (/-KHI\b/i.test(s)) return 'Karachi';
    return '';
  }
  function accredited(name) {
    var b = String(name || '').toLowerCase().replace(/\*/g, '').replace(/\s*\(.*$/, '').replace(/[^a-z0-9 ]+/g, ' ').replace(/\s+/g, ' ').trim();
    var kind = PAGE === 'ww' ? 'ww2' : 'dw', labs = lab() ? [lab()] : ['Karachi', 'Lahore'];
    var hit = '';                                            // the accreditation-scope name ('Hardness'), '' when not in scope
    labs.some(function (l) {
      return (ACCREDITED[l + '|' + kind] || []).some(function (a) { var re = ACC_RE[a.toLowerCase()]; if (re && re.test(b)) { hit = a; return true; } return false; });
    });
    return hit;
  }

  /* ------------------------------------------------------------------ 1. EDTA factor B */
  var EDTA = [
    { base: 'hardness', title: 'total hardness', anchors: ['hardness_2_1'], initials: ['hardness_2_2', 'hardness_3_2', 'hardness_4_2'],
      equals: ['hardness_equal2', 'hardness_equal3', 'hardness_equal4'], finals: ['hardness_2_1', 'hardness_3_1', 'hardness_4_1'] },
    { base: 'calcium', title: 'calcium hardness / calcium', anchors: ['cal_r1_final', 'ch_r1_final'],
      initials: ['cal_r1_initial', 'cal_r2_initial', 'cal_r3_initial', 'ch_r1_initial', 'ch_r2_initial', 'ch_r3_initial'],
      equals: ['cal_r1_equal', 'cal_r2_equal', 'cal_r3_equal', 'ch_r1_equal', 'ch_r2_equal', 'ch_r3_equal'],
      finals: ['cal_r1_final', 'cal_r2_final', 'cal_r3_final', 'ch_r1_final', 'ch_r2_final', 'ch_r3_final'] },
    { base: 'magnesium', title: 'total and calcium hardness (magnesium)', anchors: ['r1_final'],
      initials: ['r1_initial', 'r2_initial', 'r3_initial', 'r1_1_initial', 'r2_1_initial', 'r3_1_initial'],
      equals: ['r1_equal', 'r2_equal', 'r3_equal', 'r1_1_equal', 'r2_1_equal', 'r3_1_equal'],
      finals: ['r1_final', 'r2_final', 'r3_final', 'r1_1_final', 'r2_1_final', 'r3_1_final'] }
  ];
  function edtaBoxes() {
    EDTA.forEach(function (g) {
      SFX.forEach(function (s) {
        var key = g.base + '_edta_b' + s;
        if ($(key)) return;
        var anchor = null;
        g.anchors.some(function (a) { anchor = $(a + s); return !!anchor; });
        if (!anchor) return;
        var h = headingBefore(anchor);
        var box = document.createElement('div');
        box.className = 'rds-edta';
        box.innerHTML = '<label><b>EDTA factor B</b><span>mg CaCO₃ equivalent to 1.00 mL of the EDTA titrant (today\'s standardisation)</span>' +
          '<input type="number" step="any" min="0" id="' + key + '" name="' + key + '" placeholder="e.g. 1.000" title="EDTA factor B"></label>' +
          '<p class="rds-edta-note">Every ' + esc(g.title) + ' reading below is (Final − Initial) × B × … ÷ sample volume. Enter B before pressing =.</p>';
        if (h) insertAfterHeading(h, box); else anchor.closest('div').insertAdjacentElement('beforebegin', box);
        var inp = box.querySelector('input'), note = box.querySelector('.rds-edta-note');
        inp.addEventListener('change', function () {
          var redone = 0;
          g.finals.forEach(function (fId, i) {
            var fe = $(fId + s), eq = $(g.equals[i] + s);
            if (fe && eq && String(fe.value).trim() !== '') { eq.click(); redone++; }
          });
          if (redone) { note.textContent = 'B changed: ' + redone + ' reading(s) recalculated with B = ' + inp.value + '. Press = again on the averages and the steps that use these readings.'; note.classList.add('rds-edta-warn'); }
        });
      });
      SFX.forEach(function (s) {
        g.initials.forEach(function (id) {
          var e = $(id + s); if (!e || e.dataset.rdsB) return;
          e.dataset.rdsB = '1';
          var sib = e.nextElementSibling;
          if (sib && sib.textContent.trim() === ')') { var m = document.createElement('p'); m.className = 'px-1 font-bold rds-bmark'; m.title = 'EDTA factor B'; m.textContent = '× B'; sib.insertAdjacentElement('afterend', m); }
        });
      });
    });
  }
  function edtaMissing() {
    var miss = [];
    EDTA.forEach(function (g) {
      SFX.forEach(function (s) {
        var b = $(g.base + '_edta_b' + s); if (!b || !vis(b)) return;
        var used = g.finals.some(function (fId) { var fe = $(fId + s); return fe && vis(fe) && String(fe.value).trim() !== ''; });
        if (used && !(num(b.value) > 0)) miss.push(g.title + (s ? ' (' + s.slice(1) + ')' : ''));
      });
    });
    return miss;
  }

  /* ------------------------------------------------------------------ 2. QC checks (WS / RM / CRM) */
  var nQc = 0;
  function sectionName(h) {
    var t = '';
    Array.prototype.forEach.call(h.childNodes, function (n) { if (n.nodeType === 3 || (n.nodeType === 1 && !n.classList.contains('rds-rep'))) t += n.textContent; });
    t = t.replace(/\s+/g, ' ').trim().replace(/\bcalculations?\b.*$/i, '').replace(/\*/g, '').trim();
    var side = /\binlet\b/i.test(t) ? 'Inlet' : (/\boutlet\b/i.test(t) ? 'Outlet' : '');
    t = t.replace(/\b(inlet|outlet)\b/ig, '').replace(/\s+/g, ' ').trim();
    return { name: t, side: side };
  }
  function sectionMap() {                     // heading -> the inputs of its section, in one pass in document order
    var f = form(), m = new Map(), cur = null;
    if (!f) return m;
    var out = function (e) { return e.closest('#rdsLib') || e.closest('table') || e.closest('.rq-block'); };
    Array.prototype.forEach.call(f.querySelectorAll('h1, p.text-3xl, input'), function (e) {
      if (e.tagName !== 'INPUT') { if (!out(e) && !e.closest('[id^="calc_"]')) { cur = e; m.set(e, []); } return; }
      if (cur && !out(e)) m.get(cur).push(e);
    });
    return m;
  }
  function hasOwnWs(inputs) {
    return inputs.some(function (e) { return e.type === 'text' && /(^|\(|\s)WS[-\s]/i.test(e.value || ''); });
  }
  function bar(name, side) {
    var d = document.createElement('div');
    d.className = 'rq-bar';
    d.innerHTML = '<span class="rq-lbl">Quality control:</span>' + Object.keys(TYPES).map(function (k) { return '<button type="button" class="rq-add" data-t="' + k + '">+ ' + esc(TYPES[k]) + '</button>'; }).join('') + '<div class="rq-list"></div>';
    d.dataset.param = name; d.dataset.side = side || '';
    Array.prototype.forEach.call(d.querySelectorAll('.rq-add'), function (b) { b.addEventListener('click', function () { var c = addCheck(d, b.dataset.t); try { linkRow(c); } catch (e) { if (window.console) console.error('RDS QC row', e); } }); });
    return d;
  }
  /* analyst feedback 30-10-2026 (Formulas.docx): a titrimetric check (total / calcium hardness, calcium, alkalinity)
     is calculated from its titration, as the chloride working standard is: each reading = (final - initial burette)
     x factor / sample volume; the readings, their working and the average are saved and printed. */
  var TITR = [
    { re: /hardness/i, label: 'EDTA factor B (mg CaCO3 per mL EDTA)', k: 'B', mult: 1000, page: ['hardness_edta_b'], key: 'B_hardness', what: 'total hardness', eg: 'e.g. 1.000',
      text: function (f) { return '(Final - Initial) X ' + f + ' X 1000 / Volume of sample'; } },
    { re: /^calcium\b/i, label: 'EDTA factor B (mg CaCO3 per mL EDTA)', k: 'B', mult: 400.8, page: ['calcium_edta_b'], key: 'B_calcium', what: 'calcium', eg: 'e.g. 1.000',
      text: function (f) { return '(Final - Initial) X ' + f + ' X 400.8 / Volume of sample'; } },
    { re: /alkalinity/i, label: 'Normality of the acid N (any strength: 0.02, 0.1, 0.2 ...)', k: 'N', mult: 50000, page: ['alkalinity_1_3', 'alkalinity_2_3', 'alkalinity_3_3'], key: 'N_alkalinity', what: 'alkalinity', eg: 'e.g. 0.02',
      text: function (f) { return '(Final - Initial) X ' + f + ' X 50000 / Volume of sample'; } }
  ];
  /* The factor is not fixed (owner 30-10-2026: "dynamic, for any scenario"). It is taken, in this order, from the page's
     own titration section (alkalinity normality, EDTA factor B) for the same side - kept in step while the analyst has
     not typed one in the check - else the value last used in this browser, else it must be entered. */
  function titrFor(param) { return TITR.filter(function (t) { return t.re.test(String(param || '').replace(/\*+/g, '').trim()); })[0] || null; }
  function titrPage(t, side) {
    var sfx = side === 'Inlet' ? '_inlet' : (side === 'Outlet' ? '_outlet' : ''), hit = null;
    (t.page || []).some(function (id) { var e = $(id + sfx) || (sfx ? null : $(id)); if (e && String(e.value).trim() !== '') { hit = e; return true; } return false; });
    return hit;
  }
  function lastUsed(t) { try { return localStorage.getItem('rds_titr_' + t.key) || ''; } catch (e) { return ''; } }
  function remember(t, v) { try { if (v !== '' && v !== null && v !== undefined) localStorage.setItem('rds_titr_' + t.key, String(v)); } catch (e) { } }
  function titrHtml(p, t, side) {
    return '<details class="rq-titr" open><summary>Readings from the titration</summary><div class="rq-grid">' +
      '<label>' + esc(t.label) + '<input type="number" step="any" min="0" class="rq-tf" name="' + p + '_tf" placeholder="' + esc(t.eg) + '"></label>' +
      '<span class="rq-tsrc"></span><input type="hidden" name="' + p + '_tfsrc"></div>' +
      [1, 2, 3].map(function (i) {
        return '<div class="rq-grid"><span class="rq-tl">Reading ' + i + '</span>' +
          '<label>Burette initial (mL)<input type="number" step="any" class="rq-ti" data-i="' + i + '" name="' + p + '_ti' + i + '"></label>' +
          '<label>Burette final (mL)<input type="number" step="any" class="rq-tz" data-i="' + i + '" name="' + p + '_tz' + i + '"></label>' +
          '<label>Volume of sample (mL)<input type="number" step="any" class="rq-tv" data-i="' + i + '" name="' + p + '_tv' + i + '"></label></div>';
      }).join('') + '<p class="rq-tnote">Formula: ' + esc(t.text(t.k)) + '. The readings below are calculated from these entries.</p></details>';
  }
  function titrSetup(blk, t, side) {          // fills the factor and keeps it in step with the page until the analyst types one
    var box = blk.querySelector('.rq-tf'); if (!box) return;
    var src = blk.querySelector('.rq-tsrc'), srcH = blk.querySelector('[name$="_tfsrc"]');
    function show(txt) { if (src) src.textContent = txt; if (srcH) srcH.value = txt; }
    function fill() {
      if (box.dataset.own) return;
      var pg = titrPage(t, side), lu = lastUsed(t);
      if (pg) { box.value = pg.value; show('taken from the ' + t.what + ' section of this RDS'); }
      else if (lu) { box.value = lu; show('as last used - confirm it'); }
      else { box.value = ''; show(t.k === 'N' ? 'enter the normality of the acid used' : 'enter factor B of today\'s standardisation'); }
    }
    fill();
    box.addEventListener('input', function () { box.dataset.own = '1'; show('entered for this check'); remember(t, box.value); });
    (t.page || []).forEach(function (id) {
      [id, id + '_inlet', id + '_outlet'].forEach(function (x) {
        var e = $(x); if (!e || e.dataset.rqTitr) return; e.dataset.rqTitr = '1';
        e.addEventListener('change', function () { Array.prototype.forEach.call(document.querySelectorAll('.rq-block'), function (b) { if (b._titrFill) { b._titrFill(); compute(b, false); } }); });
      });
    });
    blk._titrFill = fill;
  }
  function titrLines(blk) {                   // fills Reading 1-3 from the titration entries; returns the working lines
    var t = titrFor(val(blk, 'param')); if (!t || !blk.querySelector('.rq-titr')) return [];
    var fct = num(val(blk, 'tf')), lines = [], any = false;
    [1, 2, 3].forEach(function (i) {
      var a = num(val(blk, 'ti' + i)), b = num(val(blk, 'tz' + i)), v = num(val(blk, 'tv' + i));
      if (a === null && b === null && v === null) return;
      any = true;
      if (a === null || b === null || !v || fct === null) return;
      var r = (b - a) * fct * t.mult / v;
      setv(blk, 'r' + i, rd(r, 4));
      lines.push('Reading ' + i + ' = (' + rd(b) + ' - ' + rd(a) + ') X ' + rd(fct) + ' X ' + t.mult + ' / ' + rd(v) + ' = ' + rd(r, 4));
    });
    if (lines.length) { lines.unshift((t.k === 'N' ? 'Normality of the acid N = ' + rd(fct) + ' N' : 'EDTA factor B = ' + rd(fct) + ' mg CaCO3 / mL')); remember(t, fct); }
    var src = blk.querySelector('.rq-tsrc');
    if (any && fct === null && src) src.textContent = 'enter the ' + (t.k === 'N' ? 'normality' : 'factor B') + ' - the readings are not calculated without it';
    return lines;
  }
  function addCheck(barEl, type, opts) {
    opts = opts || {};
    var n = ++nQc, p = 'qc_' + n, param = barEl.dataset.param, side = barEl.dataset.side;
    var isPh = /^ph\b/i.test(param);
    var blk = document.createElement('div');
    blk.className = 'rq-block'; blk.dataset.type = type;
    if (opts.id) blk.id = opts.id;
    blk.innerHTML =
      '<div class="rq-head"><b>' + esc(TYPES[type]) + '</b><span>' + esc(param + (side ? ' (' + side + ')' : '')) + '</span>' +
      '<button type="button" class="rq-del" title="Remove this check">Remove</button></div>' +
      '<div class="rq-grid">' +
      '<label>Identification<input type="text" name="' + p + '_ident" value="' + esc(opts.ident || '') + '" placeholder="' + (type === 'WS' ? 'e.g. WS-' + esc(param.split(' ')[0]) + '-500ppm' : 'material / lot no.') + '"></label>' +
      '<label>' + (type === 'CRM' ? 'Certified value' : 'True value') + '<input type="number" step="any" name="' + p + '_true"></label>' +
      (type !== 'WS' ? '<label>Uncertainty ± (optional)<input type="number" step="any" name="' + p + '_u"></label>' : '') +
      '<label>Unit<input type="text" name="' + p + '_unit" value="' + esc(isPh ? 'pH units' : (opts.unit || 'mg/L')) + '"></label>' +
      '</div>' + (titrFor(param) && !isPh ? titrHtml(p, titrFor(param), side) : '') + '<div class="rq-grid">' +
      [1, 2, 3].map(function (i) { return '<label>Reading ' + i + '<input type="number" step="any" class="rq-r" name="' + p + '_r' + i + '"></label>'; }).join('') +
      (isPh
        ? '<label>Acceptance ± (pH units)<input type="number" step="any" name="' + p + '_abs" value="0.05"></label>'
        : '<label>Acceptance, recovery from (%)<input type="number" step="any" name="' + p + '_lo" value="90"></label><label>to (%)<input type="number" step="any" name="' + p + '_hi" value="110"></label>') +
      '</div><div class="rq-res"><button type="button" class="rq-eq">=</button>' +
      '<label>Mean<input type="text" readonly name="' + p + '_mean"></label>' +
      '<label>' + (isPh ? 'Difference' : 'Recovery (%)') + '<input type="text" readonly name="' + p + '_rec"></label>' +
      '<label>Verdict<input type="text" readonly class="rq-verdict" name="' + p + '_verdict"></label></div>' +
      '<div class="rq-work"></div>' +
      '<input type="hidden" name="' + p + '_type" value="' + type + '"><input type="hidden" name="' + p + '_param" value="' + esc(param) + '"><input type="hidden" name="' + p + '_side" value="' + esc(side) + '">' +
      '<input type="hidden" class="rq-print" name="qc_print_' + String(n).padStart(3, '0') + '">';
    barEl.querySelector('.rq-list').appendChild(blk);
    blk.querySelector('.rq-del').addEventListener('click', function () {
      var tr = rowOf(blk), sd = (blk.querySelector('[name$="_side"]') || {}).value || '';
      if (tr && snoOf(tr).indexOf('.') > 0) {                  // R8.1: the check's own row (also a row made by the table's "+")
        var left = (tr.dataset.rqSides || '').replace(sd, '');
        if (sd && left) {                                         // the other side's check keeps the row
          tr.dataset.rqSides = left; var k = snoOf(tr).replace('.', '_'), f = tr.querySelector('[name="' + (sd === 'Inlet' ? 'inlet_' : 'outlet_') + k + '"]'); if (f) f.value = '';
          var other = Array.prototype.filter.call(document.querySelectorAll('.rq-block'), function (b) { return b !== blk && rowOf(b) === tr; })[0];
          if (other && blk.id && !other.id) { other.id = blk.id; blk.id = ''; }
        } else tr.remove();
      }
      blk.remove();
    });
    if (titrFor(param) && !isPh) titrSetup(blk, titrFor(param), side);
    blk.querySelector('.rq-eq').addEventListener('click', function () { compute(blk, true); });
    blk.addEventListener('input', function () { compute(blk, false); });
    return blk;
  }
  function val(blk, f) { var e = blk.querySelector('[name$="_' + f + '"]'); return e ? e.value : ''; }
  function setv(blk, f, v) { var e = blk.querySelector('[name$="_' + f + '"]'); if (e) e.value = v; }
  function compute(blk, loud) {
    var tlines = titrLines(blk);
    var type = blk.dataset.type, tv = num(val(blk, 'true')), reads = [1, 2, 3].map(function (i) { return num(val(blk, 'r' + i)); }).filter(function (x) { return x !== null; });
    var out = { mean: '', rec: '', verdict: '' }, abs = blk.querySelector('[name$="_abs"]'), work = [];
    if (reads.length) {
      var m = reads.reduce(function (a, b) { return a + b; }, 0) / reads.length;
      out.mean = rd(m, 4) + ' (n = ' + reads.length + ')';
      // R8 (chemist feedback, point 10): the working is shown and printed, not only the outcome
      work = work.concat(tlines);
      work.push('Mean = ' + (reads.length > 1 ? '(' + reads.map(function (x) { return rd(x); }).join(' + ') + ') / ' + reads.length : rd(reads[0])) + ' = ' + rd(m, 4) + (val(blk, 'unit') ? ' ' + val(blk, 'unit') : ''));
      if (tv !== null && tv !== 0) {
        if (abs) {
          var d = m - tv, lim = num(abs.value);
          out.rec = (d >= 0 ? '+' : '') + rd(d, 3);
          work.push('Difference = ' + rd(m, 4) + ' - ' + rd(tv) + ' = ' + out.rec);
          if (lim !== null) out.verdict = Math.abs(d) <= lim + 1e-12 ? 'Within acceptance' : 'Outside acceptance';
        } else {
          var rec = 100 * m / tv, lo = num(val(blk, 'lo')), hi = num(val(blk, 'hi'));
          out.rec = rd(rec, 1);
          work.push('Recovery = ' + rd(m, 4) + ' / ' + rd(tv) + ' X 100 = ' + out.rec + ' %');
          if (lo !== null && hi !== null) out.verdict = (rec >= lo - 1e-9 && rec <= hi + 1e-9) ? 'Within acceptance' : 'Outside acceptance';
        }
      } else if (loud) alert('Enter the ' + (type === 'CRM' ? 'certified' : 'true') + ' value of the ' + type + '.');
    } else if (loud) alert('Enter at least one reading of the ' + type + '.');
    setv(blk, 'mean', out.mean); setv(blk, 'rec', out.rec); setv(blk, 'verdict', out.verdict);
    var wk = blk.querySelector('.rq-work'); if (wk) wk.innerHTML = work.map(esc).join('<br>');
    if (reads.length) { try { fillRow(blk, rd(m, 4), out.verdict); } catch (e) { if (window.console) console.error('RDS QC row', e); } }
    var ve = blk.querySelector('.rq-verdict');
    ve.classList.toggle('rq-ok', /^Within/.test(out.verdict)); ve.classList.toggle('rq-bad', /^Outside/.test(out.verdict));
    blk.querySelector('.rq-print').value = reads.length ? JSON.stringify({
      type: type, type_label: TYPES[type], parameter: val(blk, 'param'), side: val(blk, 'side'), ident: val(blk, 'ident'),
      true_value: val(blk, 'true'), u: val(blk, 'u'), unit: val(blk, 'unit'), readings: [1, 2, 3].map(function (i) { return val(blk, 'r' + i); }),
      mean: out.mean, result: out.rec, mode: abs ? 'abs' : 'rec', work: work, lo: val(blk, 'lo'), hi: val(blk, 'hi'), abs: abs ? abs.value : '', verdict: out.verdict
    }) : '';
  }
  /* R8 (owner request 28-10-2026): a WS / RM / CRM check gets its row in the results table, as the table's "+" gives a
     CRM row its calculation. The row is the check's: S.no N.k, parameter "<name> WS|RM|CRM", result = the check's mean,
     remarks = its verdict; its id links them (calc_N_k, the page's own convention), so removing either removes both. */
  function tbody() { return document.querySelector('#qcForm tbody'); }
  function snoOf(tr) { return ((tr.querySelector('.main-sno') || {}).textContent || '').trim(); }
  window.rdsMaxSub = function (base) {
    var mx = 0;
    Array.prototype.forEach.call(document.querySelectorAll('#qcForm tbody tr'), function (tr) {
      var s = snoOf(tr); if (s.indexOf(base + '.') === 0) { var k = parseInt(s.slice(base.length + 1), 10); if (k > mx) mx = k; }
    });
    return mx;
  };
  function rowOf(blk) {
    var m = /^calc_(\d+)_(\d+)$/.exec(blk.id || ''), want = blk.dataset.rqRow || (m ? m[1] + '.' + m[2] : '');
    if (!want) return null;
    return Array.prototype.filter.call(document.querySelectorAll('#qcForm tbody tr'), function (tr) { return snoOf(tr) === want; })[0] || null;
  }
  function mainRowFor(param) {
    return Array.prototype.filter.call(document.querySelectorAll('#qcForm tbody tr'), function (tr) {
      var s = snoOf(tr), pi = tr.querySelector('input[name^="parameter_"]');
      return s && s.indexOf('.') < 0 && pi && (bareName(pi.value) === bareName(param) || sameParam(param, pi.value));
    })[0] || null;
  }
  function linkRow(blk) {
    if (!blk || rowOf(blk)) return rowOf(blk);
    var bar = blk.closest('.rq-bar'), param = bar ? bar.dataset.param : '';
    var main = mainRowFor(param), body = tbody(); if (!main || !body) return null;
    var base = snoOf(main), side = bar ? bar.dataset.side : '';
    if (side) {                                                   // in-out: the inlet and the outlet check of a kind share a row
      var twin = Array.prototype.filter.call(body.querySelectorAll('tr'), function (r) {
        return r.dataset.rqLinked && r.dataset.rqType === blk.dataset.type && snoOf(r).indexOf(base + '.') === 0 && (r.dataset.rqSides || '').indexOf(side) < 0;
      })[0];
      if (twin) { twin.dataset.rqSides = (twin.dataset.rqSides || '') + side; blk.dataset.rqRow = snoOf(twin); return twin; }
    }
    var sub = base + '.' + (window.rdsMaxSub(base) + 1), key = sub.replace('.', '_');
    var tr = main.cloneNode(true);
    Array.prototype.forEach.call(tr.querySelectorAll('.select2-container'), function (x) { x.remove(); });
    var mainSel = Array.prototype.slice.call(main.querySelectorAll('select'));
    Array.prototype.forEach.call(tr.querySelectorAll('select'), function (sl, i) {
      sl.classList.remove('select2-hidden-accessible'); ['data-select2-id', 'aria-hidden', 'tabindex'].forEach(function (a) { sl.removeAttribute(a); });
      Array.prototype.forEach.call(sl.querySelectorAll('option'), function (o) { o.removeAttribute('data-select2-id'); });
      sl.style.display = ''; sl.value = mainSel[i] ? mainSel[i].value : '';            // same staff as the parameter's row
    });
    var sc = tr.querySelector('.main-sno'); if (sc) sc.textContent = sub;
    var pname = (main.querySelector('input[name^="parameter_"]') || {}).value || param;
    Array.prototype.forEach.call(tr.querySelectorAll('input, select'), function (el) {
      var nm = el.getAttribute('name'); if (!nm) return;
      var b0 = nm.split('_')[0]; el.setAttribute('name', b0 + '_' + key);
      if (el.tagName === 'INPUT') {
        if (b0 === 'parameter') el.value = String(pname).replace(/\s*\*+\s*$/, '') + ' ' + blk.dataset.type;
        else if (b0 === 'remarks') el.value = '';
        else if (b0 === 'result' || b0 === 'inlet' || b0 === 'outlet') { el.value = ''; el.readOnly = true; el.title = 'From the ' + blk.dataset.type + ' check of the calculation section'; }
      }
    });
    var add = tr.querySelector('.add-row-btn'); if (add) { add.classList.remove('add-row-btn', 'bg-blue-500', 'hover:bg-blue-600'); add.textContent = ''; add.disabled = true; add.style.visibility = 'hidden'; }
    tr.dataset.rqLinked = '1'; tr.dataset.rqType = blk.dataset.type; tr.dataset.rqSides = side || '';
    var after = main;
    Array.prototype.forEach.call(body.querySelectorAll('tr'), function (r) { if (snoOf(r).indexOf(base + '.') === 0) after = r; });
    after.insertAdjacentElement('afterend', tr);
    blk.id = 'calc_' + key;
    if (typeof window.initializeSelect2 === 'function') setTimeout(function () { try { window.initializeSelect2(); } catch (e) { /* page without select2 */ } }, 10);
    return tr;
  }
  /* R8.1: removing a row in the results table removes every check that writes to it (the pages removed at most one, and the
     DW manual page none, so an orphaned check could bring the row back) */
  document.addEventListener('click', function (e) {
    var btn = e.target && e.target.closest ? e.target.closest('.remove-row-btn, button.bg-red-500') : null;
    var tr = btn ? btn.closest('#qcForm tbody tr') : null;
    if (!tr || snoOf(tr).indexOf('.') < 0) return;
    Array.prototype.forEach.call(document.querySelectorAll('.rq-block'), function (b) { if (rowOf(b) === tr) b.remove(); });
  }, true);
  function fillRow(blk, mean, verdict) {
    var tr = rowOf(blk) || linkRow(blk); if (!tr) return;
    var side = (blk.querySelector('[name$="_side"]') || {}).value || '';
    var key = snoOf(tr).replace('.', '_');
    var target = side === 'Inlet' ? tr.querySelector('[name="inlet_' + key + '"]') : side === 'Outlet' ? tr.querySelector('[name="outlet_' + key + '"]') : null;
    target = target || tr.querySelector('[name="result_' + key + '"]') || tr.querySelector('[name="inlet_' + key + '"]') || tr.querySelector('[name="outlet_' + key + '"]');
    if (target) target.value = mean;
    var rm = tr.querySelector('[name="remarks_' + key + '"]'); if (rm && verdict) rm.value = verdict;
  }
  function qcBars() {
    var f = form(); if (!f) return;
    var hs = headings(), SM = sectionMap();
    hs.forEach(function (h) {
      if (!vis(h) || h.dataset.rq) return;
      var ins = SM.get(h) || [];
      if (!ins.some(function (e) { return e.type === 'number' && vis(e); })) return;      // a wrapper heading without a calculation
      var sn = sectionName(h); if (!sn.name) return;
      h.dataset.rq = '1';
      var b = bar(sn.name, sn.side);
      var edta = (function () { var n = h.parentElement && h.parentElement.nextElementSibling; return n && n.classList && n.classList.contains('rds-edta') ? n : null; })() ||
                 (h.nextElementSibling && h.nextElementSibling.classList.contains('rds-edta') ? h.nextElementSibling : null);
      if (edta) edta.insertAdjacentElement('afterend', b); else insertAfterHeading(h, b);
      var acc = accredited(sn.name);
      if (acc && !hasOwnWs(ins) && !(sn.side === 'Outlet' && hs.some(function (o) { return o !== h && vis(o) && sectionName(o).name === sn.name && sectionName(o).side === 'Inlet'; })))
        DEFAULT_CHECKS.forEach(function (t) { addCheck(b, t, { ident: t === 'WS' ? 'WS-' + acc + '-' : '' }); });
    });
    Array.prototype.forEach.call(f.querySelectorAll('#rdsLib .rl-card, .rq-cardslot .rl-card'), function (c) {
      if (c.dataset.rq) return;
      c.dataset.rq = '1';
      var t = c.querySelector('.rl-title b'); if (!t || c.querySelector('input[data-k="val"]')) return;   // an observation has no check
      var m = t.textContent.match(/^(.*?)(?:\s*\((Inlet|Outlet)\))?$/);
      var b = bar(m[1].trim(), m[2] || '');
      var del = c.querySelector('.rl-del'); c.insertBefore(b, del || null);
      var acc2 = accredited(m[1]);
      if (acc2 && m[2] !== 'Outlet') DEFAULT_CHECKS.forEach(function (tp) { addCheck(b, tp, { ident: tp === 'WS' ? 'WS-' + acc2 + '-' : '' }); });
    });
  }
  function barFor(param) {
    var want = String(param || '').toLowerCase().replace(/\s+crm$/i, '').replace(/\*/g, '').trim();
    var lib = window.RDSLib, pn = lib ? String(lib.pageName(want) || want).toLowerCase().replace(/\*/g, '') : want;
    var bars = Array.prototype.filter.call(document.querySelectorAll('.rq-bar'), function (b) { return vis(b); });
    var key = function (s) { return lib ? lib.bare(s) : s; };
    return bars.filter(function (b) { var p = key(b.dataset.param.toLowerCase()); return p === key(want) || p === key(pn); })[0] ||
           bars.filter(function (b) { var p = key(b.dataset.param.toLowerCase()); return p && (key(pn).indexOf(p) === 0 || p.indexOf(key(pn)) === 0); })[0] || null;
  }
  /* the table's "+" adds a CRM row; where the page has no CRM block for the parameter the row gets a CRM check */
  var rowsBefore = null;
  document.addEventListener('click', function (e) {
    if (e.target && e.target.classList && e.target.classList.contains('add-row-btn')) rowsBefore = Array.prototype.slice.call(document.querySelectorAll('#qcForm tbody tr'));
  }, true);
  document.addEventListener('click', function (e) {
    if (!rowsBefore || !e.target || !e.target.closest || !e.target.closest('tbody')) return;
    var before = rowsBefore; rowsBefore = null;
    var added = Array.prototype.filter.call(document.querySelectorAll('#qcForm tbody tr'), function (r) { return before.indexOf(r) < 0; })[0];
    if (!added) return;
    var sno = ((added.querySelector('.main-sno') || {}).textContent || '').trim(); if (!sno) return;
    var cid = 'calc_' + sno.replace('.', '_'), blk = $(cid);
    if (blk && !/not supported/i.test(blk.textContent)) return;          // the page's own CRM block
    if (blk) blk.remove();
    var pi = added.querySelector('input[name^="parameter_"]'), param = pi ? pi.value : '';
    var b = barFor(param);
    if (!b) {
      var host = $('rqOther');
      if (!host) {
        host = document.createElement('div'); host.id = 'rqOther'; host.className = 'rq-other';
        host.innerHTML = '<h2>Quality-control checks</h2>';
        var lib = $('rdsLib'); if (lib) lib.insertAdjacentElement('beforebegin', host); else form().appendChild(host);
      }
      b = bar(param.replace(/\s+CRM$/i, ''), ''); host.appendChild(b);
    }
    var c = addCheck(b, 'CRM', { id: cid, ident: '' });
    c.scrollIntoView({ block: 'center', behavior: 'smooth' });
  });

  /* ------------------------------------------------------------------ 3. BOD triplicate (WW) */
  function bodTriplicate() {
    if (PAGE !== 'ww' || !window.RDSLib || !window.RDSLib.addCard) return;
    var SM = sectionMap();
    headings().forEach(function (h) {
      if (!vis(h) || h.dataset.rqBod) return;
      var sn = sectionName(h);
      if (!/^bod\b/i.test(sn.name) && !/biological oxygen/i.test(sn.name)) return;
      var ins = SM.get(h) || [];
      if (!ins.some(function (e) { return /^bod_/.test(e.name || ''); })) return;
      h.dataset.rqBod = '1';
      var hold = document.createElement('div'); hold.className = 'rq-bod';
      hold.innerHTML = '<p class="rq-bod-note">Triplicate determination: enter each replicate; the average is the reported result.</p>';
      var rep = (h.querySelector('.rds-rep') || {}).textContent || '';
      rep = rep.replace(/^reported:\s*/i, '').trim() || null;
      var nm = 'Biological Oxygen Demand (BOD5)';
      window.RDSLib.addCard({ parameter: nm, method: 'HACH 10099' }, sn.side, rep, { calc: 'reading', out: 'R' }, hold);
      window.RDSLib.addCard({ parameter: nm, method: 'APHA 5210 B / 4500-O C' }, sn.side, rep, { calc: 'bod', out: 'R' }, hold);
      Array.prototype.forEach.call(hold.querySelectorAll('.rl-card'), function (c) { c.classList.add('rq-libcard'); });
      // the single-determination fields of this section go into a closed panel (kept, still saved and printed)
      var blocks = [], node = h.parentElement && h.parentElement.children.length === 1 ? h.parentElement : h;
      var hs = headings(), next = hs[hs.indexOf(h) + 1] || null;
      var sib = node.nextElementSibling;
      while (sib && !(next && (sib === next || sib.contains(next))) && !sib.classList.contains('rq-bar') && !sib.classList.contains('rds-edta')) { blocks.push(sib); sib = sib.nextElementSibling; }
      var det = document.createElement('details'); det.className = 'rq-old';
      det.innerHTML = '<summary>Single-determination layout (previous)</summary>';
      if (blocks.length) { blocks[0].insertAdjacentElement('beforebegin', det); blocks.forEach(function (b) { det.appendChild(b); }); }
      (det.parentNode ? det : node).insertAdjacentElement('beforebegin', hold);
      if (!det.parentNode) node.insertAdjacentElement('afterend', hold);
    });
  }

  /* ------------------------------------------------------------------ 4. empty sample, section list */
  function emptyNotice(show) {
    var n = $('rqEmpty');
    if (!show) { if (n) n.remove(); return; }
    if (n) return;
    n = document.createElement('div'); n.id = 'rqEmpty'; n.className = 'rq-empty';
    n.innerHTML = '<b>No reported result on this sample\'s test report.</b> The report has no parameter with a result (or no parameter ticked at registration), so there is nothing to calculate. Complete the test report first, or choose another sample.';
    var t = document.querySelector('#qcForm table'); if (t) t.insertAdjacentElement('beforebegin', n); else if (form()) form().insertBefore(n, form().firstChild);
  }
  function jumpList() {
    var btn = $('rqJump');
    if (!btn) {
      btn = document.createElement('div'); btn.id = 'rqJump';
      btn.innerHTML = '<button type="button" class="rq-jbtn">Sections ▾</button><div class="rq-jlist"></div>';
      document.body.appendChild(btn);
      btn.querySelector('.rq-jbtn').addEventListener('click', function () { fill(); btn.classList.toggle('open'); });
      document.addEventListener('click', function (e) { if (!btn.contains(e.target)) btn.classList.remove('open'); });
    }
    function fill() {
      var list = btn.querySelector('.rq-jlist'); list.innerHTML = '';
      var items = headings().filter(function (h) { return vis(h) && h.dataset.rq; }).map(function (h) { var s = sectionName(h); return [s.name + (s.side ? ' (' + s.side + ')' : ''), h]; });
      Array.prototype.forEach.call(document.querySelectorAll('#rdsLib .rl-card, .rq-cardslot .rl-card'), function (c) { if (vis(c)) items.push([(c.querySelector('.rl-title b') || {}).textContent + (c.closest('#rdsLib') ? ' (library)' : ''), c]); });
      items.sort(function (a, b) { return (a[1].compareDocumentPosition(b[1]) & Node.DOCUMENT_POSITION_FOLLOWING) ? -1 : 1; });
      if (!items.length) { list.innerHTML = '<p>No calculation on the page yet.</p>'; return; }
      items.forEach(function (it) { var a = document.createElement('a'); a.href = '#'; a.textContent = it[0]; a.addEventListener('click', function (e) { e.preventDefault(); btn.classList.remove('open'); it[1].scrollIntoView({ block: 'start', behavior: 'smooth' }); }); list.appendChild(a); });
    }
  }

  /* ------------------------------------------------------------------ 5. sections in the order of the result table (R6) */
  function bareName(x) { return (window.RDSLib ? window.RDSLib.bare(x) : String(x || '').toLowerCase()).replace(/\b(inlet|outlet)\b/g, '').replace(/\s+/g, ' ').trim(); }
  function sameParam(head, row) {
    var lib = window.RDSLib, h = bareName(head), keys = [bareName(row)];
    if (lib) keys.push(bareName(lib.pageName(row) || ''));
    var ab = String(row || '').match(/\(([^)]+)\)/);                  // "Biological Oxygen Demand(BOD)5" -> BOD
    if (ab && !/^as\b/i.test(ab[1].trim())) keys.push(bareName(ab[1]));
    if (/\bmbas\b/.test(h) && /\bmbas\b/i.test(row)) return true;
    return keys.some(function (k) {
      if (!k || !h) return false;
      if (h === k || h.indexOf(k + ' ') === 0 || k.indexOf(h + ' ') === 0) return true;
      var hw = h.split(' ')[0], kw = k.split(' ')[0];                     // "Hardness" / "Total Hardness as CaCO3", "Phenolic"
      var gen = /^(total|free|residual|combined|dissolved|suspended|biological|chemical|oxygen|demand|solids|chlorine)$/;
      return (hw.length >= 5 && !gen.test(hw) && k.split(' ').indexOf(hw) >= 0) || (kw.length >= 5 && !gen.test(kw) && h.split(' ').indexOf(kw) >= 0);
    });
  }
  var ordered = false;
  function orderSections() {
    var f = form(); if (!f || ordered) return;
    var rows = Array.prototype.filter.call(f.querySelectorAll('tbody tr'), function (tr) {
      var sn = ((tr.querySelector('.main-sno') || {}).textContent || '').trim(); return sn && sn.indexOf('.') < 0;
    }).map(function (tr) { return ((tr.querySelector('input[name^="parameter_"]') || {}).value || '').trim(); });
    if (rows.length < 2) return;
    ordered = true;
    var kids = Array.prototype.slice.call(f.children);
    var stopper = function (n) { return n.querySelector && (n.id === 'rdsLib' || n.id === 'rqOther' || n.querySelector('#rdsLib, #rqOther, button[type=submit], table') || n.matches('button[type=submit], table')); };
    var tops = [];
    headings().forEach(function (h) {
      if (!vis(h) || !h.dataset.rq) return;
      var t = h; while (t.parentElement && t.parentElement !== f) t = t.parentElement;
      if (t.parentElement !== f || stopper(t)) return;
      var i = kids.indexOf(t);
      var key = rows.length + 1000 + i, nm = sectionName(h).name;
      var exact = rows.map(bareName).indexOf(bareName(nm));
      if (exact >= 0) key = exact; else rows.some(function (r, ri) { if (sameParam(nm, r)) { key = ri; return true; } return false; });
      var last = tops[tops.length - 1];
      if (last && last.i === i) { last.key = Math.min(last.key, key); return; }
      tops.push({ i: i, key: key });
    });
    if (tops.length < 2) return;
    var groups = tops.map(function (t, g) {
      var end = g + 1 < tops.length ? tops[g + 1].i : kids.length, nodes = [];
      for (var j = t.i; j < end; j++) {
        if (g + 1 === tops.length && j > t.i && (stopper(kids[j]) || (vis(kids[j]) && !/dynamic-.*-calcs/.test(kids[j].className || '')))) break;
        nodes.push(kids[j]);
      }
      return { key: t.key, nodes: nodes, i: t.i };
    });
    // library cards join the flow at their parameter's place in the table
    Array.prototype.forEach.call(document.querySelectorAll('#rdsLib .rl-cards > .rl-card'), function (c) {
      var t = c.querySelector('.rl-title b'); if (!t) return;
      var nm = t.textContent.replace(/\s*\((Inlet|Outlet)\)\s*$/, ''), key = -1;
      key = rows.indexOf(nm);
      if (key < 0) key = rows.map(bareName).indexOf(bareName(nm));
      if (key < 0) rows.some(function (r, ri) { if (sameParam(nm, r)) { key = ri; return true; } return false; });
      if (key < 0) return;
      var slot = document.createElement('div'); slot.className = 'rq-cardslot';
      slot.appendChild(c);
      groups.push({ key: key + 0.5, nodes: [slot], i: 1e6 });
    });
    groups.sort(function (a, b) { return a.key - b.key || a.i - b.i; });
    var mark = document.createElement('div'); f.insertBefore(mark, kids[tops[0].i]);
    groups.forEach(function (g) { g.nodes.forEach(function (n) { f.insertBefore(n, mark); }); });
    mark.remove();
    var lib = document.getElementById('rdsLib');
    if (lib && !lib.querySelector('.rl-card')) { var hd = lib.querySelector('.rl-head span'); if (hd) hd.textContent = 'Every parameter of this sample now sits in the order of the result table above; add a calculation here when one is needed.'; }
  }

  /* ------------------------------------------------------------------ save check, styles, hooks */
  var origSave = window.rdsBeforeSave;
  window.rdsBeforeSave = function (data) {
    var miss = edtaMissing();
    if (miss.length) { alert('Enter the EDTA factor B for ' + miss.join(', ') + ' (QA RDS-23): the readings depend on it.'); return false; }
    Array.prototype.forEach.call(document.querySelectorAll('.rq-block'), function (b) {
      compute(b, false);
      var pr = b.querySelector('.rq-print'); if (data && pr) data[pr.name] = pr.value;
    });
    Array.prototype.forEach.call(document.querySelectorAll('.rds-edta input'), function (i) { if (data) data[i.name] = i.value; });
    Array.prototype.forEach.call(document.querySelectorAll('#qcForm tbody tr'), function (tr) {   // R8: the checks' rows
      if (!tr.dataset.rqLinked || !data) return;
      var base = snoOf(tr).split('.')[0], main = Array.prototype.filter.call(document.querySelectorAll('#qcForm tbody tr'), function (r) { return snoOf(r) === base; })[0];
      var ms = main ? Array.prototype.slice.call(main.querySelectorAll('select')) : [];
      Array.prototype.forEach.call(tr.querySelectorAll('select'), function (sl, i) {      // staff of the parameter's row when not chosen
        if (!sl.value && ms[i] && ms[i].value) { sl.value = ms[i].value; if (window.jQuery) window.jQuery(sl).trigger('change'); }
      });
      Array.prototype.forEach.call(tr.querySelectorAll('input[name], select[name]'), function (i) { data[i.name] = i.value; });
    });
    var incomplete = [];                                          // R7: a check printed with "WS-Hardness-" or no true value
    Array.prototype.forEach.call(document.querySelectorAll('.rq-block'), function (b) {
      if (![1, 2, 3].some(function (i) { return String(val(b, 'r' + i)).trim() !== ''; })) return;
      var id = String(val(b, 'ident')).trim(), what = b.dataset.type + ' - ' + val(b, 'param') + (val(b, 'side') ? ' (' + val(b, 'side') + ')' : '');
      if (!id || /-$/.test(id)) incomplete.push(what + ': identification "' + id + '" is incomplete');
      if (String(val(b, 'true')).trim() === '') incomplete.push(what + ': no ' + (b.dataset.type === 'CRM' ? 'certified' : 'true') + ' value');
    });
    Array.prototype.forEach.call(document.querySelectorAll('#qcForm input'), function (i) {   // R7: a negative result is a reading error
      if (i.disabled || i.closest('table') || !/ans|result/i.test((i.name || '') + ' ' + (i.id || ''))) return;
      if (/lsi|langel|orp|redox|saturation|temp|index|rec|diff/i.test((i.name || '') + ' ' + (i.id || ''))) return;
      var v = parseFloat(i.value); if (isFinite(v) && v < 0) incomplete.push((i.name || i.id) + ' = ' + i.value + ' (negative result - check the readings)');
    });
    if (incomplete.length && !confirm('Please check before saving:\n- ' + incomplete.join('\n- ') + '\n\nPress OK to save as it is, or Cancel to complete them.')) return false;
    return typeof origSave === 'function' ? origSave(data) : true;
  };

  var css = document.createElement('style');
  css.textContent =
    '.rds-edta{margin:10px 0 18px;padding:10px 14px;border:1px solid #fcd34d;border-left:4px solid #d97706;border-radius:8px;background:#fffbeb;max-width:760px}' +
    '.rds-edta label{display:flex;flex-wrap:wrap;gap:10px;align-items:center;font-size:14px}.rds-edta label span{color:#78350f;font-size:12.5px}' +
    '.rds-edta input{width:140px!important}.rds-edta-note{font-size:12px;color:#92400e;margin:6px 0 0}.rds-edta-warn{font-weight:700}' +
    '.rds-bmark{color:#b45309;white-space:nowrap}' +
    '.rq-bar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:8px 0 16px;font-size:13px}.rq-lbl{font-weight:700;color:#334155}' +
    '.rq-add{border:1px dashed #0f5132;color:#0f5132;background:#f0fdf4;border-radius:999px;padding:4px 12px;font-size:12.5px;font-weight:600}.rq-add:hover{background:#dcfce7}' +
    '.rq-list{flex-basis:100%}' +
    '.rq-block{border:1px solid #cbd5e1;border-left:4px solid #1e40af;border-radius:8px;padding:10px 12px;margin:8px 0;background:#f8fafc;position:relative;max-width:1100px}' +
    '.rq-head{display:flex;gap:10px;align-items:baseline;font-size:14px;padding-right:70px}.rq-head span{color:#475569;font-size:13px}' +
    '.rq-del{position:absolute;top:8px;right:10px;font-size:12px;color:#b91c1c;background:none;border:none;cursor:pointer}' +
    '.rq-grid,.rq-res{display:flex;flex-wrap:wrap;gap:10px;align-items:flex-end;margin-top:8px}' +
    '.rq-grid label,.rq-res label{display:flex;flex-direction:column;font-size:12px;color:#475569;gap:3px}' +
    '.rq-grid input,.rq-res input{border:1px solid #cbd5e1;border-radius:6px;padding:6px 8px;width:150px!important;font-size:13px;min-height:34px}' +
    '.rq-work{margin-top:8px;font-size:13px;color:#1e293b;font-family:ui-monospace,Consolas,monospace;line-height:1.6}' +
    '.rq-titr{margin:6px 0;border:1px dashed #cbd5e1;border-radius:8px;padding:6px 10px}.rq-titr summary{cursor:pointer;font-weight:700;color:#1e3a8a;font-size:13px}.rq-tl{font-weight:700;font-size:12.5px;align-self:center;min-width:80px}.rq-tnote{font-size:12px;color:#475569;margin:4px 0}.rq-tsrc{font-size:12px;color:#92400e;align-self:end;padding-bottom:6px}' +
    '.rq-res input[readonly]{background:#f1f5f9;font-weight:700}.rq-eq{background:#1e40af;color:#fff;border-radius:7px;padding:6px 16px}' +
    '.rq-ok{background:#f0fdf4!important;border-color:#22c55e!important;color:#166534}.rq-bad{background:#fef2f2!important;border-color:#ef4444!important;color:#991b1b}' +
    '.rq-other{margin:30px 0;padding:16px;border:1px solid #cbd5e1;border-radius:10px;background:#fff}.rq-other h2{font-size:20px;font-weight:700;color:#0f5132}' +
    '.rq-bod{margin:6px 0 14px}.rq-bod-note{font-size:13px;color:#0f5132;font-weight:600}.rq-old{margin:10px 0;border:1px dashed #cbd5e1;border-radius:8px;padding:6px 10px}.rq-old summary{cursor:pointer;color:#475569;font-size:13px}' +
    '.rq-cardslot{margin:6px 0 18px}.rq-cardslot .rl-card{max-width:1200px}' +
    '.rq-empty{margin:14px 0;padding:12px 16px;border:1px solid #fca5a5;border-left:4px solid #b91c1c;border-radius:8px;background:#fef2f2;color:#7f1d1d;font-size:14px}' +
    '#rqJump{position:fixed;right:18px;bottom:18px;z-index:60;font-size:13px}#rqJump .rq-jbtn{background:#0f5132;color:#fff;border-radius:999px;padding:8px 16px;font-weight:600;box-shadow:0 4px 12px rgba(0,0,0,.18)}' +
    '#rqJump .rq-jlist{display:none;position:absolute;right:0;bottom:44px;max-height:60vh;overflow:auto;min-width:260px;background:#fff;border:1px solid #cbd5e1;border-radius:10px;box-shadow:0 8px 24px rgba(0,0,0,.18);padding:6px}' +
    '#rqJump.open .rq-jlist{display:block}#rqJump a{display:block;padding:6px 10px;border-radius:6px;color:#0f172a}#rqJump a:hover{background:#f1f5f9}#rqJump p{padding:6px 10px;color:#64748b}';
  (document.head || document.documentElement).appendChild(css);

  /* R7 (owner 28-10-2026): the old microbiology boxes hold only a result (no calculation); the formula-library card of
     the same parameter carries the count calculation, so the old box is hidden and left out of the save */
  var MICRO = [['ecoli', /\be\s*\.?\s*-?\s*coli\b/], ['fecal', /^f(a)?ecal coliform/], ['bacteria', /bacterial count|\btbc\b/],
    ['enterobacteria', /enterobacter/], ['total_coliform', /^(total )?coliforms?\b/], ['fecalentero', /enterococc/], ['hetrobacteria', /heterotroph/]];
  function MANUALPAGE() { return /manual/.test(location.pathname); }
  function legacyMicro() {
    var f = form(); if (!f) return;
    var cards = Array.prototype.map.call(document.querySelectorAll('.rl-card .rl-title b'), function (b) {
      return String(b.textContent || '').toLowerCase().replace(/\*/g, '').replace(/\((inlet|outlet)\)\s*$/, '').replace(/\s+/g, ' ').trim();
    });
    if (!cards.length) return;
    MICRO.forEach(function (m) {
      Array.prototype.forEach.call(f.querySelectorAll('div.my-6.' + m[0]), function (box) {
        if (box.dataset.rqHid || box.style.display === 'none') return;
        if (box.querySelector('button')) return;                  // a box with its own calculation stays
        if (Array.prototype.some.call(box.querySelectorAll('input[name$="_ans"]'), function (i) { return String(i.value).trim() !== ''; }) && !/^(n\.?d\.?|)$/i.test(String((box.querySelector('input[name$="_ans"]') || {}).value || '').trim()) && MANUALPAGE()) return;   // R9: a result typed on a manual page stays
        if (!cards.some(function (c) { return m[1].test(c); })) return;
        box.style.display = 'none'; box.dataset.rqHid = '1';
        Array.prototype.forEach.call(box.querySelectorAll('input, select'), function (i) { i.disabled = true; });
      });
    });
  }
  /* R7: an empty dilution factor counted as 0 (result 0); it starts at 1 and stays editable */
  function dfDefault() {
    var f = form(); if (!f) return;
    Array.prototype.forEach.call(f.querySelectorAll('input[placeholder]'), function (i) {
      if (i.dataset.rqDf || i.closest('#rdsLib') || i.closest('table')) return;
      if (!/^\s*d\.?\s*f\.?\s*$/i.test(i.placeholder)) return;
      i.dataset.rqDf = '1';
      if (String(i.value).trim() === '') i.value = '1';
    });
  }
  function refresh() {
    try { legacyMicro(); } catch (e) { if (window.console) console.error('RDS micro', e); }
    try { dfDefault(); } catch (e) { if (window.console) console.error('RDS DF', e); }
    try { edtaBoxes(); } catch (e) { if (window.console) console.error('RDS EDTA', e); }
    try { bodTriplicate(); } catch (e) { if (window.console) console.error('RDS BOD', e); }
    try { qcBars(); } catch (e) { if (window.console) console.error('RDS QC', e); }
  }
  var orig = window.populateQCTable;
  if (typeof orig === 'function') {
    window.populateQCTable = function () {
      var res = orig.apply(this, arguments);
      try {
        var rows = document.querySelectorAll('#qcForm tbody tr').length;
        emptyNotice(rows === 0);
      } catch (e) { /* page without a table */ }
      refresh();
      try { orderSections(); } catch (e) { if (window.console) console.error('RDS order', e); }
      return res;
    };
  }
  var tmr = null;
  function later() { clearTimeout(tmr); tmr = setTimeout(refresh, 250); }
  function start() {
    refresh(); jumpList();
    var f = form();
    if (f && window.MutationObserver) new MutationObserver(function (ms) {
      if (ms.some(function (m) { return Array.prototype.some.call(m.addedNodes, function (n) { return n.nodeType === 1 && !(n.closest && (n.closest('.rq-bar') || n.closest('.rds-edta') || n.closest('.rq-bod'))) && !(n.classList && (n.classList.contains('rq-bar') || n.classList.contains('rds-edta') || n.classList.contains('rds-bmark') || n.classList.contains('rq-bod') || n.classList.contains('rq-old'))); }) || m.type === 'attributes'; })) later();
    }).observe(f, { childList: true, subtree: true, attributes: true, attributeFilter: ['style'] });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
  window.RDSQC = { refresh: refresh, accredited: accredited, addCheck: addCheck, edtaMissing: edtaMissing, ACCREDITED: ACCREDITED, compute: compute };
})();
