/* RDS pages: a dilution factor (DF) on every calculation section (owner 31-10-2026, R12 point 2).

   A section whose own formula already carries a DF (an input with placeholder "DF" / "D.F", e.g. the metals) is left to
   it. Every other section (titrations, gravimetric, pH, BOD / COD, microbiology ...) gets a "Dilution factor" box, 1 by
   default. When the section's "=" writes its result to the results table, the layer keeps that value as the base and
   writes base x DF to the table; changing the DF re-applies it. Saved with the RDS as df_<n>, df_base_<n>, df_sec_<n>,
   df_param_<n>, df_side_<n>, df_result_<n>; the PDF prints "Dilution factor (DF = x): result = base x DF = final" under
   the section (QC/rds_pdf_extras.py). Library cards carry their own DF (static/js/rds_formula_lib.js). */
(function () {
  'use strict';
  function form() { return document.getElementById('qcForm'); }
  function vis(e) { return !!(e && e.offsetParent !== null); }
  function after(a, b) { return !!(a.compareDocumentPosition(b) & Node.DOCUMENT_POSITION_FOLLOWING); }
  function num(v) { if (v === null || v === undefined || String(v).trim() === '') return null; var x = parseFloat(v); return isFinite(x) ? x : null; }
  function out(e) { return e.closest('#rdsLib') || e.closest('table') || e.closest('.rq-block') || e.closest('.rq-bar') || e.closest('.rds-edta') || e.closest('.rds-df'); }
  function headings() {
    var f = form(); if (!f) return [];
    return Array.prototype.filter.call(f.querySelectorAll('h1, p.text-3xl'), function (h) { return !out(h) && !h.closest('[id^="calc_"]'); });
  }
  function secName(h) {
    var t = '';
    Array.prototype.forEach.call(h.childNodes, function (n) { if (n.nodeType === 3 || (n.nodeType === 1 && !n.classList.contains('rds-rep'))) t += n.textContent; });
    t = t.replace(/\s+/g, ' ').trim().replace(/\bcalculations?\b.*$/i, '').replace(/[\d.]+\s*$/, '').replace(/\*/g, '').replace(/:$/, '').trim();
    var side = /\binlet\b/i.test(t) ? 'Inlet' : (/\boutlet\b/i.test(t) ? 'Outlet' : '');
    return { name: t.replace(/\b(inlet|outlet)\b/ig, '').replace(/\s+/g, ' ').trim(), side: side };
  }
  function members(h) {                       // controls of the section: from the heading to the next heading
    var f = form(), hs = headings(), i = hs.indexOf(h), next = hs[i + 1] || null, list = [];
    Array.prototype.forEach.call(f.querySelectorAll('input, button, select'), function (e) {
      if (out(e)) return;
      if (after(h, e) && (!next || after(e, next))) list.push(e);
    });
    return list;
  }
  function decimals(s) { var m = String(s).match(/\.(\d+)$/); return m ? m[1].length : 0; }
  function rd(v, dp) { return String(+(+v).toFixed(Math.min(6, Math.max(dp, 2)))); }
  function resultInputs() {
    return Array.prototype.filter.call(form().querySelectorAll('tbody input[name^="result_"], tbody input[name^="inlet_"], tbody input[name^="outlet_"]'), function (i) { return vis(i) || true; });
  }
  function snapshot() { var m = new Map(); resultInputs().forEach(function (i) { m.set(i.name, String(i.value)); }); return m; }
  function rowParam(inp) { var tr = inp.closest('tr'), p = tr && tr.querySelector('input[name^="parameter_"]'); return p ? p.value : ''; }

  var n = 0;
  function build() {
    var f = form(); if (!f) return;
    headings().forEach(function (h) {
      if (h.dataset.rdsDf || !vis(h)) return;
      var ms = members(h);
      var native = ms.some(function (e) { return e.tagName === 'INPUT' && (/^\s*d\.?\s*f\.?\s*$/i.test(e.placeholder || '') || /(^|_)df\d*(_|$)/i.test(e.name || '')); });
      var buttons = ms.filter(function (e) { return e.tagName === 'BUTTON' && /=|final ans|calculate|average/i.test(e.textContent || ''); });
      if (native) { h.dataset.rdsDf = 'native'; return; }
      if (!buttons.length) { h.dataset.rdsDf = 'none'; return; }
      var sn = secName(h);
      if (!sn.name) {                       // an empty heading (manual pages): the parameter the section's fields belong to
        var OWN = (window.RDS_OWNERS || {})[/create_ww_qc/.test(location.pathname) ? 'ww' : 'dw'] || {};
        for (var i = 0; i < ms.length && !sn.name; i++) {
          var o = ms[i].tagName === 'INPUT' && OWN[ms[i].name];
          if (o && o.length) { sn.name = String(o[0]).replace(/\*/g, '').trim(); sn.side = /_inlet$/.test(ms[i].name) ? 'Inlet' : (/_outlet$/.test(ms[i].name) ? 'Outlet' : ''); }
        }
      }
      if (!sn.name) { h.dataset.rdsDf = 'none'; return; }
      var k = ++n, id = 'rds_df_' + k;
      var box = document.createElement('div'); box.className = 'rds-df'; box.id = id;
      box.innerHTML = '<label>Dilution factor (DF) <input type="number" step="any" min="0" name="df_' + k + '" value="1"></label>' +
        '<span class="rds-df-note">1 = undiluted. Result = calculated result &times; DF; the RDS prints the step.</span><b class="rds-df-fin"></b>' +
        '<input type="hidden" name="df_sec_' + k + '" value="' + sn.name.replace(/"/g, '&quot;') + '"><input type="hidden" name="df_side_' + k + '" value="' + sn.side + '">' +
        '<input type="hidden" name="df_base_' + k + '"><input type="hidden" name="df_result_' + k + '"><input type="hidden" name="df_param_' + k + '"><input type="hidden" name="df_row_' + k + '">';
      var p = h.parentElement;
      if (p && p !== f && p.children.length === 1 && !p.classList.contains('flex')) p.insertAdjacentElement('afterend', box); else h.insertAdjacentElement('afterend', box);
      h.dataset.rdsDf = String(k);
      var dfIn = box.querySelector('input[name="df_' + k + '"]');
      buttons.forEach(function (b) {
        b.addEventListener('click', function () {
          var before = snapshot(), secBefore = secSnapshot(h);
          setTimeout(function () { apply(k, box, h, before, secBefore); }, 0);
        }, true);
      });
      dfIn.addEventListener('input', function () { reapply(k, box); });
    });
  }
  function bare(x) { return (window.RDSLib ? window.RDSLib.bare(x) : String(x || '').toLowerCase()).replace(/\b(inlet|outlet)\b/g, '').replace(/\s+/g, ' ').trim(); }
  function rowByName(box) {                   // the table row of the section when the "=" rewrote the same value
    var sec = bare(box.querySelector('[name^="df_sec_"]').value), side = box.querySelector('[name^="df_side_"]').value;
    var lib = window.RDSLib, hits = resultInputs().filter(function (i) {
      var tr = i.closest('tr'), sn = ((tr.querySelector('.main-sno') || {}).textContent || '').trim(); if (!sn || sn.indexOf('.') >= 0) return false;
      if (side && !new RegExp('^' + side.toLowerCase() + '_').test(i.name)) return false;
      var pn = rowParam(i), b = bare(pn), p2 = lib && lib.pageName ? bare(lib.pageName(pn) || '') : '';
      return b === sec || p2 === sec || (sec.length >= 4 && (b.indexOf(sec) >= 0 || sec.indexOf(b) >= 0));
    });
    return hits.length === 1 ? hits[0] : null;
  }
  var MANUAL = /_manual/.test(location.pathname);
  function secInputs(h) { return members(h).filter(function (e) { return e.tagName === 'INPUT' && e.type !== 'hidden' && e.type !== 'button'; }); }
  function secSnapshot(h) { var m = new Map(); secInputs(h).forEach(function (i) { m.set(i, String(i.value)); }); return m; }
  function apply(k, box, h, before, secBefore) {
    // the base: the section's own final answer = the last input of the section the "=" has just written
    var written = secInputs(h).filter(function (i) { return secBefore.get(i) !== String(i.value) && num(i.value) !== null; });
    var ansE = written[written.length - 1] || null;
    var changed = resultInputs().filter(function (i) { return before.get(i.name) !== String(i.value) && String(i.value).trim() !== ''; });
    var row = changed[0] || (MANUAL ? rowByName(box) : null);
    if (!ansE && row) ansE = row;
    if (!ansE) return;
    box.querySelector('[name="df_base_' + k + '"]').value = ansE.value;
    box.querySelector('[name="df_row_' + k + '"]').value = row ? row.name : '';
    box.querySelector('[name="df_param_' + k + '"]').value = row ? rowParam(row) : (rowByName(box) ? rowParam(rowByName(box)) : '');
    reapply(k, box);
  }
  function reapply(k, box) {
    var baseS = box.querySelector('[name="df_base_' + k + '"]').value, row = box.querySelector('[name="df_row_' + k + '"]').value;
    var base = num(baseS), df = num(box.querySelector('[name="df_' + k + '"]').value);
    var res = box.querySelector('[name="df_result_' + k + '"]');
    if (base === null) return;
    if (df === null || df <= 0) { box.classList.add('rds-df-bad'); return; }
    box.classList.remove('rds-df-bad');
    var fin = df === 1 ? baseS : rd(base * df, decimals(baseS));
    res.value = fin;
    box.querySelector('.rds-df-fin').textContent = df === 1 ? '' : 'Result x DF = ' + baseS + ' x ' + df + ' = ' + fin;
    var inp = row ? form().querySelector('tbody input[name="' + row + '"]') : null;   // the row only where the section wrote it (manual pages)
    if (inp) { inp.value = fin; inp.dispatchEvent(new Event('input', { bubbles: true })); }
  }
  var css = document.createElement('style');
  css.textContent = '.rds-df{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin:6px 0 10px;padding:8px 12px;border:1px dashed #94a3b8;border-radius:8px;background:#f8fafc;font-size:13px}' +
    '.rds-df label{display:flex;gap:8px;align-items:center;font-weight:600}.rds-df input[type=number]{width:90px;padding:4px 6px;border:1px solid #cbd5e1;border-radius:6px;text-align:center}' +
    '.rds-df-note{color:#64748b;font-size:12px}.rds-df-fin{font-family:ui-monospace,monospace;font-size:13px;color:#0f5132}.rds-df.rds-df-bad{border-color:#dc2626;background:#fef2f2}';
  document.head.appendChild(css);
  var tmr = null;
  function later() { clearTimeout(tmr); tmr = setTimeout(function () { try { build(); } catch (e) { if (window.console) console.error('RDS DF', e); } }, 300); }
  var orig = window.populateQCTable;
  if (typeof orig === 'function') { window.populateQCTable = function () { var r = orig.apply(this, arguments); later(); return r; }; }
  function start() { later(); var f = form(); if (f && window.MutationObserver) new MutationObserver(function (ms) { if (ms.some(function (m) { return m.type === 'attributes' || Array.prototype.some.call(m.addedNodes, function (x) { return x.nodeType === 1 && !(x.classList && x.classList.contains('rds-df')); }); })) later(); }).observe(f, { childList: true, subtree: true, attributes: true, attributeFilter: ['style', 'class'] }); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
  window.RDSDF = { build: build };
})();
