/* RDS drafts - R14 (Lab Manager Karachi, e-mail 03-11-2026, point 8).
 *
 * The Raw Data Sheet being entered on the Add / manual pages (DW, WW) is saved as a draft: a few seconds after each
 * change, every 30 seconds while it changes, and when the page is left. The draft is kept on the server (per user,
 * sample and page) and, as a fallback, in this browser - so an emergency, a shutdown or an expired session loses
 * nothing. Reopening the page lists the user's drafts; "Resume" selects the sample and rebuilds the sheet: the rows
 * added with "+", the WS / RM / CRM checks, the formula-library cards added by hand, then every entry. Saving the RDS
 * removes its draft (server side). A draft is never printed and is not an RDS record.
 */
(function () {
  'use strict';
  var form = function () { return document.getElementById('qcForm'); };
  var KIND = /ww/.test(location.pathname) ? 'ww' : 'dw';
  var PAGE = /manual/.test(location.pathname) ? 'manual' : 'add';
  var LS = 'rds_draft_' + KIND + '_' + PAGE + '_';
  var KEEP_MS = 7 * 24 * 3600 * 1000;                     // a draft is kept 7 days after its last save (server and browser)
  var dirty = false, saving = false, restoring = false, lastSaved = '', timer = null, bar = null;

  function csrf() {
    if (typeof window.rdsCsrf === 'function') { try { return window.rdsCsrf(); } catch (e) { } }
    var m = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/); if (m) return decodeURIComponent(m[1]);
    var i = document.querySelector('input[name=csrfmiddlewaretoken]'); return i ? i.value : '';
  }
  function sel() { return document.getElementById('samples'); }
  function currentSample() {
    var s = sel(); if (!s || s.selectedIndex < 0) return '';
    var o = s.options[s.selectedIndex]; return o ? (o.getAttribute('data-sample-id') || '') : '';
  }
  function sno(tr) { return ((tr.querySelector('.main-sno') || {}).textContent || '').trim(); }
  function rows() { var f = form(); return f ? Array.prototype.filter.call(f.querySelectorAll('tbody tr'), function (tr) { return sno(tr); }) : []; }
  function fmtNow() { var d = new Date(), z = function (n) { return (n < 10 ? '0' : '') + n; }; return z(d.getDate()) + '-' + z(d.getMonth() + 1) + '-' + d.getFullYear() + ' ' + z(d.getHours()) + ':' + z(d.getMinutes()) + ':' + z(d.getSeconds()); }
  function sleep(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }

  /* ------------------------------------------------------------------ snapshot */
  function blockPrefix(blk) { var t = blk.querySelector('input[name$="_type"]'); return t ? t.name.replace(/_type$/, '') : ''; }
  function snapshot() {
    var f = form(); if (!f) return null;
    var fields = [];
    Array.prototype.forEach.call(f.querySelectorAll('input[name], select[name], textarea[name]'), function (e) {
      if (!e.name || e.type === 'file' || e.type === 'button' || e.type === 'submit' || e.name === 'csrfmiddlewaretoken') return;
      if (e.type === 'checkbox' || e.type === 'radio') fields.push([e.name, e.value, e.checked ? 1 : 0]);
      else fields.push([e.name, e.value]);
    });
    var blocks = Array.prototype.map.call(document.querySelectorAll('.rq-block'), function (b) {
      var g = function (s) { var e = b.querySelector('input[name$="_' + s + '"]'); return e ? e.value : ''; };
      var m = /^calc_(\d+)_(\d+)$/.exec(b.id || '');
      return { p: blockPrefix(b), type: b.dataset.type || g('type'), param: g('param'), side: g('side'), row: b.dataset.rqRow || (m ? m[1] + '.' + m[2] : '') };
    });
    var subs = rows().map(sno).filter(function (s) { return s.indexOf('.') > 0; }).map(function (s) {
      var blk = blocks.filter(function (b) { return b.row === s; })[0];
      var nat = document.getElementById('calc_' + s.replace('.', '_'));
      if (blk) return { sno: s, how: 'check', p: blk.p };
      if (nat && nat.dataset && nat.dataset.gen !== undefined && !nat.classList.contains('rq-block')) return { sno: s, how: 'gen', gen: +nat.dataset.gen };
      return { sno: s, how: 'plus' };
    });
    var cards = Array.prototype.map.call(document.querySelectorAll('.rl-card'), function (c) {
      return { id: c.id, calc: c.dataset.calc || '', param: c.dataset.param || '', side: c.dataset.side || '', manual: c.dataset.manual === '1' ? 1 : 0 };
    });
    var mainRows = rows().filter(function (tr) { return sno(tr).indexOf('.') < 0; });
    var rt = f.querySelector('.report-type-radio:checked');
    return { v: 1, kind: KIND, page: PAGE, sample_id: currentSample(), saved: fmtNow(), mains: mainRows.length,
             mainList: mainRows.map(function (tr) { return { sno: sno(tr), param: (tr.querySelector('input[name^="parameter_"]') || {}).value || '' }; }),
             reportType: rt ? rt.value : '',
             fields: fields, blocks: blocks, subs: subs, cards: cards };
  }

  /* ------------------------------------------------------------------ saving */
  function setStatus(txt, warn) {
    var st = bar && bar.querySelector('.rd-status'); if (!st) return;
    st.textContent = txt; st.className = 'rd-status' + (warn ? ' rd-warn' : '');
  }
  function keepLocal(snap, synced) {
    try { localStorage.setItem(LS + snap.sample_id, JSON.stringify({ synced: synced ? 1 : 0, at: snap.saved, ts: Date.now(), payload: snap })); } catch (e) { }
  }
  function save(final) {
    if (restoring || saving) return Promise.resolve();
    var sid = currentSample(); if (!sid || !rows().length) return Promise.resolve();
    var snap = snapshot(); if (!snap) return Promise.resolve();
    var body = JSON.stringify({ kind: KIND, page: PAGE, sample_id: sid, payload: snap });
    if (body === lastSaved) { dirty = false; return Promise.resolve(); }
    saving = true; keepLocal(snap, false);
    return fetch('/qc/rds_draft/save/', { method: 'POST', keepalive: !!final && body.length < 60000, credentials: 'same-origin',
                                          headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf() }, body: body })
      .then(function (r) {
        var ct = r.headers.get('content-type') || '';
        if (!r.ok || ct.indexOf('json') < 0) throw new Error(r.status === 403 ? 'not allowed' : 'signed out?');
        return r.json();
      })
      .then(function (j) { lastSaved = body; dirty = false; keepLocal(snap, true); setStatus('Draft saved ' + (j.saved_at || snap.saved) + ' (server)'); })
      .catch(function (e) { setStatus('Draft kept in this browser at ' + snap.saved + ' - not saved to the server (' + e.message + '). It is saved there when the connection or sign-in returns.', true); })
      .then(function () { saving = false; });
  }
  function touch() {
    if (restoring) return;
    dirty = true; clearTimeout(timer); timer = setTimeout(function () { save(false); }, 5000);
  }

  /* ------------------------------------------------------------------ restoring */
  async function waitFor(test, ms) { var t0 = Date.now(); while (Date.now() - t0 < ms) { if (test()) return true; await sleep(150); } return !!test(); }
  function barFor(param, side) {
    var bars = Array.prototype.filter.call(document.querySelectorAll('.rq-bar'), function (b) { return b.offsetParent !== null || true; });
    var eq = function (b) { return (b.dataset.param || '') === param && (b.dataset.side || '') === (side || ''); };
    return bars.filter(function (b) { return eq(b) && b.offsetParent !== null; })[0] || bars.filter(eq)[0] || null;
  }
  function newestBlock() { var a = document.querySelectorAll('.rq-block'); return a.length ? a[a.length - 1] : null; }
  var claimed = new Set();
  async function addCheck(b) {
    var have = Array.prototype.filter.call(document.querySelectorAll('.rq-block'), function (x) {   // made by the page itself (e.g. its own WS checks)
      if (claimed.has(x)) return false;
      var g = function (k) { var e = x.querySelector('input[name$="_' + k + '"]'); return e ? e.value : ''; };
      return (x.dataset.type || g('type')) === b.type && g('param') === b.param && g('side') === (b.side || '') && !(x.dataset.rqRow || /^calc_/.test(x.id || ''));
    })[0];
    if (have && !b.row) { claimed.add(have); return have; }
    var br = barFor(b.param, b.side); if (!br) return null;
    var before = new Set(Array.prototype.slice.call(document.querySelectorAll('.rq-block')));
    var btn = br.querySelector('.rq-add[data-t="' + b.type + '"]'); if (!btn) return null;
    btn.click(); await sleep(120);
    var nb = Array.prototype.filter.call(document.querySelectorAll('.rq-block'), function (x) { return !before.has(x); })[0] || newestBlock();
    if (nb) claimed.add(nb);
    return nb;
  }
  function rowBy(s) { return rows().filter(function (tr) { return sno(tr) === s; })[0] || null; }
  async function restore(snap, when) {
    var f = form(); if (!f || !snap) return;
    var s = sel(), opt = s ? Array.prototype.filter.call(s.options, function (o) { return o.getAttribute('data-sample-id') === snap.sample_id; })[0] : null;
    if (!opt) { alert('Sample ' + snap.sample_id + ' is not in the list on this page any more - the draft cannot be opened here.'); return; }
    if (rows().length && currentSample() && !confirm('Open the draft of ' + snap.sample_id + ' (saved ' + (when || snap.saved) + ')? What is on the page now is replaced.')) return;
    var cur = f.querySelector('.report-type-radio:checked');
    if (PAGE === 'manual' && snap.reportType && cur && cur.value !== snap.reportType) {   // the manual page reloads on a change of report type
      try { localStorage.setItem('selectedReportType', snap.reportType); sessionStorage.setItem('rdsDraftResume', JSON.stringify({ sid: snap.sample_id, when: when || '' })); } catch (e) { }
      try { sessionStorage.setItem('rdsDraftPayload', JSON.stringify(snap)); } catch (e) { }
      location.reload(); return;
    }
    restoring = true; claimed = new Set(); setStatus('Opening the draft of ' + snap.sample_id + ' ...');
    try {
      s.value = opt.value; opt.selected = true;
      /* the pages declare "const selectSample" in a script: reachable by name, not as window.selectSample */
      if (typeof selectSample === 'function') await selectSample(s); else s.dispatchEvent(new Event('change', { bubbles: true }));   // eslint-disable-line no-undef
      if (PAGE === 'manual') {                                // the manual page makes a row when a section is worked: rows again by name
        (snap.mainList || []).forEach(function (m) {
          if (!rowBy(m.sno) && m.param && typeof createRowFromCalculation === 'function') createRowFromCalculation(m.param, '', null, true);   // eslint-disable-line no-undef
        });
      }
      await waitFor(function () { return rows().filter(function (tr) { return sno(tr).indexOf('.') < 0; }).length >= (snap.mains || 1); }, 20000);
      await sleep(1200);                                      // sections, QC bars and library cards appear after the table
      var map = {}, used = new Set(), missing = [];
      // 1. the sub-rows, in their numbers' order, each made as it was made
      var subs = (snap.subs || []).slice().sort(function (a, b) { var x = a.sno.split('.').map(Number), y = b.sno.split('.').map(Number); return x[0] - y[0] || x[1] - y[1]; });
      for (var i = 0; i < subs.length; i++) {
        var u = subs[i], main = u.sno.split('.')[0];
        if (rowBy(u.sno)) continue;
        if (u.how === 'check') {
          var bd = (snap.blocks || []).filter(function (b) { return b.p === u.p; })[0];
          var nb = bd ? await addCheck(bd) : null;
          if (nb && bd) { map[bd.p] = blockPrefix(nb); used.add(bd.p); } else missing.push('check ' + u.sno);
        } else if (u.how === 'gen') {
          var g = document.querySelectorAll('.generate-crm-btn')[u.gen]; if (g) { g.click(); await sleep(400); } else missing.push('CRM ' + u.sno);
        } else {
          var tr = rowBy(main), plus = tr && tr.querySelector('.add-row-btn');
          if (plus) { plus.click(); await sleep(250); } else missing.push('row ' + u.sno);
        }
        if (!rowBy(u.sno)) missing.push(u.sno);
      }
      // 2. the checks without a row (WS, RM), in the order they were added
      var rest = (snap.blocks || []).filter(function (b) { return !used.has(b.p); }).sort(function (a, b) { return (+a.p.split('_')[1] || 0) - (+b.p.split('_')[1] || 0); });
      for (var k = 0; k < rest.length; k++) {
        var nb2 = await addCheck(rest[k]);
        if (nb2) map[rest[k].p] = blockPrefix(nb2); else missing.push(rest[k].type + ' ' + rest[k].param);
      }
      // 3. formula-library cards: the page makes its own; the ones added by hand are added again
      var cmap = {}, taken = new Set();
      (snap.cards || []).forEach(function (c) {
        var hit = Array.prototype.filter.call(document.querySelectorAll('.rl-card'), function (x) {
          return !taken.has(x.id) && x.dataset.calc === c.calc && (x.dataset.param || '') === c.param && (x.dataset.side || '') === c.side;
        })[0];
        if (!hit && c.manual) {
          var host = document.getElementById('rdsLib'), pick = host && host.querySelector('.rl-pick'), nm = host && host.querySelector('.rl-pname');
          if (pick && nm) { pick.value = c.calc; nm.value = c.param; host.querySelector('.rl-addbtn').click(); nm.value = ''; hit = host.querySelector('.rl-cards .rl-card:last-child'); }
        }
        if (hit) { taken.add(hit.id); cmap[c.id] = hit.id; } else missing.push('card ' + c.param);
      });
      // 4. every entry, under its name on the rebuilt sheet
      var rename = function (n) {
        var m = /^(qc_\d+)(_.*)$/.exec(n); if (m && map[m[1]]) return map[m[1]] + m[2];
        m = /^qc_print_(\d+)$/.exec(n); if (m && map['qc_' + (+m[1])]) return 'qc_print_' + String(+map['qc_' + (+m[1])].split('_')[1]).padStart(3, '0');
        m = /^(rl\d+)(_.*)$/.exec(n); if (m && cmap[m[1]]) return cmap[m[1]] + m[2];
        m = /^lib_print_(\d+)$/.exec(n); if (m && cmap['rl' + (+m[1])]) return 'lib_print_' + String(+cmap['rl' + (+m[1])].slice(2)).padStart(3, '0');
        return n;
      };
      var seen = {}, notPlaced = 0;
      (snap.fields || []).forEach(function (fv) {
        var name = rename(fv[0]), els = f.querySelectorAll('[name="' + (window.CSS && CSS.escape ? CSS.escape(name) : name) + '"]');
        var idx = seen[name] = (seen[name] === undefined ? 0 : seen[name] + 1), e = els[idx] || els[0];
        if (!e) { if (String(fv[1] || '').trim()) notPlaced++; return; }
        if (e.type === 'checkbox' || e.type === 'radio') e.checked = !!fv[2];
        else if (e.type !== 'file') e.value = fv[1];
      });
      Array.prototype.forEach.call(f.querySelectorAll('.rl-as'), function (x) { x.dispatchEvent(new Event('change')); });   // the card's "result as" choice
      lastSaved = ''; dirty = true;                          // saved again (to the server too) at the next interval
      setStatus('Draft of ' + snap.sample_id + ' (saved ' + (when || snap.saved) + ') opened' + (missing.length || notPlaced ? ' - check: ' + (missing.length ? missing.length + ' part(s) not rebuilt (' + missing.slice(0, 4).join('; ') + ')' : '') + (notPlaced ? (missing.length ? ', ' : '') + notPlaced + ' entr(ies) not placed' : '') : '') + '. Check the sheet, then save the RDS.', !!(missing.length || notPlaced));
    } catch (e) {
      if (window.console) console.error('RDS draft', e);
      setStatus('The draft could not be opened completely: ' + e.message, true);
    } finally { restoring = false; }
  }

  /* ------------------------------------------------------------------ the bar */
  function localDrafts() {
    var out = [];
    try {
      for (var i = 0; i < localStorage.length; i++) {
        var k = localStorage.key(i); if (k.indexOf(LS) !== 0) continue;
        var v = JSON.parse(localStorage.getItem(k) || '{}');
        if (!v || !v.ts || Date.now() - v.ts > KEEP_MS) { localStorage.removeItem(k); i--; continue; }   // not kept for long (owner 03-11-2026)
        if (!v.synced && v.payload) out.push(v);
      }
    } catch (e) { }
    return out;
  }
  function esc(s) { return String(s === null || s === undefined ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function render(list) {
    var box = bar.querySelector('.rd-list'), loc = localDrafts();
    var items = (list || []).map(function (d) { return { sid: d.sample_id, at: d.saved_at, src: 'server' }; });
    loc.forEach(function (v) { if (!items.some(function (x) { return x.sid === v.payload.sample_id; })) items.push({ sid: v.payload.sample_id, at: v.at, src: 'browser' }); });
    box.innerHTML = items.length ? items.map(function (x) {
      return '<span class="rd-item"><b>' + esc(x.sid) + '</b> <i>saved ' + esc(x.at) + (x.src === 'browser' ? ' (this browser only)' : '') + '</i> ' +
        '<button type="button" class="rd-open" data-sid="' + esc(x.sid) + '" data-src="' + x.src + '">Resume</button>' +
        '<button type="button" class="rd-del" data-sid="' + esc(x.sid) + '">Discard</button></span>';
    }).join('') : '<span class="rd-none">No draft.</span>';
  }
  function refresh() {
    return fetch('/qc/rds_draft/list/?kind=' + KIND + '&page=' + PAGE, { credentials: 'same-origin' })
      .then(function (r) { return r.ok ? r.json() : { drafts: [] }; }).catch(function () { return { drafts: [] }; })
      .then(function (j) { render(j.drafts || []); });
  }
  function open(sid, src) {
    var local = null; try { local = JSON.parse(localStorage.getItem(LS + sid) || 'null'); } catch (e) { }
    if (src === 'browser') return restore(local && local.payload, local && local.at + ' (this browser)');
    return fetch('/qc/rds_draft/get/?kind=' + KIND + '&page=' + PAGE + '&sample_id=' + encodeURIComponent(sid), { credentials: 'same-origin' })
      .then(function (r) { return r.json(); })
      .then(function (j) {
        var p = j.status === 'ok' ? j.payload : null, when = j.saved_at;
        if (local && local.payload && !local.synced) { p = local.payload; when = local.at + ' (this browser)'; }   // not yet on the server: the newer copy
        return restore(p, when);
      });
  }
  function discard(sid) {
    if (!confirm('Discard the draft of ' + sid + '?')) return;
    try { localStorage.removeItem(LS + sid); } catch (e) { }
    fetch('/qc/rds_draft/delete/', { method: 'POST', credentials: 'same-origin', headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf() },
                                     body: JSON.stringify({ kind: KIND, page: PAGE, sample_id: sid }) }).then(refresh, refresh);
  }
  function mount() {
    var f = form(); if (!f || document.getElementById('rdsDraftBar')) return;
    bar = document.createElement('div'); bar.id = 'rdsDraftBar';
    bar.innerHTML = '<div class="rd-head"><b>Drafts</b> <span>The sheet is saved as a draft while you work; resume a draft after a shutdown or an expired session. Drafts are removed when the RDS is saved, or 7 days after their last save.</span></div>' +
      '<div class="rd-list"></div><div class="rd-status"></div>';
    var anchor = sel() ? (sel().closest('div') || f) : f;
    if (anchor === f) f.insertBefore(bar, f.firstChild); else anchor.parentNode.insertBefore(bar, anchor.nextSibling);
    bar.addEventListener('click', function (e) {
      var t = e.target; if (!t || !t.dataset) return;
      if (t.classList.contains('rd-open')) open(t.dataset.sid, t.dataset.src);
      if (t.classList.contains('rd-del')) discard(t.dataset.sid);
    });
    var st = document.createElement('style');
    st.textContent = '#rdsDraftBar{border:1px solid #cbd5e1;background:#f8fafc;border-radius:8px;padding:8px 12px;margin:10px 0;font-size:13px}' +
      '#rdsDraftBar .rd-head span{color:#64748b;margin-left:6px}#rdsDraftBar .rd-list{margin-top:6px;display:flex;flex-wrap:wrap;gap:10px}' +
      '#rdsDraftBar .rd-item{background:#fff;border:1px solid #e2e8f0;border-radius:6px;padding:4px 8px}#rdsDraftBar i{color:#64748b;font-style:normal}' +
      '#rdsDraftBar button{margin-left:6px;border-radius:5px;padding:2px 8px;font-size:12px}#rdsDraftBar .rd-open{background:#0f5132;color:#fff}' +
      '#rdsDraftBar .rd-del{border:1px solid #b91c1c;color:#b91c1c;background:#fff}#rdsDraftBar .rd-status{margin-top:6px;color:#0f5132}' +
      '#rdsDraftBar .rd-status.rd-warn{color:#b45309}#rdsDraftBar .rd-none{color:#94a3b8}';
    document.head.appendChild(st);
    f.addEventListener('input', touch, true); f.addEventListener('change', touch, true); f.addEventListener('click', function (e) {
      if (e.target && e.target.closest && e.target.closest('button')) touch();            // rows, checks, cards added or removed
    }, true);
    setInterval(function () { if (dirty) save(false); }, 30000);
    window.addEventListener('pagehide', function () { if (dirty) save(true); });
    document.addEventListener('visibilitychange', function () { if (document.visibilityState === 'hidden' && dirty) save(true); });
    refresh();
    var pend = null; try { pend = JSON.parse(sessionStorage.getItem('rdsDraftResume') || 'null'); } catch (e) { }
    if (pend) {                                               // the page was reloaded for the draft's report type
      var pl = null; try { pl = JSON.parse(sessionStorage.getItem('rdsDraftPayload') || 'null'); sessionStorage.removeItem('rdsDraftResume'); sessionStorage.removeItem('rdsDraftPayload'); } catch (e) { }
      if (pl) setTimeout(function () { restore(pl, pend.when); }, 1500);
    }
  }
  /* R14.1: once the RDS is saved (its PDF comes back), this browser's copy of the draft is removed as well - the server
     removes its own copy in the same request - and no further draft is written until the sheet is changed again. */
  (function () {
    var F = window.fetch; if (!F || F._rdsDraft) return;
    var RE = /\/qc\/create_(dw|ww)_qc(_manual)?\/?(\?|$)/;
    var wrapped = function (url, opt) {
      var u = typeof url === 'string' ? url : (url && url.url) || '', sid = '';
      if (RE.test(u)) { try { sid = (JSON.parse((opt && opt.body) || '{}') || {}).sample_id || ''; } catch (e) { } }
      var pr = F.apply(this, arguments);
      if (sid) pr.then(function (r) {
        if (r && r.ok && /pdf/i.test((r.headers && r.headers.get('Content-Type')) || '')) {
          try { localStorage.removeItem(LS + sid); } catch (e) { }
          dirty = false; clearTimeout(timer); lastSaved = '';
          try { setStatus('RDS of ' + sid + ' saved - its draft is removed'); refresh(); } catch (e) { }
        }
      }, function () { });
      return pr;
    };
    wrapped._rdsDraft = true; window.fetch = wrapped;
  })();
  window.rdsDraft = { snapshot: snapshot, save: save, restore: restore, refresh: refresh, open: open };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount); else mount();
})();
