document.addEventListener('DOMContentLoaded', function () {
  var slider = document.getElementById('batch');
  if (!slider) return;
  var pk = slider.dataset.pk;
  function fmt(n) { return Number(n).toLocaleString('en-PK', {minimumFractionDigits: 2, maximumFractionDigits: 2}); }
  function upd() {
    document.getElementById('bval').textContent = slider.value;
    fetch('/dashboard/costing/api/' + pk + '/recompute/?batch=' + slider.value)
      .then(function (r) { return r.json(); })
      .then(function (d) {
        document.querySelectorAll('[data-f]').forEach(function (el) {
          var k = el.dataset.f; if (d[k] !== undefined) el.textContent = fmt(d[k]);
        });
        var max = d.price || 1;
        document.querySelectorAll('[data-bar]').forEach(function (el) {
          var v = d[el.dataset.bar] || 0;
          el.style.width = Math.max(1, (v / max * 100)) + '%';
        });
      });
  }
  slider.addEventListener('input', upd);
  upd();
});
