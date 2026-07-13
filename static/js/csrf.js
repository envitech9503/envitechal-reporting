/* Envi Tech AL - global CSRF token helper (audit #2).
   Wraps window.fetch so every same-origin unsafe request (POST/PUT/PATCH/DELETE)
   automatically carries the X-CSRFToken header read from the csrftoken cookie.
   Existing explicit X-CSRFToken headers are preserved. */
(function () {
  function getCookie(name) {
    var m = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return m ? decodeURIComponent(m.pop()) : '';
  }
  var _fetch = window.fetch;
  window.fetch = function (input, init) {
    init = init || {};
    var method = (init.method || (input && input.method) || 'GET').toUpperCase();
    var url = (typeof input === 'string') ? input : ((input && input.url) || '');
    var sameOrigin = !/^https?:\/\//i.test(url) || url.indexOf(location.origin) === 0;
    if (sameOrigin && !/^(GET|HEAD|OPTIONS|TRACE)$/.test(method)) {
      var t = getCookie('csrftoken');
      if (t) {
        if (init.headers instanceof Headers) {
          if (!init.headers.has('X-CSRFToken')) { init.headers.set('X-CSRFToken', t); }
        } else {
          init.headers = Object.assign({ 'X-CSRFToken': t }, init.headers || {});
        }
      }
    }
    return _fetch.call(this, input, init);
  };
})();
