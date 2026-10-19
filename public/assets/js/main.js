// NA Group – kleine Helfer, keine Abhängigkeiten
(function () {
  // Kontaktformular: Zeitstempel (Spam-Schutz) und Rückmeldung
  var f = document.querySelector('form.form');
  if (f) {
    var ts = f.querySelector('input[name="ts"]');
    if (ts) ts.value = Math.floor(Date.now() / 1000);
    var q = new URLSearchParams(location.search);
    var el = q.get('sent') === '1' ? document.getElementById('form-ok')
           : q.get('error') === '1' ? document.getElementById('form-err') : null;
    if (el) {
      el.hidden = false;
      history.replaceState(null, '', location.pathname + '#formular');
      f.scrollIntoView();
    }
  }
  // Produktgalerie: Klick auf Vorschaubild zeigt es groß
  var main = document.querySelector('.gallery-main');
  var thumbs = document.querySelectorAll('.thumb');
  thumbs.forEach(function (b, i) {
    if (i === 0) b.setAttribute('aria-current', 'true');
    b.addEventListener('click', function () {
      main.src = b.getAttribute('data-src');
      thumbs.forEach(function (t) { t.removeAttribute('aria-current'); });
      b.setAttribute('aria-current', 'true');
    });
  });
  // Mobiles Menü nach Klick schließen
  var tog = document.getElementById('navtoggle');
  document.querySelectorAll('.nav a').forEach(function (a) {
    a.addEventListener('click', function () { if (tog) tog.checked = false; });
  });
})();
