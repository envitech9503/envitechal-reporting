/* RDS WW - BOD and COD calculations (owner review 27-10-2026).
 *
 * Loaded by Add RDS WW and Add RDS WW (manual entry). Replaces the page's own "=" handlers for BOD and COD (single,
 * inlet and outlet sections) with:
 *   BOD (APHA 5210 B / 4500-O C):  BOD = [(D1 - D2) - S x Vs] / P,  S = (B1 - B2) / Vc  (seed-control bottle)
 *       P = sample volume / bottle volume, used at full precision (it was rounded to 3 decimals before use);
 *       warnings: DO depletion < 2.0 mg/L, residual DO < 1.0 mg/L, seed-control depletion < 2.0 mg/L, blank DO;
 *       HACH 10099: a blank dilution factor counts as 1 (it counted as 0).
 *   COD: blank D.F counts as 1 (it counted as 0); the average is over the replicates entered (the divisor was fixed at
 *       3); the working standard WS-COD-100 ppm shows its recovery (acceptance 90-110 %); an outlet working-standard
 *       block is added for inlet/outlet reports.
 *   Both: the calculated value is compared with the result on the test report (difference > 5 % is flagged).
 * The checks are written to read-only "Check" fields (bod_check*, cod_check*, cod_ws_check*) that are saved with the
 * RDS and printed on its PDF under the formula. Nothing is blocked: the analyst decides, the check is on record.
 */
(function () {
  'use strict';
  var SFX = ['', '_inlet', '_outlet'];
  var REPORT_TOL = 0.05;           // calculated vs reported: 5 %
  var WS_TRUE = 100, WS_LO = 90, WS_HI = 110;

  function $(id) { return document.getElementById(id); }
  function num(id) {
    var e = $(id); if (!e) return null;
    var s = String(e.value || '').trim(); if (s === '') return null;
    var v = parseFloat(s); return isFinite(v) ? v : null;
  }
  function put(id, v, dp) { var e = $(id); if (e) e.value = (v === null || v === undefined || !isFinite(v)) ? '' : (+v.toFixed(dp)); }
  function fmt(v, dp) { return (+v.toFixed(dp)).toString(); }

  function checkBox(afterEl, name) {
    var id = name; var box = $(id);
    if (!box && afterEl) {
      var wrap = document.createElement('div');
      wrap.className = 'rdsw-check';
      wrap.innerHTML = '<label>Check</label><input type="text" readonly id="' + id + '" name="' + id + '" placeholder="calculate to check">';
      var host = afterEl.closest('.flex.gap-2.items-center.my-6') || afterEl.closest('.flex') || afterEl.parentNode;
      host.parentNode.insertBefore(wrap, host.nextSibling);
      box = $(id);
    }
    return box;
  }
  function report(box, msgs) {
    if (!box) return;
    box.value = msgs.length ? msgs.join('; ') : 'OK';
    box.classList.toggle('rdsw-warn', msgs.length > 0);
    box.classList.toggle('rdsw-ok', msgs.length === 0);
  }
  /* the result on the test report, from the section heading ("BOD Outlet Calculation 40", "... calculations 75") */
  function reported(headId) {
    var h = $(headId); if (!h) return null;
    var m = String(h.textContent || '').match(/(-?\d+(?:\.\d+)?)\s*$/);
    return m ? parseFloat(m[1]) : null;
  }
  function vsReported(calc, rep, msgs) {
    if (rep === null || calc === null) return;
    var d = Math.abs(calc - rep), base = Math.max(Math.abs(rep), 1e-9);
    if (d / base > REPORT_TOL && d > 0.5) msgs.push('calculated ' + fmt(calc, 2) + ' differs from the reported ' + rep + ' by ' + fmt(100 * d / base, 1) + ' %');
  }

  /* ---------------- BOD ---------------- */
  function bodHach(s) {
    var r = num('bod_1' + s), df = num('bod_1_df' + s);
    if (r === null) { put('bod_1_ans' + s, null); return; }
    if (df === null) { df = 1; put('bod_1_df' + s, 1, 4); }
    put('bod_1_ans' + s, r * df, 3);
  }
  function bodP(s) {
    var sv = num('bod_sv' + s), tv = num('bod_tv' + s);
    if (sv === null || tv === null || tv === 0) return null;
    return sv / tv;
  }
  function bodPButton(s) {
    var p = bodP(s);
    if (p === null) { alert('Enter the sample volume and the bottle (total) volume.'); return; }
    put('bod_1_p' + s, p, 5); put('bod_divi' + s, p, 5);
  }
  function bodMain(s) {
    var msgs = [];
    var box = checkBox($('bod_param' + s) || $('bod_ans' + s), 'bod_check' + s);
    var P = bodP(s);
    if (P === null) { var typed = num('bod_1_p' + s); P = typed; }
    if (P === null || P === 0) { alert('P cannot be zero or empty: enter the sample volume and the bottle volume.'); return; }
    var d1 = num('bod_initial' + s), d2 = num('bod_final' + s);
    if (d1 === null || d2 === null) { alert('Enter the initial and the final DO of the sample.'); return; }
    var b1 = num('bod_seed_1' + s), b2 = num('bod_seed_2' + s), vc = num('bod_seed_ctrl' + s), vs = num('bod_seed_vol' + s);
    var seeded = [b1, b2, vc, vs].some(function (x) { return x !== null; });
    var corr = 0;
    if (seeded) {
      if (b1 === null || b2 === null || vc === null || vs === null || vc === 0) {
        alert('Seed correction: enter the seed-control initial and final DO, the seed volume in the seed-control bottle (Vc, mL) and the seed volume in the sample bottle (Vs, mL) - or clear all four if the sample was not seeded.');
        return;
      }
      corr = (b1 - b2) / vc * vs;
      if (b1 - b2 < 2.0) msgs.push('seed-control DO depletion ' + fmt(b1 - b2, 2) + ' mg/L is below 2.0');
    }
    if (d1 - d2 < 2.0) msgs.push('DO depletion ' + fmt(d1 - d2, 2) + ' mg/L is below 2.0 (APHA 5210 B)');
    if (d2 < 1.0) msgs.push('residual DO ' + fmt(d2, 2) + ' mg/L is below 1.0 (APHA 5210 B)');
    var bod = (d1 - d2 - corr) / P;
    if (bod < 0) msgs.push('negative result - check the entries');
    put('bod_ans' + s, bod, 3);
    put('bod_divi' + s, P, 5); put('bod_1_p' + s, P, 5);
    vsReported(bod, reported('bod_cal_head' + s), msgs);
    report(box, msgs);
  }

  /* ---------------- COD ---------------- */
  function codWS(s) {
    var vals = ['for_cod1' + s, 'for_cod2' + s, 'for_cod3' + s].map(num).filter(function (x) { return x !== null; });
    var box = checkBox($('cod_param' + s) || $('cod_ans' + s), 'cod_ws_check' + s);
    if (!vals.length) { alert('Enter at least one working-standard reading.'); return; }
    var avg = vals.reduce(function (a, b) { return a + b; }, 0) / vals.length;
    put('cod_divi1' + s, vals.length, 0); put('cod_ans' + s, avg, 4);
    var rec = 100 * avg / WS_TRUE, msgs = [];
    msgs.push('recovery ' + fmt(rec, 1) + ' % of ' + WS_TRUE + ' mg/L');
    var ok = rec >= WS_LO && rec <= WS_HI;
    if (!ok) msgs.push('outside ' + WS_LO + '-' + WS_HI + ' %');
    if (box) { box.value = msgs.join('; ') + (ok ? ' - acceptable' : ''); box.classList.toggle('rdsw-warn', !ok); box.classList.toggle('rdsw-ok', ok); }
  }
  function codAvg(s) {
    var n = 0, sum = 0;
    for (var k = 1; k <= 3; k++) {
      var v = num('for_cod1_' + k + s), df = num('for_cod1_' + k + '_df' + s);
      if (v === null) continue;
      if (df === null) { df = 1; put('for_cod1_' + k + '_df' + s, 1, 4); }
      sum += v * df; n++;
    }
    var box = checkBox($('cod_param_1' + s) || $('cod_ans_1' + s), 'cod_check' + s);
    if (!n) { alert('Enter at least one COD replicate.'); return; }
    var avg = sum / n;
    put('cod_divi' + s, n, 0); put('cod_ans_1' + s, avg, 4);
    var msgs = [];
    vsReported(avg, reported('COD_cal_head' + s), msgs);
    report(box, msgs);
  }

  /* ---------------- wiring: capture phase, before the page's own handlers ---------------- */
  var MAP = {};
  SFX.forEach(function (s) {
    MAP['bod_1_equal' + s] = function () { bodHach(s); };
    MAP['bod_2_equal' + s] = function () { bodPButton(s); };
    MAP['bod_equal' + s] = function () { bodMain(s); };
    MAP['cod_equal' + s] = function () { codWS(s); };
    MAP['cod_equal_1' + s] = function () { codAvg(s); };
  });
  document.addEventListener('click', function (e) {
    var b = e.target && e.target.closest && e.target.closest('button');
    if (!b || !MAP[b.id]) return;
    e.preventDefault(); e.stopImmediatePropagation(); e.stopPropagation();
    MAP[b.id]();
  }, true);

  /* ---------------- page enhancements (idempotent; sections appear after a sample is chosen) ---------------- */
  function enhanceBod(s) {
    var vs = $('bod_seed_vol' + s);
    if (vs && !$('bod_seed_ctrl' + s)) {
      var close = $('bod_seed_2' + s) && $('bod_seed_2' + s).nextElementSibling;   // the ")" after B2
      var div = document.createElement('p'); div.className = 'px-1'; div.textContent = '÷';
      var vc = document.createElement('input');
      vc.id = 'bod_seed_ctrl' + s; vc.name = 'bod_seed_ctrl' + s; vc.type = 'number'; vc.step = 'any';
      vc.placeholder = 'Vc (mL)'; vc.title = 'Seed volume in the seed-control bottle (mL)';
      vc.className = 'text-center p-2'; vc.style.width = '100px';
      if (close) { close.parentNode.insertBefore(vc, close.nextSibling); close.parentNode.insertBefore(div, vc); }
      var row = vs.parentNode;
      if (row && !row.querySelector('.rdsw-legend')) {
        var lg = document.createElement('div'); lg.className = 'rdsw-legend';
        lg.innerHTML = 'BOD = [(D1 − D2) − (B1 − B2) ÷ Vc × Vs] ÷ P &nbsp;•&nbsp; D1/D2 sample initial/final DO, B1/B2 seed-control initial/final DO, '
          + 'Vc seed in control bottle (mL), Vs seed in sample bottle (mL), P = sample volume ÷ bottle volume. Leave the seed boxes empty if the sample was not seeded.';
        var formulaRow = row.closest('.flex.gap-2.items-center.my-6') || row.parentNode;
        formulaRow.parentNode.insertBefore(lg, formulaRow.nextSibling);
      }
    }
    var labels = { bod_initial: 'D1 initial DO', bod_final: 'D2 final DO', bod_seed_1: 'B1 seed I.DO', bod_seed_2: 'B2 seed F.DO', bod_seed_vol: 'Vs (mL)' };
    Object.keys(labels).forEach(function (k) { var e = $(k + s); if (e) { e.placeholder = labels[k]; e.title = labels[k]; e.style.width = '96px'; } });
    ['bod_divi' + s].forEach(function (id) { var e = $(id); if (e) { e.readOnly = true; e.title = 'P = sample volume ÷ bottle volume (calculated)'; e.classList.add('rdsw-ro'); } });
    var p = $('bod_1_p' + s); if (p) { p.readOnly = true; p.classList.add('rdsw-ro'); }
  }
  function enhanceCod(s) {
    ['cod_divi' + s, 'cod_divi1' + s].forEach(function (id) {
      var e = $(id); if (e) { e.readOnly = true; e.title = 'Number of readings entered (calculated)'; e.classList.add('rdsw-ro'); }
    });
    for (var k = 1; k <= 3; k++) { var d = $('for_cod1_' + k + '_df' + s); if (d) d.placeholder = 'D.F (1)'; }
  }
  /* inlet/outlet reports: the outlet section has no working-standard block - add one like the inlet's */
  function addOutletWS() {
    var head = $('COD_cal_head_outlet');
    if (!head || $('cod_equal_outlet')) return;
    var block = document.createElement('div');
    block.className = 'space-y-2 cod my-6';
    block.innerHTML =
      '<input type="text" name="cod_head_outlet" value="WS-COD-100ppm (Outlet):">' +
      '<div class="flex gap-2 items-center my-6"><p class="font-bold">Formula :</p><div>' +
      '<div class="flex gap-2 items-center">' +
      '<input style="width:80px" id="for_cod1_outlet" name="for_cod1_outlet" placeholder="WS 1" class="text-center p-2" type="number" step="any"><p class="px-3"> + </p>' +
      '<input style="width:80px" id="for_cod2_outlet" name="for_cod2_outlet" placeholder="WS 2" class="text-center p-2" type="number" step="any"><p class="px-3"> + </p>' +
      '<input style="width:80px" id="for_cod3_outlet" name="for_cod3_outlet" placeholder="WS 3" class="text-center p-2" type="number" step="any"></div>' +
      '<hr class="my-2 border border-black"><div class="text-center"><input id="cod_divi1_outlet" name="cod_divi1_outlet" class="text-center p-2" type="number" step="any"></div></div>' +
      '<div class="flex gap-2 items-center"><button type="button" id="cod_equal_outlet" class="bg-blue-600 px-4 py-2 text-gray-200 rounded-lg">=</button>' +
      '<input id="cod_ans_outlet" name="cod_ans_outlet" class="p-2" type="number" step="any" placeholder="Average">' +
      '<input id="cod_param_outlet" name="cod_param_outlet" class="p-2" type="text" value="mg/L"></div></div>';
    var hostHead = head.closest('.space-y-2') || head.parentNode;
    hostHead.parentNode.insertBefore(block, hostHead.nextSibling);
  }
  function enhance() {
    SFX.forEach(function (s) { enhanceBod(s); enhanceCod(s); });
    addOutletWS();
    SFX.forEach(function (s) { enhanceCod(s); });
  }
  var css = document.createElement('style');
  css.textContent =
    '.bod input[type=text][name^=bod_head],.cod input[type=text][name^=cod_head]{min-width:min(520px,100%);font-weight:600}' +
    '.bod .flex.flex-wrap,.bod .flex.gap-2.items-center{flex-wrap:wrap}' +
    '.rdsw-legend{font-size:12.5px;color:#475569;background:#f8fafc;border:1px dashed #cbd5e1;border-radius:6px;padding:6px 10px;margin:4px 0 10px}' +
    '.rdsw-check{display:flex;gap:8px;align-items:center;margin:2px 0 14px}.rdsw-check label{font-weight:700;font-size:13px}' +
    '.rdsw-check input{flex:1;min-width:260px;border:1px solid #cbd5e1;border-radius:6px;padding:6px 9px;font-size:13px;background:#f8fafc}' +
    '.rdsw-check input.rdsw-warn{background:#fff7ed;border-color:#f59e0b;color:#92400e}.rdsw-check input.rdsw-ok{background:#f0fdf4;border-color:#22c55e;color:#166534}' +
    '.rdsw-ro{background:#f1f5f9!important;color:#334155}';
  document.head.appendChild(css);
  var t = null;
  new MutationObserver(function () { clearTimeout(t); t = setTimeout(enhance, 120); }).observe(document.documentElement, { childList: true, subtree: true });
  if (document.readyState !== 'loading') enhance(); else document.addEventListener('DOMContentLoaded', enhance);

  /* searchable sample list (waste-water reports of the user's laboratory, newest first) */
  function sampleSearch() {
    if (!window.jQuery || !jQuery.fn.select2) return;
    var s = jQuery('#samples');
    if (s.length && !s.hasClass('select2-hidden-accessible')) { s.select2({ width: '340px', placeholder: 'Select sample' }); }
  }
  window.addEventListener('load', function () { setTimeout(sampleSearch, 300); });
})();
