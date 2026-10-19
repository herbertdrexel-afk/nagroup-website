// Kontaktformular: Zeitstempel setzen (Spam-Schutz) und Rückmeldung anzeigen
(function () {
  var f = document.querySelector('form.form');
  if (!f) return;
  var ts = f.querySelector('input[name="ts"]');
  if (ts) ts.value = Math.floor(Date.now() / 1000);
  var q = new URLSearchParams(location.search);
  var el = q.get('sent') === '1' ? document.getElementById('form-ok')
         : q.get('error') === '1' ? document.getElementById('form-err') : null;
  if (el) {
    el.hidden = false;
    history.replaceState(null, '', location.pathname + '#kontakt');
    document.getElementById('kontakt').scrollIntoView();
  }
})();
// Logo-Leiste: Klick öffnet die passende Firma im Netzwerk
(function () {
  function openFromHash() {
    var el = location.hash && document.getElementById(location.hash.slice(1));
    if (el && el.tagName === 'DETAILS') el.open = true;
  }
  window.addEventListener('hashchange', openFromHash);
  openFromHash();
})();
