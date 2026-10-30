/* RDS manual pages: a calculation section is shown only when its parameter is in the results table or opened with the
   picker above the sections (the manual page makes the row from the section's "=") (owner 30-10-2026,
   zero-error check of the RDS). The fields of each section belong to the parameter(s) that reveal it on the Add page
   (window.RDS_OWNERS, static/js/rds_field_owners.js, the same map the PDF uses: QC/rds_field_owners.json). */
(function () {
  'use strict';
  if (!/_manual/.test(location.pathname)) return;
  var KIND = /create_ww_qc/.test(location.pathname) ? 'ww' : 'dw';
  var OWN = (window.RDS_OWNERS || {})[KIND], L = window.RDSLib;
  if (!OWN || !L) return;
  var GENERIC = { total: 1, dissolved: 1, solids: 1, free: 1, caco3: 1, compounds: 1, residual: 1, count: 1, water: 1, calculation: 1, calculations: 1, reading: 1, readings: 1, average: 1, standard: 1, working: 1 };
  function words(s) { var o = {}; (L.bare(s) + ' ' + L.norm(s)).split(/[^a-z0-9]+/).forEach(function (w) { if (w.length >= 4 && !GENERIC[w]) o[w] = 1; }); return o; }
  /* sections the Add-page map holds no field of (R11.1, same rules as QC/rds_print_filter.py): by the field's stem */
  var STEMS = [
    [/^(for_)?total_?coliform/, ['Coliform']], [/^(for_)?fecalentero/, ['Fecal Enterococci']],
    [/^(for_)?hetro|^(for_)?hetero/, ['Heterotrophic Bacteria', 'Total Bacterial Count']], [/^(for_)?enterobact/, ['Enterobacteriaceae']],
    [/^(for_)?ecoli|^(for_)?e_coli/, ['E.coli']], [/^(for_)?fa?ecal/, ['Faecal coliform']],
    [/^(for_)?bacteria/, ['Total Bacterial Count', 'Heterotrophic Bacteria']], [/^(for_)?coliform/, ['Coliform']],
    [/^(for_)?carbonate/, ['Carbonates', 'Bicarbonate', 'Carbonate', 'Carbonate Hardness']]
  ];
  var EXTRA_SYN = { 'tbc': 'total bacterial count', 'tpc': 'total bacterial count', 'total plate count': 'total bacterial count', 'total viable count': 'total bacterial count',
    'total coliforms': 'coliform', 'faecal coliform': 'faecal coliform', 'fecal coliforms': 'faecal coliform', 'hpc': 'heterotrophic bacteria', 'heterotrophic plate count': 'heterotrophic bacteria' };
  function stemOwners(name) { var k = String(name || '').toLowerCase(); for (var i = 0; i < STEMS.length; i++) if (STEMS[i][0].test(k)) return STEMS[i][1]; return null; }
  var K = {};
  var ALLNAMES = []; Object.keys(OWN).forEach(function (f) { OWN[f].forEach(function (n) { if (ALLNAMES.indexOf(n) < 0) ALLNAMES.push(n); }); });
  STEMS.forEach(function (st) { st[1].forEach(function (n) { if (ALLNAMES.indexOf(n) < 0) ALLNAMES.push(n); }); });
  ALLNAMES.forEach(function (n) {
    [L.norm(n), L.bare(n)].forEach(function (k) { if (k && !(k in K)) K[k] = n; });
    var m = L.norm(n).match(/\(([^)]*)\)/); if (m && !(m[1].trim() in K)) K[m[1].trim()] = n;
  });
  function pageName(rep) {
    var n = L.norm(rep), b = L.bare(rep); if (n in K) return K[n]; if (b in K) return K[b];
    var syn = (L.SYN || {})[b] || (L.SYN || {})[n] || EXTRA_SYN[b] || EXTRA_SYN[n], list = syn ? (Array.isArray(syn) ? syn : [syn]) : [];
    for (var i = 0; i < list.length; i++) { if (list[i] in K) return K[list[i]]; if (L.bare(list[i]) in K) return K[L.bare(list[i])]; }
    var b2 = b.replace(/ as caco3$/, '').replace(/ as phenols?$/, ''); if (K[b2]) return K[b2];
    if (/colony counts?|viable count|plate count|bacterial count|\bcfu\b/.test(b)) return K['heterotrophic bacteria'] || K['total bacterial count'] || null;   // plate counts (22 / 37 °C)
    return null;
  }
  var form = document.getElementById('qcForm'), table = document.getElementById('table');
  if (!form || !table) return;
  var st = document.createElement('style'); st.textContent = '.rds-gated{display:none !important}.rds-gate-note{margin:12px 0;padding:8px 12px;border-radius:6px;background:#f1f5f9;color:#475569;font-size:14px}'; document.head.appendChild(st);
  function ownersOf(e) { return OWN[e.name] || stemOwners(e.name); }
  function meets(a, b) { return a.some(function (x) { return b.indexOf(x) >= 0; }); }
  var blocks = [];
  function findBlocks() {
    blocks = []; var seen = [];
    Array.prototype.forEach.call(form.querySelectorAll('input[name],select[name],textarea[name]'), function (e) {
      var o = ownersOf(e); if (!o || table.contains(e) || e.closest('#rdsLib')) return;
      var c = e, own = o.slice();
      while (c.parentElement && c.parentElement !== form && !c.parentElement.contains(table)) {
        var p = c.parentElement, ok = true, u = own.slice();
        Array.prototype.forEach.call(p.querySelectorAll('input[name],select[name],textarea[name]'), function (x) {
          var ox = ownersOf(x); if (!ox) return; if (!meets(ox, own)) ok = false; else ox.forEach(function (n) { if (u.indexOf(n) < 0) u.push(n); });
        });
        if (!ok) break; c = p; own = u;
      }
      var i = seen.indexOf(c);
      if (i < 0) { seen.push(c); blocks.push({ el: c, own: own }); }
      else own.forEach(function (n) { if (blocks[i].own.indexOf(n) < 0) blocks[i].own.push(n); });
    });
    blocks = blocks.filter(function (b) { return !blocks.some(function (o) { return o !== b && o.el.contains(b.el); }); });
  }
  var picked = {};                                   // the parameters opened with the picker (the row comes from the "=" of the section)
  function present() {
    var pages = Object.assign({}, picked), loose = {};
    Array.prototype.forEach.call(table.querySelectorAll('input[name^="parameter_"]'), function (i) {
      var v = (i.value || '').trim(); if (!v) return;
      var pn = pageName(v); if (pn) pages[pn] = 1; else Object.assign(loose, words(v));
    });
    return function (own) { return own.some(function (n) { if (pages[n]) return true; var w = words(n); return Object.keys(w).some(function (x) { return loose[x]; }); }); };
  }
  var note = null, pick = null, same = {};
  function esc(t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function picker() {
    if (note) return;
    note = document.createElement('div'); note.className = 'rds-gate-note';
    var names = {}; same = {}; blocks.forEach(function (b) { b.own.forEach(function (n) { var k = n.replace(/\*/g, '').trim(); if (!names[k]) names[k] = n; (same[names[k]] = same[names[k]] || []).push(n); }); });
    var opts = Object.keys(names).sort(function (a, b) { return a.toLowerCase() < b.toLowerCase() ? -1 : 1; });
    note.innerHTML = '<span class="rds-gate-msg"></span> <label style="margin-left:8px">Open the calculation of: <select class="rds-gate-pick" style="padding:4px 6px;border:1px solid #cbd5e1;border-radius:4px"><option value="">- parameter -</option>' +
      opts.map(function (k) { return '<option value="' + esc(names[k]) + '">' + esc(k) + '</option>'; }).join('') + '</select></label> <span class="rds-gate-open"></span>';
    table.parentNode.insertBefore(note, table.nextSibling);
    pick = note.querySelector('.rds-gate-pick');
    pick.addEventListener('change', function () { if (pick.value) { (same[pick.value] || [pick.value]).forEach(function (n) { picked[n] = 1; }); pick.value = ''; apply(); } });
    note.addEventListener('click', function (e) { var x = e.target.closest('[data-close]'); if (x) { var n = x.getAttribute('data-close'); (same[n] || [n]).forEach(function (m) { delete picked[m]; }); apply(); } });
  }
  function apply() {
    if (!blocks.length) findBlocks();
    picker();
    var has = present(), shown = 0;
    blocks.forEach(function (b) {
      var on = has(b.own); b.el.classList.toggle('rds-gated', !on); if (on) shown++;
      // a section the page itself left hidden (WW manual: the microbiology sections' reveal is commented out) opens like on the Add page
      if (on && b.el.style.display === 'none') { b.el.dataset.rdsInline = 'none'; b.el.style.display = ''; }
      else if (!on && b.el.dataset.rdsInline) { b.el.style.display = 'none'; delete b.el.dataset.rdsInline; }
    });
    note.querySelector('.rds-gate-msg').textContent = shown ? 'Calculation sections shown: the parameters of the results table and those opened here; only the parameters of the results table are printed.' : 'No calculation section is open: open one here; its "=" adds the parameter to the results table.';
    note.querySelector('.rds-gate-open').innerHTML = Object.keys(picked).filter(function (n) { return n in same; }).map(function (n) { return '<button type="button" data-close="' + esc(n) + '" title="Close" style="margin:2px;padding:1px 8px;border:1px solid #94a3b8;border-radius:10px;background:#fff">' + esc(n.replace(/\*/g, '').trim()) + ' &times;</button>'; }).join('');
  }
  window.RDSManualGate = { apply: apply, blocks: function () { return blocks; }, open: function (n) { picked[n] = 1; apply(); } };
  table.addEventListener('input', apply); table.addEventListener('change', apply);
  try { new MutationObserver(function () { apply(); }).observe(table, { childList: true, subtree: true }); } catch (e) {}
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { setTimeout(apply, 300); }); else setTimeout(apply, 300);
  window.addEventListener('load', function () { setTimeout(apply, 600); });
})();
