/* RDS page behaviour (QA audit 27-10-2026, release R2).
   - RDS-17: choosing another sample after one is loaded reloads the page for that sample, so no section or figure of
     the previous sample stays on the page (it used to be saved under the new sample).
   - RDS-18: before saving, a sample must be chosen and every row with a result needs Performed By and Checked By;
     the save carries the CSRF token; a server error is shown instead of being opened as a file. */
(function () {
  'use strict';
  function csrf() {
    var m = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);
    if (m) return decodeURIComponent(m[1]);
    var i = document.querySelector('input[name="csrfmiddlewaretoken"]');
    return i ? i.value : '';
  }
  function submitButtons() { return Array.prototype.slice.call(document.querySelectorAll('#qcForm button[type="submit"], #qcForm input[type="submit"]')); }
  function busy(on) { submitButtons().forEach(function (b) { b.disabled = on; b.style.opacity = on ? '0.6' : ''; }); }
  function rowResult(sno) {
    var names = ['result_' + sno, 'inlet_' + sno, 'outlet_' + sno];
    for (var i = 0; i < names.length; i++) {
      var e = document.querySelector('[name="' + names[i] + '"]');
      if (e && String(e.value).trim() !== '' && !/^n\/?a$/i.test(String(e.value).trim())) return true;
    }
    return false;
  }
  function beforeSave(data) {
    if (!data.sample_id || data.sample_id === 'undefined') { alert('Select a sample before saving the RDS.'); return false; }
    var missing = [];
    Array.prototype.forEach.call(document.querySelectorAll('select[name^="performed_by_"]'), function (sel) {
      var sno = sel.name.replace('performed_by_', '');
      var chk = document.querySelector('select[name="checked_by_' + sno + '"]');
      if (!rowResult(sno)) return;
      if (!sel.value || (chk && !chk.value)) missing.push(sno.replace('_', '.'));
    });
    if (missing.length) {
      alert('Select Performed By and Checked By for row(s) ' + missing.join(', ') + ' before saving (ISO/IEC 17025 technical record).');
      return false;
    }
    busy(true); setTimeout(function () { busy(false); }, 8000);
    return true;
  }
  function pdfResponse(response) {
    busy(false);
    if (response.ok && /pdf/i.test(response.headers.get('content-type') || '')) return response.blob();
    return response.text().then(function (t) {
      var msg = 'The RDS was not saved.';
      try { var j = JSON.parse(t); if (j && (j.message || j.error)) msg += ' ' + (j.message || j.error); } catch (e) { if (response.status) msg += ' (server status ' + response.status + ')'; }
      alert(msg);
      throw new Error(msg);
    });
  }
  window.rdsCsrf = csrf;
  window.rdsBeforeSave = beforeSave;
  window.rdsPdfResponse = pdfResponse;

  /* one sample per page load */
  var loaded = false, dirty = false;
  document.addEventListener('input', function () { if (loaded) dirty = true; }, true);
  function currentSampleId() {
    var o = document.querySelector('#samples option:checked');
    if (!o) return '';
    try { return JSON.parse(o.value).sample_id || ''; } catch (e) { return o.getAttribute('data-sample-id') || ''; }
  }
  var prevValue = null;
  var orig = window.populateQCTable;
  if (typeof orig === 'function') {
    window.populateQCTable = function () {
      var sel = document.getElementById('samples');
      if (loaded) {
        if (dirty && !confirm('Changing the sample clears the figures entered on this page. Continue?')) {
          if (sel && prevValue !== null && window.jQuery) window.jQuery(sel).val(prevValue).trigger('change.select2');
          return;
        }
        var sid = currentSampleId();
        location.href = location.pathname + '?sample=' + encodeURIComponent(sid);
        return;
      }
      loaded = true; prevValue = sel ? sel.value : null;
      var args = Array.prototype.slice.call(arguments), rt = args[3];
      var na = function (v) { return /^\s*(n\/?a|-|)\s*$/i.test(String(v === undefined || v === null ? '' : v)); };
      if (Array.isArray(args[0])) args[0] = args[0].filter(function (it) {          // parameters not reported (N/A) are not RDS rows (QA RDS-33)
        return rt === 'in-out' ? !(na(it.inlet_result) && na(it.outlet_result)) : !na(it.test_result !== undefined ? it.test_result : it.result);
      });
      window.__rdsStartDate = arguments[2] || '';          // analysis date for the row dates (QA RDS-16)
      var res = orig.apply(this, args);
      if (rt === 'in-out') hideSingleOnly();
      return res;
    };
  }
  /* in-out reports: a section that exists only for a single result (its heading ends "undefined") is hidden, so the
     formula library gives the parameter an inlet card and an outlet card instead (QA RDS-20) */
  function hideSingleOnly() {
    Array.prototype.forEach.call(document.querySelectorAll('h1, h2'), function (h) {
      if (!h.offsetParent || !/undefined\s*$/.test(h.textContent || '')) return;
      var box = h.parentElement;
      while (box && box !== document.body && box.style.display !== 'block') box = box.parentElement;
      if (!box || box === document.body) return;
      var cls = (box.className || '').split(/\s+/).filter(function (c) { return c && !/^(space|my|mt|mb|p|px|py|flex|gap|grid|text|w|h)-/.test(c) && !/^(flex|grid|hidden|block)$/.test(c); })[0];
      (cls ? document.querySelectorAll('.' + CSS.escape(cls)) : [box]).forEach(function (d) { d.style.display = 'none'; });
    });
  }
  function preselect() {
    var want = new URLSearchParams(location.search).get('sample');
    var sel = document.getElementById('samples');
    if (!want || !sel || !window.jQuery) return;
    var opt = Array.prototype.find.call(sel.options, function (o) {
      try { return JSON.parse(o.value).sample_id === want; } catch (e) { return false; }
    });
    if (opt) window.jQuery(sel).val(opt.value).trigger('change');
  }
  /* premium finish (QA R4): one look for every calculation section, field tips from the placeholders, headings with
     the reported result shown as such */
  var css = document.createElement('style');
  css.textContent =
    '#qcForm input[type=number],#qcForm input[type=text]:not(.select2-search__field){border:1px solid #cbd5e1;border-radius:6px;background:#fff;min-height:36px}' +
    '#qcForm input[type=number]:focus,#qcForm input[type=text]:focus{outline:none;border-color:#0f5132;box-shadow:0 0 0 3px rgba(15,81,50,.15)}' +
    '#qcForm input[readonly]{background:#f1f5f9}' +
    '#qcForm input::placeholder{color:#94a3b8}' +
    '#qcForm h1.text-3xl,#qcForm h1.text-2xl{font-size:1.25rem!important;font-weight:700;color:#0f5132;text-align:left!important;border-left:4px solid #0f5132;padding:6px 0 6px 12px;margin:30px 0 14px!important;background:linear-gradient(90deg,#ecfdf5,transparent)}' +
    '#qcForm button.bg-blue-600{background:#0f5132!important;border-radius:8px;font-weight:600}' +
    '#qcForm button.bg-blue-600:hover{background:#0b3d26!important}' +
    '#qcForm hr.my-20{margin:28px 0!important;border-color:#e2e8f0}' +
    '#qcForm .rds-rep{font-weight:500;color:#1e40af;font-size:.9rem;margin-left:8px}';
  (document.head || document.documentElement).appendChild(css);
  function polish() {
    Array.prototype.forEach.call(document.querySelectorAll('#qcForm input[placeholder]'), function (i) { if (!i.title) i.title = i.placeholder; });
    Array.prototype.forEach.call(document.querySelectorAll('#qcForm h1'), function (h) {
      if (h.dataset.rdsDone === h.textContent || (h.children.length && !h.querySelector('.rds-rep'))) return;   // R5: polished again when the page rewrites the heading
      if (h.querySelector('.rds-rep')) return;
      var t = (h.textContent || '').replace(/\*/g, '').replace(/\s+/g, ' ').trim();
      if (!t) return;
      var m = t.match(/^(.*?\b[Cc]alculations?)\s+(\S.*)$/);
      if (m && !/undefined/.test(m[2])) { h.textContent = m[1].replace(/\bcalculations?\b/i, 'Calculation'); var sp = document.createElement('span'); sp.className = 'rds-rep'; sp.textContent = 'reported: ' + m[2]; h.appendChild(sp); }
      else h.textContent = t.replace(/\bcalculations?\b/i, 'Calculation');
      h.dataset.rdsDone = h.textContent;
    });
  }
  window.RDSPage = { polish: polish };
  document.addEventListener('DOMContentLoaded', polish);
  var _pq = window.populateQCTable;
  if (typeof _pq === 'function') window.populateQCTable = function () { var r = _pq.apply(this, arguments); try { polish(); } catch (e) {} return r; };
  if (document.readyState === 'complete') setTimeout(preselect, 300);
  else window.addEventListener('load', function () { setTimeout(preselect, 300); });
})();
