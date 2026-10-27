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
      window.__rdsStartDate = arguments[2] || '';          // analysis date for the row dates (QA RDS-16)
      return orig.apply(this, arguments);
    };
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
  if (document.readyState === 'complete') setTimeout(preselect, 300);
  else window.addEventListener('load', function () { setTimeout(preselect, 300); });
})();
